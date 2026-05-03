from pydantic import BaseModel


class Invoice(BaseModel):
    id: str
    customer: str
    amount: float


class FetchInvoiceDataRequest(BaseModel):
    year: int
    month: int


class FetchInvoiceDataResponse(BaseModel):
    invoices: list[Invoice]


class ValidateInvoicesRequest(BaseModel):
    invoices: list[Invoice]


class GenerateReportRequest(BaseModel):
    invoices: list[Invoice]


class GenerateReportResponse(BaseModel):
    content: str
