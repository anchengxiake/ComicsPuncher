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

脚本会依次对每个账号执行签到，并汇总结果。

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

### Q: 无法推送通知

**A**: 检查步骤：
1. 推送配置是否正确填写
2. Token/Key 是否有效期内
3. 查看脚本日志中的推送错误信息

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

## 📄 许可证

MIT License

## 🙏 致谢

- [niuhuan/pica-go](https://github.com/niuhuan/pica-go) - 哔咔漫画 API 参考
- [hhairu/JMComic-Crawler](https://github.com/hhairu/JMComic-Crawler) - JM 爬虫库
- [whyour/qinglong](https://github.com/whyour/qinglong) - 青龙面板


### 3. 账号配置
在运行之前，请打开 `main.py`，在 `用户配置区` 修改以下信息：
- `PICA_USER / PICA_PW`: 哔咔漫画账号密码。
- `JM_USER / JM_PW`: 禁漫天堂账号密码。
- `MY_PROXY`: **(重要)** 如果你在国内运行，请填写你的代理地址（如 `http://127.0.0.1:7897`），否则无法连接服务器。如果服务器在海外，请保持为空。

---

1. **(可选) 任务计划**:
如果你想每天自动跑，可以在 Windows “任务计划程序” 中创建一个基本任务，程序指向 `python.exe`，参数指向 `main.py` 的完整路径。

---

### 4. Linux 平台部署 (服务器挂机)

建议将脚本部署在海外 VPS（如腾讯云轻量香港、AWS、搬瓦工等），可省去代理配置。

#### **Crontab 定时任务**

1. **安装环境 (以 Ubuntu 为例)**:

```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

2. **设置定时任务**:

输入 `crontab -e`，在文件末尾添加以下行：
```bash
# 每天凌晨 08:30 自动执行打卡并记录日志
30 8 * * * /usr/bin/python3 /root/ComicsPuncher/main.py >> /root/ComicsPuncher/log.txt 2>&1
```

---

### 4. 常见问题 (FAQ)
* Q: 哔咔登录报错 `ERROR - 登录失败: {'code': 400, ...}`
  * A: 通常是签名密钥过期或代理失效。本项目已同步最新的签名算法。


* Q: 禁漫天堂域名无法连接？
  * A: 脚本会自动通过官方 API 更新最新域名，请确保你的网络能够访问 JM 的分流服务器。
