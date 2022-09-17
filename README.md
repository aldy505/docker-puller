# Docker Puller

This repository is heavily inspired from [docker-puller](https://github.com/glowdigitalmedia/docker-puller)
and [an article that was using the repository](https://www.andreagrandi.it/2014/10/25/automatically-pull-updated-docker-images-and-restart-containers-with-docker-puller/)
to automatically pull a Docker image from some registry. I thought I'd do a rewrite of the API and write it
on a more efficient programming language. I was trying to learn Crystal, sadly official SDK for Docker Engine
API for Crystal was not available. The only available official SDK for it was for Go and Python. I'm a bit
bored of writing programs in Go now, so I guess I'd do Python this time.

**Fair warning:** Please do not join me to reinvent the wheel. Use existing automatic puller that you would usually
use if you are using Kubernetes or Docker Swarm.

## Deploy

Please go to the `conf/containers` directory, and put your Docker container services there.
The filename (example: `hello-world.json`) indicates your container name (in this case, it's `hello-world`).
Please do not omit any fields that exists on the container configuration file, but leave it as their empty state.

If you are building this from source, everything there will be copied to the Docker image.

I envision this application to run as a Docker container itself. It should be fine if you are not deploying it
as a Docker container.

```shell
docker build -t docker-puller:latest .

docker run -e DOCKER_HOST="/var/run/docker.sock" -e PORT=8000 \
  -e ENVIRONMENT=production -e TOKEN="your-token-here" \
  --health-cmd "curl -f -X GET --header 'token: your-token-here' http://localhost:8000/health" \
  --health-interval 15s --health-retries 5 --health-timeout 10s \
  -p 8000:8000 -v "/var/run/docker.sock:/var/run/docker.sock" -d \
  docker-puller:latest
```

If at some point I provided the pre-built Docker image, you can use it, and mount the container configuration
directory to `/app/conf/containers`.

## Contributing

Yes, please. I'm using PyCharm Professional to develop this one with the Python interpreter resides inside the
WSL (Windows Subsystem for Linux) host. There is no support other than virtualenv. 
We're all forced to use virtualenv.

## License

```text
Copyright 2022 Reinaldy Rafli <aldy505@proton.me>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

See [LICENSE](./LICENSE)