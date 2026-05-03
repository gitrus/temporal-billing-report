import asyncio
import os

import temporalio.client
import temporalio.worker
from temporalio.contrib.pydantic import pydantic_data_converter

from src.domain.workflow.workflow import BillingReportWorkflow
from src.temporal.names import TASK_QUEUE
from src.transport.activities.activities import fetch_invoice_data, generate_report


async def run_worker(task_queue: str) -> None:
    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    client = await temporalio.client.Client.connect(
        address, data_converter=pydantic_data_converter
    )
    worker = temporalio.worker.Worker(
        client,
        task_queue=task_queue,
        workflows=[BillingReportWorkflow],
        activities=[fetch_invoice_data, generate_report],
    )
    print(f"Worker started on task queue '{task_queue}'")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(run_worker(TASK_QUEUE))
