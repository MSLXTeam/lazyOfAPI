# lazyOfAPI

> 一个简单的用于请求OpenFrp API的库
> 
> 隧道信息相关参数名称及内容类型请参阅[OpenFrp的官方文档](https://github.com/ZGIT-Network/OPENFRP-APIDOC?tab=readme-ov-file#openfrp-openapi-%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97)
> 
> 本文档遵循CC BY-NC-SA许可.

## 文档约定

### 返回值类型

```DynamicClass``` 代表一个动态类对象，可以用 ```getattr()``` 获取其中内容

## 用户相关API

### 登录 ```bool```

#### 示例代码

```python
from lazyOfAPI.OpenFrpAPI import OpenFrpAPI
api = OpenFrpAPI()
api.login("test@test.com","test@test.com")
```

#### 返回值释义

返回一个布尔值,指示是否登陆成功.建议在程序中添加相关判断,只有返回 ```True``` 后才能进行下一步操作.

### 获取用户信息 ```str```

> 建议与上文的登录API配合使用以在登陆后显示当前用户信息.

#### 示例代码

```python
from lazyOfAPI.OpenFrpAPI import OpenFrpAPI
api = OpenFrpAPI()
api.get_user_info()
```

#### 返回值释义

返回一个字符串,内容为已经经过处理的用户信息,软件可以直接读取并显示.

### 签到 ```str```

> 不要设计任何自动签到的功能,例如登陆后自动发送签到请求,此类行为是违反OpenFrpAPI使用条款的.

#### 示例代码

```python
from lazyOfAPI.OpenFrpAPI import OpenFrpAPI
api = OpenFrpAPI()
api.sign()
```

#### 返回值释义

签到失败时的返回值固定为```签到失败````.建议程序显示时如果不是失败的返回内容,直接显示返回的内容即可.

## 隧道相关API

### 创建隧道 ```Dict[str,str]```

#### 示例代码

```python
from lazyOfAPI.OpenFrpAPI import OpenFrpAPI, ProxyTypes
api = OpenFrpAPI()
api.create_proxy(
    node_id="1", # 节点id
    name="test",
    protocol_type=ProxyTypes.tcp, # 隧道类型,推荐使用ProxyTypes中的枚举值
    local_addr="127.0.0.1",
    local_port=25565,
    remote_port=1000000 # 使用随机远程端口
    # 其他参数
)
```

> 你也可以使用new_proxy方法,参数与本方法相同.但是由于new_proxy方法只会返回一个代表操作成功与否的布尔值,所以不推荐使用.

#### 返回值释义

返回字典的key为欲创建的隧道的名称,value为用户隧道id
需要注意的是,如果执行中出现了**任何Exception**,则key固定为failed,而value中会提供traceback文本.

### 删除隧道 ```bool```

#### 示例代码

```python
from lazyOfAPI.OpenFrpAPI import OpenFrpAPI
api = OpenFrpAPI()
api.remove_proxy(proxy_id="12345") # 隧道id
```

#### 返回值释义

返回一个布尔值,指示是否成功删除.建议在程序中添加相关判断,只有返回 ```True``` 后才能进行下一步操作.

### 编辑隧道 ```bool```

#### 示例代码

```python
from lazyOfAPI.OpenFrpAPI import OpenFrpAPI, ProxyTypes
api = OpenFrpAPI()
other_proxy_info = {}
api.edit_proxy(
    proxy_id="1", # 隧道id
    name="test",
    protocol_type=ProxyTypes.tcp, # 隧道类型,推荐使用ProxyTypes中的枚举值
    local_addr="127.0.0.1",
    local_port=25565,
    remote_port=1000000, # 使用随机远程端口
    **other_proxy_info
)
```

> 代码中other_proxy_info实际上是一个包含节点其他信息的字典,其会被直接解包到发送信息的json中,接受的内容详见[OpenFrp官方文档](https://github.com/ZGIT-Network/OPENFRP-APIDOC?tab=readme-ov-file#7-%E7%BC%96%E8%BE%91%E9%9A%A7%E9%81%93-header)



### 获取用户隧道 ```DynamicClass```

#### 示例代码

```python
from lazyOfAPI.OpenFrpAPI import OpenFrpAPI
api = OpenFrpAPI()
api.get_user_proxies()
```

#### 返回值释义

正常情况下,返回的DynamicClass中应该包含两项数据: ```total``` 和 ```list```.

```total``` 为用户隧道总数,```list```为用户隧道列表.

下面是list中每一项的一些常用键名/属性名:

| 键名(属性名)        | 释义              |
|----------------|-----------------|
| id             | 此隧道ID（数字）       |
| proxyName      | 隧道名称            |
| proxyType      | 隧道类型            |
| localIp        | 此隧道的本地IP地址      |
| localPort      | 此隧道的本地端口        |
| useCompression | 是否启用数据压缩        |
| remotePort     | 此隧道的远程端口        |
| sk             | 此隧道的访问密码        |
| status         | 状态(为false时无法启动) |
| online         | 在线状态            |
| connectAddress | 链接此隧道的域名/IP地址   |
