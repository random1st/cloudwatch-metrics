import logging
import os
import time
from datetime import datetime
from functools import wraps

import aiobotocore

from cloudwatch_metrics import units
from cloudwatch_metrics.config import Config
from cloudwatch_metrics.utils import chunks

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class CloudwatchMetricRecorderAsync:
    default_limit = 20

    def __init__(
            self,
            config=Config(),
            session: aiobotocore.AioSession = None,
            profile: str = None,
            region: str = None,
            endpoint_url: str = None,
    ):

        self.config = config
        self.region = region
        self.endpoint_url = endpoint_url
        self.profile = profile

        self._session = session
        self._client = None

        self.__buffer = []
        self.__time = time.time()

    @property
    def session(self):
        if self._session is None:
            if self.profile:
                _LOGGER.debug("Load aiobotocore session from profile %s", self.profile)
                self._session = aiobotocore.AioSession(profile=self.profile)
            else:
                _LOGGER.debug("Load default aiobotocore  session")
                self._session = aiobotocore.get_session()
        return self._session

    @property
    def client(self, *args, **kwargs):
        _LOGGER.debug("Create CloudWatchClient")
        if self.endpoint_url:
            _LOGGER.debug("Use custom endpoint, %s", self.endpoint_url)
            kwargs.update(endpoint_url=self.endpoint_url)

        if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
            _LOGGER.debug("Received credentials from environment")
            kwargs.update({
                "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
                "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
                "region_name": os.getenv("AWS_DEFAULT_REGION", self.region),
            })
            if os.environ.get("AWS_SESSION_TOKEN"):
                kwargs["aws_session_token"] = os.environ.get("AWS_SESSION_TOKEN")

        self._client = self.session.create_client("cloudwatch", *args, **kwargs)
        return self._client

    async def put_metric(self, metric, measurement, value, unit, timestamp=None):
        if self.config.enabled:
            data = {
                "MetricName": metric,
                "Dimensions": [{"Name": metric, "Value": measurement}, ],
                "Value": value,
                "Unit": unit,
                "Timestamp": datetime.fromtimestamp(timestamp)
                if timestamp
                else datetime.utcnow(),
            }
            self.__buffer.append(data)
            current_time = time.time()
            if (
                    len(self.__buffer) >= self.config.buffer_size
                    or current_time - self.__time >= self.config.flush_timeout
            ):
                await self._emit()
                self.__time = current_time

    async def _emit(self):
        async with self.client as client:
            for chunk in chunks(self.__buffer, self.default_limit):
                await client.put_metric_data(
                    Namespace=self.config.namespace, MetricData=chunk
                )
        self.__buffer = []

    async def timeit(self, metric_name=None):
        async def wrapper(func):
            @wraps(func)
            async def wrapped(*f_args, **f_kwargs):
                start_time = time.time()
                result = func(*f_args, **f_kwargs)
                delta = (time.time() - start_time) * 1e6
                await self.put_metric(
                    metric_name or func.__name__,
                    "Time of execution",
                    delta,
                    units.MICROSECONDS,
                )
                return result

            return wrapped

        return wrapper

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._emit()


cloudwatch_metric_recorder = CloudwatchMetricRecorderAsync()
