# 发票SDK

这是发票SDK，支持发票开具、红冲、查询等功能。
发票SDK python 电子发票/数电发票/全电发票/数电票/开票
基础

[中文文档](https://github.com/fapiaoapi/invoice "文档")

* 获取授权
* 登录数电发票平台
* 获取人脸二维码
* 获取人脸二维码认证状态
* 获取认证状态

发票开具

* 数电蓝票开具接口
* 获取销项数电版式文件

发票红冲

* 申请红字前查蓝票信息接口
* 申请红字信息表
* 开负数发票


## 安装
通过pypi安装:
[pypi地址](https://pypi.org/project/tax-invoice/ "发票sdk")

```bash
pip install tax-invoice
```
```bash
from tax.invoice import InvoiceClient
from tax.invoice.utils.other import calculate_tax
import time
import traceback  # 新增导入

# 配置信息
appKey = "YOUR_APP_KEY"""
appSecret = "YOUR_APP_SECRET"
nsrsbh = "91500112MADFAQ9xxx"  # 统一社会信用代码
title = "重庆悦江河科技有限公司"  # 名称（营业执照）
username = "1912284xxxx"  # 手机号码（电子税务局）
password = ""  # 个人用户密码（电子税务局）
sf = "01"  # 身份（电子税务局）
fphm = "24502000000045823936"
token = ""


# 初始化客户端
client = InvoiceClient(
    app_key=appKey,
    app_secret=appSecret,
    base_url="https://api.fa-piao.com"
)



try:
    # 获取授权
    if token :
        client.auth.set_token(token)
    else:
        auth_response = client.auth.get_authorization(nsrsbh=nsrsbh)
        if auth_response.get("code") == 200:
            print(f"授权成功，Token: {auth_response.get('data', {}).get('token')}")
            token = auth_response.get('data', {}).get('token')

    # 获取认证状态
    status_response = client.auth.query_face_auth_state(nsrsbh=nsrsbh, username=username)
    status_code = status_response.get("code")

    if status_code == 200:
        print("认证状态: 无需认证")
        
        # amount = 200
        # taxRate = 0.01
        # isIncludeTax = False # 是否含税
        # # 税额计算
        # se =  float(calculate_tax(amount,taxRate,isIncludeTax))  # 强制转换为浮点数
        # print("价税合计：" + str(amount))
        # print("税率：" + str(taxRate))
        # print("合计金额：" + str(amount - se))
        # print(("含税" if isIncludeTax else "不含税") + " 合计税额：" + str(se))

        # 开具蓝票示例
        invoice_params = {
            "fpqqlsh": appKey + str(int(time.time() * 1000)),
            "fplxdm": "82",
            "kplx": "0",
            "xhdwsbh": nsrsbh,
            "xhdwmc": title,
            "xhdwdzdh": "重庆市渝北区仙桃街道汇业街1号17-2 19122840xxxx",
            "xhdwyhzh": "中国工商银行 310008670920023xxxx",
            "ghdwmc": "个人",
            "zsfs": "0",
            
            # 添加商品明细
            "fyxm": [
                {
                    "fphxz": "0",
                    "spmc": "*信息技术服务*软件开发服务",
                    "je": "10",
                    "sl": "0.01",
                    "se": "0.1",
                    "hsbz": "1",
                    "spbm": "3040201010000000000"
                }
            ],
            
            # 合计金额
            "hjje": "9.9",
            "hjse": "0.1",
            "jshj": "10"
        }
        
        invoice_response = client.invoice.issue_blue_invoice(**invoice_params)
        print(f"{invoice_response.get('code')} 开票结果: {invoice_response.get('msg')}")
        
        if invoice_response.get("code") == 200:
            print(f"发票号码: {invoice_response.get('data', {}).get('Fphm')}")
            print(f"开票日期: {invoice_response.get('data', {}).get('Kprq')}")
            fphm = invoice_response.get('data', {}).get('Fphm')
            time.sleep(10)  # 等待10秒
        
        # 下载发票
        pdf_params = {
            "downflag": "4",
            "nsrsbh": nsrsbh,
            "username": username,
            "fphm": fphm
        }
        
        pdf_response = client.invoice.get_pdf_ofd_xml(**pdf_params)
        if pdf_response.get("code") == 200:
            print(pdf_response.get("data"))

    elif status_code == 420:
        print("登录(短信认证)")
        # 登录数电发票平台 短信
        
        # # 1 发短信验证码
        # sms_code = ""
        # login_response = client.auth.login_dppt(nsrsbh=nsrsbh, username=username, password=password, sms_code=None)
        # if login_response.get("code") == 200:
        #     print(login_response.get("msg"))
        #     print(f"请{username}接收验证码")
        #     time.sleep(60)  # 模拟等待60秒
        
        # # 2 输入验证码
        # print("请输入验证码")
        # sms_code = input("验证码: ")  # 这里可以根据实际情况获取验证码
        # login_response2 = client.auth.login_dppt(nsrsbh=nsrsbh, username=username, password=password, sms_code=sms_code)
        # if login_response2.get("code") == 200:
        #     print(login_response2.get("data"))
        #     print("验证成功")
    
    elif status_code == 430:
        print("人脸认证")
        # 1 获取人脸二维码
        qr_code_response = client.auth.get_face_img(nsrsbh=nsrsbh, username=username, type="1")
        print("二维码: " + str(qr_code_response.get("data")))
        
        ewmlyx = qr_code_response.get("data", {}).get("ewmlyx")
        if ewmlyx == "swj":
            print("请使用税务局app扫码")  # ewm自己生成二维码
        elif ewmlyx == "grsds":
            print("个人所得税app扫码")  # ewm是二维码的base64
        
        # 2 认证完成后 获取人脸二维码认证状态
        rzid = qr_code_response.get("data", {}).get("rzid")
        # rzid = "5c028e62f23e4b5ca57668bc74c0de98"
        face_status_response = client.auth.get_face_state(nsrsbh=nsrsbh, rzid=rzid, username=username, type="1")
        print("code: " + str(face_status_response.get("code")))
        print("data: " + str(face_status_response.get("data")))
        
        if face_status_response.get("data") is not None:
            slzt = face_status_response.get("data", {}).get("slzt")
            if slzt == "1":
                print("未认证")
            elif slzt == "2":
                print("成功")
            elif slzt == "3":
                print("二维码过期-->重新获取人脸二维码")
    
    elif status_code == 401:
        # 重新授权
        print(f"{status_response.get('code')}授权失败:{status_response.get('msg')}")
    
    else:
        print(f"{status_response.get('code')}  {status_response.get('msg')}")

except Exception as e:
    # 打印完整堆栈信息（包含行号）
    traceback.print_exc()  # 新增堆栈跟踪
    
    # 添加上下文信息（可选）
    print(f"\n错误发生时参数状态：")
    print(f"当前时间戳: {int(time.time())}")

```