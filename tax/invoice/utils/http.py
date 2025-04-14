import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from tax.invoice.utils.signature import calculate_signature, generate_random_string, get_timestamp

# 禁用不安全请求警告
disable_warnings(InsecureRequestWarning)

class HttpClient:
    def __init__(self, base_url, app_key, app_secret, verify_ssl=False):
        self.base_url = base_url
        self.app_key = app_key
        self.app_secret = app_secret
        self.verify_ssl = verify_ssl
        self.authorization = None
    
    def set_authorization(self, token):
        """设置授权令牌"""
        self.authorization = token
    
    def _prepare_headers(self, method, path, random_string, timestamp, signature):
        """准备请求头"""
        headers = {
            'AppKey': self.app_key,
            'TimeStamp': timestamp,
            'RandomString': random_string,
            'Sign': signature
        }
        
        if self.authorization:
            headers['Authorization'] = self.authorization
            
        return headers
    
    
    
    def request(self, method, path, data=None, params=None, files=None):
        """发送HTTP请求"""
        # 准备签名参数
        random_string = generate_random_string(20)
        timestamp = get_timestamp()
        
        # 计算签名
        signature = calculate_signature(
            method,
            path,
            random_string,
            timestamp,
            self.app_key,
            self.app_secret
        )
        
        # 准备请求头
        headers = self._prepare_headers(method, path, random_string, timestamp, signature)
        
        # 构建完整URL
        url = f"{self.base_url}{path}"
        
        try:
            # 发送请求
            if method.upper() == 'GET':
                response = requests.get(
                    url=url,
                    params=data,
                    headers=headers,
                    verify=self.verify_ssl
                )
            else:  # POST
                # 创建multipart/form-data格式数据
                if data and not files:
                    files = {k: (None, str(v)) for k, v in data.items()}
                    data = None
                
                response = requests.post(
                    url=url,
                    data=data,
                    files=files,
                    headers=headers,
                    verify=self.verify_ssl
                )
            
            # 解析响应
            try:
                result = response.json()
            except ValueError:
                result = {"code": response.status_code, "msg": "非JSON响应", "data": response.text}
            
            return result
            
        except Exception as e:
            return {
                "code": 500,
                "msg": f"请求异常: {str(e)}",
                "data": None
            }