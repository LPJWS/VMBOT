FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /tg_bot
WORKDIR /tg_bot
COPY ./requirements.txt /tg_bot/
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 80
COPY . /tg_bot/
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone