from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.models.purchase_request import RequestStatus, Department

class PurchaseRequestBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    department: Department
    requested_by: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=50)
    vendor: Optional[str] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    notes: Optional[str] = None

class PurchaseRequestCreate(PurchaseRequestBase):
    pass

class PurchaseRequestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    department: Optional[Department] = None
    requested_by: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    unit: Optional[str] = Field(None, min_length=1, max_length=50)
    vendor: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    notes: Optional[str] = None

class RequestApprove(BaseModel):
    notes: Optional[str] = None
    approved_by: str

class RequestReject(BaseModel):
    reason: str = Field(..., min_length=1)
    rejected_by: str

class RequestHistoryResponse(BaseModel):
    id: int
    request_id: int
    action: str
    status_from: Optional[RequestStatus]
    status_to: Optional[RequestStatus]
    notes: Optional[str]
    performed_by: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PurchaseRequestResponse(PurchaseRequestBase):
    id: int
    status: RequestStatus
    created_at: datetime
    updated_at: Optional[datetime]
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    history: List[RequestHistoryResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
