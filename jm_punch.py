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
        self.user_data = None

    def run(self):
        """执行禁漫天堂登录并自动完成活跃"""
        try:
            logging.info(f"正在尝试登录禁漫 (用户: {self.username})...")
            
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

            # 登录接口返回的数据包含完整用户信息
            resp = client.login(self.username, self.password)
            self.user_data = resp.res_data

            logging.info("=" * 40)
            logging.info("🎉 禁漫登录成功！")
            logging.info(f"   用户名: {self.user_data.get('username')}")
            logging.info(f"   金币余额: {self.user_data.get('coin')}")
            
            # 检查是否有额外信息
            level = self.user_data.get('level')
            if level:
                logging.info(f"   用户等级: {level}")
            
            exp = self.user_data.get('exp')
            if exp:
                logging.info(f"   经验值: {exp}")
            
            logging.info("=" * 40)
            
            return True

        except ConnectionError as e:
            logging.error(f"❌ 禁漫网络连接异常: {e}")
            raise
        except Exception as e:
            logging.error(f"❌ 禁漫运行异常: {e}")
            raise
