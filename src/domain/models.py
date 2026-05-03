from pydantic import BaseModel


class BillingReportWorkflowRequest(BaseModel):
    user_uid: str
    year: int
    month: int
