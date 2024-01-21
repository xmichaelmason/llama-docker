Python, Flask, MariaDB, MongoDB, and Redis, dockerized.

Change your environment variables in .env, don't track changes to the file.

```sh
docker-compose up -d
docker-compose stop
```

After making changes to the flask app, rebuild the containers:
```sh
docker-compose up --build -d
```

Point web browser to http://localhost:5000

![Alt text](initial_run.png)