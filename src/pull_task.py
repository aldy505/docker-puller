import json
from os import path

from docker import DockerClient
from docker.errors import APIError, NotFound
from docker.types import LogConfig, Healthcheck

from containers_configuration import ContainerConfiguration
from pull_request import PullRequest


def pull_task(docker_client: DockerClient, configuration_path: str, request: PullRequest):
    try:
        f = open(path.join(configuration_path, "containers", request.container_name + ".json"), mode="r")
        configuration: ContainerConfiguration = json.load(f)

        try:
            docker_client.images.pull(repository=request.image_repository, tag=request.image_tag,
                                      all_tags=False)

            try:
                container_model = docker_client.containers.get(request.container_name)
                container_model.stop()
            except NotFound:
                # It's ok if the container was not found
                pass

            docker_client.containers.run(
                image=f"{request.image_repository}:{request.image_tag}",
                command=configuration["command"],
                detach=True,
                cap_add=configuration["cap_add"],
                cap_drop=configuration["cap_drop"],
                cpuset_cpus=configuration["cpu_cpus"],
                cpuset_mems=configuration["cpu_mem"],
                environment=configuration["environment"],
                healthcheck=Healthcheck(test=configuration["healthcheck"]["test"],
                                        interval=configuration["healthcheck"]["interval"],
                                        timeout=configuration["healthcheck"]["timeout"],
                                        retries=configuration["healthcheck"]["retries"],
                                        start_period=configuration["healthcheck"]["start_period"]),
                hostname=configuration["hostname"],
                labels=configuration["labels"],
                log_config=LogConfig(type=configuration["log_config"]["driver"],
                                     config=configuration["log_config"]["options"]),
                mem_limit=configuration["memory_limit"],
                mem_reservation=configuration["memory_reservation"],
                name=request.container_name,
                network=configuration["network"],
                ports={k: tuple(v) for k, v in configuration["ports"].items()},
                restart_policy={"Name": configuration["restart_policy"]["name"],
                                "MaximumRetryCount": configuration["restart_policy"]["maximum_retry_count"]},
                volumes=configuration["volumes"]
            )

            docker_client.containers.prune()
            docker_client.images.prune()
        except APIError as e:
            print("Failed during Docker API execution:")
            print(e)
        finally:
            f.close()
    except OSError as e:
        print("Failed during opening file:")
        print(e)
