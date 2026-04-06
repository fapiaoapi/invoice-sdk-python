# 电子发票/数电发票 Python SDK | 开票、验真、红冲一站式集成

[![PyPI version](https://img.shields.io/pypi/v/tax-invoice.svg)](https://pypi.org/project/tax-invoice/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/fapiaoapi/invoice-sdk-python/blob/master/LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)

**发票 Python SDK** 专为电子发票、数电发票（全电发票）场景设计，支持**开票、红冲、版式文件下载**等核心功能，快速对接税务平台API。

**关键词**: 电子发票SDK,数电票Python,开票接口,发票api,发票开具,发票红冲,全电发票集成

---

## 📖 核心功能

### 基础认证
- ✅ **获取授权** - 快速接入税务平台身份认证
- ✅ **人脸二维码登录** - 支持数电发票平台扫码登录
- ✅ **认证状态查询** - 实时获取纳税人身份状态

### 发票开具
- 🟦 **数电蓝票开具** - 支持增值税普通/专用电子发票
- 📄 **版式文件下载** - 自动获取销项发票PDF/OFD/XML文件

### 发票红冲
- 🔍 **红冲前蓝票查询** - 精确检索待红冲的电子发票
- 🛑 **红字信息表申请** - 生成红冲凭证
- 🔄 **负数发票开具** - 自动化红冲流程

---

## 🚀 快速安装

```bash
pip install tax-invoice
```

[📦 查看pypi地址](https://pypi.org/project/tax-invoice/ "发票sdk")

---



[📚 查看完整中文文档](https://fa-piao.com/doc.html?source=github) | [💡 更多示例代码](https://github.com/fapiaoapi/invoice-sdk-python/tree/master/examples)

---

## 🔍 为什么选择此SDK？
- **精准覆盖中国数电发票标准** - 严格遵循国家最新接口规范
- **开箱即用** - 无需处理XML/签名等底层细节，专注业务逻辑
- **企业级验证** - 已在生产环境处理超100万张电子发票

---

## 📊 支持的开票类型
| 发票类型       | 状态   |
|----------------|--------|
| 数电发票（普通发票） | ✅ 支持 |
| 数电发票（增值税专用发票） | ✅ 支持 |
| 数电发票（铁路电子客票）  | ✅ 支持 |
| 数电发票（航空运输电子客票行程单） | ✅ 支持  |
| 数电票（二手车销售统一发票） | ✅ 支持  |
| 数电纸质发票（增值税专用发票） | ✅ 支持  |
| 数电纸质发票（普通发票） | ✅ 支持  |
| 数电纸质发票（机动车发票） | ✅ 支持  |
| 数电纸质发票（二手车发票） | ✅ 支持  |

---

## 🤝 贡献与支持
- 提交Issue: [问题反馈](https://github.com/fapiaoapi/invoice-sdk-python/issues)
- 商务合作: yuejianghe@qq.com
```bash

from tax.invoice import InvoiceClient
import time
import traceback  # 新增导入
import json
import redis

import qrcode
import io
import base64
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
xhdwdzdh = "重庆市渝北区龙溪街道丽园路2号XXXX 1325580XXXX" # 地址和电话 空格隔开
xhdwyhzh = "工商银行XXXX 15451211XXXX"  #开户行和银行账号 空格隔开



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

#字符串转二维码图片base64
def str_to_qr_base64(data: str) -> str:
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # 生成图像（PIL Image）
    img = qr.make_image(fill_color="black", back_color="white")

    # 将图像保存到内存中的字节流
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    # 获取 Base64 编码
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_base64


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

def blue_invoice():
    # 开票税额计算demo
    # @link https://github.com/fapiaoapi/invoice-sdk-python/blob/master/examples/tax_example.py
    invoice_params = {
        "fpqqlsh": APP_KEY + str(int(time.time() * 1000)), # 建议用你的订单号
        "fplxdm": "82",
        "kplx": "0",
        "xhdwsbh": nsrsbh,
        "username": username,
        "xhdwmc": title,
        "xhdwdzdh": xhdwdzdh,
        "xhdwyhzh": xhdwyhzh,
        "ghdwmc": "个人",
        # "ghdwsbh": "91330100563015xxxx",
        "zsfs": "0",
        "bz": "",
        # 添加商品明细
        "fyxm": [
            {
                "fphxz": "0",
                "spmc": "*研发和技术服务*技术服务费",
                "je": 114.68,
                "sl": 0.01,
                "se": 1.14,
                "hsbz": 1,
                "spbm": "3040105000000000000"
            }
        ],
        
        # 合计金额
        "hjje": 113.54,
        "hjse": 1.14,
        "jshj": 114.68
    }

     # 数电蓝票开具接口 文档
     # @link https://fa-piao.com/doc.html#api6?source=github
    return client.invoice.blue_invoice(**invoice_params)
def get_pdf_ofd_xml(fphm):
    pdf_params = {
        "downflag": "4",
        "nsrsbh": nsrsbh,
        "username": username,
        "fphm": fphm
    }
    # 获取销项数电版式文件 文档 PDF/OFD/XML
    # @link https://fa-piao.com/doc.html#api7?source=github
    pdf_response = client.invoice.get_pdf_ofd_xml(**pdf_params)
    if pdf_response.get("code") == 200:
        print(pdf_response.get("data"))



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
    
    # 一 获取授权token  可从缓存redis中获取Token
    get_token()
    # 前端模拟数电发票/电子发票开具 (蓝字发票)
    # @link https://fa-piao.com/fapiao.html?source=github

    # 二 开具蓝票
    invoice_response = blue_invoice()
    match invoice_response.get("code"):
        case 200:
            print("获取pdf/ofd/xml")
            print(f"data: {invoice_response.get('data')}")       
            # 三 获取pdf/ofd/xml           
            get_pdf_ofd_xml(invoice_response.get('data', {}).get('Fphm'))
        case 420:
            print("登录(短信认证)")
            # 登录数电发票平台 短信
            # 前端模拟短信认证弹窗
            # @link https://fa-piao.com/fapiao.html?action=sms&source=github

            # 1 发短信验证码
            # @link https://fa-piao.com/doc.html#api2?source=github
            login_response = client.auth.login_dppt(nsrsbh=nsrsbh, username=username, password=password)
            if login_response.get("code") == 200:
                deadline = (datetime.now() + timedelta(seconds=300)).strftime("%Y-%m-%d %H:%M:%S")
                try:
                    # 设置 timeout=300 表示 300 秒
                    sms = inputimeout(prompt=f"请在300秒内({deadline}前)输入验证码: ", timeout=300)
                    print(f"\n你输入了: {sms}")
                    # 2 输入验证码
                    # @link https://fa-piao.com/doc.html#api2?source=github    
                    login_response2 = client.auth.login_dppt(nsrsbh=nsrsbh, username=username, password=password, sms=sms)
                    if login_response2.get("code") == 200:
                        print(login_response2.get("data"))
                        print("\n短信验证成功")
                        print("\n再次调用blue_invoice")
                        invoice_response = blue_invoice()
                        get_pdf_ofd_xml(invoice_response.get('data', {}).get('Fphm')  )
                except TimeoutOccurred:
                    print("\n短信认证输入超时!")         
        case 430:
            print("人脸认证")
            # 前端模拟人脸认证弹窗
            # @link https://fa-piao.com/fapiao.html?action=face&source=github

            # 1 获取人脸二维码
            # @link https://fa-piao.com/doc.html#api3?source=github
            qr_code_response = client.face.get_face_img(nsrsbh=nsrsbh, username=username, type="1")
 
            ewmly = qr_code_response.get("data", {}).get("ewmly")
            if ewmly == "swj":
                print("\n请使用电子税务局app扫码")
                print("\n成功做完人脸认证,请输入数字 1")  
                # ewm自己生成二维码 安装pip install qrcode[pil]
                if qr_code_response.get("data", {}).get("ewm") is not None and len(qr_code_response.get("data", {}).get("ewm")) < 500:
                    # ewm = qr_code_response.get("data", {}).get("ewm")
                    # qr_base64 = str_to_qr_base64(ewm)
                    # qr_code_response.get("data", {}).update({"ewm": qr_base64})
                    # print(qr_base64)
                    # 前端使用示例: base64Uri = 'data:image/png;base64,' + qr_base64
                    
                    print_qr_code(qr_code_response.get("data", {}).get("ewm"))
                    deadline = (datetime.now() + timedelta(seconds=300)).strftime("%Y-%m-%d %H:%M:%S")
                    try:
                    # 设置 timeout=300 表示 300 秒
                        input_num = inputimeout(prompt=f"请在300秒内({deadline}前)输入: ", timeout=300)
                        print(f"\n你输入了: {input_num}")
                        # 2 认证完成后 获取人脸二维码认证状态
                        # @link https://fa-piao.com/doc.html#api4?source=github
                        rzid = qr_code_response.get("data", {}).get("rzid")
                        face_status_response = client.face.get_face_state(nsrsbh=nsrsbh, rzid=rzid, username=username, type="1")
                        print("code: " + str(face_status_response.get("code")))
                        print("data: " + str(face_status_response.get("data")))                        
                        if face_status_response.get("data") is not None:
                            slzt = face_status_response.get("data", {}).get("slzt")
                            if slzt == "1":
                                print("\n人脸未认证")
                            elif slzt == "2":
                                print("\n人脸认证成功")
                                print("\n请再次调用blue_invoice")
                                invoice_response = blue_invoice()           
                                get_pdf_ofd_xml(invoice_response.get('data', {}).get('Fphm'))
                            elif slzt == "3":
                                print("\n人脸认证二维码过期-->重新获取人脸二维码")
                    except TimeoutOccurred:
                        print("\n人脸认证输入超时!")                    
            elif ewmly == "grsds":
                print("个人所得税app扫码")  # ewm是二维码的base64
        case 401:
            # 重新授权
            print(f"{invoice_response.get('code')}授权失败:{invoice_response.get('msg')}")
            print("重新授权 获取token 缓存到redis")
            get_token(True)
            invoice_response = blue_invoice()
            get_pdf_ofd_xml(invoice_response.get('data', {}).get('Fphm'))
        case _:
            print(f"{invoice_response.get('code')}异常: {invoice_response.get('msg')}")

except Exception as e:
    # 打印完整堆栈信息（包含行号）
    traceback.print_exc()  # 新增堆栈跟踪
    
    # 添加上下文信息（可选）
    print(f"\n错误发生时参数状态：")
    print(f"当前时间戳: {int(time.time())}")

```
[扫码登录demo](examples\face_login_example.py "扫码登录")
[发票红冲demo](examples\red_invoice_example.py "发票红冲")
[发票税额计算demo](examples\tax_example.py "发票税额计算")
