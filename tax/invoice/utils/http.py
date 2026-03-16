import urllib3
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util.retry import Retry
from tax.invoice.utils.signature import calculate_signature, generate_random_string, get_timestamp
from urllib.parse import urlencode, parse_qs
import json

# 禁用不安全请求警告
disable_warnings(InsecureRequestWarning)

class HttpClient:
    def __init__(self, base_url, app_key, app_secret, verify_ssl=False, max_retries=3, timeout=30):
        self.base_url = base_url
        self.app_key = app_key
        self.app_secret = app_secret
        self.verify_ssl = verify_ssl
        self.authorization = None
        
        # 配置重试策略
        retry = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        
        # 初始化连接池
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED' if verify_ssl else 'CERT_NONE',
            maxsize=10,
            retries=retry,
            timeout=timeout
        )
    
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
    
    def _build_multipart_fields(self, data):
        fields = {}
        for key, value in data.items():
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        for sub_key, sub_value in item.items():
                            fields[f'{key}[{i}][{sub_key}]'] = str(sub_value)
                    else:
                        fields[f'{key}[{i}]'] = str(item)
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    fields[f'{key}[{sub_key}]'] = str(sub_value)
            else:
                fields[key] = str(value)
        return fields

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
            if method.upper() == 'GET':
                query_params = params if params is not None else data
                if query_params:
                    url = f"{url}?{urlencode(query_params)}"
                response = self.http.request('GET', url, headers=headers)
            else:  # POST
                if data:
                    fields = self._build_multipart_fields(data)
                    
                    response = self.http.request(
                        'POST',
                        url,
                        fields=fields,
                        headers=headers
                    )
                elif files:
                    # 处理文件上传
                    response = self.http.request(
                        'POST',
                        url,
                        fields=files,
                        headers=headers
                    )
                else:
                    # 无数据的POST请求
                    response = self.http.request('POST', url, headers=headers)
            
            # 解析响应
            try:
                result = json.loads(response.data.decode('utf-8'))
            except ValueError:
                result = {
                    "code": response.status,
                    "msg": "非JSON响应",
                    "data": response.data.decode('utf-8')
                }
            
            return result
            
        except Exception as e:
            return {
                "code": 500,
                "msg": f"请求异常: {str(e)}",
                "data": None
            }
