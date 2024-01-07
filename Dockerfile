FROM python:3.10

ARG PYPI_MIRROR="https://mirror.baidu.com/pypi/simple"

WORKDIR /root/paddleocr_api

EXPOSE 8866

COPY . .

RUN apt-get update && apt-get install libgl1-mesa-glx libgl1-mesa-dri libglapi-mesa libgl1-mesa-dev -y && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "app.py"]

