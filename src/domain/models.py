from pydantic import BaseModel


class BillingReportWorkflowRequest(BaseModel):
    year: int
    month: int
