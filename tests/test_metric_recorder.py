import boto3
from .conftest import MockClass
from .conftest import MockMetrics
from .conftest import MockAwsCredentials

class TestMetricRecorder:

    def test_put_metric(self, monkeypatch, mockConfig):
        from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
        mock_client = boto3.client(MockAwsCredentials.service, region_name=MockAwsCredentials.region, endpoint_url=MockAwsCredentials.endpoint_url)
        monkeypatch.setattr(CloudwatchMetricRecorder, "client", mock_client)
        CloudwatchMetricRecorder(config=mockConfig).put_metric(MockMetrics.mock_put_metric_name, MockMetrics.mock_put_metric_d_value, MockMetrics.mock_put_metric_value, MockMetrics.mock_put_metric_unit)

        metrics = mock_client.list_metrics()["Metrics"]
        metric = metrics[0]
        assert metric["Namespace"] == mockConfig.namespace
        assert metric["MetricName"] == MockMetrics.mock_put_metric_name
        assert metric["Dimensions"][0]["Value"] == MockMetrics.mock_put_metric_d_value
        assert metric["Dimensions"][0]["Name"] == MockMetrics.mock_put_metric_name

    def test_timeit(self, monkeypatch, mockConfig):
        from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
        mock_client = boto3.client(MockAwsCredentials.service, region_name=MockAwsCredentials.region, endpoint_url=MockAwsCredentials.endpoint_url)
        monkeypatch.setattr(CloudwatchMetricRecorder, "client", mock_client)
        CloudwatchMetricRecorder(config=mockConfig).timeit(MockClass())(MockClass())(MockClass())

        metrics = mock_client.list_metrics()["Metrics"]
        metric = metrics[1]
        assert metric["Namespace"] == mockConfig.namespace
        assert metric["MetricName"] == MockClass().__name__
        assert metric["Dimensions"][0]["Name"] == MockClass().__name__


