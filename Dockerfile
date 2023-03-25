FROM python:3.11.2

ENV LANG C.UTF-8
ENV TZ UTC
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/app:/app
ENV TERM xterm-256color

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    curl

RUN pip install --upgrade pip
RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH /root/.local/bin:$PATH

RUN poetry config virtualenvs.create false

ENV PYTHONPATH /app
ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/
RUN poetry install
RUN poe _bash_completion >> /root/.bashrc

COPY . /app

EXPOSE 8080

COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
CMD ["bin/entrypoint"]
