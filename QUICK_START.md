# 快速参考指南

## ComicsPuncher 青龙面板集成 - 快速上手

### ⚡ 30秒快速开始

```bash
# 1. 设置环境变量
export PICA_ACCOUNT="哔咔账号:密码"
export JM_ACCOUNT="禁漫账号:密码"

# 2. 运行脚本
python main.py
```

---

## 📋 常用配置

### 基础配置

```bash
# 单账号
PICA_USER=username
PICA_PW=password
JM_USER=username
JM_PW=password
```

### 多账号配置

```bash
# 使用 & 分隔
PICA_ACCOUNT=user1:pass1&user2:pass2&user3:pass3

# 或使用换行分隔
PICA_ACCOUNT=user1:pass1
user2:pass2
user3:pass3
```

### 代理配置（国内必需）

```bash
MY_PROXY=http://127.0.0.1:7890
```

### 推送通知

```bash
# Server 酱
PUSH_KEY=SCT开头的key

# PushPlus
PUSH_PLUS_TOKEN=your_token

# Telegram
TG_BOT_TOKEN=bot_token
TG_USER_ID=user_id

# 钉钉
DD_BOT_TOKEN=token
DD_BOT_SECRET=secret
```

---

## 🐳 青龙面板部署

### 方式一：订阅脚本

```
https://github.com/账号/ComicsPuncher.git
```

### 方式二：手动上传

1. 下载所有脚本文件到本地
2. 上传到青龙容器的 `/ql/scripts/` 目录

### 配置步骤

1. **环境变量** → 添加上述配置
2. **定时任务** → 创建新任务
   - 任务名：漫画签到
   - 脚本：/ql/scripts/ComicsPuncher/main.py
   - Cron：30 8 * * *
   - 类型：Python

---

## 🔧 Cron 表达式

| 表达式 | 说明 |
|-------|-----|
| `30 8 * * *` | 每天8:30 |
| `0 0 * * *` | 每天0:00 |
| `0 9 * * 1-5` | 工作日9:00 |
| `0 */6 * * *` | 每6小时 |
| `0 9,17 * * *` | 每天9:00和17:00 |

---

## 📂 文件说明

| 文件 | 用途 |
|-----|-----|
| `main.py` | 主脚本，支持多账号 |
| `pica_punch.py` | 哔咔漫画签到模块 |
| `jm_punch.py` | 禁漫天堂签到模块 |
| `notify.py` | 推送通知模块 |
| `requirements.txt` | 依赖包列表 |
| `README.md` | 完整文档 |
| `QINGLONG_GUIDE.md` | 青龙部署指南 |

---

## ❓ 常见问题速查

| 问题 | 解决方案 |
|-----|--------|
| 登录失败 | 检查账号密码和代理设置 |
| 无法推送 | 验证Token/Key是否正确 |
| 多账号不生效 | 检查账号分隔符（& 或换行） |
| 找不到通知模块 | 确保notify.py在脚本目录中 |
| 密码包含特殊字符 | 使用换行分隔或URL编码 |

---

## 💡 小贴士

✅ **推荐做法**
- 使用环境变量而不是硬编码
- 使用多账号而不是单账号
- 配置推送通知及时了解执行结果
- 在海外VPS运行可省去代理配置

❌ **避免做法**
- 直接修改脚本中的账号密码
- 在脚本中硬编码敏感信息
- 使用不稳定的代理
- 忽视任务日志和错误提示

---

## 📞 获取帮助

1. 查看 [QINGLONG_GUIDE.md](./QINGLONG_GUIDE.md) 了解详细步骤
2. 查看 [ADAPTION_SUMMARY.md](./ADAPTION_SUMMARY.md) 了解技术细节
3. 在青龙面板查看任务日志
4. 检查环境变量配置是否正确

---

## 🚀 高级用法

### 多个漫画平台

```bash
# 同时管理3个哔咔账号和2个禁漫账号
PICA_ACCOUNT=pica_user1:pass1&pica_user2:pass2&pica_user3:pass3
JM_ACCOUNT=jm_user1:pass1&jm_user2:pass2
```

### 多个推送渠道

```bash
# 同时配置多个推送，脚本会同时发送所有渠道
PUSH_KEY=SCT_xxx
PUSH_PLUS_TOKEN=token_xxx
TG_BOT_TOKEN=bot_xxx
TG_USER_ID=user_xxx
```

### 跳过推送

```bash
# 某些标题不推送
SKIP_PUSH_TITLE=标题1
标题2
标题3
```

---

## 📊 输出示例

```
2026-02-02 08:30:00 - INFO - ==================================================
2026-02-02 08:30:00 - INFO - 🚀 漫画平台签到脚本启动
2026-02-02 08:30:00 - INFO - ==================================================
2026-02-02 08:30:01 - INFO - 📱 开始执行哔咔打卡 (2 个账号)...
2026-02-02 08:30:01 - INFO - 哔咔账号 1/2: user1
2026-02-02 08:30:02 - INFO - 正在尝试登录哔咔 (用户: user1)...
2026-02-02 08:30:03 - INFO - 🎉 哔咔登录成功
2026-02-02 08:30:03 - INFO - 🎉 哔咔签到成功！
2026-02-02 08:30:04 - INFO - 🔞 开始执行禁漫打卡 (1 个账号)...
2026-02-02 08:30:05 - INFO - 🎉 禁漫登录成功！
2026-02-02 08:30:06 - INFO - ==================================================
2026-02-02 08:30:06 - INFO - 📊 签到汇总:
✅ 哔咔账号 1 签到成功
✅ 哔咔账号 2 签到成功
✅ 禁漫账号 1 签到成功
2026-02-02 08:30:06 - INFO - ==================================================
2026-02-02 08:30:07 - INFO - ✅ 推送成功
```

---

**版本**：1.0.0  
**更新**：2026-02-02  
**状态**：✅ 完全就绪
