from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from src.domain import models as m
    from src.temporal.names import ActivityName, WorkflowName
    from src.transport.activities import schema as am


@workflow.defn(name=WorkflowName.BillingReport)
class BillingReportWorkflow:
    @workflow.run
    async def run(self, request: m.BillingReportWorkflowRequest) -> str:
        invoices_resp: am.FetchInvoiceDataResponse = await workflow.execute_activity(
            ActivityName.fetch_invoice_data,
            am.FetchInvoiceDataRequest(year=request.year, month=request.month),
            result_type=am.FetchInvoiceDataResponse,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        report_resp: am.GenerateReportResponse = await workflow.execute_activity(
            ActivityName.generate_report,
            am.GenerateReportRequest(invoices=invoices_resp.invoices),
            result_type=am.GenerateReportResponse,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        workflow.logger.info("Report ready:\n%s", report_resp.content)
        return report_resp.content
