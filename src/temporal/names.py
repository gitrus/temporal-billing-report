from enum import StrEnum, auto

TASK_QUEUE = "billing-report"


class WorkflowName(StrEnum):
    BillingReport = auto()


class ActivityName(StrEnum):
    fetch_invoice_data = auto()
    validate_invoices = auto()
    generate_report = auto()
