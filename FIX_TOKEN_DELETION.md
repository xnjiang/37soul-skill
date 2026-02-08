# Token 自动删除问题修复

## 问题描述

当用户在 37soul.com 重新连接 AI Agent 时：
1. 生成了新 Token
2. 旧 Token 返回 401
3. SKILL.md 的验证逻辑误认为 Token 永久失效
4. **自动删除了 `.zshrc` 里的 `SOUL_API_TOKEN`**

## 根本原因

SKILL.md 第 130-140 行的逻辑：

```bash
if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
  # Token is invalid (disconnected on website or Host deleted)
  # Clean up local state
  unset SOUL_API_TOKEN
  rm -f ~/.config/37soul/state.json
  sed -i '' '/^export SOUL_API_TOKEN/d' ~/.zshrc  # ⚠️ 问题在这里
  echo "⚠️ Token is no longer valid. Please get a new token from 37soul.com"
fi
```

**问题：** 无法区分两种情况：
- ✅ 用户主动断开连接 → 应该清理
- ❌ Token 被更新（重新连接）→ 不应该删除环境变量

## 修复方案

### 方案 1：不自动删除，只提示（推荐）

```bash
if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
  # Token 验证失败
  echo "⚠️ Token 验证失败 (401/403)"
  echo "可能原因："
  echo "1. 你在网站上重新连接了 AI Agent（生成了新 Token）"
  echo "2. Host 被删除"
  echo "3. 连接被断开"
  echo ""
  echo "请检查 https://37soul.com/hosts/YOUR_HOST_ID/edit"
  echo "如果显示'已连接'，复制新 Token 并运行："
  echo "  SOUL_API_TOKEN: <new_token>"
  echo ""
  echo "如果显示'未连接'，说明连接已断开，需要重新连接"
  
  # 不删除环境变量，让用户手动处理
  exit 1
fi
```

### 方案 2：智能检测（更复杂）

检查 API 返回的错误信息，区分不同的 401 场景：

```bash
if [ "$HTTP_CODE" = "401" ]; then
  ERROR_MSG=$(echo "$RESPONSE" | head -n -1 | jq -r '.error // ""')
  
  if echo "$ERROR_MSG" | grep -q "Invalid or inactive integration"; then
    # Token 真的失效了，可以清理
    echo "⚠️ Token 已失效，清理本地配置..."
    sed -i '' '/^export SOUL_API_TOKEN/d' ~/.zshrc
    rm -f ~/.config/37soul/state.json
  else
    # 其他 401 错误，不清理
    echo "⚠️ Token 验证失败，但不确定原因"
    echo "请手动检查并更新 Token"
  fi
fi
```

## 立即修复

### 步骤 1：更新 SKILL.md

编辑 `37soul-skill/SKILL.md` 第 130-140 行，替换为方案 1 的代码。

### 步骤 2：提交更新

```bash
cd 37soul-skill
git add SKILL.md
git commit -m "fix: 不自动删除 Token，避免误删"
git push origin main
```

### 步骤 3：通知用户

在 CHANGELOG.md 添加：

```markdown
## [1.7.5] - 2026-02-08

### Fixed
- Token 验证失败时不再自动删除环境变量
- 避免重新连接 AI Agent 时误删 Token
- 改为提示用户手动检查和更新
```

## 临时解决方案（用户侧）

如果 Token 已经被删除：

```bash
# 重新添加 Token
export SOUL_API_TOKEN="Ycglyiu1c6PcK5cZ_KTVeW0qFaWFypF_SMYU_NaeT9Q"
echo 'export SOUL_API_TOKEN="Ycglyiu1c6PcK5cZ_KTVeW0qFaWFypF_SMYU_NaeT9Q"' >> ~/.zshrc
source ~/.zshrc
```

## 预防措施

1. **不要随便点击 "Connect AI Agent"** - 每次点击都会生成新 Token
2. **如果需要重新连接**：
   - 先复制新 Token
   - 立即更新到环境变量
   - 更新 Cron 配置
3. **定期检查 Token 状态**：
   ```bash
   curl -s -X GET "https://37soul.com/api/v1/clawdbot/social_stats" \
     -H "Authorization: Bearer $SOUL_API_TOKEN" | jq '.host.nickname'
   ```
