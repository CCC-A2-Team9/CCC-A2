# team:   group 9
# member:
# Zhaoxiang NING, 1261076, Luoyang, China
# Xinyi ZHOU, 1281911, Wuxi, China
# Haochu WANG, 1281962, Nantong, China
# Gengchang XU, 1214774, Zhuhai, China
# Shiming ZHENG, 1149897, Melbourne, Australia
FROM python:3.7-slim-buster
WORKDIR /code

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV HTTP_PROXY http://wwwproxy.unimelb.edu.au:8000/
ENV HTTPS_PROXY http://wwwproxy.unimelb.edu.au:8000/
ENV no_proxy localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.u nimelb.edu.au,.cloud.unimelb.edu.au

COPY requirements.txt requirements.txt
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install -r requirements.txt 
COPY . .
CMD python3 data_stream.py