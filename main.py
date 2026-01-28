import logging
from pica_punch import PicaPuncher
from jm_punch import JmPuncher

# 日志格式设置
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- 用户配置区 ---
PICA_USER = "哔咔用户名"
PICA_PW = "哔咔密码"

JM_USER = "禁漫用户名"
JM_PW = "禁漫密码"

# 本地代理端口
MY_PROXY = ""  # 例如 "127.0.0.1:7890"
# ----------------

if __name__ == "__main__":
    # 执行哔咔打卡
    pica = PicaPuncher(PICA_USER, PICA_PW, MY_PROXY)
    pica.run()

    # 执行 JM 打卡
    jm = JmPuncher(JM_USER, JM_PW, MY_PROXY)
    jm.run()
