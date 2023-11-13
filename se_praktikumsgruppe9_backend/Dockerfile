FROM python:3.10-buster

WORKDIR /app

COPY . .
ENV PYTHONUNBUFFERED=1
# copy source and install dependencies
#RUN pip install --upgrade pip
RUN pip install -r src/requirements.txt
RUN python src/manage.py makemigrations
RUN python src/manage.py migrate
#RUN python src/manage.py test src/. --verbosity=2
# start server
EXPOSE 8000

# 127.0.0.1:8000
CMD ["python","src/manage.py","runserver","0.0.0.0:8000"]

# docker image ls
# docker run -p 8000:8000 f3f
# docker save -o backend_img.tar f3f754fe1b1b

# docker image tag trtest marwer/se_backend9:latest
# docker image push marwer/se_backend9:latest