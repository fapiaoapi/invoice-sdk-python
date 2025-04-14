class InvoiceAPI:
    """发票相关API"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def issue_blue_invoice(self, **kwargs):
        """
        数电蓝票开具接口
        
        Args:
            **kwargs: 发票开具所需的所有参数
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/blueTicket"
        return self.http_client.request("POST", path, kwargs)
    
    def get_pdf_ofd_xml(self, nsrsbh, fphm, downflag, kprq=None, username=None, addSeal=None):
        """
        获取销项数电版式文件
        
        Args:
            nsrsbh: 纳税人识别号
            fphm: 发票号码
            downflag: 获取版式类型(1：PDF 2：OFD 3：XML 4：下载地址5：base64文件)
            kprq: 开票日期（可选，格式：yyyyMMddHHmmss）
            username: 用户电票平台账号（可选）
            addSeal: 是否添加签章（可选，1-添加，其余任意值-不添加）
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/pdfOfdXml"
        data = {
            "nsrsbh": nsrsbh,
            "fphm": fphm,
            "downflag": downflag
        }
        
        if kprq:
            data["kprq"] = kprq
        if username:
            data["username"] = username
        if addSeal:
            data["addSeal"] = addSeal
        
        return self.http_client.request("POST", path, data)
    
    def ret_invice_msg(self, nsrsbh, fphm, sqyy, username, xhdwsbh=None):
        """
        数电申请红字前查蓝票信息接口
        
        Args:
            nsrsbh: 纳税人识别号
            fphm: 发票号码
            sqyy: 申请原因代码（1-销货退回，2-开票有误，3-服务中止，4-发票作废，5-其他）
            username: 用户电票平台账号
            xhdwsbh: 销货单位识别号（可选）
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/retInviceMsg"
        data = {
            "nsrsbh": nsrsbh,
            "fphm": fphm,
            "sqyy": sqyy,
            "username": username
        }
        
        if xhdwsbh:
            data["xhdwsbh"] = xhdwsbh
        
        return self.http_client.request("POST", path, data)
    
    def apply_red_info(self, params):
        """
        申请红字信息表
        
        Args:
            params: 申请红字信息表所需的参数字典，包括：
                xhdwsbh: 销货单位识别号
                yfphm: 原发票号码
                username: 用户电票平台账号
                sqyy: 申请原因代码
                chyydm: 冲红原因代码
                其他可选参数
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/applyRedInfo"
        return self.http_client.request("POST", path, params)
    
    def red_ticket(self, params):
        """
        数电票负数开具
        
        Args:
            params: 开具红字发票所需的参数字典，包括：
                fpqqlsh: 发票请求流水号
                username: 用户电票平台账号
                xhdwsbh: 销货单位识别号
                tzdbh: 通知单编号（红字信息表编号）
                yfphm: 原发票号码
                其他可选参数
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/redTicket"
        return self.http_client.request("POST", path, params)
    
    