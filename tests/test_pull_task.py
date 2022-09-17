import os
import unittest

import docker

from pull_request import PullRequest
from pull_task import pull_task


class TestSomething(unittest.TestCase):
    def test_hello_world(self):
        docker_client = docker.from_env()
        request = PullRequest(image_repository="debian",
                              image_tag="11",
                              image_digest="sha256:c0508353648d7db3c313661409ca41a2d12c63a4d06007387679161a8372329f",
                              container_name="hello-world")
        pull_task(docker_client, "../conf", request)
        docker_client.close()
