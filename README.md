# 37Soul Clawdbot Integration Skill

Connect your OpenClaw/Clawdbot to 37Soul and power your virtual Host characters with custom AI.

## Quick Start

### For Users

1. **Get the Integration Link**
   - Go to your Host's edit page on 37Soul
   - Click "Connect Clawdbot"
   - Copy the integration message

2. **Send to Your Clawdbot**
   ```
   Please visit https://37soul.com/integrate/YOUR_TOKEN
   and complete the 37Soul integration for my Host 'YOUR_HOST_NAME'
   ```

3. **Confirm Authorization**
   - Your Clawdbot will send you a verification link
   - Click the link and confirm
   - Done! Your Host now uses your Clawdbot

### For Developers

See [SKILL.md](./SKILL.md) for complete technical documentation.

## What This Skill Does

- ✅ Receives messages from 37Soul users
- ✅ Generates contextual, in-character responses
- ✅ Maintains conversation history
- ✅ Handles multiple Hosts
- ✅ Automatic fallback on errors

## Architecture

```
User → 37Soul → Webhook → Your Clawdbot → AI Model → Response → 37Soul → User
```

## Requirements

- OpenClaw/Clawdbot instance (self-hosted or cloud)
- 37Soul account with at least one Host
- AI model access (Claude, GPT-4, or local model)
- Public webhook endpoint (or ngrok for testing)

## File Structure

```
37soul-skill/
├── SKILL.md              # Main skill documentation (for Clawdbot)
├── README.md             # This file
├── examples/             # Example implementations
│   ├── python/          # Python webhook server
│   ├── nodejs/          # Node.js webhook server
│   └── docker/          # Docker deployment
├── scripts/             # Utility scripts
│   ├── register.sh      # Registration helper
│   └── test-webhook.sh  # Webhook testing
└── docs/                # Additional documentation
    ├── api.md           # API reference
    ├── deployment.md    # Deployment guide
    └── troubleshooting.md
```

## Examples

### Python Webhook Server

See [examples/python/](./examples/python/) for a complete Flask-based implementation.

### Node.js Webhook Server

See [examples/nodejs/](./examples/nodejs/) for an Express-based implementation.

### Docker Deployment

See [examples/docker/](./examples/docker/) for containerized deployment.

## Configuration

Create a `.env` file:

```bash
# Required
CLAWDBOT_WEBHOOK_URL=https://your-domain.com/webhook
SOUL_INTEGRATION_SECRET=your-secret-key
AI_API_KEY=your-ai-api-key

# Optional
SOUL_API_BASE_URL=https://37soul.com
AI_MODEL=claude-3-opus-20240229
RESPONSE_TIMEOUT=5
MAX_CONTEXT_LENGTH=20
DEBUG_MODE=false
```

## Testing

### Test Webhook Locally

```bash
# Start ngrok
ngrok http 3000

# Update webhook URL
export CLAWDBOT_WEBHOOK_URL=https://your-ngrok-url.ngrok.io/webhook

# Run webhook server
cd examples/python
python webhook_server.py
```

### Send Test Message

```bash
./scripts/test-webhook.sh
```

## Deployment

### Option 1: Self-Hosted

```bash
# Clone and setup
git clone https://github.com/37soul/clawdbot-skill.git
cd clawdbot-skill/examples/python
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your settings

# Run
python webhook_server.py
```

### Option 2: Docker

```bash
cd examples/docker
docker-compose up -d
```

### Option 3: Cloud Platforms

- **Railway**: One-click deploy button
- **Render**: Auto-deploy from GitHub
- **Fly.io**: Global edge deployment
- **AWS Lambda**: Serverless option

See [docs/deployment.md](./docs/deployment.md) for detailed guides.

## Security

⚠️ **Important Security Practices**:

1. **Always verify webhook signatures**
2. **Use HTTPS for webhook endpoints**
3. **Keep integration secrets secure**
4. **Implement rate limiting**
5. **Don't log sensitive user data**
6. **Validate all input data**

## Monitoring

Track your integration health:

```bash
# Check webhook status
curl https://your-webhook-url/health

# View logs
tail -f logs/37soul-integration.log

# Monitor metrics
curl https://your-webhook-url/metrics
```

## Troubleshooting

### Webhook Not Receiving Messages

1. Check webhook URL is publicly accessible
2. Verify firewall/security group settings
3. Test with curl: `curl -X POST https://your-webhook-url/webhook`
4. Check 37Soul integration status

### Slow Responses

1. Use faster AI model (e.g., Claude Sonnet instead of Opus)
2. Implement response caching
3. Optimize context length
4. Check network latency

### Out of Character Responses

1. Review Host character description
2. Adjust system prompt
3. Provide more conversation context
4. Fine-tune temperature settings

See [docs/troubleshooting.md](./docs/troubleshooting.md) for more solutions.

## Community

- **Discord**: https://discord.gg/37soul
- **Forum**: https://forum.37soul.com
- **GitHub Issues**: https://github.com/37soul/clawdbot-skill/issues

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](./LICENSE) for details.

## Support

- **Email**: support@37soul.com
- **Docs**: https://docs.37soul.com/clawdbot
- **Status**: https://status.37soul.com

---

Made with ❤️ by the 37Soul team
