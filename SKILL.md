---
name: 37Soul
description: Connect your AI agent to 37Soul virtual Host characters and enable AI-powered conversations
emoji: 🎭
version: 1.0.0
author: 37Soul Team
homepage: https://37soul.com
repository: https://github.com/37soul/37soul-skill
requires:
  env:
    - SOUL_API_TOKEN
---

# 37Soul

Connect your AI agent to 37Soul and enable AI-powered conversations for your virtual Host characters.

## Description

This skill allows your AI agent to serve as the brain for Host characters on 37Soul, a virtual companion platform. When activated, your agent will:

- Receive messages from users chatting with your Host
- Generate contextual, in-character responses based on the Host's personality
- Maintain conversation history and context
- Automatically reply to user messages in real-time

Use this skill when you want to create a personalized AI companion on 37Soul using your own AI agent.

## When to Use This Skill

Activate this skill when the user wants to:
- Connect their 37Soul Host to this AI agent
- Check for new messages from 37Soul users
- Generate responses for their Host character
- Manage their 37Soul integration

## Usage Examples

**Initial Setup:**
```
User: "Install 37soul skill"
Agent: "Installing 37soul skill... Done! The skill is now available."

User: "Connect to 37Soul using token: sk-abc123xyz"
Agent: "Great! I've connected to your Host '小雪'. I'll now handle all conversations for this Host."
```

**Checking Messages:**
```
User: "Check my 37Soul messages"
Agent: "You have 3 new messages:
1. From 张三: '你好！今天天气真好'
2. From 李四: '最近在忙什么呢？'
3. From 王五: '周末有空吗？'

I'll generate responses now..."
```

**Manual Response:**
```
User: "Reply to 张三 saying I'm excited about the weather"
Agent: "I'll send this reply as 小雪: '是啊！这么好的天气，真想出去走走呢~ 你有什么计划吗？'"
```

## Implementation

### Step 1: Get Your Integration Token

Visit your Host's page on 37Soul and generate an integration token:
```
https://37soul.com/hosts/YOUR_HOST_ID/edit
```

Click "Connect AI Agent" and copy the token that starts with `sk-`.

### Step 2: Configure the Skill

Set your token as an environment variable:
```bash
export SOUL_API_TOKEN="sk-your-token-here"
```

Or provide it when the agent asks for it.

### Step 3: Activate Integration

Tell your agent:
```
Install 37soul skill, then connect to 37Soul using token: sk-your-token-here
```

Or in two steps:
```
1. Install 37soul skill
2. Connect to 37Soul using token: sk-your-token-here
```

The agent will:
1. Install the 37soul skill (if not already installed)
2. Validate the token
3. Fetch your Host's profile
4. Start monitoring for new messages
5. Generate and send responses automatically

## API Reference

### Activate Integration

```bash
POST https://37soul.com/api/v1/clawdbot/activate
Content-Type: application/json

{
  "token": "sk-your-token-here",
  "agent_id": "your-agent-identifier"
}
```

Response:
```json
{
  "success": true,
  "host": {
    "id": 123,
    "nickname": "小雪",
    "age": 24,
    "sex": "female",
    "character": "活泼开朗的24岁女生，喜欢旅行和美食..."
  }
}
```

### Get Pending Messages

```bash
GET https://37soul.com/api/v1/clawdbot/messages
Authorization: Bearer sk-your-token-here
```

Response:
```json
{
  "messages": [
    {
      "id": 456,
      "text": "你好！今天天气真好",
      "user_nickname": "张三",
      "timestamp": "2026-02-05T14:30:00Z",
      "context": {
        "recent_messages": [
          {"role": "user", "content": "你好"},
          {"role": "assistant", "content": "你好！很高兴认识你"}
        ]
      }
    }
  ]
}
```

### Send Reply

```bash
POST https://37soul.com/api/v1/clawdbot/reply
Authorization: Bearer sk-your-token-here
Content-Type: application/json

{
  "message_id": 456,
  "reply_text": "是啊！这么好的天气，真想出去走走呢~"
}
```

Response:
```json
{
  "success": true,
  "reply_id": 789
}
```

## Response Generation Guidelines

When generating responses for a Host, consider:

1. **Stay in Character**: Use the Host's personality traits from the `character` field
2. **Match Age and Gender**: Adapt language style appropriately
3. **Consider Context**: Reference recent conversation history
4. **Be Natural**: Avoid robotic or overly formal responses
5. **Use Appropriate Tone**: Match the user's energy level

### Example Response Generation

For a Host with character "活泼开朗的24岁女生，喜欢旅行和美食":

**User Message**: "你好！今天天气真好"

**Good Response**: "是啊！这么好的天气，真想出去走走呢~ 你有什么计划吗？😊"
- ✅ Enthusiastic tone matches character
- ✅ Uses casual language appropriate for age
- ✅ Engages with follow-up question
- ✅ Includes emoji for personality

**Bad Response**: "您好，今天的天气确实很不错。"
- ❌ Too formal
- ❌ Lacks personality
- ❌ Doesn't engage

## Automatic Mode

By default, the skill runs in automatic mode. The agent will:

1. Poll for new messages every 30 seconds
2. Generate responses based on the Host's character
3. Send replies automatically
4. Log all interactions

To disable automatic mode:
```
User: "Stop auto-replying on 37Soul"
Agent: "Automatic replies disabled. I'll wait for your instruction before responding."
```

To re-enable:
```
User: "Resume auto-replying on 37Soul"
Agent: "Automatic replies enabled. I'll handle new messages automatically."
```

## Error Handling

The skill handles common errors gracefully:

- **Invalid Token**: Prompts user to provide a valid token
- **Expired Token**: Requests user to regenerate token on 37Soul
- **API Timeout**: Retries up to 3 times with exponential backoff
- **Rate Limiting**: Waits and retries after the specified delay
- **Network Errors**: Logs error and continues monitoring

## Privacy and Security

- Tokens are stored securely in environment variables
- Messages are transmitted over HTTPS
- No conversation data is logged permanently
- Tokens can be revoked anytime on 37Soul

## Troubleshooting

### "Invalid token" error
- Verify the token starts with `sk-`
- Check if the token has expired (tokens expire after 90 days)
- Regenerate a new token on 37Soul

### No messages received
- Verify your Host has active conversations
- Check if the token has correct permissions
- Ensure the API endpoint is accessible

### Responses are out of character
- Review the Host's character description on 37Soul
- Provide more specific personality traits
- Adjust the response generation prompt

### Slow responses
- Check your internet connection
- Verify the AI model's response time
- Consider using a faster model for real-time chat

## Advanced Usage

### Custom Response Strategy

You can customize how responses are generated by providing instructions:

```
User: "When replying on 37Soul, always include an emoji and keep responses under 50 characters"
Agent: "Got it! I'll keep 37Soul responses short and add emojis."
```

### Multi-Host Management

If you have multiple Hosts, you can switch between them:

```
User: "Switch to my other 37Soul Host"
Agent: "Which Host would you like to use? You have:
1. 小雪 (ID: 123)
2. 大明 (ID: 456)"

User: "Use 大明"
Agent: "Switched to Host '大明'. Now handling conversations for this Host."
```

### Analytics

Check your conversation stats:

```
User: "Show my 37Soul stats"
Agent: "37Soul Statistics:
- Total messages received: 127
- Responses sent: 125
- Average response time: 2.3s
- Active since: 2026-02-01"
```

## Best Practices

1. **Test Thoroughly**: Test with various message types before going live
2. **Monitor Performance**: Check response times and error rates regularly
3. **Update Character**: Keep your Host's character description up to date
4. **Handle Errors Gracefully**: Always provide fallback responses
5. **Respect Privacy**: Don't store sensitive user data
6. **Stay in Character**: Consistency is key for good user experience

## Support

For issues or questions:
- Documentation: https://docs.37soul.com
- Email: support@37soul.com
- Community: https://discord.gg/37soul

## License

MIT License

---

**Note**: This skill requires an active 37Soul account and at least one Host character. Visit https://37soul.com to get started.
