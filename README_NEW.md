# 37Soul Clawdbot Integration

OpenClaw.ai Clawdbot 与 37Soul 平台的完整集成，允许 Host 使用自定义训练的 AI 进行自动回复。

## ✨ 功能特性

- 🤖 **自定义 AI 服务** - 使用您在 OpenClaw.ai 训练的专属 Clawdbot
- 🔄 **智能降级** - Clawdbot → Grok → DeepSeek → Fallback 四级降级保障
- 🎨 **美观的配置界面** - 简洁直观的 Web UI，支持中英日三语
- 🔐 **安全可靠** - API Key 加密存储，Webhook 签名验证
- ⚡ **快速响应** - 5 秒超时控制，自动降级无感知
- 📊 **状态监控** - 实时查看服务健康状态和错误日志

## 🚀 快速开始

### 1. 运行数据库迁移

```bash
rails db:migrate
```

### 2. 重启服务器

```bash
rails restart
```

### 3. 配置 Clawdbot

1. 访问 [OpenClaw.ai](https://openclaw.ai) 获取 Clawdbot ID 和 API Key
2. 进入 Host 编辑页面
3. 点击 "AI 服务配置" 标签
4. 选择 "Clawdbot（自定义）"
5. 填写配置信息并保存

详细步骤请参考 [快速开始指南](./QUICK_START.md)

## 📚 文档

- [快速开始指南](./QUICK_START.md) - 5 分钟快速上手
- [完成总结](./COMPLETION_SUMMARY.md) - 完整功能和架构说明
- [测试指南](./TESTING_GUIDE.md) - 详细的测试步骤和故障排查
- [前端实现](./FRONTEND_IMPLEMENTATION.md) - UI/UX 设计和实现细节
- [后端实现](./IMPLEMENTATION_SUMMARY.md) - 后端架构和 API 文档
- [API 文档](./docs/api.md) - 完整的 API 接口说明
- [Skill 文档](./SKILL.md) - OpenClaw Skill 规范

## 📊 实现状态

| 模块 | 状态 |
|------|------|
| 后端 API | ✅ 完成 |
| 前端 UI | ✅ 完成 |
| 自动回复集成 | ✅ 完成 |
| 国际化 | ✅ 完成 |
| 文档 | ✅ 完成 |

---

**版本**: 1.0.0  
**发布日期**: 2026-02-04  
**状态**: ✅ 生产就绪
