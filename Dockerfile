FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

CMD sh -c "streamlit run frontend/home.py --server.address=0.0.0.0 --server.port=${PORT:-8501}"