FROM python:3.8

WORKDIR /root/new_boy
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY /web /root/new_boy/web
WORKDIR /root/new_boy/web

CMD flask run -h "0.0.0.0" -p 80 --debugger