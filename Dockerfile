# 基础镜像，采用开发时的python版本
FROM python:3.9
# 维护者信息，开发者邮箱
MAINTAINER liji200918@outlook.com
# 创造code文件夹
RUN mkdir /code
# 将当前目录上下文件（.）全部复制到code文件夹中，
ADD . /code
# 将code文件夹设置为工作文件夹
WORKDIR /code
# 安装运行环境
RUN pip install -r requirements.txt

# CMD ['python', './code/']



