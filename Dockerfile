FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --home-dir /home/appuser --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app

COPY --chown=appuser:appuser main.py /app/main.py
COPY --chown=appuser:appuser index.html /app/index.html
COPY --chown=appuser:appuser utils.py /app/utils.py

USER appuser

EXPOSE 5005

CMD ["python", "main.py"]
