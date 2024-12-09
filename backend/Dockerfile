FROM python:3.12.5-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY setup.py .

COPY ./recycling_app ./recycling_app
COPY ./tests ./tests

RUN pip install .

RUN python -c "from torchvision import models; models.resnet101(weights=models.ResNet101_Weights.DEFAULT)"

EXPOSE 8000

CMD ["uvicorn", "recycling_app.main:app", "--host", "0.0.0.0", "--port", "8000"]


