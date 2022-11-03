FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /vk_bot
WORKDIR /vk_bot
COPY ./requirements.txt /vk_bot/
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 80
COPY . /vk_bot/
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone