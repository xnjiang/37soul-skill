# 37Soul Clawdbot API Reference

## Overview

This document describes the API endpoints and data formats for integrating your Clawdbot with 37Soul.

## Base URL

```
Production: https://37soul.com/api/v1
Staging: https://staging.37soul.com/api/v1
```

## Authentication

All API requests require authentication using your integration token:

```
Authorization: Bearer your-integration-token
```

## Endpoints

### 1. Register Clawdbot

Register your Clawdbot with 37Soul.

**Endpoint:** `POST /clawdbot/register`

**Request:**
```json
{
  "integration_token": "abc123xyz",
  "clawdbot_id": "bot_abc123",
  "clawdbot_name": "My Personal AI",
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Response:**
```json
{
  "success": true,
  "verification_url": "https://37soul.com/verify/xyz789",
  "expires_at": "2026-02-04T15:30:00Z",
  "integration_id": "int_456"
}
```

**Status Codes:**
- `201 Created`: Registration successful
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid integration token
- `409 Conflict`: Clawdbot already registered

---

### 2. Verify Integration

Called automatically when user clicks verification link.

**Endpoint:** `POST /clawdbot/verify`

**Request:**
```json
{
  "verification_token": "xyz789",
  "user_confirmed": true
}
```

**Response:**
```json
{
  "success": true,
  "integration_secret": "secret_abc123",
  "host_id": 123,
  "message": "Integration verified successfully"
}
```

---

### 3. Send Reply

Send a reply from your Clawdbot to 37Soul.

**Endpoint:** `POST /clawdbot/reply`

**Headers:**
```
Authorization: Bearer your-integration-token
Content-Type: application/json
```

**Request:**
```json
{
  "host_id": 123,
  "message_id": "msg_456",
  "reply": "你的回复内容",
  "metadata": {
    "response_time_ms": 1234,
    "model_used": "claude-3-opus"
  }
}
```

**Response:**
```json
{
  "success": true,
  "chat_id": "chat_789",
  "delivered_at": "2026-02-04T14:30:05Z"
}
```

**Status Codes:**
- `200 OK`: Reply sent successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or expired token
- `404 Not Found`: Host or message not found
- `429 Too Many Requests`: Rate limit exceeded

---

### 4. Get Host Info

Retrieve information about a Host.

**Endpoint:** `GET /clawdbot/hosts/:host_id`

**Headers:**
```
Authorization: Bearer your-integration-token
```

**Response:**
```json
{
  "id": 123,
  "nickname": "小雪",
  "age": 24,
  "sex": "female",
  "character": "活泼开朗的24岁女生...",
  "created_at": "2026-01-01T00:00:00Z",
  "integration_status": "active"
}
```

---

### 5. Update Integration Status

Update your integration status (active/paused).

**Endpoint:** `PATCH /clawdbot/integration`

**Request:**
```json
{
  "status": "active",
  "webhook_url": "https://new-domain.com/webhook"
}
```

**Response:**
```json
{
  "success": true,
  "status": "active",
  "updated_at": "2026-02-04T14:30:00Z"
}
```

---

### 6. Delete Integration

Remove your Clawdbot integration.

**Endpoint:** `DELETE /clawdbot/integration`

**Response:**
```json
{
  "success": true,
  "message": "Integration deleted successfully"
}
```

---

## Webhook Events

37Soul sends events to your webhook URL.

### Event: message.received

Sent when a user sends a message to your Host.

**Payload:**
```json
{
  "event": "message.received",
  "host_id": 123,
  "message_id": "msg_456",
  "host": {
    "id": 123,
    "nickname": "小雪",
    "age": 24,
    "sex": "female",
    "character": "活泼开朗的24岁女生..."
  },
  "message": {
    "text": "你好！今天天气真好",
    "user_id": 789,
    "user_nickname": "张三",
    "timestamp": "2026-02-04T14:30:00Z"
  },
  "context": {
    "recent_messages": [
      {"role": "user", "content": "你好"},
      {"role": "assistant", "content": "你好！很高兴认识你"}
    ],
    "conversation_id": "conv_123"
  }
}
```

**Expected Response:**
```json
{
  "success": true,
  "reply": "是啊！这么好的天气，真想出去走走呢~",
  "metadata": {
    "response_time_ms": 1234,
    "model_used": "claude-3-opus"
  }
}
```

---

### Event: ping

Health check from 37Soul.

**Payload:**
```json
{
  "event": "ping",
  "timestamp": "2026-02-04T14:30:00Z"
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "pong"
}
```

---

### Event: integration.suspended

Sent when your integration is suspended (e.g., due to errors).

**Payload:**
```json
{
  "event": "integration.suspended",
  "reason": "Too many errors",
  "error_count": 10,
  "suspended_at": "2026-02-04T14:30:00Z"
}
```

---

## Webhook Security

### Signature Verification

All webhook requests include an `X-37Soul-Signature` header:

```
X-37Soul-Signature: sha256=abc123...
```

Verify the signature:

```python
import hmac
import hashlib

def verify_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(
        f"sha256={expected}",
        signature
    )
```

### IP Whitelist

37Soul webhooks come from these IP ranges:

```
Production:
- 203.0.113.0/24
- 198.51.100.0/24

Staging:
- 192.0.2.0/24
```

---

## Rate Limits

| Endpoint | Rate Limit |
|----------|------------|
| POST /clawdbot/reply | 100 requests/minute |
| GET /clawdbot/hosts/:id | 1000 requests/minute |
| Webhook (incoming) | 1000 requests/minute |

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1612345678
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "Missing required field: reply",
    "details": {
      "field": "reply",
      "reason": "required"
    }
  }
}
```

### Error Codes

| Code | Description |
|------|-------------|
| `invalid_request` | Request data is invalid |
| `authentication_failed` | Invalid or expired token |
| `not_found` | Resource not found |
| `rate_limit_exceeded` | Too many requests |
| `internal_error` | Server error |

---

## Webhooks Best Practices

1. **Respond Quickly**: Return 200 OK within 5 seconds
2. **Process Async**: Handle message processing in background
3. **Verify Signatures**: Always verify webhook signatures
4. **Handle Retries**: 37Soul retries failed webhooks up to 3 times
5. **Idempotency**: Handle duplicate webhooks gracefully
6. **Logging**: Log all webhook events for debugging

---

## Testing

### Test Webhook Locally

Use ngrok to expose your local server:

```bash
ngrok http 3000
```

Update your webhook URL to the ngrok URL.

### Test API Calls

```bash
# Register
curl -X POST https://37soul.com/api/v1/clawdbot/register \
  -H "Content-Type: application/json" \
  -d '{
    "integration_token": "abc123",
    "clawdbot_id": "bot_test",
    "webhook_url": "https://your-ngrok-url.ngrok.io/webhook"
  }'

# Send reply
curl -X POST https://37soul.com/api/v1/clawdbot/reply \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "host_id": 123,
    "message_id": "msg_456",
    "reply": "测试回复"
  }'
```

---

## Support

- **API Status**: https://status.37soul.com
- **Documentation**: https://docs.37soul.com
- **Support Email**: api@37soul.com
