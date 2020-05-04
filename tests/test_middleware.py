import time
from pytest import fixture


class MockHttpRequest:
    _encoding = None
    _upload_handlers = []

    def __init__(self):
        self.GET = {}
        self.POST = {}
        self.COOKIES = {}
        self.META = {}
        self.FILES = {}
        self.path = ''
        self.path_info = ''
        self.method = None
        self.resolver_match = None
        self.content_type = None
        self.content_params = None


class MockHttpResponse:
    status_code = 200

    def __init__(self):
        pass


class MockHttpResponse4xx(MockHttpResponse):
    status_code = 400


class MockHttpResponse5xx(MockHttpResponse):
    status_code = 500


class TestMiddleware:

    start_time = 1587450924.562038
    finish_time = 1587451302.836959
    put_metrics_calls = 0
    time_call_counts = 0

    def put_metric_2xx_handler(self, *args):
        if self.put_metrics_calls != 1:
            assert args == ('2xx', 'responses-2xx-quantity', 1, 'Count')
        else:
            assert args == ('request-time-handler', 'execution-time', (self.finish_time - self.start_time) * 1e6,
                            'Microseconds')
        self.put_metrics_calls += 1
        return None

    def put_metric_4xx_handler(self, *args):
        if self.put_metrics_calls != 1:
            assert args == ('4xx', 'responses-4xx-quantity', 1, 'Count')
        else:
            assert args == ('request-time-handler', 'execution-time', (self.finish_time - self.start_time) * 1e6,
                            'Microseconds')
        self.put_metrics_calls += 1
        return None

    def put_metric_5xx_handler(self, *args):
        if self.put_metrics_calls != 1:
            assert args == ('5xx', 'responses-5xx-quantity', 1, 'Count')
        else:
            assert args == ('request-time-handler', 'execution-time', (self.finish_time - self.start_time) * 1e6,
                            'Microseconds')
        self.put_metrics_calls += 1
        return None

    def _mock_time(self):
        if self.time_call_counts == 0:
            mock_time = self.start_time
        else:
            mock_time = self.finish_time
        self.time_call_counts += 1
        return mock_time

    @fixture
    def init_env_variables(self, monkeypatch):
        monkeypatch.setenv('CLOUDWATCH__METRICS_NAMESPACE', 'test-namespace')
        monkeypatch.setenv('CLOUDWATCH__METRICS_ENABLE', 'True')
        monkeypatch.setenv('CLOUDWATCH__METRICS_BUFFER_SIZE', '2')
        monkeypatch.setenv('CLOUDWATCH__METRICS_FLUSH_TIMEOUT', '10')
        monkeypatch.setattr(time, 'time', lambda: 1587450924.562038)

    @fixture
    def time_patching(self, monkeypatch):
        monkeypatch.setattr(time, 'time', self._mock_time)

    def test_middleware_2xx_response(self, monkeypatch, init_env_variables, time_patching):
        from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
        from cloudwatch_metrics.metric_middleware import CloudWatchMiddleware

        self.time_call_counts = 0
        monkeypatch.setattr(CloudwatchMetricRecorder, 'put_metric', self.put_metric_2xx_handler)
        request = MockHttpRequest()
        response = MockHttpResponse()
        middleware = CloudWatchMiddleware(lambda x: response)
        mw_response = middleware.__call__(request)

        assert response == mw_response
        assert response.status_code == mw_response.status_code
        self.put_metrics_calls = 0

    def test_middleware_4xx_response(self, monkeypatch, init_env_variables, time_patching):
        from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
        from cloudwatch_metrics.metric_middleware import CloudWatchMiddleware

        self.time_call_counts = 0
        monkeypatch.setattr(CloudwatchMetricRecorder, 'put_metric', self.put_metric_4xx_handler)
        request = MockHttpRequest()
        response = MockHttpResponse4xx()
        middleware = CloudWatchMiddleware(lambda x: response)
        mw_response = middleware.__call__(request)

        assert response == mw_response
        assert response.status_code == mw_response.status_code
        self.put_metrics_calls = 0

    def test_middleware_5xx_response(self, monkeypatch, init_env_variables, time_patching):
        from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
        from cloudwatch_metrics.metric_middleware import CloudWatchMiddleware

        self.time_call_counts = 0
        monkeypatch.setattr(CloudwatchMetricRecorder, 'put_metric', self.put_metric_5xx_handler)
        request = MockHttpRequest()
        response = MockHttpResponse5xx()
        middleware = CloudWatchMiddleware(lambda x: response)
        mw_response = middleware.__call__(request)

        assert response == mw_response
        assert response.status_code == mw_response.status_code
        self.put_metrics_calls = 0
