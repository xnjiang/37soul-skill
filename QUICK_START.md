# 🚀 Clawdbot Integration - 快速开始指南

## 5 分钟快速上手

### 步骤 1: 运行数据库迁移（1 分钟）

```bash
cd /path/to/37soul
rails db:migrate
```

**预期输出**:
```
== 20260204_create_clawdbot_integrations: migrating =======================
-- create_table(:clawdbot_integrations)
   -> 0.0234s
== 20260204_create_clawdbot_integrations: migrated (0.0235s) ==============

== 20260204_create_integration_requests: migrating ========================
-- create_table(:integration_requests)
   -> 0.0156s
== 20260204_create_integration_requests: migrated (0.0157s) ===============

== 20260204_create_verification_requests: migrating =======================
-- create_table(:verification_requests)
   -> 0.0178s
== 20260204_create_verification_requests: migrated (0.0179s) ==============

== 20260204_add_ai_service_type_to_hosts: migrating =======================
-- add_column(:hosts, :ai_service_type, :string)
   -> 0.0089s
== 20260204_add_ai_service_type_to_hosts: migrated (0.0090s) ==============
```

### 步骤 2: 重启服务器（30 秒）

```bash
# 开发环境
rails restart

# 或者
touch tmp/restart.txt
```

### 步骤 3: 验证安装（1 分钟）

```bash
rails console
```

```ruby
# 检查表是否创建
ActiveRecord::Base.connection.table_exists?('clawdbot_integrations')
# => true

# 检查 Host 模型
Host.first.respond_to?(:clawdbot_integration)
# => true

# 检查翻译
I18n.t('hosts.edit.ai_service_title', locale: 'zh-CN')
# => "AI 服务配置"

# 退出
exit
```

### 步骤 4: 访问配置界面（1 分钟）

1. 启动 Rails 服务器（如果还没启动）:
   ```bash
   rails server
   ```

2. 在浏览器中访问: `http://localhost:3000`

3. 登录你的账户

4. 进入任意 Host 的编辑页面

5. 点击 "AI 服务配置" 标签页

6. 你应该看到三个 AI 服务选项：
   - ✅ DeepSeek（免费）
   - ✅ Grok（高级）
   - ✅ Clawdbot（自定义）

### 步骤 5: 配置 Clawdbot（2 分钟）

1. **获取 Clawdbot 凭证**:
   - 访问 [OpenClaw.ai](https://openclaw.ai)
   - 创建或登录账户
   - 创建一个新的 Clawdbot
   - 复制 Clawdbot ID（例如：`bot_abc123`）
   - 生成 API Key（例如：`sk_...`）

2. **在 37Soul 中配置**:
   - 选择 "Clawdbot（自定义）" 单选按钮
   - 配置面板会自动展开
   - 填写 Clawdbot ID
   - 填写 API Key
   - 点击 "测试连接" 按钮
   - 看到 "✅ 连接成功！" 消息
   - 点击 "保存配置" 按钮

3. **完成！**
   - 页面会自动刷新
   - 你的 Host 现在使用 Clawdbot 进行自动回复

---

## 🧪 快速测试

### 测试自动回复

```bash
rails console
```

```ruby
# 1. 获取你的 Host
host = Host.find(YOUR_HOST_ID)

# 2. 检查配置
host.ai_service_type
# => "clawdbot"

host.clawdbot_integration.active?
# => true

# 3. 创建测试聊天
user = User.find(YOUR_USER_ID)
chatship = host.chatships.find_or_create_by!(chatter: user)

# 4. 发送测试消息
chat = chatship.chats.create!(
  user: user,
  category: :txt,
  text: "你好！"
)

# 5. 触发自动回复
host.auto_reply_to(chat)

# 6. 查看回复
chatship.chats.last.text
# => "小雪: 你好！很高兴见到你..."

# 7. 检查日志
# 在 log/development.log 中应该看到：
# === 使用 Clawdbot 服务 ===
# === Clawdbot 成功生成回复: ... ===
```

---

## 📋 快速检查清单

完成以下检查以确保一切正常：

- [ ] 数据库迁移成功
- [ ] 服务器重启成功
- [ ] 可以访问 Host 编辑页面
- [ ] 可以看到 "AI 服务配置" 标签页
- [ ] 可以选择 Clawdbot 选项
- [ ] 可以填写配置信息
- [ ] 测试连接成功
- [ ] 保存配置成功
- [ ] 自动回复使用 Clawdbot

---

## 🆘 遇到问题？

### 问题 1: 迁移失败

**错误**: `PG::UndefinedTable: ERROR: relation "clawdbot_integrations" does not exist`

**解决**:
```bash
# 检查迁移状态
rails db:migrate:status

# 如果有待执行的迁移，运行：
rails db:migrate

# 如果还是失败，尝试：
rails db:rollback
rails db:migrate
```

### 问题 2: 看不到 "AI 服务配置" 标签

**可能原因**:
1. 浏览器缓存问题
2. 服务器没有重启

**解决**:
```bash
# 清除浏览器缓存（Ctrl+Shift+R 或 Cmd+Shift+R）

# 重启服务器
rails restart

# 或者强制重启
pkill -9 -f puma
rails server
```

### 问题 3: 测试连接失败

**错误**: "❌ 连接失败"

**检查**:
1. Clawdbot ID 是否正确
2. API Key 是否正确
3. 网络连接是否正常
4. OpenClaw.ai 服务是否可用

**解决**:
```ruby
# 在 Rails console 中手动测试
integration = ClawdbotIntegration.last
service = ClawdbotService.new(integration)

# 测试连接
service.test_connection
# 查看错误信息

# 检查 API Key
integration.api_key.present?
# => true

# 检查 Clawdbot ID
integration.clawdbot_id
# => "bot_abc123"
```

### 问题 4: 自动回复不使用 Clawdbot

**检查**:
```ruby
host = Host.find(YOUR_HOST_ID)

# 1. 检查 ai_service_type
host.ai_service_type
# 应该是 "clawdbot"，如果不是：
host.update(ai_service_type: 'clawdbot')

# 2. 检查集成状态
host.clawdbot_integration.active?
# 应该是 true

# 3. 检查最后错误
host.clawdbot_integration.last_error
# 如果有错误，会显示错误信息
```

---

## 📚 下一步

完成快速开始后，你可以：

1. **阅读完整文档**:
   - [完成总结](./COMPLETION_SUMMARY.md)
   - [测试指南](./TESTING_GUIDE.md)
   - [前端实现](./FRONTEND_IMPLEMENTATION.md)

2. **探索高级功能**:
   - 更新配置
   - 查看使用统计
   - 配置 Webhook

3. **优化配置**:
   - 调整超时时间
   - 配置降级策略
   - 监控服务健康

---

## 💡 提示和技巧

### 提示 1: 使用环境变量

如果你有多个环境（开发、测试、生产），可以使用环境变量：

```bash
# .env
OPENCLAW_API_URL=https://api.openclaw.ai/v1
```

### 提示 2: 查看日志

开发时，实时查看日志很有帮助：

```bash
tail -f log/development.log | grep "Clawdbot"
```

### 提示 3: 快速切换服务

在 Rails console 中快速切换 AI 服务：

```ruby
host = Host.find(YOUR_HOST_ID)

# 切换到 Clawdbot
host.update(ai_service_type: 'clawdbot')

# 切换到 Grok
host.update(ai_service_type: 'grok')

# 切换到 DeepSeek
host.update(ai_service_type: 'deepseek')
```

### 提示 4: 批量配置

如果你有多个 Host 需要配置：

```ruby
# 为所有 Host 创建相同的 Clawdbot 配置
Host.where(user_id: YOUR_USER_ID).each do |host|
  next if host.clawdbot_integration.present?
  
  host.create_clawdbot_integration(
    clawdbot_id: "bot_abc123",
    api_key: "sk_your_api_key",
    enabled: true
  )
  
  host.update(ai_service_type: 'clawdbot')
end
```

---

## 🎉 恭喜！

你已经成功配置了 Clawdbot 集成！

现在你的 Host 可以使用自定义训练的 AI 进行更个性化的对话了。

如果遇到任何问题，请查看：
- [故障排查](#-遇到问题)
- [测试指南](./TESTING_GUIDE.md)
- [完整文档](./COMPLETION_SUMMARY.md)

**祝使用愉快！** 🚀

---

**文档版本**: 1.0.0  
**最后更新**: 2026-02-04
