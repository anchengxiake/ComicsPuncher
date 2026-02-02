"""
漫画平台自动签到脚本
cron "30 8 * * *" script-path=main.py,tag=ComicsPuncher
new Env('漫画签到')
"""
import logging
import os
import sys
import re
from pica_punch import PicaPuncher
from jm_punch import JmPuncher

# 日志格式设置
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============ 青龙通知模块加载 ============
notify = None
try:
    from notify import send
    notify = send
    logging.info("✅ 已加载 notify 通知模块")
except ImportError:
    logging.warning("⚠️ 未加载通知模块，跳过通知功能")


def parse_accounts(account_str):
    """
    解析账号字符串，支持多种分隔符
    格式: user1:pass1&user2:pass2 或 user1:pass1\\nuser2:pass2
    返回: [(user, pass), ...]
    """
    if not account_str:
        return []
    
    # 支持 & 和换行符作为分隔符
    accounts = re.split(r'[&\n]', account_str.strip())
    result = []
    
    for account in accounts:
        account = account.strip()
        if ':' in account:
            user, pwd = account.split(':', 1)
            result.append((user.strip(), pwd.strip()))
    
    return result


def get_config_from_env():
    """
    从环境变量获取配置
    支持两种模式：
    1. 独立配置: PICA_USER, PICA_PW, JM_USER, JM_PW
    2. 统一配置: PICA_ACCOUNT, JM_ACCOUNT (多账号用 & 或 \\n 分隔)
    """
    
    pica_accounts = []
    jm_accounts = []
    proxy = os.getenv('MY_PROXY', '').strip() or None
    
    # 模式1: 统一账号变量
    pica_account_str = os.getenv('PICA_ACCOUNT', '').strip()
    jm_account_str = os.getenv('JM_ACCOUNT', '').strip()
    
    if pica_account_str:
        pica_accounts = parse_accounts(pica_account_str)
    else:
        # 模式2: 独立变量（兼容原始配置）
        pica_user = os.getenv('PICA_USER', '').strip()
        pica_pw = os.getenv('PICA_PW', '').strip()
        if pica_user and pica_pw:
            pica_accounts.append((pica_user, pica_pw))
    
    if jm_account_str:
        jm_accounts = parse_accounts(jm_account_str)
    else:
        jm_user = os.getenv('JM_USER', '').strip()
        jm_pw = os.getenv('JM_PW', '').strip()
        if jm_user and jm_pw:
            jm_accounts.append((jm_user, jm_pw))
    
    return pica_accounts, jm_accounts, proxy


def send_notification(title, content):
    """统一的通知函数"""
    if notify:
        try:
            notify(title, content)
            logging.info("✅ 推送成功")
        except Exception as e:
            logging.error(f"❌ 推送失败: {e}")
    else:
        logging.info(f"📢 {title}\n{content}")


def main():
    """主函数"""
    logging.info("=" * 50)
    logging.info("🚀 漫画平台签到脚本启动")
    logging.info("=" * 50)
    
    # 获取配置
    pica_accounts, jm_accounts, proxy = get_config_from_env()
    
    if not pica_accounts and not jm_accounts:
        logging.error("❌ 未配置任何账号，请检查环境变量")
        logging.error("支持的环境变量:")
        logging.error("  - PICA_ACCOUNT: 哔咔账号配置")
        logging.error("  - JM_ACCOUNT: 禁漫账号配置")
        logging.error("  - MY_PROXY: 代理地址 (可选)")
        sys.exit(1)
    
    results = []
    
    # 执行哔咔打卡
    if pica_accounts:
        logging.info(f"📱 开始执行哔咔打卡 ({len(pica_accounts)} 个账号)...")
        for idx, (user, pwd) in enumerate(pica_accounts, 1):
            try:
                logging.info(f"哔咔账号 {idx}/{len(pica_accounts)}: {user}")
                pica = PicaPuncher(user, pwd, proxy)
                pica.run()
                results.append(f"✅ 哔咔账号 {idx} 签到成功")
            except Exception as e:
                logging.error(f"❌ 哔咔账号 {idx} 签到失败: {e}")
                results.append(f"❌ 哔咔账号 {idx} 签到失败: {e}")
    
    # 执行 JM 打卡
    if jm_accounts:
        logging.info(f"🔞 开始执行禁漫打卡 ({len(jm_accounts)} 个账号)...")
        for idx, (user, pwd) in enumerate(jm_accounts, 1):
            try:
                logging.info(f"禁漫账号 {idx}/{len(jm_accounts)}: {user}")
                jm = JmPuncher(user, pwd, proxy)
                jm.run()
                results.append(f"✅ 禁漫账号 {idx} 签到成功")
            except Exception as e:
                logging.error(f"❌ 禁漫账号 {idx} 签到失败: {e}")
                results.append(f"❌ 禁漫账号 {idx} 签到失败: {e}")
    
    # 汇总结果并通知
    summary = "\n".join(results)
    logging.info("=" * 50)
    logging.info("📊 签到汇总:\n" + summary)
    logging.info("=" * 50)
    
    send_notification("漫画平台签到", summary)


if __name__ == "__main__":
    main()
