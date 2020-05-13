import time

from cloudwatch_metrics.units import COUNT, MICROSECONDS
from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder


METRICS_MAPPING = {
    '2': ['2xx', 'responses-2xx-quantity', 1, COUNT],
    '4': ['4xx', 'responses-4xx-quantity', 1, COUNT],
    '5': ['5xx', 'responses-5xx-quantity', 1, COUNT],
}

REQUEST_TIME_METRIC_NAME = 'request-time-handler'
REQUEST_TIME_MEASUREMENT = 'execution-time'


class CloudWatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        delta = (time.time() - start_time) * 1e6
        with CloudwatchMetricRecorder() as recorder:
            try:
                metric_config = METRICS_MAPPING[str(response.status_code)[0]]
                recorder.put_metric(*metric_config)
                recorder.put_metric(REQUEST_TIME_METRIC_NAME, REQUEST_TIME_MEASUREMENT, delta, MICROSECONDS)
            except KeyError:
                pass

        return response
