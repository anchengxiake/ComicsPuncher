# ComicsPuncher 漫画平台自动签到助手

本项目是一个基于 Python 的自动化工具，旨在帮助用户实现 **哔咔漫画 (PicaComic)** 与 **禁漫天堂 (JMComic)** 的每日自动签到与打卡活跃。

## 🌟 功能特性

- **哔咔漫画**: 参考了[Golang版的哔咔漫画API](https://github.com/niuhuan/pica-go)，支持自动登录与每日打卡。
- **禁漫天堂**: 基于 `jmcomic` 库，模拟移动端 API 交互，登录即自动完成活跃。
- **多平台支持**: 适配 Windows/Linux 环境，支持配置 HTTP 代理。
- **🆕 青龙面板支持**: 完全兼容[青龙面板](https://github.com/whyour/qinglong)，支持通过环境变量配置，支持多推送渠道通知。
- **多账号支持**: 支持同时管理多个漫画平台账号。
- **推送通知**: 支持 Server酱、PushPlus、Telegram、钉钉等多种推送渠道。

## 📦 部署选项

### 选项 1: 本地直接运行

最简单的方式，适合个人电脑。

### 选项 2: Linux Crontab

适合部署在海外 VPS 或服务器上。

### 选项 3: 青龙面板 ⭐ 推荐

最推荐的方式！支持 Web 界面管理、日志查看、自动推送等功能。

> 📖 [点击查看完整的青龙部署指南](./QINGLONG_GUIDE.md)

## 🚀 快速开始

### 1. 环境准备

确保你的系统中已安装 Python 3.8+。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置账号

#### 方式一：直接修改代码（本地运行）
打开 `main.py`，在顶部修改以下信息：
```python
PICA_USER = "你的哔咔账号"
PICA_PW = "你的哔咔密码"
JM_USER = "你的禁漫账号"  
JM_PW = "你的禁漫密码"
MY_PROXY = ""  # 国内需要代理
```

#### 方式二：环境变量配置 ⭐ 推荐（支持多账号）

支持以下环境变量：

```bash
# 单账号模式
export PICA_USER="哔咔账号"
export PICA_PW="哔咔密码"
export JM_USER="禁漫账号"
export JM_PW="禁漫密码"

# 多账号模式（用 & 或换行分隔）
export PICA_ACCOUNT="user1:pass1&user2:pass2"
export JM_ACCOUNT="user1:pass1&user2:pass2"

# 可选：代理配置
export MY_PROXY="http://127.0.0.1:7890"
```

### 4. 运行脚本

```bash
# 直接运行
python main.py

# 或
python3 main.py
```

### 5. 定时运行

#### Windows - 任务计划程序

创建基本任务，设置：
- 程序：`python.exe` 的完整路径
- 参数：`main.py` 的完整路径
- 触发时间：每天 8:30

#### Linux - Crontab

```bash
crontab -e

# 添加以下行（每天8:30执行）
30 8 * * * /usr/bin/python3 /path/to/main.py >> /path/to/log.txt 2>&1
```

#### 青龙面板

详见 [QINGLONG_GUIDE.md](./QINGLONG_GUIDE.md)

---

## 📝 代理配置指南

### 为什么需要代理？

哔咔漫画和禁漫天堂的服务器可能在国外，国内用户需要代理才能访问。

### 代理格式

```bash
# HTTP 代理
export MY_PROXY="http://127.0.0.1:7890"

# HTTPS 代理  
export MY_PROXY="https://127.0.0.1:7890"

# SOCKS5 代理
export MY_PROXY="socks5://127.0.0.1:1080"
```

### 常见代理工具

- **Clash**: http://127.0.0.1:7890
- **V2Ray**: http://127.0.0.1:10809
- **Shadowsocks**: socks5://127.0.0.1:1080
- **Trojan**: http://127.0.0.1:10809

---

## 📢 推送通知

脚本支持登录成功时发送通知。配置以下环境变量：

```bash
# Server 酱（微信推送）
export PUSH_KEY="SCT开头的key"

# PushPlus（企业微信等）
export PUSH_PLUS_TOKEN="token"

# Telegram 机器人
export TG_BOT_TOKEN="bot_token"
export TG_USER_ID="user_id"

# 钉钉机器人
export DD_BOT_TOKEN="token"
export DD_BOT_SECRET="secret"
```

---

## 🔄 多账号管理

支持同时管理多个账号，使用 `&` 或换行分隔：

```bash
# 方式一：使用 & 分隔
export PICA_ACCOUNT="user1:pass1&user2:pass2&user3:pass3"

# 方式二：使用换行分隔
export PICA_ACCOUNT="user1:pass1
user2:pass2
user3:pass3"
```

脚本会依次对每个账号执行签到，并汇总结果。

---

---

## 🆕 青龙面板集成

ComicsPuncher 已完全适配青龙面板！主要优势：

✅ Web UI 界面管理  
✅ 可视化日志查看  
✅ 环境变量动态配置  
✅ 支持多推送渠道  
✅ 容器化部署  
✅ 定时任务管理  

### 快速部署

1. 在青龙面板的 **订阅管理** 中添加本项目
2. 在 **环境变量** 中配置账号和推送信息
3. 在 **定时任务** 中创建签到任务

[查看详细的青龙部署指南 →](./QINGLONG_GUIDE.md)

---

## 🔧 常见问题 (FAQ)

### Q: 哔咔登录失败

**A**: 检查以下问题：
1. 账号密码是否正确
2. 是否需要配置代理（国内用户必需）
3. 代理是否正常工作
4. 网络连接是否正常

### Q: 禁漫天堂无法连接

**A**: 禁漫天堂的域名可能变化，脚本会自动更新。如果仍无法连接：
1. 检查代理配置
2. 确保能访问 JM 的分流服务器
3. 查看最新版本是否有更新

### Q: 多账号只有一个生效

**A**: 检查账号分隔符是否正确：
```bash
# ✅ 正确
PICA_ACCOUNT="user1:pass1&user2:pass2"

# ❌ 错误
PICA_ACCOUNT="user1:pass1,user2:pass2"  # 不支持逗号
```

### Q: 密码中包含特殊字符怎么办？

**A**: 使用换行分隔：
```bash
export PICA_ACCOUNT="user1:pass@123
user2:pass&456"
```

### Q: 无法推送通知

**A**: 检查步骤：
1. 推送配置是否正确填写
2. Token/Key 是否有效期内
3. 查看脚本日志中的推送错误信息

## 📄 许可证

MIT License

## 🙏 致谢

- [niuhuan/pica-go](https://github.com/niuhuan/pica-go) - 哔咔漫画 API 参考
- [hhairu/JMComic-Crawler](https://github.com/hhairu/JMComic-Crawler) - JM 爬虫库
- [whyour/qinglong](https://github.com/whyour/qinglong) - 青龙面板
