class FaceAPI:
    """人脸认证相关API"""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    def get_face_img(self, nsrsbh, username=None, type=None):
        """
        获取人脸二维码
        
        Args:
            nsrsbh: 纳税人识别号
            username: 用户电票平台账号（可选）
            type: 类型（可选，值为2获取个人所得税二维码）
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/getFaceImg"
        data = {"nsrsbh": nsrsbh}
        
        if username:
            data["username"] = username
        if type:
            data["type"] = type
        
        return self.http_client.request("GET", path, data)
    
    def get_face_state(self, nsrsbh, rzid, username=None, type=None):
        """
        获取人脸二维码认证状态
        
        Args:
            nsrsbh: 纳税人识别号
            rzid: 认证id
            username: 用户电票平台账号（可选）
            type: 类型（可选，值为2查询个人所得税二维码认证状态）
            
        Returns:
            API响应结果
        """
        path = "/v5/enterprise/getFaceState"
        data = {
            "nsrsbh": nsrsbh,
            "rzid": rzid
        }
        
        if username:
            data["username"] = username
        if type:
            data["type"] = type
        
        return self.http_client.request("GET", path, data)