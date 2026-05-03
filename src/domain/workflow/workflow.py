from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    import pydantic as _

    from src.domain import models as m
    from src.temporal.names import ActivityName, WorkflowName
    from src.transport.activities import schema as schm


@workflow.defn(name=WorkflowName.BillingReport)
class BillingReportWorkflow:
    @workflow.run
    async def run(self, request: m.BillingReportWorkflowRequest) -> str:
        invoices_resp: schm.FetchInvoiceDataResponse = await workflow.execute_activity(
            ActivityName.fetch_invoice_data,
            schm.FetchInvoiceDataRequest(year=request.year, month=request.month),
            result_type=schm.FetchInvoiceDataResponse,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        validated_resp: schm.FetchInvoiceDataResponse = await workflow.execute_activity(
            ActivityName.validate_invoices,
            schm.ValidateInvoicesRequest(invoices=invoices_resp.invoices),
            result_type=schm.FetchInvoiceDataResponse,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(
                maximum_attempts=5,
                initial_interval=timedelta(seconds=1),
                backoff_coefficient=1.0,
            ),
        )

        report_resp: schm.GenerateReportResponse = await workflow.execute_activity(
            ActivityName.generate_report,
            schm.GenerateReportRequest(invoices=validated_resp.invoices),
            result_type=schm.GenerateReportResponse,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        workflow.logger.info("Report ready:\n%s", report_resp.content)
        return report_resp.content
