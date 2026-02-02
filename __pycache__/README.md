# ComicsPuncher 漫画平台签到脚本

简单的哔咔漫画和禁漫天堂自动签到脚本，完全支持[青龙面板](https://github.com/whyour/qinglong)。

## 🌟 特性

- ✅ 哔咔漫画自动签到（pica_punch.py）
- ✅ 禁漫天堂自动登录（jm_punch.py）  
- ✅ 支持多账号管理
- ✅ 支持推送通知（Server酱、PushPlus、Telegram、钉钉）
- ✅ 无需额外依赖（仅需 requests）

## 📦 文件说明

| 文件 | 说明 |
|-----|-----|
| `pica_punch.py` | 哔咔漫画签到脚本 |
| `jm_punch.py` | 禁漫天堂签到脚本 |

两个脚本都可以独立在青龙面板中运行。

## 🚀 青龙面板部署

### 1. 添加订阅

在青龙面板 **订阅管理** 中添加本项目：

```
https://github.com/你的账号/ComicsPuncher.git
```

或直接上传 `pica_punch.py` 和 `jm_punch.py` 到 `/ql/scripts/` 目录。

### 2. 配置环境变量

在青龙面板 **环境变量** 中添加：

#### 哔咔漫画

```
# 单账号
PICA_USER=username
PICA_PW=password

# 或多账号（用 & 或换行分隔）
PICA_ACCOUNT=user1:pass1&user2:pass2
```

#### 禁漫天堂

```
# 单账号
JM_USER=username
JM_PW=password

# 或多账号（用 & 或换行分隔）
JM_ACCOUNT=user1:pass1&user2:pass2
```

#### 可选配置

```
# 代理（国内需要）
MY_PROXY=http://127.0.0.1:7890

# 推送通知
PUSH_KEY=SCT开头的key              # Server酱
PUSH_PLUS_TOKEN=token            # PushPlus
TG_BOT_TOKEN=token               # Telegram
TG_USER_ID=user_id
DD_BOT_TOKEN=token               # 钉钉
DD_BOT_SECRET=secret
```

### 3. 创建定时任务

在青龙面板 **定时任务** 中创建：

**哔咔签到：**

| 字段 | 值 |
|-----|-----|
| 任务名称 | 哔咔签到 |
| 脚本路径 | `/ql/scripts/pica_punch.py` |
| Cron表达式 | `30 8 * * *` |
| 任务类型 | Python |

**禁漫签到：**

| 字段 | 值 |
|-----|-----|
| 任务名称 | 禁漫签到 |
| 脚本路径 | `/ql/scripts/jm_punch.py` |
| Cron表达式 | `30 8 * * *` |
| 任务类型 | Python |

## 📝 Cron 表达式

```
30 8 * * *     # 每天8:30
0 0 * * *      # 每天0:00
0 9 * * 1-5    # 工作日9:00
0 */4 * * *    # 每4小时
```

## 🔄 多账号配置

支持同时管理多个账号：

```bash
# 方式1：使用 & 分隔
PICA_ACCOUNT=user1:pass1&user2:pass2&user3:pass3

# 方式2：使用换行分隔
PICA_ACCOUNT=user1:pass1
user2:pass2
user3:pass3
```

脚本会依次对每个账号执行，并汇总结果。

## 📢 推送通知

脚本支持集成多个推送渠道，同时配置时会全部发送：

- **Server酱**：`PUSH_KEY=SCT...`
- **PushPlus**：`PUSH_PLUS_TOKEN=...`  
- **Telegram**：`TG_BOT_TOKEN=...` + `TG_USER_ID=...`
- **钉钉**：`DD_BOT_TOKEN=...` + `DD_BOT_SECRET=...`

## ❓ FAQ

### Q: 脚本找不到 notify 模块？

A: notify 模块是可选的。如果青龙面板没有这个模块，脚本会跳过推送，正常运行签到。

### Q: 账号登录失败？

A: 
1. 确认账号密码正确
2. 国内用户需要配置代理：`MY_PROXY=http://127.0.0.1:7890`
3. 检查账号是否被锁定
4. 查看青龙面板的任务日志了解具体错误信息

### Q: 多账号只有一个生效？

A: 检查账号分隔符是否正确：
```bash
# ✅ 正确
PICA_ACCOUNT=user1:pass1&user2:pass2

# ❌ 错误（不支持逗号）
PICA_ACCOUNT=user1:pass1,user2:pass2
```

### Q: 密码中包含特殊字符？

A: 使用换行分隔：
```bash
PICA_ACCOUNT=user1:pass@123
user2:pass&456
```

### Q: 执行报错 KeyError？

A: 这通常表示 API 返回的数据结构与脚本预期不符，可能原因：
1. 哔咔/禁漫 API 有更新
2. 账号登录异常（被限流、IP被封禁等）
3. 网络连接问题或代理失效

建议：
- 检查账号是否能正常登录官方网站
- 检查代理是否有效
- 查看完整的任务日志
- 到项目 Issues 页面报告问题

## 📄 许可证

MIT License

## 🙏 致谢

- 青龙面板：https://github.com/whyour/qinglong
- 哔咔漫画 API 参考：https://github.com/niuhuan/pica-go
