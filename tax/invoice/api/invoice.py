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
    
    # 这里可以添加其他发票相关API，如查蓝票信息、申请红字信息表、开负数发票等