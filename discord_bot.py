# -*- coding: utf-8 -*-
import requests
import json
import random
import time
import logging
from typing import List, Dict
from collections import deque
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 用于存储已发送的消息
sent_messages = deque(maxlen=30)  # 保存最近30条消息的历史

def countdown(seconds: int):
    """
    显示倒计时进度条
    """
    # ANSI颜色代码
    GREEN = '\033[92m'  # 绿色
    BLUE = '\033[94m'   # 蓝色
    RESET = '\033[0m'   # 重置颜色
    
    for remaining in range(seconds, 0, -1):
        progress = int(50 * (seconds - remaining) / seconds)
        bar = GREEN + '=' * progress + '>' + ' ' * (50 - progress) + RESET
        time_display = BLUE + f"{remaining}秒" + RESET
        sys.stdout.write(f'\r[{bar}] {time_display} ')
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\r' + ' ' * 70 + '\r')
    sys.stdout.flush()

def get_random_message() -> str:
    """
    返回随机消息，确保不重复
    """
    messages = [
        "大家好",
        "Hello everyone",
        "GM",
        "早上好",
        "晚上好",
        "今天天气真好",
        "加油",
        "are you ok?",
        "吃饭了没，烙铁",
        "你好",
        "你好!",
        "嘿, 你好吗?",
        "嗨, 最近怎么样?",
        "很高兴见到你!",
        "好久不见!",
        "一切都还好吗?",
        "今天过得怎么样?",
        "嗨! 一切顺利吗?",
        "你好啊!",
        "嗨, 见到你真高兴!",
        "嘿, 最近忙什么呢?",
        "哈喽, 朋友!",
        "你好, 最近可好?",
        "你好, 很久没联系了!",
        "今天看起来不错哦!",
        "嗨嗨, 你来了!",
        "你好吗, 朋友?",
        "嗨, 今天有什么计划?",
        "嘿, 今天心情怎么样?",
        "你好, 最近有什么新鲜事?",
        "嗨嗨, 想你了!",
        "你好, 一切都还顺利吧?",
        "嘿, 好久不见, 最近可忙?",
        "你好, 你看起来很精神!",
        "嗨, 看到你真开心!",
        "哈喽, 今天遇到什么有趣的事了吗?",
        "嗨, 最近有空聊聊吗?",
        "你好, 有什么需要帮忙的吗?",
        "嘿, 最近过得如何?",
        "哈喽, 今天怎么安排的?",
        "你好, 见到你真高兴!",
        "嗨, 你看起来棒极了!",
        "你好, 最近有什么好消息吗?",
        "哈喽, 来聊聊吧!",
        "你好, 新的一天, 加油哦!",
        "嗨, 你的笑容真好看!",
        "你好, 最近在忙什么呢?",
        "哈喽, 好久没联系了, 一切都好吧?",
        "你好, 看到你心情变好啦!",
        "嘿, 今天的你真不错!",
        "嗨嗨, 别来无恙?",
        "你好, 有什么好推荐的吗?",
        "嗨, 最近有什么趣事吗?",
        "你好, 看到你真是惊喜!",
        "嘿, 好久不见, 聊聊近况吧!",
        "你好, 感觉今天特别适合见面!",
        "哈喽, 一切都还好吧?",
        "嗨, 你的状态看起来很好哦!",
        "你好, 最近生活如何?",
        "嘿, 今天的天气真不错!",
        "你好, 有什么计划吗?",
        "嗨嗨, 新的一天也要加油哦!"
    ]
    
    available_messages = [msg for msg in messages if msg not in sent_messages]
    
    if not available_messages:
        sent_messages.clear()
        available_messages = messages
    
    message = random.choice(available_messages)
    sent_messages.append(message)
    return message

def send_message(channel_id: str, token: str, message: str = None) -> bool:
    """
    向指定频道发送消息
    """
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    
    payload = {
        "content": message or get_random_message(),
        "nonce": str(random.randint(1000000000000000000, 9999999999999999999)),
        "tts": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logger.info(f"消息发送成功: {payload['content']}")
        return True
    except Exception as e:
        logger.error(f"发送消息失败: {str(e)}")
        return False

def main():
    configs = [
        {
            "name": "备注1",
            "token": "这里填写Discord令牌",
            "channels": ["这里填写频道ID"]
        },

        #这个是第二个账户的配置，如果你有很多dc号，则添加对应的token和channels，只有一个号的话就删掉下方[]中括号的内容（包括中括号）
        {
            "name": "备注2",
            "token": "同上面一样",
            "channels": ["同理"]
        }
    ]
    
    print("Discord自动发言脚本启动")
    print("按 Ctrl+C 停止运行")
    print("-" * 50)
    
    try:
        while True:
            for config in configs:
                token = config["token"]
                channels = config["channels"]
                name = config["name"]
                
                for channel_id in channels:
                    print(f"\n使用 {name} 发送消息...")
                    send_message(channel_id, token)
                    
                    sleep_time = random.randint(30, 80)#这里设置的是在（30秒--80秒）的时间区间内随机发送消息
                    print(f"等待 {sleep_time} 秒后继续...")
                    countdown(sleep_time)
                    
    except KeyboardInterrupt:
        print("\n程序已停止运行")
    except Exception as e:
        logger.error(f"运行时出错: {str(e)}")
        time.sleep(60)

if __name__ == "__main__":
    main()
