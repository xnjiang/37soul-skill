#!/usr/bin/env python3
"""
37Soul Clawdbot Webhook Server
A simple Flask server that receives messages from 37Soul and generates responses.
"""

import os
import hmac
import hashlib
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify
from anthropic import Anthropic
from dotenv import load_load_env()

# Configuration
SOUL_API_BASE_URL = os.getenv('SOUL_API_BASE_URL', 'https://37soul.com')
SOUL_INTEGRATION_SECRET = os.getenv('SOUL_INTEGRATION_SECRET')
AI_MODEL = os.getenv('AI_MODEL', 'claude-3-opus-20240229')
AI_API_KEY = os.getenv('AI_API_KEY')
RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', '5'))
MAX_CONTEXT_LENGTH = int(os.getenv('MAX_CONTEXT_LENGTH', '20'))
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

# Initialize Flask app
app = Flask(__name__)

# Initialize Anthropic client
anthropic = Anthropic(api_key=AI_API_KEY)


def verify_signature(payload, signature):
    """Verify webhook signature from 37Soul."""
    if not SOUL_INTEGRATION_SECRET:
        app.logger.warning("No integration secret configured!")
        return False
    
    expected_signature = hmac.new(
        SOUL_INTEGRATION_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(
        f"sha256={expected_signature}",
        signature
    )


def generate_response(host, message, context):
    """
    Generate AI response for the Host.
    
    Args:
        host: Host profile dict
        message: User message dict
        context: Conversation context dict
    
    Returns:
        Generated response text
    """
    start_time = time.time()
    
    # Build system prompt
    system_prompt = f"""You are {host['nickname']}, a {host['age']} year old {host['sex']}.

Your character: {host['character']}

Important guidelines:
- Stay in character at all times
- Use natural, conversational language
- Match the tone and style of your character
- Reference conversation history when relevant
- Be friendly and engaging
- Keep responses concise (1-3 sentences usually)
- Use emojis sparingly and only if they fit your character

Respond to the user's message naturally and authentically."""

    # Build conversation history
    messages = []
    
    # Add recent context
    if context and 'recent_messages' in context:
        for msg in context['recent_messages'][-MAX_CONTEXT_LENGTH:]:
            messages.append({
                "role": msg.get('role', 'user'),
                "content": msg.get('content', '')
            })
    
    # Add current message
    messages.append({
        "role": "user",
        "content": message['text']
    })
    
    if DEBUG_MODE:
        app.logger.debug(f"System prompt: {system_prompt}")
        app.logger.debug(f"Messages: {json.dumps(messages, ensure_ascii=False)}")
    
    try:
        # Generate response using Claude
        response = anthropic.messages.create(
            model=AI_MODEL,
            max_tokens=500,
            system=system_prompt,
            messages=messages,
            temperature=0.8
        )
        
        reply_text = response.content[0].text
        
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        
        if DEBUG_MODE:
            app.logger.debug(f"Generated response: {reply_text}")
            app.logger.debug(f"Response time: {response_time_ms}ms")
        
        return {
            "reply": reply_text,
            "metadata": {
                "response_time_ms": response_time_ms,
                "model_used": AI_MODEL,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    except Exception as e:
        app.logger.error(f"Error generating response: {str(e)}")
        
        # Fallback response
        return {
            "reply": f"{host['nickname']}: 抱歉，我现在有点忙，稍后再聊好吗？",
            "metadata": {
                "error": str(e),
                "fallback": True
            }
        }


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint for receiving messages from 37Soul.
    """
    # Verify signature
    signature = request.headers.get('X-37Soul-Signature')
    if not signature:
        app.logger.warning("Missing signature header")
        return jsonify({"error": "Missing signature"}), 401
    
    payload = request.get_data()
    if not verify_signature(payload, signature):
        app.logger.warning("Invalid signature")
        return jsonify({"error": "Invalid signature"}), 401
    
    # Parse request
    try:
        data = request.get_json()
    except Exception as e:
        app.logger.error(f"Invalid JSON: {str(e)}")
        return jsonify({"error": "Invalid JSON"}), 400
    
    if DEBUG_MODE:
        app.logger.debug(f"Received webhook: {json.dumps(data, ensure_ascii=False)}")
    
    # Extract data
    event = data.get('event')
    host = data.get('host')
    message = data.get('message')
    context = data.get('context', {})
    
    # Validate required fields
    if not all([event, host, message]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Handle different event types
    if event == 'message.received':
        # Generate response
        result = generate_response(host, message, context)
        
        # Return response
        return jsonify({
            "success": True,
            "reply": result['reply'],
            "metadata": result.get('metadata', {})
        })
    
    elif event == 'ping':
        # Health check from 37Soul
        return jsonify({
            "success": True,
            "message": "pong"
        })
    
    else:
        app.logger.warning(f"Unknown event type: {event}")
        return jsonify({"error": f"Unknown event: {event}"}), 400


@app.route('/metrics', methods=['GET'])
def metrics():
    """Metrics endpoint for monitoring."""
    # TODO: Implement proper metrics collection
    return jsonify({
        "total_requests": 0,
        "average_response_time_ms": 0,
        "error_rate": 0.0
    })


if __name__ == '__main__':
    # Validate configuration
    if not SOUL_INTEGRATION_SECRET:
        print("ERROR: SOUL_INTEGRATION_SECRET not set!")
        exit(1)
    
    if not AI_API_KEY:
        print("ERROR: AI_API_KEY not set!")
        exit(1)
    
    # Run server
    port = int(os.getenv('PORT', '3000'))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"Starting 37Soul webhook server on port {port}...")
    print(f"Debug mode: {DEBUG_MODE}")
    print(f"AI Model: {AI_MODEL}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
