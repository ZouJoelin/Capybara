
--------------------------------------
## 查询后台状态 [GET]
```https://capybara.mynatapp.cc/api/status```
进入小程序以及每次更换打印机地点，查询服务器及打印机状态无异常。

有以下几种异常情况：
1. 服务器掉线：404，"Tunnel capybara.mynatapp.cc not found"
2. 应用框架异常：
    - 502，"{'error_message': 'A Server Error Occurred'}"
    - 404，"{'error_message': 'Not Found'}"
3. 打印机状态异常：503，"{'error_message': 'xxxxxxx'}"

#### 请求参数
无

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "backend_status"  | "ok" | 200 |

#### 错误码
* 404：服务器掉线
"Tunnel capybara.mynatapp.cc not found"

* 502: 应用框架异常
"{'error_message': 'A Server Error Occurred'}"

* 503：打印机状态异常 

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "error_message"  | "打印机盖未闭合" |  |
|   | "打印机纸张不足" |  |
|   | "打印机墨粉不足" |  |
|   | "打印机有纸张堵塞" |  |
|   | "打印机未连接" |  |
|   | "打印机发生未知错误" |  |

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
| "open_id"  |  |  |
| "notification"  | "新通知" | 默认None |

#### 错误码
* 401

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "error_message"  | "access_token failed" | 授权失败，具体原因在reason字段 |
| "reason"  |  | 错误原因 |
| "errcode"  |  | 错误码，据此可查微信开发文档 |

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
| "fileName"  | str | 安全处理过的文件名 |
| "pages"  | int |  |

#### 错误码
* 400

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "error_message"  | "请上传正确的pdf文件" |  |

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
| "coins"  | int | 默认 0 |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "fee"  | str |  |

#### 错误码
* 400

|  key   | value  | 说明 |
|  ----  | ----  | --- |
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
## 获取打印信息 [GET]
```https://capybara.mynatapp.cc/api/print_order_info```
#### 请求参数
无

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "filename"  | str | 文件名 |
| "pages"  | int | 页数 |
| "paper_type"  | str | 默认“A4” |
| "color"  | str | 默认“黑白” |
| "sides"  | str | 单面、双面长边、双面短边 |
| "copies"  | int | 份数 |
| "price"  | str | 价格 |

##### 请求示例
无

##### 应答示例
无


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

#### 错误码
* 500

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "error_message"  | "下单失败" |  |

##### 请求示例
无

##### 应答示例
无


-------------------------------------------------
## 轮询订单支付状态 [GET]
```https://capybara.mynatapp.cc/api/polling_query```
客户端进入支付界面后，轮询该接口，获取当前订单支付状态。如果支付成功，跳转打印页面并执行打印命令。

#### 请求参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "out_trade_no"  | str | 每个订单在商户后端的唯一标识，调用/api/pay/接口时获取，据此订单号查询 |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "message"  | "SUCCESS" | 支付成功 |
|   | "NOTPAY" | 暂未支付 |

#### 错误码
* 403

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "error_message"  | "订单不存在" | 非法的out_trade_no |
|   | "该订单已关闭， 请重新下单" | 使用已失效的out_trade_no |

##### 请求示例
1. https://capybara.mynatapp.cc/api/polling_query?out_trade_no=20240424T1528DAY
2. https://capybara.mynatapp.cc/api/polling_query?out_trade_no=20240424T1637RBW
3. https://capybara.mynatapp.cc/api/polling_query?out_trade_no=20240423T2243BNP
4. https://capybara.mynatapp.cc/api/polling_query?out_trade_no=20240428T1816AAA

##### 应答示例
1. {"message":"SUCCESS"}
2. {"message":"NOTPAY"}
3. {"error_message":	"该订单已关闭， 请重新下单"}
4. {"error_message":	"订单不存在"}


-------------------------------------------------
## 关闭订单 [GET]
```https://capybara.mynatapp.cc/api/close_print_order```
客户端在支付页面中点击“返回”按钮时，建议关闭当前订单号。

#### 请求参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "out_trade_no"  | str | 每个订单在商户后端的唯一标识，调用/api/pay/接口时获取 |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "message"  |  |  |
| "code"  | 204 | No Content |

##### 请求示例
https://capybara.mynatapp.cc/api/close_print_order?out_trade_no=20240423T2243BNP

##### 应答示例
{"code":204,"message":""}


-------------------------------------------------
## 执行打印命令 [GET]
```https://capybara.mynatapp.cc/api/print_file```
检查违规，并执行打印命令。

#### 请求参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "out_trade_no"  | str | 每个订单在商户后端的唯一标识，调用/api/pay/接口时获取。后端会打印数据库中该订单号所对应的文件 |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "message"  | "正在打印" |  |
| "filename"  | str | 前端用于渲染“打印中”提示信息 |

#### 错误码
* 403

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "error_message"  | "订单不存在" | 非法的out_trade_no |
|   | "订单未支付，请尝试刷新本页面" | 未支付订单。也可能是后台的问题，建议客户端先刷新试试 |
|   | "订单已关闭" | 使用的是关闭的订单号 |
|   | "订单号所对应文件已打印过" | 已打印 |
|   | "订单号与提交文件不符" |  |
|   | "打印失败" | 后台执行打印命令时出错 |

##### 请求示例
1. https://capybara.mynatapp.cc/api/print_file?out_trade_no=20240424T1637RBW
2. https://capybara.mynatapp.cc/api/print_file?out_trade_no=20240423T2243BNP
3. https://capybara.mynatapp.cc/api/print_file?out_trade_no=20240428T1816AAA

##### 应答示例
1. {"error_message":	"订单未支付，请尝试刷新本页面"}
2. {"error_message":	"订单已关闭"}
3. {"error_message":	"订单不存在"}


-------------------------------------------------
## 获取用户信息 [GET]
```https://capybara.mynatapp.cc/api/get_user_info```
用open_id换取数据库中用户个人信息。

#### 请求参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "open_id"  | str |  |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "nickname"  | str | 黄毛鸭头 |
| "student_name"  | str | 邹家林 |
| "student_id"  | str | 19333091 |
| "university_region_school"  | str | 中山大学-东校区-生命科学学院 |
| "dormitory"  | str | 慎思园六号 |
| "coins"  | int | 3 |

#### 错误码
* 403

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "error_message" | "open_id不匹配" | session["open_id"]与请求的open_id不符 |
|  | "用户不存在" | 跳转至 /complete_user_info 接口 |


##### 请求示例

##### 应答示例


-------------------------------------------------
## 完善用户信息 [POST]
```https://capybara.mynatapp.cc/api/complete_user_info```
完善数据库中open_id所指向的用户的个人信息。

#### 请求参数
* Body (form-data)

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "open_id"  | str |  |
| "nickname"  | str | 黄毛鸭头 |
| "student_name"  | str | 邹家林 |
| "student_id"  | str | 19333091 |
| "university"  | str | 中山大学 |
| "region"  | str | 东校区 |
| "school"  | str | 生命科学学院 |
| "dormitory"  | str | 慎思园六号 |

#### 应答参数
|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "message"  | "register completed" |  |

#### 错误码
* 400

|  key   | value  | 说明 |
|  ----  | ----  | --- |
| "error_message"  | "错误的用户信息" | 非法的字段，让用户重新填写 |

##### 请求示例

##### 应答示例















