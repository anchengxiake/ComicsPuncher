import time
import hmac
import hashlib
import requests
import logging


class PicaPuncher:
    """
    哔咔漫画自动签到类
    基于哔咔官方 API 实现
    """

    API_URL = "https://picaapi.picacomic.com"
    SECRET_KEY = r"~d}$Q7$eIni=V)9\RK/P.RM4;9[7|@/CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn"
    API_KEY = "C69BAF41DA5ABD1FFEDC6D2FEA56B"

    def __init__(self, username, password, proxy=None):
        self.username = username
        self.password = password
        self.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.user_info = None

    def _get_headers(self, path, method, token=None):
        """构建哔咔特有的加密请求头"""
        nonce = "b1ab87b4800d4d4590a11701b8551afa"  # 固定随机数
        ts = str(int(time.time()))

        # 签名算法: url路径 + 时间戳 + 随机数 + 请求方式 + API_KEY
        raw = (path + ts + nonce + method + self.API_KEY).lower()
        signature = hmac.new(
            self.SECRET_KEY.encode(), raw.encode(), hashlib.sha256
        ).hexdigest()

        headers = {
            "api-key": self.API_KEY,
            "signature": signature,
            "time": ts,
            "nonce": nonce,
            "app-channel": "2",  # 分流通道
            "app-version": "2.2.1.2.3.3",
            "app-uuid": "defaultUuid",
            "app-platform": "android",
            "app-build-version": "44",
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.8.1",
            "accept": "application/vnd.picacomic.com.v1+json",
        }
        if token:
            headers["authorization"] = token
        return headers

    def run(self):
        """执行全流程：登录 -> 获取用户信息 -> 签到"""
        try:
            # 1. 登录
            logging.info(f"正在尝试登录哔咔 (用户: {self.username})...")
            login_path = "auth/sign-in"
            res = requests.post(
                f"{self.API_URL}/{login_path}",
                json={"email": self.username, "password": self.password},
                headers=self._get_headers(login_path, "POST"),
                proxies=self.proxies,
                timeout=20,
            )

            login_data = res.json()
            if res.status_code != 200 or login_data.get("message") != "success":
                logging.error(f"❌ 哔咔登录失败: {login_data.get('message')}")
                raise Exception(f"Login failed: {login_data.get('message')}")

            token = login_data["data"]["token"]
            self.user_info = login_data["data"]["user"]
            logging.info("🎉 哔咔登录成功")
            logging.info(f"   用户: {self.user_info.get('email')}")
            logging.info(f"   经验值: {self.user_info.get('exp')}")

            # 2. 签到
            logging.info("正在进行哔咔签到...")
            punch_path = "users/punch-in"
            res = requests.post(
                f"{self.API_URL}/{punch_path}",
                headers=self._get_headers(punch_path, "POST", token),
                proxies=self.proxies,
                timeout=20,
            )

            punch_data = res.json()
            if punch_data.get("message") == "success":
                punch_info = punch_data["data"]["res"]
                logging.info("=" * 30)
                logging.info("✅ 哔咔签到成功！")
                logging.info(f"   状态: {punch_info.get('status')}")
                logging.info(f"   奖励: +{punch_info.get('punchInDay')} 天连续签到")
                logging.info("=" * 30)
                return True
            elif punch_data.get("message") == "user already punch in":
                logging.info("⚠️  哔咔今日已签到")
                return True
            else:
                logging.warning(f"⚠️  哔咔签到反馈: {punch_data.get('message')}")
                return False

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ 哔咔网络异常: {e}")
            raise
        except Exception as e:
            logging.error(f"❌ 哔咔运行异常: {e}")
            raise
