import pytest

@pytest.fixture("module")
def mockConfig():
    from cloudwatch_metrics.config import Config
    yield Config(namespace='test', buffer_size=1)

class MockMetrics():
    mock_put_metric_name = "Metric"
    mock_put_metric_value = 1.5
    mock_put_metric_unit = "Count"
    mock_put_metric_d_value = "1.5"

class MockAwsCredentials():
    region = "us-east-1"
    service = "cloudwatch"
    endpoint_url = "http://127.0.0.1:4582"
    service = "cloudwatch"


class MockClass():

    __name__ = "name"

    def __call__(self, test):
        print
        'called'
