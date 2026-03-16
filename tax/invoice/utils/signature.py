import hashlib
import hmac  # 添加hmac模块导入
import random
import string
import time


def calculate_signature(method, path, random_string, timestamp, app_key, app_secret):
    """计算HMAC-SHA256签名"""
    # 构建签名字符串，与服务器端保持一致
    sign_content = f"Method={method}&Path={path}&RandomString={random_string}&TimeStamp={timestamp}&AppKey={app_key}"
    
    # 使用HMAC-SHA256计算签名，以secret作为密钥
    signature = hmac.new(
        app_secret.encode('utf-8'),
        sign_content.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # 转为大写
    return signature.upper()


def generate_random_string(length=16):
    """
    生成指定长度的随机字符串
    
    Args:
        length: 字符串长度，默认16
        
    Returns:
        随机字符串
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_timestamp():
    """
    获取当前时间戳（秒）
    
    Returns:
        当前时间戳字符串
    """
    return str(int(time.time()))