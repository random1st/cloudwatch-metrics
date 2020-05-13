import pytest
import aioboto3


class MockConfig:
    from cloudwatch_metrics.config import Config
    config = Config(namespace='test', buffer_size=1)

class MockClass():

    __name__ = "name"

    def __call__(self):
        'called'


class TestMetricRecorderAsync:

    region = "us-east-1"
    host = "127.0.0.1"
    port = "4582"
    endpoint_url = "http://127.0.0.1:4582"
    service = "cloudwatch"
    mock_put_metric_name = "Metric"
    mock_put_metric_value = 1.5
    mock_put_metric_unit = "Count"
    mock_put_metric_d_value = "1.5"

    @pytest.mark.asyncio
    async def test_put_metric(self, monkeypatch):
        from cloudwatch_metrics.metric_recorder_async import CloudwatchMetricRecorderAsync
        async with aioboto3.client(self.service, region_name=self.region, endpoint_url=self.endpoint_url) as mock_client:
          monkeypatch.setattr(CloudwatchMetricRecorderAsync, "client", mock_client)
          await CloudwatchMetricRecorderAsync(config=MockConfig().config).put_metric(self.mock_put_metric_name, self.mock_put_metric_d_value, self.mock_put_metric_value, self.mock_put_metric_unit)

        async with aioboto3.client(self.service, region_name=self.region, endpoint_url=self.endpoint_url) as mock_client:
          metrics = await mock_client.list_metrics()


        metric = metrics["Metrics"][0]
        assert metric["Namespace"] == MockConfig().config.namespace
        assert metric["MetricName"] == self.mock_put_metric_name
        assert metric["Dimensions"][0]["Value"] == self.mock_put_metric_d_value
        assert metric["Dimensions"][0]["Name"] == self.mock_put_metric_name


    @pytest.mark.asyncio
    async def test_timeit(self, monkeypatch):
        from cloudwatch_metrics.metric_recorder_async import CloudwatchMetricRecorderAsync
        async with aioboto3.client(self.service, region_name=self.region, endpoint_url=self.endpoint_url) as mock_client:
          monkeypatch.setattr(CloudwatchMetricRecorderAsync, "client", mock_client)
          mock_class_first_iteration = await CloudwatchMetricRecorderAsync(config=MockConfig().config).timeit()
          mock_class_second_iteration = await mock_class_first_iteration(MockClass())
          mock_class_third_iteration = await mock_class_second_iteration()

        async with aioboto3.client(self.service, region_name=self.region, endpoint_url=self.endpoint_url) as mock_client:
          metrics = await mock_client.list_metrics()
          metric = metrics["Metrics"][1]

          assert metric["Namespace"] == MockConfig.config.namespace
          assert metric["MetricName"] == MockClass().__name__
          assert metric["Dimensions"][0]["Name"] == MockClass().__name__
