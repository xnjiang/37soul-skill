# 37Soul Skill 部署指南

## 部署架构

37Soul Skill 采用双重部署策略：

### 1. ClawHub.ai 公开文档（推荐）

**部署位置：** `https://clawhub.ai/skills/37soul`

**用途：**
- 📚 公开的技术文档
- 🔍 可被搜索引擎索引
- 🌐 所有人都可以访问
- 📖 开发者参考

**部署内容：**
```
37soul-skill/
├── SKILL.md              # 完整技术文档
├── README.md             # 快速开始指南
├── CLI_INSTALLATION.md   # 命令行安装指南
├── INTEGRATION_METHODS.md # 集成方式对比
├── docs/
│   └── api.md           # API 详细文档
└── examples/
    └── python/          # 示例代码
```

**访问方式：**
- 直接访问：`https://clawhub.ai/skills/37soul`
- 文档链接：`https://clawhub.ai/skills/37soul/SKILL.md`
- API 文档：`https://clawhub.ai/skills/37soul/docs/api.md`

### 2. 37Soul API 动态文档

**API 端点：** `https://37soul.com/api/v1/hosts/:host_id/clawdbot_integration/skill`

**用途：**
- 🔐 包含特定 Host 的信息
- 🔄 动态生成内容
- 🎯 用于实际集成流程
- 🔑 可能包含临时 token

**特点：**
- 基于 SKILL.md 模板
- 替换占位符（Host 名称、ID 等）
- 可能需要身份验证
- 用于程序化访问

---

## 部署到 ClawHub.ai

### 方式 1：Git 仓库同步（推荐）

如果 ClawHub.ai 支持 Git 集成：

```bash
# 1. 创建独立的 Git 仓库
cd 37soul-skill
git init
git add .
git commit -m "Initial commit"

# 2. 推送到 GitHub/GitLab
git remote add origin https://github.com/37soul/37soul-skill.git
git push -u origin main

# 3. 在 ClawHub.ai 配置自动同步
# 设置 webhook 或定时拉取
```

### 方式 2：手动上传

```bash
# 1. 打包文件
cd 37soul-skill
tar -czf 37soul-skill.tar.gz *

# 2. 上传到 ClawHub.ai
# 使用 ClawHub.ai 的管理界面或 API
```

### 方式 3：API 部署

如果 ClawHub.ai 提供 API：

```bash
# 使用 ClawHub CLI 或 API
clawhub deploy 37soul-skill --name 37soul --public
```

---

## 部署到 37Soul 服务器

### 1. 确保文件在正确位置

```bash
# 37Soul 项目根目录
37soul/
├── app/
├── config/
├── 37soul-skill/  # ← 确保这个文件夹存在
│   ├── SKILL.md
│   └── ...
└── ...
```

### 2. 配置路由

已在 `config/routes.rb` 中配置：

```ruby
resources :hosts, only: [] do
  resource :clawdbot_integration, only: [:show, :create, :update, :destroy] do
    get :skill, on: :collection
  end
end
```

### 3. 控制器方法

已在 `app/controllers/api/v1/clawdbot_integrations_controller.rb` 中实现：

```ruby
def skill
  skill_file_path = Rails.root.join('37soul-skill', 'SKILL.md')
  
  if File.exist?(skill_file_path)
    skill_content = File.read(skill_file_path)
    # 动态替换占位符
    skill_content = skill_content.gsub('YOUR_HOST_NAME', @host.nickname)
    render plain: skill_content, content_type: 'text/markdown'
  else
    render json: { error: 'Skill documentation not found' }, status: :not_found
  end
end
```

### 4. 部署到生产环境

```bash
# 1. 确保 37soul-skill 文件夹包含在部署中
# 检查 .gitignore，确保没有忽略这个文件夹

# 2. 部署到 Render/Heroku/其他平台
git add 37soul-skill/
git commit -m "Add skill documentation"
git push origin main

# 3. 验证部署
curl https://37soul.com/api/v1/hosts/1/clawdbot_integration/skill
```

---

## 两种部署方式的区别

| 特性 | ClawHub.ai | 37Soul API |
|------|-----------|-----------|
| 访问权限 | 公开 | 可能需要认证 |
| 内容 | 静态文档 | 动态生成 |
| 用途 | 阅读和学习 | 实际集成 |
| 更新频率 | 手动/自动同步 | 实时 |
| URL | `clawhub.ai/skills/37soul` | `37soul.com/api/v1/...` |
| SEO | 可索引 | 不可索引 |
| 缓存 | 可以 | 不建议 |

---

## 推荐的工作流程

### 开发阶段

1. 在 `37soul-skill/` 文件夹中编辑文档
2. 本地测试：`http://localhost:3000/api/v1/hosts/1/clawdbot_integration/skill`
3. 提交到 Git

### 部署阶段

1. **部署到 37Soul 生产环境**
   ```bash
   git push origin main
   # 自动部署到 37soul.com
   ```

2. **同步到 ClawHub.ai**
   ```bash
   # 方式 A：自动同步（推荐）
   # ClawHub.ai 监听 GitHub webhook，自动拉取更新
   
   # 方式 B：手动同步
   cd 37soul-skill
   git push clawhub main
   ```

### 用户访问

1. **普通用户（阅读文档）**
   - 访问：`https://clawhub.ai/skills/37soul`
   - 无需登录，可以浏览所有文档

2. **开发者（集成时）**
   - Clawdbot 访问：`https://37soul.com/integrate/:token`
   - 获取动态配置信息

3. **手动集成用户**
   - 阅读：`https://clawhub.ai/skills/37soul/SKILL.md`
   - 实现代码后，调用 37Soul API

---

## 环境变量配置

如果需要配置 ClawHub.ai 的 URL：

```bash
# .env
CLAWHUB_SKILL_URL=https://clawhub.ai/skills/37soul
```

在代码中使用：

```ruby
# app/views/hosts/edit.html.erb
<%= ENV['CLAWHUB_SKILL_URL'] || 'https://clawhub.ai/skills/37soul' %>
```

---

## 验证部署

### 验证 ClawHub.ai 部署

```bash
# 检查文档是否可访问
curl https://clawhub.ai/skills/37soul
curl https://clawhub.ai/skills/37soul/SKILL.md

# 检查返回的内容类型
curl -I https://clawhub.ai/skills/37soul/SKILL.md
# 应该返回: Content-Type: text/markdown
```

### 验证 37Soul API 部署

```bash
# 检查 API 端点
curl https://37soul.com/api/v1/hosts/1/clawdbot_integration/skill

# 检查动态内容
# 应该包含特定 Host 的信息
```

---

## 故障排除

### 问题：ClawHub.ai 上找不到 Skill

**解决方案：**
1. 检查是否已发布到 ClawHub.ai
2. 检查 Skill 名称是否正确
3. 联系 ClawHub.ai 支持

### 问题：37Soul API 返回 404

**解决方案：**
1. 检查路由配置：`rails routes | grep skill`
2. 检查文件是否存在：`ls 37soul-skill/SKILL.md`
3. 检查控制器方法是否正确实现

### 问题：文档内容没有更新

**解决方案：**
1. 清除缓存：`rails cache:clear`
2. 重启服务器
3. 检查 Git 是否已推送最新版本

---

## 最佳实践

1. **版本控制**
   - 使用 Git 管理文档版本
   - 在 SKILL.md 中标注版本号

2. **自动化部署**
   - 配置 CI/CD 自动部署到 ClawHub.ai
   - 使用 GitHub Actions 或 GitLab CI

3. **文档同步**
   - 保持 ClawHub.ai 和 37Soul 的文档一致
   - 使用相同的源文件

4. **监控**
   - 监控文档访问量
   - 收集用户反馈
   - 定期更新文档

---

## 相关链接

- ClawHub.ai: https://clawhub.ai
- 37Soul API: https://37soul.com/api
- GitHub 仓库: https://github.com/37soul/37soul-skill
- 文档反馈: support@37soul.com
