# ComicsPuncher 青龙集成指南

本文档说明如何在 [青龙面板](https://github.com/whyour/qinglong) 上部署和运行 ComicsPuncher 脚本。

## 📋 前提条件

- 已部署青龙面板（版本 2.10+）
- Python 3.8+
- 网络访问正常（需要访问漫画平台和推送服务）

## 🚀 快速开始

### 1. 添加脚本订阅

在青龙面板的 **订阅管理** 页面添加以下订阅：

```
https://github.com/你的账号/ComicsPuncher.git
```

或者直接将脚本文件放到青龙容器的 `/ql/scripts/` 目录下。

### 2. 配置环境变量

在青龙面板的 **环境变量** 页面添加以下环境变量：

#### 哔咔漫画配置

**单账号模式：**
```
PICA_USER=你的哔咔账号
PICA_PW=你的哔咔密码
```

**多账号模式（推荐）：**
```
PICA_ACCOUNT=user1:pass1&user2:pass2
# 或使用换行分隔：
PICA_ACCOUNT=user1:pass1
user2:pass2
```

#### 禁漫天堂配置

**单账号模式：**
```
JM_USER=你的禁漫账号
JM_PW=你的禁漫密码
```

**多账号模式（推荐）：**
```
JM_ACCOUNT=user1:pass1&user2:pass2
# 或使用换行分隔：
JM_ACCOUNT=user1:pass1
user2:pass2
```

#### 代理配置（可选）

如果在国内运行，需要配置代理：

```
MY_PROXY=http://127.0.0.1:7890
# 或
MY_PROXY=socks5://127.0.0.1:1080
```

#### 推送通知配置（可选）

支持多种推送渠道：

**Server酱（微信推送）：**
```
PUSH_KEY=SCT开头的key
```

**PushPlus（企业微信/钉钉）：**
```
PUSH_PLUS_TOKEN=你的token
```

**Telegram机器人：**
```
TG_BOT_TOKEN=你的bot_token
TG_USER_ID=你的user_id
```

**钉钉机器人：**
```
DD_BOT_TOKEN=钉钉机器人token
DD_BOT_SECRET=钉钉机器人密钥
```

### 3. 添加定时任务

在青龙面板的 **定时任务** 页面，创建新任务：

| 字段 | 值 |
|-----|-----|
| 任务名称 | 漫画签到 |
| 脚本路径 | `/ql/scripts/ComicsPuncher/main.py` |
| 定时规则 | `30 8 * * *` （每天8:30执行） |
| 任务类型 | Python |

或者使用以下 Cron 表达式的其他时间：
```
# 每天上午8点30分
30 8 * * *

# 每天凌晨0点
0 0 * * *

# 工作日早上9点
0 9 * * 1-5
```

## 📝 环境变量详解

### 账号格式

所有账号配置都支持以下格式：

```
# 单账号
username:password

# 多账号（用 & 分隔）
user1:pass1&user2:pass2&user3:pass3

# 多账号（用换行分隔）
user1:pass1
user2:pass2
user3:pass3
```

> **⚠️ 重要提示**：账号密码中如果包含特殊字符（如 `&`、`@` 等），需要进行 URL 编码或使用换行分隔。

### 推送渠道优先级

脚本支持以下推送渠道（按优先级）：

1. **Server酱** - `PUSH_KEY` - 微信推送
2. **PushPlus** - `PUSH_PLUS_TOKEN` - 企业微信/钉钉/其他
3. **Telegram** - `TG_BOT_TOKEN` + `TG_USER_ID` - Telegram推送
4. **钉钉** - `DD_BOT_TOKEN` + `DD_BOT_SECRET` - 钉钉机器人

任何配置的推送渠道都会同时发送通知。

## 🔧 安装依赖

青龙面板通常会自动安装 `requirements.txt` 中的依赖包：

```
requests>=2.25.0
jmcomic>=4.0.0
```

如果自动安装失败，可以在青龙容器中手动安装：

```bash
docker exec -it qinglong pip install -r /ql/scripts/ComicsPuncher/requirements.txt
```

## 📊 日志查看

任务执行后，可以在青龙面板的 **任务日志** 中查看执行结果：

```
✅ 哔咔签到成功！
✅ 禁漫登录成功！
📊 签到汇总:
✅ 哔咔账号 1 签到成功
✅ 禁漫账号 1 签到成功
```

## 🐛 常见问题

### Q: 脚本找不到通知模块

**A**: 确保 `notify.py` 和 `main.py` 在同一目录。如果青龙面板报错找不到模块，可能需要：

1. 检查脚本路径是否正确
2. 确保有执行权限：`chmod +x main.py`
3. 手动在青龙容器中安装依赖：`pip install requests jmcomic`

### Q: 账号登录失败

**A**: 常见原因：

1. **密码错误** - 确保账号密码正确
2. **账号被锁定** - 登录官方网站检查账号状态
3. **网络问题** - 检查代理配置，确保能访问服务器
4. **密码包含特殊字符** - 使用换行分隔或进行URL编码

### Q: 代理不生效

**A**: 代理格式检查：

```
# ✅ 正确格式
http://127.0.0.1:7890
socks5://127.0.0.1:1080

# ❌ 错误格式
127.0.0.1:7890      # 缺少协议
http://127.0.0.1    # 缺少端口
```

### Q: 无法推送通知

**A**: 检查步骤：

1. 确保已在环境变量中配置推送渠道
2. 检查推送 Token/Key 是否正确
3. 查看脚本日志是否有推送错误
4. 尝试使用其他推送渠道测试

### Q: 多账号只有一个生效

**A**: 检查账号分隔符：

```bash
# ✅ 使用 & 分隔多个账号
PICA_ACCOUNT=user1:pass1&user2:pass2

# ✅ 使用换行分隔
PICA_ACCOUNT=user1:pass1
user2:pass2

# ❌ 以下格式不支持
PICA_ACCOUNT=user1:pass1,user2:pass2   # 错误：不支持逗号
PICA_ACCOUNT=user1:pass1 user2:pass2   # 错误：不支持空格
```

## 📚 示例配置

### 完整配置示例

```
# 哔咔漫画 - 3个账号
PICA_ACCOUNT=pica_user1:pica_pass1&pica_user2:pica_pass2&pica_user3:pica_pass3

# 禁漫天堂 - 2个账号
JM_ACCOUNT=jm_user1:jm_pass1
jm_user2:jm_pass2

# 代理（国内需要）
MY_PROXY=http://127.0.0.1:7890

# 推送通知
PUSH_KEY=SCT1234567890abcdefghij
PUSH_PLUS_TOKEN=abcdefghijklmnop

# 定时任务 Cron 表达式
30 8 * * *
```

### Cron 表达式说明

```
# 格式：分 时 日 月 周
# ┌───────────── 分 (0-59)
# │ ┌───────────── 时 (0-23)
# │ │ ┌───────────── 日 (1-31)
# │ │ │ ┌───────────── 月 (1-12)
# │ │ │ │ ┌───────────── 周 (0-7, 0和7都代表周日)
# │ │ │ │ │
# * * * * *

# 示例
30 8 * * *     # 每天8点30分
0 */4 * * *    # 每4小时执行一次
0 9 * * 1-5    # 工作日上午9点
30 8 * * 0     # 每周日上午8点30分
```

## 🔄 与其他脚本对接

脚本遵循青龙面板标准，可以与其他脚本并行运行。建议：

1. 错开签到时间，避免同时执行过多任务
2. 使用不同的推送渠道以便区分
3. 定期检查日志，及时发现问题

## 📖 更多信息

- [青龙面板官方文档](https://qinglong.whyour.cn/)
- [哔咔漫画API参考](https://github.com/niuhuan/pica-go)
- [jmcomic库文档](https://github.com/hhairu/JMComic-Crawler)

## 📄 许可证

本项目遵循 MIT 许可证。

---

**最后更新**：2026-02-02
**支持版本**：Python 3.8+, 青龙 2.10+
