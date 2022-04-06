FROM python:3.8.13-alpine3.15

WORKDIR app

COPY . .

RUN pip install -r requirements.txt

ENV DISCORD_TOKEN ${DISCORD_TOKEN}
ENV DISCORD_GUILD ${DISCORD_GUILD}

CMD ["python3", "src"]