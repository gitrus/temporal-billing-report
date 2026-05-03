from temporalio import activity

from src.temporal.names import ActivityName
from src.transport.activities import schema as schm


@activity.defn(name=ActivityName.fetch_invoice_data)
async def fetch_invoice_data(
    request: schm.FetchInvoiceDataRequest,
) -> schm.FetchInvoiceDataResponse:
    activity.logger.info("Fetching invoices for %d-%02d", request.year, request.month)
    # Replace with real API / DB call
    return schm.FetchInvoiceDataResponse(
        invoices=[
            schm.Invoice(id="inv-001", customer="Acme Corp", amount=1200.00),
            schm.Invoice(id="inv-002", customer="Globex", amount=850.50),
        ]
    )


@activity.defn(name=ActivityName.generate_report)
async def generate_report(
    request: schm.GenerateReportRequest,
) -> schm.GenerateReportResponse:
    total = sum(inv.amount for inv in request.invoices)
    lines = [f"  {inv.customer}: ${inv.amount:.2f}" for inv in request.invoices]
    content = "Billing Report\n" + "\n".join(lines) + f"\nTotal: ${total:.2f}"
    return schm.GenerateReportResponse(content=content)
