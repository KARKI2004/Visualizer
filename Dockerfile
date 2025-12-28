FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHERUSAGESTATS=false \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "streamlit run app.py --server.port ${PORT:-8080} --server.address 0.0.0.0"]
