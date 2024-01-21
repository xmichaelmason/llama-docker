Change your environment variables in .env, don't track changes to the file.

```sh
docker-compose up -d
docker-compose stop
```

After making changes to the flask app, rebuild the containers:
```sh
docker-compose up --build -d
```
