
from tax.invoice import InvoiceClient
import time
import traceback  # 新增导入
import json
import redis

import qrcode
import io
import base64 as b64lib
import math
from PIL import Image
import time
from inputimeout import inputimeout, TimeoutOccurred
# pip install inputimeout
from datetime import datetime, timedelta



APP_KEY = ''
APP_SECRET = ''

# 配置信息
nsrsbh = ""  # 统一社会信用代码
title = ""  # 名称（营业执照）
username = ""  # 手机号码（电子税务局）
password = ""  # 个人用户密码（电子税务局）
type = "6"# 6基础 7标准

ewmlx = "1";# 1 电子税务局app人脸二维码登录，10 电子税务局app扫码登录 2 个税app人脸二维码登录，3 个税app扫码确认登录

token = ""
debug = True

# 连接Redis 安装pip install redis
r = redis.Redis(
        host='127.0.0.1',
        port=6379,
        password="test123456",  # 如果有密码，填写密码
        db=0,  # 使用第0个数据库
        decode_responses=True  # 自动将Redis返回的字节转为字符串
    )

# 初始化客户端
client = InvoiceClient(
    app_key=APP_KEY,
    app_secret=APP_SECRET,
    base_url="https://api.fa-piao.com",
    debug=debug
)




#字符串转二维码图片  在命令行打印
def print_qr_code(data):
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L, # 低容错率，生成的图案更稀疏
        box_size=1,  # 字符画中通常设为1
        border=1,    # 边框宽度
    )
    qr.add_data(data)
    qr.make(fit=True)

    # 使用终端输出模式
    # qrcode 库支持将二维码输出为 ANSI 字符
    qr.print_ascii(invert=True) # invert=True 会让背景变黑，码变白（适合深色背景终端）

# base64 二维码图片  在命令行打印
def print_qr_code_base64(base64):
    base64_data = base64.strip()
    if base64_data.startswith("data:image") and "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]

    missing_padding = len(base64_data) % 4
    if missing_padding:
        base64_data += "=" * (4 - missing_padding)

    try:
        image_bytes = b64lib.b64decode(base64_data, validate=True)
    except Exception as exc:
        raise ValueError("无效的 Base64 二维码数据") from exc

    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    image = image.point(lambda p: 0 if p < 128 else 255, mode="1")

    width, height = image.size
    pixels = image.load()

    min_x, min_y, max_x, max_y = width, height, -1, -1
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 0:
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

    if max_x < min_x or max_y < min_y:
        raise ValueError("二维码图像中未检测到有效内容")

    crop = image.crop((min_x, min_y, max_x + 1, max_y + 1))
    crop_w, crop_h = crop.size
    crop_px = crop.load()

    run_lengths = []

    def collect_runs_from_row(row):
        run = 1
        prev = crop_px[0, row]
        for cx in range(1, crop_w):
            cur = crop_px[cx, row]
            if cur == prev:
                run += 1
            else:
                run_lengths.append(run)
                run = 1
                prev = cur
        run_lengths.append(run)

    def collect_runs_from_col(col):
        run = 1
        prev = crop_px[col, 0]
        for cy in range(1, crop_h):
            cur = crop_px[col, cy]
            if cur == prev:
                run += 1
            else:
                run_lengths.append(run)
                run = 1
                prev = cur
        run_lengths.append(run)

    collect_runs_from_row(crop_h // 2)
    collect_runs_from_col(crop_w // 2)

    module_size = run_lengths[0]
    for length in run_lengths[1:]:
        module_size = math.gcd(module_size, length)
    module_size = max(1, module_size)

    total_modules = round(crop_w / module_size)
    qr_candidates = [n for n in range(21, 178, 4) if n <= total_modules]
    if not qr_candidates:
        raise ValueError("无法识别二维码网格")
    modules_count = qr_candidates[-1]

    border = (total_modules - modules_count) // 2
    if border < 0:
        border = 0

    modules = []
    for r in range(modules_count):
        row = []
        for c in range(modules_count):
            sx = (border + c) * module_size + (module_size // 2)
            sy = (border + r) * module_size + (module_size // 2)
            sx = min(max(sx, 0), crop_w - 1)
            sy = min(max(sy, 0), crop_h - 1)
            row.append(crop_px[sx, sy] == 0)
        modules.append(row)

    qr = qrcode.QRCode(border=1)
    qr.modules = modules
    qr.modules_count = modules_count
    qr.data_cache = [1]
    
    qr.print_ascii(invert=True)


def get_token(force_update=False):
    key =  nsrsbh + "@" + username + "@TOKEN"
    if force_update:
        # 获取授权Token文档
         # @link https://fa-piao.com/doc.html#api1?source=github
        auth_response = client.auth.get_authorization(nsrsbh,type)
        # auth_response = client.auth.get_authorization(nsrsbh,type,username,password)
        if auth_response.get("code") == 200:
            print(f"授权成功，Token: {auth_response.get('data', {}).get('token')}")
            token = auth_response.get('data', {}).get('token')
            r.set(key, token, ex=3600*24*30)  # 过期时间30天
            client.auth.set_token(token)
    else:
        token = r.get(key)
        if token:
            client.auth.set_token(token)
        else:
            get_token(force_update=True)


try:
    get_token()

    # 获取认证状态
    status_response = client.auth.query_face_auth_state(nsrsbh=nsrsbh, username=username)
    match status_response.get("code"):
        case 200:
            print("认证状态: 无需认证")
        case 420:
            print("420 需要登录(人脸认证)") # 短信或者人脸认证
            login_response = client.auth.login_dppt(nsrsbh=nsrsbh, username=username, password=password, sms=None, sf=None, ewmlx=ewmlx)
            if login_response.get("code") == 200:
                deadline = (datetime.now() + timedelta(seconds=300)).strftime("%Y-%m-%d %H:%M:%S")
                try:
                    qrcode_data = login_response.get('data', {}).get('qrcode')
                    ewmid = login_response.get('data', {}).get('ewmid')
                    length = len(str(qrcode_data))
                    if  length < 500:
                        print_qr_code(qrcode_data)
                    else:
                        print_qr_code_base64(qrcode_data)
                    print("成功做完人脸认证,请输入数字 1")
                    sms = inputimeout(prompt=f"请在300秒内({deadline}前)输入验证码: ", timeout=300)
                    print(f"\n你输入了: {sms}")
                    login_response2 = client.auth.login_dppt(nsrsbh=nsrsbh, username=username, password=password, sms=None, sf=None, ewmlx=ewmlx, ewmid=ewmid)
                    if login_response2.get("code") == 200:
                        print(login_response2.get("data"))
                        print("\n420 扫码验证成功")
                    else:
                        print("\n420 扫码验证失败"+login_response2.get("msg"))
                        # 税务app登陆信息与当前纳税人不符，请您查看税务app信息或使用短信验证码登陆   
                        # 请在电子税务局app 右上角切换到对应的企业 再试
                            
                except TimeoutOccurred:
                    print("\n短信认证输入超时!")

        case 430:
            print("430 需要人脸认证")
        case 401:
            # 重新授权
            print(f"{invoice_response.get('code')}授权失败:{invoice_response.get('msg')}")
        case _:
            print(f"{invoice_response.get('code')}异常: {invoice_response.get('msg')}")

except Exception as e:
    # 打印完整堆栈信息（包含行号）
    traceback.print_exc()  # 新增堆栈跟踪

    # 添加上下文信息（可选）
    print(f"\n错误发生时参数状态：")
    print(f"当前时间戳: {int(time.time())}")


