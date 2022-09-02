# New_boy
*A sharing printer project*

## V1 （支付打印）
* Client-side: `Bootstrap`
    - index.html
    - pay.html
    - print.html
* Server-side: `Flask`
    - /index
    - /pay      *[WX-pay:Native]*
    - /print    *[HP_API]?*

## V2 （同时访问）
__?__：多并发，会话冲突     =>    `gunicorn` & `gevent` & `nginx`
__?__: session & cookies

## V3 （注册优惠）

### 目的：
> 1. 提高营业额
> 2. 采集数据
> 3. 激发高并发 

 __采集__：姓名；学号；学院
 __认证__：邮箱

* Client-side
    - +login.html
* Server-side
    - +SQLite
    - +email_API?