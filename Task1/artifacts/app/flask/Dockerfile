FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN set -eux; \
    addgroup --system --gid 10001 app; \
    adduser  --system --uid 10001 --ingroup app --home /app --shell /usr/sbin/nologin app

COPY requirements.txt /app/requirements.txt

RUN set -eux; \
    python -m pip install --no-cache-dir --upgrade pip setuptools wheel; \
    python -m pip install --no-cache-dir -r /app/requirements.txt

COPY --chown=app:app main.py utils.py index.html /app/

USER app

EXPOSE 5005

CMD ["python", "main.py"]
