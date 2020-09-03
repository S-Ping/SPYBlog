FROM python:3.7.6
MAINTAINER SPing
COPY ./spy_blog /home/spy_blog
WORKDIR /home/spy_blog
RUN apt-get install --no-install-recommends --no-install-suggests -y \
    default-libmysqlclient-dev \
    gcc \
    && pip install -r ./requirements.txt -i https://pypi.douban.com/simple/
CMD ["gunicorn", "-c", "gunicorn.conf",  "app:app"]