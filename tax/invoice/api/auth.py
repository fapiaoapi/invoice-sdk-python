class AuthAPI:
    """授权相关API"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def set_token(self, token):
        """
        手动设置授权token
        
        Args:
            token: 授权token字符串
            
        Returns:
            None
        """
        self.http_client.set_authorization(token)
    
    def get_authorization(self, nsrsbh,type="6"):
        """
        获取授权
        
        Args:
            nsrsbh: 纳税人识别号
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/authorization"
        data = {"nsrsbh": nsrsbh}
        if type == "5":
            data["type"] = type
        
        result = self.http_client.request("POST", path, data)
        
        # 如果成功获取token，设置到http_client中
        if result.get("code") == 200 and result.get("data", {}).get("token"):
            self.http_client.set_authorization(result["data"]["token"])
        
        return result
    
    def login_dppt(self, nsrsbh, username, password, sms=None, sf=None, ewmlx=None, ewmid=None):
        """
        登录数电发票平台
        
        Args:
            nsrsbh: 纳税人识别号
            username: 用户电票平台账号
            password: 用户电票平台密码
            sms: 验证码（可选）
            sf: 电子税务局身份（可选）
            ewmlx: 二维码类型（可选）
            ewmid: 二维码ID（可选）
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/loginDppt"
        data = {
            "nsrsbh": nsrsbh,
            "username": username,
            "password": password
        }
        
        # 添加可选参数
        if sms:
            data["sms"] = sms
        if sf:
            data["sf"] = sf
        if ewmlx:
            data["ewmlx"] = ewmlx
        if ewmid:
            data["ewmid"] = ewmid
        
        return self.http_client.request("POST", path, data)
    
    def query_face_auth_state(self, nsrsbh, username=None):
        """
        获取认证状态
        
        Args:
            nsrsbh: 纳税人识别号
            username: 用户电票平台账号（可选）
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/queryFaceAuthState"
        data = {"nsrsbh": nsrsbh}
        
        if username:
            data["username"] = username
        
        return self.http_client.request("POST", path, data)