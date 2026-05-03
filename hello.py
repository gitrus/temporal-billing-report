import asyncio
import os
import uuid

import temporalio.client
from temporalio.contrib.pydantic import pydantic_data_converter

from src.domain import models as m
from src.domain.workflow.workflow import BillingReportWorkflow
from src.temporal.names import TASK_QUEUE

async def main() -> None:
    year, month = 2026, 5
    user_uid = os.environ.get("USER_UID", str(uuid.uuid4()))
    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    client = await temporalio.client.Client.connect(
        address, data_converter=pydantic_data_converter
    )
    report = await client.execute_workflow(
        BillingReportWorkflow.run,
        m.BillingReportWorkflowRequest(user_uid=user_uid, year=year, month=month),
        id=f"br-{user_uid}-{year}-{month:02d}",
        task_queue=TASK_QUEUE,
    )
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
