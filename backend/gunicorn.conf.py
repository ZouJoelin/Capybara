###########################################################
# https://docs.gunicorn.org/en/stable/settings.html#config
###########################################################

# import multiprocessing


# basic
bind = '127.0.0.1:8000'                             #绑定监听ip和端口号
workers = 3 #multiprocessing.cpu_count() * 2 + 1       #同时执行的进程数，推荐为当前CPU个数*2+1
worker_class = 'gevent'                               #sync, gevent,meinheld   #工作模式选择，默认为sync，这里设定为gevent异步
worker_connections = 1000


# limit
backlog = 1024                                        #等待服务客户的数量，最大为2048，即最大挂起的连接数
max_requests = 0                                   #自动重启前最大http请求数量


# debug
daemon = False                                        #是否后台运行
reload = False                                         #当代码有修改时，自动重启workers。适用于开发环境。


#log
capture_output = True                                 # Redirect stdout/stderr to log file

pidfile = '../log/gunicorn.pid'

loglevel = 'info'                                     #errorlog level: debug info warning error critical
# errorlog = './log/gunicorn.error.log'                                        #设置问题记录日志

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = errorlog = '../log/gunicorn.log' #'-'                                       #设置访问日志


