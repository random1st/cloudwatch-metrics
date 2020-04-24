import datetime
import time
import boto3
import pytest
from botocore.stub import Stubber
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


class TestMiddleware:
    # def __init__(self):
    #     self.start_time = time.time()
    #     self.finish_time = time.time() + 200
    #     self.delta = (self.finish_time - self.start_time) * 1e6
    #     self.time_calls = 0
    start_time = 1587450924.562038
    finish_time = 1587451302.836959

    @fixture
    def init_env_variables(self, monkeypatch):
        monkeypatch.setenv('CLOUDWATCH__METRICS_NAMESPACE', 'test-namespace')
        monkeypatch.setenv('CLOUDWATCH__METRICS_ENABLE', 'True')
        monkeypatch.setenv('CLOUDWATCH__METRICS_BUFFER_SIZE', '2')
        monkeypatch.setenv('CLOUDWATCH__METRICS_FLUSH_TIMEOUT', '10')
        monkeypatch.setattr(time, 'time', lambda: 1587450924.562038)

    # def patch_client(self, *args, **kwargs):
    #     cl = boto3.client('cloudwatch')
    #     stubber = Stubber(cl)
    #     expected_params = {'Namespace': 'test-namespace',
    #                        'MetricData': [{'Dimensions': [{'Name': '2xx', 'Value': 'responses-2xx-quantity'}],
    #                                        'MetricName': '2xx',
    #                                        'Timestamp': datetime.datetime.fromtimestamp(self.__class__.start_time),
    #                                        'Unit': 'Count',
    #                                        'Value': 1},
    #                                       {'Dimensions': [{'Name': 'request-time-handler', 'Value': 'execution-time'}],
    #                                        'MetricName': 'request-time-handler',
    #                                        'Timestamp': datetime.datetime.fromtimestamp(self.__class__.finish_time),
    #                                        'Unit': 'Microseconds',
    #                                        'Value': 378274920.94039917}]}
    #     stubber.add_response('put_metric_data', {}, expected_params)
    #     stubber.activate()
    #     return cl

    def _mock_time(self):
        time_for_test = 0
        if self.time_calls == 0:
            time_for_test = self.__class__.start_time
        else:
            time_for_test = self.__class__.finish_time
        self.time_calls += 1
        return time_for_test

    # def _mock_client(self, recorder):
    #     recorder._CloudwatchMetricRecorder__buffer[0]['Timestamp'] = self.__class__.start_time
    #     recorder._CloudwatchMetricRecorder__buffer[1]['Timestamp'] = self.__class__.finish_time
    #     # monkeypatch.setattr(time, 'time', self._mock_time)
    #     return recorder

    def test_middleware(self, monkeypatch, init_env_variables):
        self.time_calls = 0
        from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
        from cloudwatch_metrics.metric_middleware import CloudWatchMiddleware
        from cloudwatch_metrics.config import Config
        monkeypatch.setattr(time, 'time', self._mock_time)

        # monkeypatch.setattr(CloudwatchMetricRecorder, 'client', property(self.patch_client))
        cl = boto3.client('cloudwatch')
        stubber = Stubber(cl)
        expected_params = {'Namespace': 'test-namespace',
                           'MetricData': [{'Dimensions': [{'Name': '2xx', 'Value': 'responses-2xx-quantity'}],
                                           'MetricName': '2xx',
                                           'Timestamp': datetime.datetime.fromtimestamp(self.__class__.start_time),
                                           'Unit': 'Count',
                                           'Value': 1},
                                          {'Dimensions': [{'Name': 'request-time-handler', 'Value': 'execution-time'}],
                                           'MetricName': 'request-time-handler',
                                           'Timestamp': datetime.datetime.fromtimestamp(self.__class__.finish_time),
                                           'Unit': 'Microseconds',
                                           'Value': 378274920.94039917}]}
        # stubber.add_response('put_metric_data', {}, expected_params)
        stubber.add_response('put_metric_data', {}, None)
        stubber.activate()
        monkeypatch.setattr(CloudwatchMetricRecorder, 'client', cl)
        request = MockHttpRequest()
        response = MockHttpResponse()
        middleware = CloudWatchMiddleware(lambda x: response)
        response = middleware.__call__(request)
        self.time_calls = 0
