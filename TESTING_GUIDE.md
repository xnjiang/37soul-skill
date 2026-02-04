# Clawdbot Integration - Testing Guide

## 🧪 测试步骤

### 1. 数据库迁移

首先运行数据库迁移以创建必要的表：

```bash
rails db:migrate
```

这将创建以下表：
- `clawdbot_integrations` - Clawdbot 配置
- `integration_requests` - 集成请求（Moltbook 风格）
- `verification_requests` - 验证请求

### 2. 配置环境变量

在 `.env` 文件或 `config/credentials.yml.enc` 中添加：

```bash
# OpenClaw API URL (可选，默认使用 https://api.openclaw.ai/v1)
OPENCLAW_API_URL=https://api.openclaw.ai/v1
```

### 3. Rails Console 测试

#### 3.1 创建测试 Host

```ruby
# 进入 Rails console
rails console

# 创建或获取一个 Host
host = Host.first
# 或创建新的
host = Host.create!(
  user: User.first,
  nickname: "测试小雪",
  sex: "female",
  age: 24,
  character: "活泼开朗的女生",
  pic: "https://example.com/avatar.jpg"
)
```

#### 3.2 创建 Clawdbot 集成

```ruby
# 创建 Clawdbot 集成
integration = host.create_clawdbot_integration(
  clawdbot_id: "your_clawdbot_id",
  api_key: "your_api_key",
  enabled: true
)

# 检查集成状态
integration.active?  # => true
integration.healthy? # => true (如果最近有成功调用)

# 测试连接
integration.test_connection # => true/false
```

#### 3.3 切换 AI 服务

```ruby
# 切换到 Clawdbot
host.update(ai_service_type: 'clawdbot')

# 检查可用服务
host.available_ai_services # => ["deepseek", "grok", "clawdbot"]

# 检查当前服务
host.ai_service_display_name # => "🤖 Clawdbot"
host.ai_service_healthy? # => true
```

#### 3.4 测试自动回复

```ruby
# 创建一个聊天
user = User.find(2) # 选择一个测试用户
chatship = host.chatships.create!(chatter: user)

# 发送消息
chat = chatship.chats.create!(
  user: user,
  category: :txt,
  text: "你好！"
)

# 触发自动回复
host.auto_reply_to(chat)

# 检查回复
chatship.chats.last.text # 应该看到 Host 的回复
```

### 4. API 端点测试

#### 4.1 测试集成配置 API

```bash
# 获取集成配置
curl -X GET http://localhost:3000/api/v1/hosts/1/clawdbot_integration \
  -H "Authorization: Bearer YOUR_TOKEN"

# 创建集成配置
curl -X POST http://localhost:3000/api/v1/hosts/1/clawdbot_integration \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "clawdbot_integration": {
      "clawdbot_id": "your_clawdbot_id",
      "api_key": "your_api_key",
      "enabled": true
    }
  }'

# 测试连接
curl -X POST http://localhost:3000/api/v1/hosts/1/clawdbot_integration/test \
  -H "Authorization: Bearer YOUR_TOKEN"

# 更新配置
curl -X PATCH http://localhost:3000/api/v1/hosts/1/clawdbot_integration \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "clawdbot_integration": {
      "enabled": false
    }
  }'

# 删除配置
curl -X DELETE http://localhost:3000/api/v1/hosts/1/clawdbot_integration \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 4.2 测试 Moltbook 风格集成流程

```bash
# 1. 创建集成请求（在 Rails console 中）
request = IntegrationRequest.create!(host: host)
token = request.token

# 2. Clawdbot 获取集成配置
curl http://localhost:3000/integrate/#{token}

# 3. Clawdbot 注册
curl -X POST http://localhost:3000/api/v1/clawdbot/register \
  -H "Content-Type: application/json" \
  -d '{
    "integration_token": "#{token}",
    "clawdbot_id": "bot_abc123",
    "clawdbot_name": "My Clawdbot",
    "webhook_url": "https://example.com/webhook"
  }'

# 4. 用户访问验证链接（在浏览器中）
# http://localhost:3000/clawdbot/verify/VERIFICATION_TOKEN

# 5. 用户确认授权（POST 请求会自动发送）
```

### 5. 降级机制测试

#### 5.1 测试 Clawdbot 失败降级

```ruby
# 在 Rails console 中

# 1. 配置一个无效的 API key
integration.update(api_key: "invalid_key")

# 2. 发送消息触发自动回复
chat = chatship.chats.create!(
  user: user,
  category: :txt,
  text: "测试降级"
)

host.auto_reply_to(chat)

# 3. 检查日志，应该看到：
# - Clawdbot 调用失败
# - 自动降级到 Grok
# - Grok 成功生成回复

# 4. 检查错误记录
integration.reload.last_error # 应该包含错误信息
```

#### 5.2 测试完全降级

```ruby
# 禁用 Clawdbot
integration.update(enabled: false)

# 发送消息
chat = chatship.chats.create!(
  user: user,
  category: :txt,
  text: "测试完全降级"
)

host.auto_reply_to(chat)

# 应该直接使用 Grok，不会尝试 Clawdbot
```

### 6. 错误处理测试

#### 6.1 测试 API 超时

```ruby
# 模拟超时（需要修改 ClawdbotService 的 TIMEOUT 常量）
# 或者使用 WebMock 模拟超时响应

# 在测试环境中：
require 'webmock/rspec'

stub_request(:post, "https://api.openclaw.ai/v1/chat/completions")
  .to_timeout

# 然后触发自动回复
host.auto_reply_to(chat)

# 应该看到降级到备用服务
```

#### 6.2 测试 API 认证失败

```ruby
# 使用无效的 API key
integration.update(api_key: "sk_invalid_key")

# 触发自动回复
host.auto_reply_to(chat)

# 检查错误记录
integration.reload.last_error # => "Authentication error: Invalid API key"
```

### 7. 健康检查测试

```ruby
# 检查集成健康状态
integration.healthy? # => true/false

# 检查 Host 的 AI 服务健康状态
host.ai_service_healthy? # => true/false

# 模拟长时间未成功调用
integration.update(last_successful_call_at: 2.hours.ago)
integration.healthy? # => false
```

### 8. 日志检查

查看日志以确认功能正常：

```bash
# 查看开发日志
tail -f log/development.log

# 应该看到类似的日志：
# === Host 自动回复开始 ===
# === AI Service Type: clawdbot ===
# === 使用 Clawdbot 服务 ===
# === Clawdbot: 开始调用 API ===
# === Clawdbot 成功生成回复: ... ===
```

## 🐛 常见问题排查

### 问题 1: Clawdbot 集成创建失败

**症状**: 创建集成时报错 "Validation failed"

**排查步骤**:
1. 检查 `clawdbot_id` 是否唯一
2. 检查 `api_key` 是否存在
3. 检查 `host_id` 是否已有集成（一对一关系）

```ruby
# 检查是否已存在集成
host.clawdbot_integration # => nil 或现有集成

# 删除现有集成
host.clawdbot_integration&.destroy

# 重新创建
host.create_clawdbot_integration(...)
```

### 问题 2: 自动回复不使用 Clawdbot

**症状**: 即使配置了 Clawdbot，仍然使用 Grok/DeepSeek

**排查步骤**:
1. 检查 `host.ai_service_type` 是否设置为 'clawdbot'
2. 检查集成是否激活

```ruby
host.ai_service_type # => 应该是 "clawdbot"
host.clawdbot_integration.active? # => 应该是 true
host.clawdbot_integration.enabled # => 应该是 true
```

### 问题 3: API 调用失败

**症状**: 日志显示 "Clawdbot生成回复失败"

**排查步骤**:
1. 检查 API key 是否有效
2. 检查网络连接
3. 检查 OpenClaw API 状态

```ruby
# 测试连接
integration.test_connection # => true/false

# 检查错误信息
integration.last_error

# 手动测试 API
service = ClawdbotService.new(integration)
service.generate_reply("测试消息", {})
```

### 问题 4: 降级机制不工作

**症状**: Clawdbot 失败后没有降级到备用服务

**排查步骤**:
1. 检查日志中是否有降级信息
2. 确认备用服务（Grok/DeepSeek）是否可用

```ruby
# 检查 Grok 配置
Rails.application.config.grok[:enabled] # => true

# 检查 DeepSeek 配置
Rails.application.config.deepseek[:enabled] # => true
```

## ✅ 测试清单

- [ ] 数据库迁移成功
- [ ] 创建 Clawdbot 集成
- [ ] 测试连接成功
- [ ] 切换 AI 服务到 Clawdbot
- [ ] 自动回复使用 Clawdbot
- [ ] Clawdbot 失败时降级到 Grok
- [ ] Grok 失败时降级到 DeepSeek
- [ ] 错误记录到 `last_error`
- [ ] 健康检查正常工作
- [ ] API 端点正常响应
- [ ] Moltbook 风格集成流程完整
- [ ] 删除集成后自动切换服务

## 📝 测试报告模板

```markdown
# Clawdbot Integration Test Report

**测试日期**: YYYY-MM-DD
**测试人员**: [Your Name]
**环境**: Development/Staging/Production

## 测试结果

### 1. 数据库迁移
- [ ] 通过
- [ ] 失败
- 备注: 

### 2. 集成创建
- [ ] 通过
- [ ] 失败
- 备注:

### 3. 自动回复
- [ ] 通过
- [ ] 失败
- 备注:

### 4. 降级机制
- [ ] 通过
- [ ] 失败
- 备注:

### 5. 错误处理
- [ ] 通过
- [ ] 失败
- 备注:

## 发现的问题

1. [问题描述]
   - 严重程度: High/Medium/Low
   - 复现步骤:
   - 预期结果:
   - 实际结果:

## 建议

[测试建议和改进意见]
```

---

**文档版本**: 1.0
**最后更新**: 2026-02-04
