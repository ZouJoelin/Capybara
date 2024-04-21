
--------------------------------------
## 查询打印机状态 [GET]
```https://capybara.mynatapp.cc/api/status```
进入小程序以及每次更换打印机地点，查询打印机状态无异常。

#### 请求参数
无

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "backend_status"  | "ok" | √ |
|   | "door_open" | 打印机盖未闭合 |
|   | "out_of_paper" | 纸张不足 |
|   | "out_of_toner" | 墨粉不足 |
|   | "jam" | 纸张堵塞 |
|   | "offline" | 打印机未连接 |
|   | "unknown_error" | 未知错误 |

#### 错误码
无

##### 请求示例
* curl 
```curl --location 'https://capybara.mynatapp.cc/api/status'```
* postman
https://warped-spaceship-750669.postman.co/request/33534605-5a030443-3f46-435f-9c48-35d22db21ab2

##### 应答示例
```{"backend_status":"ok"}```

-------------------------------------------------
## 初始化当前会话 [GET]
```https://capybara.mynatapp.cc/```
确认打印机状态无误后，初始化当前会话。

#### 请求参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "code"  | str | wx.login()获取code后调用此接口并传入code，以便后端换取open_id |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "initialized"  | "ok" | √ |
| "error_message"  | "access_token failed!!!" | 授权失败，具体原因在reason字段 |
| "errcode"  |  | 错误码，据此可查微信开发文档 |
| "errmsg"  |  | 冗余信息，与errocde一致 |

#### 错误码
无

##### 请求示例
* curl 
```curl --location 'https://capybara.mynatapp.cc/'```
* postman
https://warped-spaceship-750669.postman.co/request/33534605-a01c68b7-847d-4dff-8827-e1ca748f689c

##### 应答示例
```{"initialized":"ok"}```

-------------------------------------------------
## 获取pdf页数 [POST]
```https://capybara.mynatapp.cc/api/auto_count/pages```
后台自动数pdf页数，并顺便保存文件到后台。

#### 请求参数
* Body (form-data)

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "file"  | file blob | |
| "fileName"  | str | |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "pages"  | int |  |
| "error_message"  | "请上传正确的pdf文件" |  |

#### 错误码
无

##### 请求示例
* postman
https://warped-spaceship-750669.postman.co/request/33534605-a01c68b7-847d-4dff-8827-e1ca748f689c

##### 应答示例
```{"pages":2}```

-------------------------------------------------
## 获取订单价格 [POST]
```https://capybara.mynatapp.cc/api/auto_count/fee```
后台自动计算价格

#### 请求参数
* Body (form-data)

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "pages"  | int | 必填 |
| "paper_type"  | str | 默认"A4" |
| "color"  | str | 默认"黑白" |
| "sides"  | str | "one-sided", "two-sided-long-edge", "two-sided-short-edge"  |
| "copies"  | int | 必填 |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "fee"  | int |  |
| "error_message"  | "请先上传文件" |  |
|   | "请输入正确的纸张类型" |  |
|   | "请输入正确的打印颜色" |  |
|   | "请选择正确的单双面选项" |  |
|   | "打印份数需为正整数" |  |

##### 请求示例
* postman
https://warped-spaceship-750669.postman.co/request/33534605-1605e60c-3237-4703-92e6-08f688d2db44

##### 应答示例
```{"fee":0.06}```

-------------------------------------------------
## 小程序下单 [GET]
```https://capybara.mynatapp.cc/api/pay```
小程序统一下单，移动端使用pay_jsapi()，返回wx.requestPayment()需要的参数；PC端使用pay_native()，返回支付二维码url。

#### 请求参数
无

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "out_trade_no"  | str | 每个订单在商户后端的唯一标识，例：20230527T1838XCF (2023.05.27 + 18:38 + 三个随机大写字母组合) |
| "jsapi_sign"  | json | wx.requestPayment()需要的所有参数字段：appId, timestamp, nonceStr, package, signType, paySign |
| "error_message"  | "下单失败" |  |

##### 请求示例
无


##### 应答示例
无

-------------------------------------------------
## 获取打印信息 [GET]
```https://capybara.mynatapp.cc/api/order```
#### 请求参数
无

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "file_name"  | str | 文件名 |
| "pages"  | int | 页数 |
| "paper_type"  | str | 默认“A4” |
| "color"  | str | 默认“黑白” |
| "sides"  | str | 单面、双面长边、双面短边 |
| "copies"  | int | 份数 |
| "price"  | str/int | 价格 |

##### 请求示例
无

##### 应答示例
无
...


















