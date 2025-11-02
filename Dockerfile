FROM python:3.13-slim AS builder

RUN mkdir /app
WORKDIR /app

# Python optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt



FROM python:3.13-slim

RUN addgroup --system faedoguerra && adduser --system --group faedoguerra
RUN mkdir -p /app/staticfiles
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .
RUN chmod +x entrypoint.sh
RUN chown -R faedoguerra:faedoguerra /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER faedoguerra

ENTRYPOINT ["./entrypoint.sh"]
