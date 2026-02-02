"""
禁漫天堂自动签到脚本
cron "30 8 * * *" script-path=jm_punch.py,tag=禁漫签到
new Env('禁漫签到')
"""
import logging
import os
import sys
import re
import json
import time
import requests
from datetime import datetime

# 日志格式
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 尝试加载通知模块
notify = None
try:
    from notify import send
    notify = send
    logging.info("✅ 已加载 notify 通知模块")
except ImportError:
    logging.warning("⚠️ 未加载通知模块")


class JmPuncher:
    """禁漫天堂自动登录（通过 API）"""

    def __init__(self, username, password, proxy=None):
        self.username = username
        self.password = password
        self.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.session = requests.Session()
        if self.proxies:
            self.session.proxies.update(self.proxies)

    def get_domain(self):
        """获取最新的禁漫域名"""
        try:
            # 从官方API获取最新域名
            resp = self.session.get(
                "https://comic-api-doc.jmhh.net/api/getContentIndexDomain",
                timeout=10
            )
            data = resp.json()
            if data.get("code") == 200:
                return data["data"].get("domain", "https://api.jmhh.net")
        except:
            pass
        return "https://api.jmhh.net"

    def run(self):
        try:
            logging.info(f"正在尝试登录禁漫 (用户: {self.username})...")
            
            # 获取最新域名
            domain = self.get_domain()
            
            # 登录接口
            login_url = f"{domain}/user/login"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "username": self.username,
                "password": self.password
            }
            
            resp = self.session.post(login_url, data=data, headers=headers, timeout=20)
            result = resp.json()
            
            if result.get("code") != 0:
                logging.error(f"❌ 禁漫登录失败: {result.get('message', '未知错误')}")
                return False
            
            user_data = result.get("data", {})
            username_from_api = user_data.get("username", self.username)
            
            logging.info(f"🎉 禁漫登录成功！用户: {username_from_api}")
            
            # 显示用户信息
            level = user_data.get("level")
            coin = user_data.get("coin")
            if level:
                logging.info(f"   等级: {level}")
            if coin:
                logging.info(f"   金币: {coin}")
            
            return True

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ 禁漫网络异常: {e}")
            return False
        except Exception as e:
            logging.error(f"❌ 禁漫异常: {e}")
            return False


def parse_accounts(account_str):
    """解析账号: user1:pass1&user2:pass2 或 user1:pass1\nuser2:pass2"""
    if not account_str:
        return []
    accounts = re.split(r'[&\n]', account_str.strip())
    result = []
    for account in accounts:
        account = account.strip()
        if ':' in account:
            user, pwd = account.split(':', 1)
            result.append((user.strip(), pwd.strip()))
    return result


if __name__ == "__main__":
    print(f"==== 禁漫签到开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====\n")

    # 获取配置
    jm_accounts = []
    
    # 优先使用 JM_ACCOUNT（多账号）
    jm_account_str = os.getenv('JM_ACCOUNT', '').strip()
    if jm_account_str:
        jm_accounts = parse_accounts(jm_account_str)
    else:
        # 兼容旧配置
        jm_user = os.getenv('JM_USER', '').strip()
        jm_pw = os.getenv('JM_PW', '').strip()
        if jm_user and jm_pw:
            jm_accounts.append((jm_user, jm_pw))
    
    proxy = os.getenv('MY_PROXY', '').strip() or None

    if not jm_accounts:
        logging.error("❌ 未配置禁漫账号，请设置 JM_ACCOUNT 或 JM_USER/JM_PW")
        sys.exit(1)

    print(f"✅ 检测到共 {len(jm_accounts)} 个禁漫账号\n")
    print("----------禁漫开始尝试登录----------")

    msg = ""
    for idx, (user, pwd) in enumerate(jm_accounts, 1):
        log = f"\n🙍🏻 第{idx}个账号 ({user})\n"
        msg += log
        
        puncher = JmPuncher(user, pwd, proxy)
        if puncher.run():
            result_msg = f"✅ 登录成功\n"
            msg += result_msg
        else:
            result_msg = f"❌ 登录失败\n"
            msg += result_msg
        
        logging.info(log + result_msg)
        
        # 多账号间随机延迟
        if idx < len(jm_accounts):
            time.sleep(1)

    print("----------禁漫登录执行完毕----------")
    print(f"\n==== 禁漫签到完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====")
    
    # 推送通知
    if notify:
        try:
            notify("禁漫签到", msg[:-1])  # 去掉最后的换行符
        except Exception as e:
            logging.error(f"推送失败: {e}")
