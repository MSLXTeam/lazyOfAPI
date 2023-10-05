import random
import string
import traceback

import requests
from enum import Enum
from typing import Any, Dict, Optional, Union


class DynamicClass:
    def __init__(self, data: Dict[str, Any]) -> None:
        """初始化一个动态类，将字典的键值对转换为类的属性"""
        self.__dict__.update(data)


class ProxyTypes(Enum):
    """代理类型枚举"""
    tcp = "tcp"
    udp = "udp"
    http = "http"
    https = "https"
    stcp = "stcp"
    xtcp = "xtcp"


def generate_random_string(length=10) -> str:
    """生成一个指定长度的随机字符串。

    默认长度是10。字符串包括大写字母、小写字母和数字。

    参数:
        length (int): 随机字符串的长度。默认是10。

    返回:
        str: 生成的随机字符串。
    """
    characters = string.ascii_letters + string.digits  # 包括大写字母、小写字母和数字
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


class OpenFrpAPI:
    def __init__(self, base_url: str = "https://of-dev-api.bfsea.xyz") -> None:
        """初始化OpenFrpAPI类"""
        self.base_url = base_url
        self.headers: Dict[str, str] = {}
        self.session: str = ""
        self.info: str = ""
        self.proxy: Optional[Dict[str, str]] = None

    def login(self, username: str, password: str) -> bool:
        """用户登录"""
        url = self.base_url + "/user/login"
        data = {"username": username, "password": password}
        response = requests.post(url, data=data, proxies=self.proxy)
        result = response.json()
        if result["flag"]:
            self.headers['Authorization'] = response.headers['Authorization']
            self.session = result["data"]
            return True
        return False

    def get_user_info(self) -> str:
        """获取用户信息"""
        if (self.headers == {} or
                "Authorization" not in self.headers.keys() or
                self.headers.get("Authorization") == "" or
                self.session == ""):
            return ""
        url = self.base_url + "/frp/api/getUserInfo"
        response = requests.post(url, headers=self.headers, proxies=self.proxy)
        user_info = DynamicClass(response.json())
        self.info = f"""
            用户名: {getattr(user_info, "username", "获取失败")}
            用户注册ID: {getattr(user_info, "id", "获取失败")}
            用户注册邮箱: {getattr(user_info, "email", "获取失败")}
            是否已进行实名认证: {'已认证' if getattr(user_info, "realname", False) else '未认证'}
            注册时间: {getattr(user_info, "regtime", "获取失败")}
            用户组: {getattr(user_info, "friendlyGroup", "获取失败")}
            用户密钥: {getattr(user_info, "token", "获取失败")}
            上行带宽: {getattr(user_info, "outLimit", "获取失败")} Kbps
            下行带宽: {getattr(user_info, "inLimit", "获取失败")} Kbps
            剩余流量: {getattr(user_info, "traffic", "获取失败")} Mib
            已用隧道: {getattr(user_info, "used", "获取失败")} 条
            总共隧道条数: {getattr(user_info, "proxies", "获取失败")} 条
        """
        return self.info

    def get_user_proxies(self) -> DynamicClass:
        """获取用户隧道"""
        url = self.base_url + "/frp/api/getUserProxies"
        response = requests.post(url, headers=self.headers, proxies=self.proxy)
        return DynamicClass(getattr(DynamicClass(response.json()), "data"))

    def new_proxy(self, node_id: str, name: str = "", protocol_type: Union[str, ProxyTypes] = ProxyTypes.tcp,
                  local_addr: str = "127.0.0.1", local_port: int = "25565", remote_port: int = 1000000,
                  **kwargs: Any) -> bool:
        """创建新隧道"""
        url = self.base_url + "/frp/api/newProxy"
        proxy_type = protocol_type.value if isinstance(protocol_type, Enum) else protocol_type

        if remote_port >= 1000000:
            while True:
                remote_port = random.randint(10000, 90000)
                if remote_port != 25565:
                    break

        if name == "":
            name = "lazyOfAPI_"
            name += proxy_type
            name += generate_random_string()

        data = {
            "session": self.session,
            "name": name,
            "node_id": node_id,
            "type": proxy_type,
            "local_addr": local_addr,
            "local_port": local_port,
            "remote_port": remote_port,
            **kwargs
        }
        response = requests.post(url, data=data, headers=self.headers, proxies=self.proxy)
        return getattr(DynamicClass(response.json()), "flag", False)

    def create_proxy(self, node_id: str, name: str = "", protocol_type: Union[str, ProxyTypes] = ProxyTypes.tcp,
                     local_addr: str = "127.0.0.1", local_port: int = "25565", remote_port: int = 1000000,
                     **kwargs: Any) -> Dict[str, str]:
        try:
            self.new_proxy(node_id, name, protocol_type, local_addr, local_port, remote_port, **kwargs)
            usr_proxies = self.get_user_proxies()
            list_proxies = getattr(usr_proxies,"list")
            for item in list_proxies:
                if getattr(item, "proxyName") == name:
                    return {name: getattr(item, "id")}
        except Exception:
            return {"failed": traceback.format_exc()}

    def remove_proxy(self, proxy_id: str) -> bool:
        """删除隧道"""
        url = self.base_url + "/frp/api/removeProxy"
        data = {"session": self.session, "proxy_id": proxy_id}
        response = requests.post(url, data=data, headers=self.headers, proxies=self.proxy)
        return getattr(DynamicClass(response.json()),"flag")

    def get_node_list(self) -> DynamicClass:
        """获取节点列表"""
        url = self.base_url + "/frp/api/getNodeList"
        response = requests.get(url, headers=self.headers, proxies=self.proxy)
        return DynamicClass(getattr(DynamicClass(response.json()), "data"))

    def edit_proxy(self, proxy_id: str, **kwargs: Any) -> bool:
        """编辑代理"""
        url = self.base_url + "/frp/api/editProxy"
        data = {"session": self.session, "proxy_id": proxy_id, **kwargs}
        response = requests.post(url, data=data, headers=self.headers, proxies=self.proxy)
        return getattr(DynamicClass(response.json()), "flag")

    def sign(self) -> Union[str,bool]:
        """用户签到"""
        url = self.base_url + "/frp/api/userSign"
        response = requests.post(url, headers=self.headers, proxies=self.proxy)
        info = DynamicClass(response.json())
        if getattr(info, "flag", False):
            return getattr(info, "msg", "签到成功")
        else:
            return "签到失败"
