FROM python:3.12.5-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY setup.py .

COPY ./recycling_app ./recycling_app
COPY ./tests ./tests

RUN pip install .

RUN python -c "from torchvision import models; models.resnet101(weights=models.ResNet101_Weights.DEFAULT)"
RUN python -c "from torchvision import models; models.resnet152(weights=models.ResNet152_Weights.DEFAULT)"
RUN python -c "from torchvision import models; models.vgg19(weights=models.VGG19_Weights.DEFAULT)"

RUN pytest tests 

EXPOSE 8000

CMD ["uvicorn", "recycling_app.main:app", "--host", "0.0.0.0", "--port", "8000"]


