from pydantic import BaseModel


class RestartPolicyConfiguration(BaseModel):
    name: str
    maximum_retry_count: int


class HealthcheckConfiguration(BaseModel):
    test: str
    interval: str
    timeout: str
    retries: int
    start_period: str


class LogConfiguration(BaseModel):
    driver: str
    options: dict[str, str]


class ContainerConfiguration(BaseModel):
    hostname: str
    image: str
    command: str
    network: str
    ports: dict[str, list[str]]
    restart_policy: RestartPolicyConfiguration
    environment: dict[str, str]
    volumes: dict[str, str]
    healthcheck: HealthcheckConfiguration
    labels: dict[str, str]
    log_config: LogConfiguration
    cap_add: list[str]
    cap_drop: list[str]
    cpu_cpus: str
    cpu_mem: str
    memory_limit: str
    memory_reservation: str
