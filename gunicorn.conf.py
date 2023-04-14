import multiprocessing

bind = '0.0.0.0:8000'                             #绑定监听ip和端口号
workers = multiprocessing.cpu_count() * 2 + 1       #同时执行的进程数，推荐为当前CPU个数*2+1
worker_class = 'gevent'                               #sync, gevent,meinheld   #工作模式选择，默认为sync，这里设定为gevent异步

backlog = 2048                                        #等待服务客户的数量，最大为2048，即最大挂起的连接数
max_requests = 1000                                   #默认的最大客户端并发数量
daemon = False                                        #是否后台运行
reload = True                                         #当代码有修改时，自动重启workers。适用于开发环境。
loglevel = 'info'                                     # debug info warning error critical
accesslog = '-'                                       #设置访问日志
errorlog = '-'                                        #设置问题记录日志