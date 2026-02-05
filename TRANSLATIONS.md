# Clawdbot 集成翻译

## 已添加的翻译键

### 选项卡标题
| 键 | 中文 | 英文 | 日文 |
|----|------|------|------|
| `integration_tab_clawdbot` | Clawdbot | Clawdbot | Clawdbot |
| `integration_tab_cli` | 命令行 | CLI | コマンドライン |
| `integration_tab_manual` | 手动配置 | Manual | 手動設定 |

### Clawdbot 一键集成
| 键 | 中文 | 英文 | 日文 |
|----|------|------|------|
| `clawdbot_instruction_title` | 复制下面的消息，发送给您的 Clawdbot | Copy the message below and send it to your Clawdbot | 以下のメッセージをコピーしてClawdbotに送信してください |
| `clawdbot_copy_button` | 复制指令 | Copy Instruction | 指示をコピー |
| `clawdbot_copied` | 已复制！ | Copied! | コピーしました！ |
| `clawdbot_next_steps` | 接下来会发生什么？ | What happens next? | 次に何が起こりますか？ |
| `clawdbot_step1` | 发送后，您的 Clawdbot 会自动完成配置 | Your Clawdbot will automatically complete the configuration | 送信後、Clawdbotが自動的に設定を完了します |
| `clawdbot_step2` | Clawdbot 会发送验证链接给您 | Clawdbot will send you a verification link | Clawdbotが確認リンクを送信します |
| `clawdbot_step3` | 点击链接确认授权 | Click the link to confirm authorization | リンクをクリックして承認を確認 |
| `clawdbot_step4` | 完成！您的 Host 现在使用 Clawdbot | Done! Your Host now uses Clawdbot | 完了！HostがClawdbotを使用するようになりました |
| `clawdbot_no_bot` | 还没有 Clawdbot？ | Don't have a Clawdbot? | Clawdbotをお持ちでないですか？ |
| `clawdbot_learn_more` | 了解如何创建 | Learn how to create | 作成方法を学ぶ |

### 命令行安装
| 键 | 中文 | 英文 | 日文 |
|----|------|------|------|
| `cli_instruction_title` | 在终端中运行以下命令 | Run the following command in your terminal | ターミナルで以下のコマンドを実行してください |
| `cli_copy_button` | 复制命令 | Copy Command | コマンドをコピー |
| `cli_copied` | 已复制！ | Copied! | コピーしました！ |
| `cli_next_steps` | 接下来会发生什么？ | What happens next? | 次に何が起こりますか？ |
| `cli_step1` | CLI 工具会自动下载并启动安装向导 | CLI tool will download and start the installation wizard | CLIツールがダウンロードされ、インストールウィザードが起動します |
| `cli_step2` | 按照提示输入您的 AI Agent 信息 | Follow prompts to enter your AI Agent information | プロンプトに従ってAI Agent情報を入力 |
| `cli_step3` | 点击验证链接确认授权 | Click verification link to confirm authorization | 確認リンクをクリックして承認 |
| `cli_step4` | 完成！集成已配置完成 | Done! Integration configured | 完了！統合が設定されました |
| `cli_need_nodejs` | 需要安装 Node.js | Node.js required | Node.jsが必要です |
| `cli_download_nodejs` | 下载 Node.js | Download Node.js | Node.jsをダウンロード |

### 手动配置
| 键 | 中文 | 英文 | 日文 |
|----|------|------|------|
| `manual_two_steps` | 手动配置需要两步 | Manual configuration requires two steps | 手動設定には2つのステップが必要です |
| `manual_step1_title` | 阅读技术文档 | Read technical documentation | 技術ドキュメントを読む |
| `manual_step1_button` | 打开文档 | Open Documentation | ドキュメントを開く |
| `manual_step2_title` | 获取此 Host 的集成链接 | Get integration link for this Host | このHostの統合リンクを取得 |
| `manual_step2_desc` | 生成一个包含此 Host 信息的集成链接，发送给您的 AI Agent | Generate a link containing this Host's information to send to your AI Agent | このHostの情報を含むリンクを生成し、AI Agentに送信します |
| `manual_generate_link` | 生成集成链接 | Generate Integration Link | 統合リンクを生成 |
| `manual_generating` | 生成中... | Generating... | 生成中... |
| `manual_generated` | 已生成 | Generated | 生成完了 |
| `manual_regenerate` | 重新生成链接 | Regenerate Link | リンクを再生成 |
| `manual_link_expires` | 15分钟有效 | Valid for 15 minutes | 15分間有効 |
| `manual_copy_link` | 复制链接 | Copy Link | リンクをコピー |
| `manual_link_copied` | 已复制！ | Copied! | コピーしました！ |
| `manual_next_steps` | 接下来会发生什么？ | What happens next? | 次に何が起こりますか？ |
| `manual_step1` | 您的 AI Agent 访问集成链接 | Your AI Agent accesses the integration link | AI Agentが統合リンクにアクセス |
| `manual_step2` | Agent 调用注册 API 并获取验证链接 | Agent calls registration API and gets verification link | Agentが登録APIを呼び出し、確認リンクを取得 |
| `manual_step3` | 您点击验证链接确认授权 | You click verification link to confirm authorization | 確認リンクをクリックして承認 |
| `manual_step4` | 完成！您的 Host 现在使用 AI Agent | Done! Your Host now uses AI Agent | 完了！HostがAI Agentを使用するようになりました |
| `manual_need_help` | 需要帮助？ | Need help? | ヘルプが必要ですか？ |
| `manual_view_docs` | 查看完整文档 | View full documentation | 完全なドキュメントを表示 |

## 使用方法

在视图中使用翻译：

```erb
<%= t('.integration_tab_clawdbot') %>
<%= t('.clawdbot_instruction_title') %>
<%= t('.cli_copy_button') %>
<%= t('.manual_generate_link') %>
```

## 文件位置

- 中文：`config/locales/views/hosts/zh-CN.yml`
- 英文：`config/locales/views/hosts/en.yml`
- 日文：`config/locales/views/hosts/ja.yml`

## 注意事项

1. 所有翻译键都在 `hosts.edit` 命名空间下
2. 使用 `.` 前缀表示相对路径（在 hosts/edit 视图中）
3. 保持三种语言的翻译同步更新
4. 翻译应该简洁明了，符合各语言习惯

## 待办事项

- [ ] 添加更多语言支持（如韩语、法语等）
- [ ] 添加错误消息的翻译
- [ ] 添加成功消息的翻译
- [ ] 添加工具提示的翻译
