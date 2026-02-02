#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
青龙面板统一通知模块 - 支持多种推送渠道
"""
import base64
import hashlib
import hmac
import json
import os
import re
import threading
import time
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

import requests

# 原先的 print 函数和主线程的锁
_print = print
mutex = threading.Lock()


# 定义新的 print 函数
def print(text, *args, **kw):
    """
    使输出有序进行，不出现多线程同一时间输出导致错乱的问题。
    """
    with mutex:
        _print(text, *args, **kw)


# 通知服务
# fmt: off
push_config = {
    'HITOKOTO': True,                  # 启用一言（随机句子）

    'BARK_PUSH': '',                    # bark IP 或设备码
    'BARK_ARCHIVE': '',                 
    'BARK_GROUP': '',                   
    'BARK_SOUND': '',                   
    'BARK_ICON': '',                    
    'BARK_LEVEL': '',                   
    'BARK_URL': '',                     

    'CONSOLE': False,                    # 控制台输出

    'DD_BOT_SECRET': '',                # 钉钉机器人的 DD_BOT_SECRET
    'DD_BOT_TOKEN': '',                 # 钉钉机器人的 DD_BOT_TOKEN

    'PUSH_KEY': '',                     # server 酱的 PUSH_KEY

    'PUSH_PLUS_TOKEN': '',              # pushplus 推送的用户令牌
    'PUSH_PLUS_USER': '',               # pushplus 推送的群组编码

    'TG_BOT_TOKEN': '',                 # tg 机器人的 TG_BOT_TOKEN
    'TG_USER_ID': '',                   # tg 机器人的 TG_USER_ID
    'TG_API_HOST': '',                  # tg 代理 api
    'TG_PROXY_AUTH': '',                # tg 代理认证参数
    'TG_PROXY_HOST': '',                # tg 机器人的 TG_PROXY_HOST
    'TG_PROXY_PORT': '',                # tg 机器人的 TG_PROXY_PORT
}
# fmt: on

for k in push_config:
    if os.getenv(k):
        v = os.getenv(k)
        push_config[k] = v


def serverJ(title: str, content: str) -> None:
    """
    通过 serverJ 推送消息。
    """
    if not push_config.get("PUSH_KEY"):
        return
    print("serverJ 服务启动")

    data = {"text": title, "desp": content.replace("\n", "\n\n")}

    match = re.match(r"sctp(\d+)t", push_config.get("PUSH_KEY"))
    if match:
        num = match.group(1)
        url = f'https://{num}.push.ft07.com/send/{push_config.get("PUSH_KEY")}.send'
    else:
        url = f'https://sctapi.ftqq.com/{push_config.get("PUSH_KEY")}.send'

    response = requests.post(url, data=data).json()

    if response.get("errno") == 0 or response.get("code") == 0:
        print("serverJ 推送成功！")
    else:
        print(f'serverJ 推送失败！错误码：{response["message"]}')


def dingding_bot(title: str, content: str) -> None:
    """
    使用 钉钉机器人 推送消息。
    """
    if not push_config.get("DD_BOT_SECRET") or not push_config.get("DD_BOT_TOKEN"):
        return
    print("钉钉机器人 服务启动")

    timestamp = str(round(time.time() * 1000))
    secret_enc = push_config.get("DD_BOT_SECRET").encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, push_config.get("DD_BOT_SECRET"))
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'https://oapi.dingtalk.com/robot/send?access_token={push_config.get("DD_BOT_TOKEN")}&timestamp={timestamp}&sign={sign}'
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"msgtype": "text", "text": {"content": f"{title}\n\n{content}"}}
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=15
    ).json()

    if not response["errcode"]:
        print("钉钉机器人 推送成功！")
    else:
        print("钉钉机器人 推送失败！")


def pushplus_bot(title: str, content: str) -> None:
    """
    通过 pushplus 推送消息。
    """
    if not push_config.get("PUSH_PLUS_TOKEN"):
        return
    print("PUSHPLUS 服务启动")

    url = "https://www.pushplus.plus/send"
    data = {
        "token": push_config.get("PUSH_PLUS_TOKEN"),
        "title": title,
        "content": content,
        "topic": push_config.get("PUSH_PLUS_USER"),
    }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=body, headers=headers).json()

    code = response["code"]
    if code == 200:
        print("PUSHPLUS 推送成功！")
    else:
        print("PUSHPLUS 推送失败！")


def telegram_bot(title: str, content: str) -> None:
    """
    使用 telegram 机器人 推送消息。
    """
    if not push_config.get("TG_BOT_TOKEN") or not push_config.get("TG_USER_ID"):
        return
    print("tg 服务启动")

    if push_config.get("TG_API_HOST"):
        url = f"{push_config.get('TG_API_HOST')}/bot{push_config.get('TG_BOT_TOKEN')}/sendMessage"
    else:
        url = (
            f"https://api.telegram.org/bot{push_config.get('TG_BOT_TOKEN')}/sendMessage"
        )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "chat_id": str(push_config.get("TG_USER_ID")),
        "text": f"{title}\n\n{content}",
        "disable_web_page_preview": "true",
    }
    proxies = None
    if push_config.get("TG_PROXY_HOST") and push_config.get("TG_PROXY_PORT"):
        if push_config.get("TG_PROXY_AUTH") is not None and "@" not in push_config.get(
            "TG_PROXY_HOST"
        ):
            push_config["TG_PROXY_HOST"] = (
                push_config.get("TG_PROXY_AUTH")
                + "@"
                + push_config.get("TG_PROXY_HOST")
            )
        proxyStr = "http://{}:{}".format(
            push_config.get("TG_PROXY_HOST"), push_config.get("TG_PROXY_PORT")
        )
        proxies = {"http": proxyStr, "https": proxyStr}
    response = requests.post(
        url=url, headers=headers, params=payload, proxies=proxies
    ).json()

    if response["ok"]:
        print("tg 推送成功！")
    else:
        print("tg 推送失败！")


def add_notify_function():
    notify_function = []
    if push_config.get("DD_BOT_TOKEN") and push_config.get("DD_BOT_SECRET"):
        notify_function.append(dingding_bot)
    if push_config.get("PUSH_KEY"):
        notify_function.append(serverJ)
    if push_config.get("PUSH_PLUS_TOKEN"):
        notify_function.append(pushplus_bot)
    if push_config.get("TG_BOT_TOKEN") and push_config.get("TG_USER_ID"):
        notify_function.append(telegram_bot)
    if not notify_function:
        print("无推送渠道，请检查通知变量是否正确")
    return notify_function


def send(title: str, content: str, ignore_default_config: bool = False, **kwargs):
    """
    统一推送函数
    """
    if kwargs:
        global push_config
        if ignore_default_config:
            push_config = kwargs
        else:
            push_config.update(kwargs)

    if not content:
        print(f"{title} 推送内容为空！")
        return

    notify_function = add_notify_function()
    ts = [
        threading.Thread(target=mode, args=(title, content), name=mode.__name__)
        for mode in notify_function
    ]
    [t.start() for t in ts]
    [t.join() for t in ts]


def main():
    send("测试标题", "测试内容")


if __name__ == "__main__":
    main()
