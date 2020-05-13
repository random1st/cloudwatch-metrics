import asyncio
import os
import random

os.environ['CLOUDWATCH__METRICS_NAMESPACE'] = 'rv_test'

from cloudwatch_metrics import units
from cloudwatch_metrics.metric_recorder import CloudwatchMetricRecorder
from cloudwatch_metrics.metric_recorder_async import CloudwatchMetricRecorderAsync
#
# with CloudwatchMetricRecorder(profile='awem-dev') as rec:
#     for _ in range(1000):
#         rec.put_metric('test_metric','bullshit',random.randint(0,10000), units.COUNT)


async def main():
    async with  CloudwatchMetricRecorderAsync(profile='awem-dev') as rec:
        for _ in range(1000):
            await rec.put_metric('test_metric', 'bullshit', random.randint(0,10000), units.COUNT)


asyncio.run(main())