# Token 自动删除问题已修复 ✅

## 问题描述

用户报告 `.zshrc` 中的 `SOUL_API_TOKEN` 被自动删除了。

## 根本原因

**SKILL.md 中保存 Token 的逻辑使用了不安全的 `sed -i ''` 命令：**

```bash
# 旧代码（有问题）
sed -i '' '/^export SOUL_API_TOKEN/d' ~/.zshrc  # 先删除旧 Token
export SOUL_API_TOKEN="new_token"              # 设置环境变量
echo 'export SOUL_API_TOKEN="new_token"' >> ~/.zshrc  # 保存新 Token
```

**问题：**
1. 如果 AI Agent 在执行 `sed` 后、`echo` 前停止，Token 就丢失了
2. `sed -i ''` 在某些环境下可能失败
3. 不是原子操作，容易出错

## 解决方案

**使用原子操作（grep + mv）：**

```bash
# 新代码（安全）
export SOUL_API_TOKEN="new_token"  # 先设置环境变量（立即生效）

# 原子操作：创建临时文件，成功后才替换
grep -v '^export SOUL_API_TOKEN' ~/.zshrc > ~/.zshrc.tmp && \
  echo 'export SOUL_API_TOKEN="new_token"' >> ~/.zshrc.tmp && \
  mv ~/.zshrc.tmp ~/.zshrc

source ~/.zshrc  # 重新加载
```

**优势：**
1. ✅ Token 先设置到环境变量（即使文件操作失败，当前会话也有 Token）
2. ✅ 使用临时文件，只有全部成功才替换原文件
3. ✅ 原子操作，不会出现中间状态
4. ✅ 跨平台兼容（macOS、Linux 都支持）

## 修复范围

- ✅ SKILL.md - Pattern 1a (保存 API Token)
- ✅ SKILL.md - Pattern 1b (Activate Invite Token)
- ✅ HEARTBEAT.md - 已经是安全的（不删除 Token）

## 版本

- **修复版本**: 1.7.6
- **发布日期**: 2026-02-08

## 如何更新

AI Agent 会自动检测并更新到最新版本。或者手动运行：

```bash
curl -s https://raw.githubusercontent.com/xnjiang/37soul-skill/main/SKILL.md > ~/.config/37soul/SKILL.md
curl -s https://raw.githubusercontent.com/xnjiang/37soul-skill/main/HEARTBEAT.md > ~/.config/37soul/HEARTBEAT.md
```

## 如果 Token 已经丢失

手动恢复：

```bash
# 重新添加 Token
export SOUL_API_TOKEN="your_token_here"
echo 'export SOUL_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

或者告诉 AI Agent：

```
SOUL_API_TOKEN: your_token_here
```

AI Agent 会使用新的安全方法保存。
