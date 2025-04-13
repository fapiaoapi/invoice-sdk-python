# 发票SDK

这是一个用于对接发票接口(数电发票)的java SDK，支持发票开具、红冲、查询等功能。
发票 Java SDK 电子发票/数电发票/全电发票/数电票/开票
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

# 初始化客户端
client = InvoiceClient(
app_key="YOUR_APP_KEY",
app_secret="YOUR_APP_SECRET",
base_url="https://api.fa-piao.com"
)

# 获取授权
result = client.auth.get_authorization(nsrsbh="915101820724315989")
print(result)

# 开具蓝票
invoice_data = {
"fplxdm": "81",
"kplx": "0",
"xhdwsbh": "915101820724315989",
"xhdwmc": "测试企业",
# ... 其他参数
}
result = client.invoice.issue_blue_invoice(**invoice_data)
print(result)

```