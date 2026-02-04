#!/bin/bash
# Test webhook with a sample message

WEBHOOK_URL="${CLAWDBOT_WEBHOOK_URL:-http://localhost:3000/webhook}"
SECRET="${SOUL_INTEGRATION_SECRET:-test-secret}"

# Sample payload
PAYLOAD='{
  "event": "message.received",
  "host": {
    "id": 123,
    "nickname": "小雪",
    "age": 24,
    "sex": "female",
    "character": "活泼开朗的24岁女生，喜欢旅行和美食，性格外向热情"
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
}'

# Calculate signature
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')

echo "Testing webhook at: $WEBHOOK_URL"
echo "Payload:"
echo "$PAYLOAD" | jq .
echo ""
echo "Sending request..."
echo ""

# Send request
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-37Soul-Signature: sha256=$SIGNATURE" \
  -d "$PAYLOAD" \
  | jq .

echo ""
echo "Test complete!"
