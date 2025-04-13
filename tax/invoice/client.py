from tax.invoice.utils.http import HttpClient
from tax.invoice.api.auth import AuthAPI
from tax.invoice.api.face import FaceAPI
from tax.invoice.api.invoice import InvoiceAPI

class InvoiceClient:
    """数电发票API客户端"""
    
    def __init__(self, app_key, app_secret, base_url="https://api.fa-piao.com", verify_ssl=False):
        """
        初始化客户端
        
        Args:
            app_key: API密钥
            app_secret: API密钥对应的秘钥
            base_url: API基础URL
            verify_ssl: 是否验证SSL证书
        """
        self.http_client = HttpClient(base_url, app_key, app_secret, verify_ssl)
        
        # 初始化各API模块
        self.auth = AuthAPI(self.http_client)
        self.face = FaceAPI(self.http_client)
        self.invoice = InvoiceAPI(self.http_client)