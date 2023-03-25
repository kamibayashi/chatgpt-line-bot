#!/bin/bash

UVICORN_PORT=8080

if [ -n "$PORT" ]; then
  UVICORN_PORT=$PORT
fi

poe migrate

if [ "$BUILD_ENV" = "development" ]; then
  uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
else
  uvicorn app.main:app --host 0.0.0.0 --port $UVICORN_PORT --timeout-keep-alive 620
fi
