import boto3


class MockConfig:
    from cloudwatch_metrics.config import Config
    config = Config(namespace='test', buffer_size=1)

class MockClass:

    __name__ = "name"

    def __call__(self, test):
        print
        'called'

class TestMetricRecorder:

    region = "us-east-1"
    service = "cloudwatch"
    mock_put_metric_name = "Metric"
    mock_put_metric_value = 1.5
    mock_put_metric_unit = "Count"
    mock_put_metric_d_value = "1.5"
    endpoint_url = "http://127.0.0.1:4582"
    service = "cloudwatch"


    def test_put_metric(self, monkeypatch):
        from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
        mock_client = boto3.client(self.service, region_name=self.region, endpoint_url=self.endpoint_url)
        monkeypatch.setattr(CloudwatchMetricRecorder, "client", mock_client)
        CloudwatchMetricRecorder(config=MockConfig().config).put_metric(self.mock_put_metric_name, self.mock_put_metric_d_value, self.mock_put_metric_value, self.mock_put_metric_unit)

        metrics = mock_client.list_metrics()["Metrics"]
        metric = metrics[0]
        assert metric["Namespace"] == MockConfig.config.namespace
        assert metric["MetricName"] == self.mock_put_metric_name
        assert metric["Dimensions"][0]["Value"] == self.mock_put_metric_d_value
        assert metric["Dimensions"][0]["Name"] == self.mock_put_metric_name

    def test_timeit(self, monkeypatch):
        from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
        mock_client = boto3.client(self.service, region_name=self.region, endpoint_url=self.endpoint_url)
        monkeypatch.setattr(CloudwatchMetricRecorder, "client", mock_client)
        CloudwatchMetricRecorder(config=MockConfig().config).timeit(MockClass())(MockClass())(MockClass())

        metrics = mock_client.list_metrics()["Metrics"]
        metric = metrics[1]
        assert metric["Namespace"] == MockConfig.config.namespace
        assert metric["MetricName"] == MockClass().__name__
        assert metric["Dimensions"][0]["Name"] == MockClass().__name__


