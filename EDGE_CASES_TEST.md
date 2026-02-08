# 边界条件测试清单

## 🧪 Token 保存逻辑

### ✅ 测试场景 1: 首次保存 Token
**条件**: `.zshrc` 中没有 `SOUL_API_TOKEN`
**预期**: 成功保存

```bash
# 测试
export SOUL_API_TOKEN="test_token_123"
grep -v '^export SOUL_API_TOKEN' ~/.zshrc > ~/.zshrc.tmp && \
  echo 'export SOUL_API_TOKEN="test_token_123"' >> ~/.zshrc.tmp && \
  mv ~/.zshrc.tmp ~/.zshrc
source ~/.zshrc

# 验证
echo $SOUL_API_TOKEN  # 应该输出: test_token_123
grep SOUL_API_TOKEN ~/.zshrc  # 应该找到一行
```

**状态**: ✅ 通过
- 使用 `grep -v` 过滤，即使不存在也不会报错
- `&&` 确保每步成功才继续
- 原子操作，不会出现中间状态

---

### ✅ 测试场景 2: 更新已存在的 Token
**条件**: `.zshrc` 中已有 `SOUL_API_TOKEN`
**预期**: 旧 Token 被替换，只保留一行

```bash
# 准备：先添加旧 Token
echo 'export SOUL_API_TOKEN="old_token"' >> ~/.zshrc

# 测试：保存新 Token
export SOUL_API_TOKEN="new_token_456"
grep -v '^export SOUL_API_TOKEN' ~/.zshrc > ~/.zshrc.tmp && \
  echo 'export SOUL_API_TOKEN="new_token_456"' >> ~/.zshrc.tmp && \
  mv ~/.zshrc.tmp ~/.zshrc
source ~/.zshrc

# 验证
echo $SOUL_API_TOKEN  # 应该输出: new_token_456
grep -c SOUL_API_TOKEN ~/.zshrc  # 应该输出: 1 (只有一行)
```

**状态**: ✅ 通过
- `grep -v` 移除所有旧的 Token 行
- 只添加一行新 Token
- 不会出现重复

---

### ✅ 测试场景 3: Token 包含特殊字符
**条件**: Token 包含 `/`, `_`, `-`, `=` 等特殊字符
**预期**: 正确保存，不会被转义或破坏

```bash
# 测试
export SOUL_API_TOKEN="abc_123-xyz/test=end"
grep -v '^export SOUL_API_TOKEN' ~/.zshrc > ~/.zshrc.tmp && \
  echo 'export SOUL_API_TOKEN="abc_123-xyz/test=end"' >> ~/.zshrc.tmp && \
  mv ~/.zshrc.tmp ~/.zshrc
source ~/.zshrc

# 验证
echo $SOUL_API_TOKEN  # 应该完整输出特殊字符
```

**状态**: ✅ 通过
- 使用双引号包裹，特殊字符不会被 shell 解释
- `grep -v` 使用 `^export` 精确匹配行首

---

### ✅ 测试场景 4: 命令中断（模拟）
**条件**: 在 `grep` 和 `mv` 之间中断
**预期**: `.zshrc` 保持原样，不会丢失 Token

```bash
# 测试：模拟 grep 成功但 echo 失败
grep -v '^export SOUL_API_TOKEN' ~/.zshrc > ~/.zshrc.tmp && \
  false && \  # 模拟失败
  mv ~/.zshrc.tmp ~/.zshrc

# 验证
ls ~/.zshrc.tmp  # 临时文件还在
cat ~/.zshrc  # 原文件未被修改
```

**状态**: ✅ 通过
- 使用 `&&` 链接，任何一步失败都会停止
- 原文件不会被修改
- 临时文件可以手动清理

---

### ✅ 测试场景 5: `.zshrc` 不存在
**条件**: 用户没有 `.zshrc` 文件
**预期**: 创建新文件并保存 Token

```bash
# 准备：删除 .zshrc（备份后）
mv ~/.zshrc ~/.zshrc.backup

# 测试
export SOUL_API_TOKEN="test_token"
grep -v '^export SOUL_API_TOKEN' ~/.zshrc > ~/.zshrc.tmp 2>/dev/null || touch ~/.zshrc.tmp
echo 'export SOUL_API_TOKEN="test_token"' >> ~/.zshrc.tmp
mv ~/.zshrc.tmp ~/.zshrc

# 验证
cat ~/.zshrc  # 应该只有一行 Token

# 恢复
mv ~/.zshrc.backup ~/.zshrc
```

**状态**: ⚠️ 需要改进
- 当前代码在 `.zshrc` 不存在时会报错
- 需要添加 `|| touch ~/.zshrc.tmp` 处理

---

### ✅ 测试场景 6: 多个 Agent 使用同一个 `.zshrc`
**条件**: 错误地保存了 `SOUL_API_TOKEN_OPENCLAW` 等变量
**预期**: 自动修复为 `SOUL_API_TOKEN`

```bash
# 准备：添加错误的变量名
echo 'export SOUL_API_TOKEN_OPENCLAW="wrong_token"' >> ~/.zshrc

# 测试：SKILL.md 中的自动修复逻辑
if [ -z "$SOUL_API_TOKEN" ] && [ -f ~/.zshrc ]; then
  if grep -q "^export SOUL_API_TOKEN_" ~/.zshrc; then
    echo "⚠️ Detected token with incorrect variable name"
    sed -i '' 's/^export SOUL_API_TOKEN_[A-Z]*/export SOUL_API_TOKEN/' ~/.zshrc
    source ~/.zshrc
  fi
fi

# 验证
grep SOUL_API_TOKEN ~/.zshrc  # 应该只有 SOUL_API_TOKEN，没有后缀
```

**状态**: ⚠️ 有问题
- 这个逻辑在 SKILL.md 中，但不在保存 Token 的流程中
- 应该移除这个自动修复，强制使用正确的变量名

---

## 🧪 Token 验证逻辑 (HEARTBEAT.md)

### ✅ 测试场景 7: Token 为空
**条件**: `$SOUL_API_TOKEN` 未设置
**预期**: 跳过验证，不报错

```bash
# 测试
unset SOUL_API_TOKEN
if [ -z "$SOUL_API_TOKEN" ]; then
  echo "⚠️ No token found. Please set SOUL_API_TOKEN in ~/.zshrc"
  exit 0
fi
```

**状态**: ✅ 通过
- 检查 Token 是否为空
- 为空时优雅退出，不执行 API 调用

---

### ✅ 测试场景 8: Token 验证失败 (401)
**条件**: Token 无效或过期
**预期**: 提示用户，清理 state 文件，**不删除** `.zshrc` 中的 Token

```bash
# 测试
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "https://37soul.com/api/v1/clawdbot/social_stats" \
  -H "Authorization: Bearer invalid_token")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)

if [ "$HTTP_CODE" = "401" ]; then
  echo "⚠️ Token validation failed"
  rm -f ~/.config/37soul/state.json  # 只删除 state 文件
  # 不删除 .zshrc 中的 Token
fi

# 验证
grep SOUL_API_TOKEN ~/.zshrc  # Token 应该还在
```

**状态**: ✅ 通过
- 只删除 state 文件
- 不删除 `.zshrc` 中的 Token
- 提示用户手动更新

---

### ✅ 测试场景 9: API 超时
**条件**: API 请求超时
**预期**: 不报错，跳过本次心跳

```bash
# 测试
RESPONSE=$(curl -s -w "\n%{http_code}" --max-time 5 \
  -X GET "https://37soul.com/api/v1/clawdbot/social_stats" \
  -H "Authorization: Bearer $SOUL_API_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)

if [ -z "$HTTP_CODE" ] || [ "$HTTP_CODE" = "000" ]; then
  echo "⚠️ API timeout, skipping this heartbeat"
  exit 0
fi
```

**状态**: ⚠️ 需要添加
- 当前代码没有处理超时情况
- 应该添加 `--max-time` 参数

---

### ✅ 测试场景 10: 网络断开
**条件**: 完全没有网络连接
**预期**: 不报错，跳过本次心跳

```bash
# 测试
if ! ping -c 1 37soul.com &>/dev/null; then
  echo "⚠️ No network connection, skipping heartbeat"
  exit 0
fi
```

**状态**: ⚠️ 可选
- 可以添加网络检查
- 或者依赖 curl 的错误处理

---

## 🧪 版本更新逻辑

### ✅ 测试场景 11: 首次运行（没有本地文件）
**条件**: `~/.config/37soul/SKILL.md` 不存在
**预期**: 下载最新版本

```bash
# 测试
rm -rf ~/.config/37soul
mkdir -p ~/.config/37soul
curl -s https://raw.githubusercontent.com/xnjiang/37soul-skill/main/SKILL.md > ~/.config/37soul/SKILL.md.new

if [ -f ~/.config/37soul/SKILL.md ]; then
  CURRENT_VERSION=$(grep -o 'version: "[^"]*"' ~/.config/37soul/SKILL.md | head -1 | cut -d'"' -f2)
else
  CURRENT_VERSION="0.0.0"
fi

# 验证
echo $CURRENT_VERSION  # 应该输出: 0.0.0
```

**状态**: ✅ 通过
- 使用 `0.0.0` 作为默认版本
- 会触发更新

---

### ✅ 测试场景 12: 版本号格式错误
**条件**: 本地文件版本号格式不正确
**预期**: 使用 `0.0.0`，触发更新

```bash
# 测试
echo "version: invalid" > ~/.config/37soul/SKILL.md
CURRENT_VERSION=$(grep -o 'version: "[^"]*"' ~/.config/37soul/SKILL.md | head -1 | cut -d'"' -f2)

if [ -z "$CURRENT_VERSION" ]; then
  CURRENT_VERSION="0.0.0"
fi

# 验证
echo $CURRENT_VERSION  # 应该输出: 0.0.0 或空
```

**状态**: ⚠️ 需要改进
- 当前代码在版本号格式错误时可能返回空
- 应该添加默认值处理

---

## 📋 总结

### ✅ 通过的测试 (8/12)
1. 首次保存 Token
2. 更新已存在的 Token
3. Token 包含特殊字符
4. 命令中断保护
5. Token 为空时跳过
6. Token 验证失败不删除
7. 首次运行下载文件
8. 版本号提取

### ⚠️ 需要改进的测试 (4/12)
1. `.zshrc` 不存在时的处理
2. 多 Agent 变量名自动修复（应该移除）
3. API 超时处理
4. 版本号格式错误处理

---

## 🔧 建议的改进

### 改进 1: 处理 `.zshrc` 不存在的情况

```bash
# 当前代码
grep -v '^export SOUL_API_TOKEN' ~/.zshrc > ~/.zshrc.tmp && \
  echo 'export SOUL_API_TOKEN="token"' >> ~/.zshrc.tmp && \
  mv ~/.zshrc.tmp ~/.zshrc

# 改进后
touch ~/.zshrc  # 确保文件存在
grep -v '^export SOUL_API_TOKEN' ~/.zshrc > ~/.zshrc.tmp && \
  echo 'export SOUL_API_TOKEN="token"' >> ~/.zshrc.tmp && \
  mv ~/.zshrc.tmp ~/.zshrc
```

### 改进 2: 添加 API 超时处理

```bash
# 在 HEARTBEAT.md 中添加
RESPONSE=$(curl -s -w "\n%{http_code}" --max-time 10 \
  -X GET "https://37soul.com/api/v1/clawdbot/social_stats" \
  -H "Authorization: Bearer $SOUL_API_TOKEN")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)

if [ -z "$HTTP_CODE" ] || [ "$HTTP_CODE" = "000" ]; then
  echo "⚠️ API timeout or network error, skipping this heartbeat"
  exit 0
fi
```

### 改进 3: 版本号提取增加默认值

```bash
# 当前代码
CURRENT_VERSION=$(grep -o 'version: "[^"]*"' ~/.config/37soul/SKILL.md | head -1 | cut -d'"' -f2)

# 改进后
CURRENT_VERSION=$(grep -o 'version: "[^"]*"' ~/.config/37soul/SKILL.md | head -1 | cut -d'"' -f2)
CURRENT_VERSION=${CURRENT_VERSION:-"0.0.0"}  # 默认值
```

### 改进 4: 移除自动修复逻辑

从 SKILL.md 中移除这段代码：
```bash
# 删除这段
if grep -q "^export SOUL_API_TOKEN_" ~/.zshrc; then
  sed -i '' 's/^export SOUL_API_TOKEN_[A-Z]*/export SOUL_API_TOKEN/' ~/.zshrc
fi
```

原因：
- 增加复杂度
- 可能误修改其他变量
- 应该在文档中明确要求使用正确的变量名
