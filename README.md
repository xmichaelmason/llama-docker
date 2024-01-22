llama-cpp-python, dockerized with cuda.

llama-docker
- cuda
- flask
- mariadb
- mongodb
- redis
- TODO: vectordb, llama-index, langchain, stable diffusion

Host system requires docker engine, nvidia drivers, nvidia-container-toolkit, nvidia-cuda-toolkit

- Docker: https://docs.docker.com/engine/install/
- nvidia container toolit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
- nvidia cuda toolkit: https://docs.nvidia.com/cuda/cuda-quick-start-guide/index.html

Change your environment variables in .env, don't track changes to the file. This is not production ready.

```sh
cd llama-docker
docker compose up -d # start the containers
docker compose stop # stop the containers
```

After making changes to the flask app, rebuild the containers:
```sh
docker compose up --build -d
```

### Flask server
- Point web browser to http://{ip address}:5000

![Alt text](initial_run.png)

### llama-cpp-python OpenAI compatible server

Accessible at http://{ip address}:5001

Configured with multi-model support: https://llama-cpp-python.readthedocs.io/en/latest/server/#configuration-and-multi-model-support

Your model folder is configured in the docker-compose.yml file. This is where your .gguf model files should be placed. Mine are located at "~/llm/models" and that folder is mounted to /models inside the container.

The internal port is 8080, we map it out to 5001 for external access.

```YAML
services:
  ...
  cuda:
    ...
    volumes:
      - ./cuda:/app
      - ~/llm/models:/models
```

API configuration is handled in llama_config.json. I strongly suggest you familiarize yourself with the llama-cpp-python documentation!

```sh
docker compose up -d

[+] Running 5/5
 ✔ Container llama-docker-mariadb-1  Started                                                                                                                         0.0s 
 ✔ Container llama-docker-mongo-1    Started                                                                                                                         0.0s 
 ✔ Container llama-docker-redis-1    Started                                                                                                                         0.0s 
 ✔ Container llama-docker-cuda-1     Started                                                                                                                         0.0s 
 ✔ Container llama-docker-web-1      Started       
```

```sh
docker ps

CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS          PORTS                                         NAMES
7f0dca11338b   llama-docker-web    "gunicorn -w 2 -b :5…"   24 minutes ago   Up 30 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp     llama-docker-web-1
5d17b2cce06f   llama-docker-cuda   "python3 -m llama_cp…"   24 minutes ago   Up 30 seconds   0.0.0.0:5001->8080/tcp, :::5001->8080/tcp     llama-docker-cuda-1
b5045b26e2ab   mongo               "docker-entrypoint.s…"   52 minutes ago   Up 31 seconds   0.0.0.0:5003->27017/tcp, :::5003->27017/tcp   llama-docker-mongo-1
c66526999ae7   redis               "docker-entrypoint.s…"   52 minutes ago   Up 31 seconds   0.0.0.0:5004->6379/tcp, :::5004->6379/tcp     llama-docker-redis-1
c90972615843   mariadb             "docker-entrypoint.s…"   52 minutes ago   Up 31 seconds   0.0.0.0:5002->3306/tcp, :::5002->3306/tcp     llama-docker-mariadb-1
```

```sh
docker logs <container id>

...
...
llama_new_context_with_model: n_ctx      = 2048
llama_new_context_with_model: freq_base  = 10000.0
llama_new_context_with_model: freq_scale = 1
llama_kv_cache_init:  CUDA_Host KV buffer size =  1120.00 MiB
llama_kv_cache_init:      CUDA0 KV buffer size =   480.00 MiB
llama_new_context_with_model: KV self size  = 1600.00 MiB, K (f16):  800.00 MiB, V (f16):  800.00 MiB
llama_new_context_with_model: graph splits (measure): 5
llama_new_context_with_model:      CUDA0 compute buffer size =   194.00 MiB
llama_new_context_with_model:  CUDA_Host compute buffer size =   194.00 MiB
AVX = 1 | AVX_VNNI = 0 | AVX2 = 1 | AVX512 = 1 | AVX512_VBMI = 1 | AVX512_VNNI = 1 | FMA = 1 | NEON = 0 | ARM_FMA = 0 | F16C = 1 | FP16_VA = 0 | WASM_SIMD = 0 | BLAS = 1 | SSE3 = 1 | SSSE3 = 1 | VSX = 0 | 
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```
