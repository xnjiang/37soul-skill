# Token Generation Bug Fix

## 问题描述

用户点击"一键连接"按钮后，收到集成 URL，但访问该 URL 时返回错误：
```json
{"error":"Invalid or expired integration token"}
```

## 根本原因

在 `API::V1::ClawdbotIntegrationsController#generate_token` 方法中，代码手动生成 token 并设置 expires_at：

```ruby
# 错误的实现
def generate_token
  token = SecureRandom.urlsafe_base64(32)
  
  integration_request = IntegrationRequest.create!(
    host: @host,
    token: token,
    expires_at: 15.minutes.from_now
  )
  
  integration_url = integrate_clawdbot_url(token: token)
  # ...
end
```

但是 `IntegrationRequest` 模型有 `before_validation` 回调：

```ruby
class IntegrationRequest < ActiveRecord::Base
  before_validation :generate_token, on: :create
  before_validation :set_expiration, on: :create
  
  private
  
  def generate_token
    self.token = SecureRandom.urlsafe_base64(32)
  end
  
  def set_expiration
    self.expires_at = 15.minutes.from_now
  end
end
```

这导致：
1. Controller 手动设置 `token = "ABC123"`
2. Model 的 `before_validation` 回调将其覆盖为 `token = "XYZ789"`
3. Controller 返回给前端的 URL 包含 `"ABC123"`
4. 但数据库中保存的是 `"XYZ789"`
5. 用户访问 URL 时，token 不匹配，返回错误

## 解决方案

让模型自动生成 token，不要手动设置：

```ruby
# 正确的实现
def generate_token
  # 创建 IntegrationRequest (token 和 expires_at 会自动生成)
  integration_request = IntegrationRequest.create!(host: @host)
  
  # 返回集成 URL
  integration_url = integrate_clawdbot_url(token: integration_request.token)
  
  render json: {
    success: true,
    integration_url: integration_url,
    token: integration_request.token,
    expires_at: integration_request.expires_at
  }
end
```

## 修改的文件

- `app/controllers/api/v1/clawdbot_integrations_controller.rb`

## 测试验证

```bash
# 创建 IntegrationRequest
rails runner "
host = Host.find(84)
ir = IntegrationRequest.create!(host: host)
puts 'Token: ' + ir.token
puts 'Valid?: ' + ir.valid_token?.to_s
"

# 验证 token 可以被找到
rails runner "
token = 'YOUR_TOKEN_HERE'
ir = IntegrationRequest.find_by(token: token)
puts ir.present? ? '✅ Found' : '❌ Not found'
"
```

## 状态

✅ 已修复 - 2026-02-04
