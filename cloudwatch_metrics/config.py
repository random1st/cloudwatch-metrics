import os


class Config:
    def __init__(
            self,
            namespace: str = None,
            enabled: bool = True,
            buffer_size: int = 20,
            flush_timeout: int = 10,
    ):
        self.namespace = namespace or os.getenv("CLOUDWATCH__METRICS_NAMESPACE")
        self.enabled = enabled or os.getenv("CLOUDWATCH__METRICS_ENABLE")
        self.buffer_size = buffer_size or os.getenv("CLOUDWATCH__METRICS_BUFFER_SIZE")
        self.flush_timeout = flush_timeout or os.getenv("CLOUDWATCH__METRICS_FLUSH_TIMEOUT")
