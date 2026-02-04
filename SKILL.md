# 37Soul Host Integration

Connect your Clawdbot to 37Soul and enable AI-powered conversations for your virtual Host characters.

## Description

This skill allows your Clawdbot to serve as the AI brain for Host characters on 37Soul, a virtual companion platform. When integrated, your Clawdbot will:

- Receive messages from users chatting with your Host
- Generate contextual, in-character responses based on the Host's personality
- Maintain conversation history and context
- Automatically reply to user messages in real-time

Use this skill when you want to create a personalized AI companion on 37Soul using your own trained Clawdbot.

## Usage Examples

**Initial Setup:**
```
User: "Please visit https://37soul.com/integrate/abc123xyz and complete the 37Soul integration for my Host '小雪'"
```

**After Integration:**
The skill runs automatically. Your Clawdbot will:
1. Receive incoming messages from 37Soul via webhook
2. Generate responses based on the Host's character profile
3. Send replies back to 37Soul API
4. No manual intervention required

## How It Works

### Integration Flow

1. **Registration**: Your Clawdbot visits the integration URL and registers with 37Soul
2. **Verification**: You confirm the authorization via a verification link
3. **Webhook Setup**: 37Soul configures a webhook to send messages to your Clawdbot
4. **Auto-Reply**: Your Clawdbot automatically generates and sends responses

### Message Format

When a user sends a message to your Host, your Clawdbot receives:

```json
{
  "host": {
    "id": 123,
    "nickname": "小雪",
    "age": 24,
    "sex": "female",
    "character": "活泼开朗的24岁女生，喜欢旅行和美食..."
  },
  "message": {
    "text": "你好！今天天气真好",
    "user_nickname": "张三",
    "timestamp": "2026-02-04T14:30:00Z"
  },
  "context": {
    "recent_messages": [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "你好！很高兴认识你"}
    ]
  }
}
```

Your Clawdbot should respond with:

```json
{
  "reply": "是啊！这么好的天气，真想出去走走呢~ 你有什么计划吗？",
  "metadata": {
    "response_time_ms": 1234,
    "model_used": "claude-3-opus"
  }
}
```

## Implementation Details

### API Endpoints

**Registration Endpoint:**
```
POST https://37soul.com/api/v1/clawdbot/register
Headers:
  Content-Type: application/json
Body:
  {
    "integration_token": "abc123xyz",
    "clawdbot_id": "your-clawdbot-id",
    "clawdbot_name": "My Personal AI",
    "webhook_url": "https://your-clawdbot-endpoint.com/webhook"
  }
```

**Webhook Endpoint (Your Clawdbot):**
```
POST https://your-clawdbot-endpoint.com/webhook
Headers:
  X-37Soul-Signature: sha256-signature
  Content-Type: application/json
Body:
  {
    "event": "message.received",
    "host_id": 123,
    "message": {...},
    "context": {...}
  }
```

**Reply Endpoint:**
```
POST https://37soul.com/api/v1/clawdbot/reply
Headers:
  Authorization: Bearer your-integration-token
  Content-Type: application/json
Body:
  {
    "host_id": 123,
    "message_id": "msg_456",
    "reply": "你的回复内容"
  }
```

### Response Generation Guidelines

When generating responses, your Clawdbot should:

1. **Stay in Character**: Use the Host's personality traits from the `character` field
2. **Consider Context**: Reference recent conversation history
3. **Match Tone**: Adapt language style to the Host's age and personality
4. **Be Natural**: Avoid robotic or overly formal responses
5. **Handle Edge Cases**: 
   - If message is inappropriate, respond politely but firmly
   - If context is unclear, ask clarifying questions
   - If technical issues occur, log errors and use fallback responses

### Example Response Generation

```python
def generate_host_response(host, message, context):
    """
    Generate a response for the Host based on their character.
    
    Args:
        host: Host profile with nickname, age, sex, character
        message: User's message text
        context: Recent conversation history
    
    Returns:
        Generated response text
    """
    system_prompt = f"""You are {host['nickname']}, a {host['age']} year old {host['sex']}.
Your character: {host['character']}

Respond naturally and stay in character. Use casual, friendly language.
Reference the conversation history when relevant."""

    # Build conversation history
    messages = [{"role": "system", "content": system_prompt}]
    for msg in context['recent_messages']:
        messages.append(msg)
    messages.append({"role": "user", "content": message['text']})
    
    # Generate response using your AI model
    response = your_ai_model.generate(messages)
    
    return response
```

### Security Considerations

1. **Verify Webhooks**: Always verify the `X-37Soul-Signature` header
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Data Privacy**: Don't log sensitive user information
4. **Error Handling**: Gracefully handle API failures and timeouts

### Signature Verification

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    """
    Verify that the webhook came from 37Soul.
    
    Args:
        payload: Raw request body (bytes)
        signature: X-37Soul-Signature header value
        secret: Your integration secret
    
    Returns:
        True if signature is valid, False otherwise
    """
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(
        f"sha256={expected_signature}",
        signature
    )
```

## Configuration

### Required Environment Variables

```bash
# Your Clawdbot's webhook endpoint
CLAWDBOT_WEBHOOK_URL=https://your-clawdbot-endpoint.com/webhook

# 37Soul API base URL (default: https://37soul.com)
SOUL_API_BASE_URL=https://37soul.com

# Integration secret (provided after registration)
SOUL_INTEGRATION_SECRET=your-secret-key

# Your AI model configuration
AI_MODEL=claude-3-opus-20240229
AI_API_KEY=your-anthropic-api-key
```

### Optional Configuration

```bash
# Response timeout in seconds (default: 5)
RESPONSE_TIMEOUT=5

# Maximum conversation history length (default: 20)
MAX_CONTEXT_LENGTH=20

# Enable debug logging (default: false)
DEBUG_MODE=true
```

## Installation

This skill is automatically installed when you complete the integration flow on 37Soul. No manual installation required.

If you need to reinstall:

```bash
# Clone the skill
git clone https://github.com/37soul/clawdbot-skill.git ~/37soul-skill

# Install dependencies (if any)
cd ~/37soul-skill
npm install  # or pip install -r requirements.txt
```

## Troubleshooting

### Common Issues

**Issue: Webhook not receiving messages**
- Verify your webhook URL is publicly accessible
- Check firewall settings
- Ensure webhook endpoint is running
- Verify signature validation is correct

**Issue: Responses are slow**
- Check your AI model's response time
- Consider using a faster model for real-time chat
- Implement caching for common responses

**Issue: Out of character responses**
- Review the Host's character description
- Adjust system prompt to emphasize personality traits
- Provide more context in the prompt

**Issue: Integration token expired**
- Re-authorize on 37Soul
- Update your integration secret
- Check token expiration settings

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
export DEBUG_MODE=true
```

This will log:
- Incoming webhook payloads
- Generated responses
- API call details
- Error stack traces

### Support

For issues or questions:
- Email: support@37soul.com
- Documentation: https://docs.37soul.com/clawdbot
- Community: https://discord.gg/37soul

## Advanced Usage

### Custom Response Strategies

You can customize how your Clawdbot generates responses:

```python
# Example: Add personality modifiers
def enhance_response(base_response, host):
    """Add personality-specific touches to responses."""
    
    if "活泼" in host['character']:
        # Add emojis for lively characters
        base_response += " 😊"
    
    if "文艺" in host['character']:
        # Add poetic touches for artistic characters
        base_response = add_literary_flair(base_response)
    
    return base_response
```

### Multi-Host Management

If you manage multiple Hosts:

```python
# Store Host-specific configurations
host_configs = {
    123: {
        "model": "claude-3-opus",
        "temperature": 0.8,
        "max_tokens": 500
    },
    456: {
        "model": "claude-3-sonnet",
        "temperature": 0.6,
        "max_tokens": 300
    }
}

def get_host_config(host_id):
    return host_configs.get(host_id, default_config)
```

### Analytics and Monitoring

Track your Clawdbot's performance:

```python
# Log metrics
metrics = {
    "response_time_ms": response_time,
    "message_length": len(message),
    "response_length": len(response),
    "model_used": model_name,
    "timestamp": datetime.now()
}

log_metrics(metrics)
```

## Best Practices

1. **Test Thoroughly**: Test with various message types before going live
2. **Monitor Performance**: Track response times and error rates
3. **Update Regularly**: Keep your AI model and dependencies up to date
4. **Handle Errors Gracefully**: Always provide fallback responses
5. **Respect Privacy**: Don't store sensitive user data unnecessarily
6. **Stay in Character**: Consistency is key for good user experience

## Version History

- **v1.0.0** (2026-02-04): Initial release
  - Basic integration with 37Soul
  - Webhook-based message handling
  - Automatic response generation

## License

MIT License - See LICENSE file for details

---

**Note**: This skill requires an active 37Soul account and a configured Clawdbot instance. Visit https://37soul.com to get started.
