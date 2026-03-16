
from tax.invoice import InvoiceClient
import time
import traceback  

# 配置信息
APP_KEY = ''
APP_SECRET = ''

# 配置信息
nsrsbh = ""  # 统一社会信用代码
title = ""  # 名称（营业执照）
username = ""  # 手机号码（电子税务局）
password = ""  # 个人用户密码（电子税务局）
sf = "01"  # 身份（电子税务局）
fphm = "26112000001018143646"
token = ""

try:
    # 创建客户端
    client = InvoiceClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        base_url="https://api.fa-piao.com"
    )
    if token:
        client.auth.set_token(token)
    else:
        # 获取授权
        auth_response = client.auth.get_authorization(nsrsbh=nsrsbh)
        if auth_response['code'] == 200:
            print(f"授权成功，Token: {auth_response['data']['token']}")

    # 1. 数电申请红字前查蓝票信息接口
    SQYY = '2'
    query_invoice_response = client.invoice.ret_invice_msg(
        nsrsbh=nsrsbh,
        fphm=fphm,
        sqyy=SQYY,
        username=username,
        xhdwsbh=nsrsbh
    )

    if query_invoice_response['code'] == 200:
        print("1 可以申请红字")
        time.sleep(2)
        
        # 2. 申请红字信息表
        apply_red_params = {
            'xhdwsbh': nsrsbh,
            'yfphm': fphm,
            'username': username,
            'sqyy': '2',
            'chyydm': '01'
        }
        apply_red_response = client.invoice.apply_red_info(apply_red_params)

        if apply_red_response['code'] == 200:
            print("2 申请红字信息表")
            time.sleep(2)
            
            # 3. 开具红字发票
            red_invoice_params = {
                'fpqqlsh': f'red{fphm}',
                'username': username,
                'xhdwsbh': nsrsbh,
                'tzdbh': apply_red_response['data']['xxbbh'],
                'yfphm': fphm
            }
            red_invoice_response = client.invoice.red_ticket(red_invoice_params)

            if red_invoice_response['code'] == 200:
                print("3 负数开具成功")
            else:
                print(f"{red_invoice_response['code']} 数电票负数开具失败: {red_invoice_response['msg']}")
                print(red_invoice_response['data'])
        else:
            print(f"{apply_red_response['code']} 申请红字信息表失败: {apply_red_response['msg']}")
            print(apply_red_response['data'])
    else:
        print(f"{query_invoice_response['code']} 查询发票信息失败: {query_invoice_response['msg']}")
        print(query_invoice_response['data'])
except Exception as e:
    # 打印完整堆栈信息（包含行号）
    traceback.print_exc()  # 新增堆栈跟踪
    
    # 添加上下文信息（可选）
    print(f"\n错误发生时参数状态：")
    print(f"当前时间戳: {int(time.time())}")