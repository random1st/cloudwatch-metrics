from .conftest import MockClass
from .conftest import MockMetrics
from .conftest import MockAwsCredentials
import pytest
import aioboto3

class TestMetricRecorderAsync:

    @pytest.mark.asyncio
    async def test_put_metric(self, monkeypatch, mockConfig):
        from cloudwatch_metrics.metric_recorder_async import CloudwatchMetricRecorderAsync
        async with aioboto3.client(MockAwsCredentials.service, region_name=MockAwsCredentials.region, endpoint_url=MockAwsCredentials.endpoint_url) as mock_client:
          monkeypatch.setattr(CloudwatchMetricRecorderAsync, "client", mock_client)
          await CloudwatchMetricRecorderAsync(config=mockConfig).put_metric(MockMetrics.mock_put_metric_name, MockMetrics.mock_put_metric_d_value, MockMetrics.mock_put_metric_value, MockMetrics.mock_put_metric_unit)

        async with aioboto3.client(MockAwsCredentials.service, region_name=MockAwsCredentials.region, endpoint_url=MockAwsCredentials.endpoint_url) as mock_client:
          metrics = await mock_client.list_metrics()


        metric = metrics["Metrics"][0]
        assert metric["Namespace"] == mockConfig.namespace
        assert metric["MetricName"] == MockMetrics.mock_put_metric_name
        assert metric["Dimensions"][0]["Value"] == MockMetrics.mock_put_metric_d_value
        assert metric["Dimensions"][0]["Name"] == MockMetrics.mock_put_metric_name


    @pytest.mark.asyncio
    async def test_timeit(self, monkeypatch, mockConfig):
        from cloudwatch_metrics.metric_recorder_async import CloudwatchMetricRecorderAsync
        async with aioboto3.client(MockAwsCredentials.service, region_name=MockAwsCredentials.region, endpoint_url=MockAwsCredentials.endpoint_url) as mock_client:
          monkeypatch.setattr(CloudwatchMetricRecorderAsync, "client", mock_client)
          mock_class_first_iteration = await CloudwatchMetricRecorderAsync(config=mockConfig).timeit()
          mock_class_second_iteration = await mock_class_first_iteration(MockClass())
          mock_class_third_iteration = await mock_class_second_iteration(MockClass)

        async with aioboto3.client(MockAwsCredentials.service, region_name=MockAwsCredentials.region, endpoint_url=MockAwsCredentials.endpoint_url) as mock_client:
          metrics = await mock_client.list_metrics()
          metric = metrics["Metrics"][1]

          assert metric["Namespace"] == mockConfig.namespace
          assert metric["MetricName"] == MockClass().__name__
          assert metric["Dimensions"][0]["Name"] == MockClass().__name__
