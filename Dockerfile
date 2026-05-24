FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run","frontend/home.py","--server.address=0.0.0.0","--server.port=8501"]