# ChatGpt Line Bot

Line chat bot on Cloud Run on GCP.

### Settings

- Register and set line message API.
    - https://developers.line.biz/ja/services/messaging-api/

- Create a cloud sql mysql instance and database.
  - You have to setup the appropriate settings to connect to cloud sql from cloud run.

```sql
CREATE DATABASE `chatgpt_line_bot_production` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE DATABASE `chatgpt_line_bot_development` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

CREATE USER 'chatgpt_line_bot' @'%' IDENTIFIED WITH mysql_native_password BY 'xxx';
CREATE USER 'chatgpt_line_bot' @'localhost' IDENTIFIED WITH mysql_native_password BY 'xxx';


GRANT ALL PRIVILEGES ON *.* TO 'chatgpt_line_bot' @'localhost';

FLUSH PRIVILEGES;
```

- Deploy to cloud run.
  - You have to set the appropriate GPC permissions to deploy to cloud run from the command.


```sh
gcloud builds submit --config cloudbuild.yaml --substitutions=_BUILD_ENV=production
```

- Set cloud run url to callback url on line message API.

### Migration

- You can migrate in docker container.

```sh
poe makemigrations
poe migrate
```

### Development

```
BUILD_ENV=development docker-compose build --no-cache
BUILD_ENV=development docker-compose up -d

curl http://localhost:8080/health
```
