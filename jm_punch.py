import logging
from jmcomic import JmOption


class JmPuncher:
    """
    禁漫天堂自动签到类
    基于 jmcomic 库实现，模拟移动端 API 登录
    """

    def __init__(self, username, password, proxy=None):
        self.username = username
        self.password = password
        self.proxy = proxy

    def run(self):
        try:
            # 构造禁漫配置
            option = JmOption.construct(
                {
                    "client": {
                        "username": self.username,
                        "password": self.password,
                        "proxies": {"http": self.proxy, "https": self.proxy}
                        if self.proxy
                        else None,
                    }
                }
            )
            client = option.build_jm_client()

            logging.info(f"正在尝试登录 JM (用户: {self.username})...")
            # 登录接口返回的数据包含完整用户信息
            resp = client.login(self.username, self.password)
            user_data = resp.res_data

            logging.info("=" * 20)
            logging.info("🎉 JM 登录活跃成功！")
            logging.info(f"用户名: {user_data.get('username')}")
            logging.info(f"金币余额: {user_data.get('coin')}")
            logging.info("=" * 20)

        except Exception as e:
            logging.error(f"JM 运行异常: {e}")
