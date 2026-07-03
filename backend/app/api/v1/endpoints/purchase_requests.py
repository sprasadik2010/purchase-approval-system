# backend/app/api/v1/endpoints/purchase_requests.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload  # Add this import
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.purchase_request import PurchaseRequest, RequestHistory, RequestStatus
from app.schemas.purchase_request import (
    PurchaseRequestCreate, PurchaseRequestUpdate, 
    PurchaseRequestResponse, RequestApprove, RequestReject,
    RequestHistoryResponse
)
from app.services.notification_service import NotificationService

router = APIRouter()

@router.post("/", response_model=PurchaseRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_request(
    request: PurchaseRequestCreate,
    db: AsyncSession = Depends(get_db)
):
    # Create new purchase request
    db_request = PurchaseRequest(**request.model_dump())
    db.add(db_request)
    await db.flush()
    
    # Create history entry
    history = RequestHistory(
        request_id=db_request.id,
        action="created",
        status_to=RequestStatus.PENDING,
        performed_by=request.requested_by,
        notes="Request created"
    )
    db.add(history)
    await db.commit()
    
    # Refresh with eager loading for history
    result = await db.execute(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == db_request.id)
        .options(selectinload(PurchaseRequest.history))
    )
    db_request = result.scalar_one()
    
    # Send notification to manager (don't let it fail the request)
    try:
        await NotificationService.send_notification(
            "new_request",
            f"New purchase request: {db_request.title}",
            db_request.id
        )
    except Exception as e:
        print(f"⚠️ Notification failed: {e}")
    
    return db_request

@router.get("/", response_model=List[PurchaseRequestResponse])
async def get_purchase_requests(
    status: Optional[RequestStatus] = None,
    department: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = select(PurchaseRequest)
    
    if status:
        query = query.where(PurchaseRequest.status == status)
    if department:
        query = query.where(PurchaseRequest.department == department)
    
    # Add eager loading for history
    query = query.options(selectinload(PurchaseRequest.history))
    query = query.order_by(desc(PurchaseRequest.created_at)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{request_id}", response_model=PurchaseRequestResponse)
async def get_purchase_request(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Eagerly load the history relationship
    result = await db.execute(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == request_id)
        .options(selectinload(PurchaseRequest.history))
    )
    request = result.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@router.put("/{request_id}", response_model=PurchaseRequestResponse)
async def update_purchase_request(
    request_id: int,
    request_update: PurchaseRequestUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == request_id)
        .options(selectinload(PurchaseRequest.history))
    )
    request = result.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != RequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending requests can be updated")
    
    update_data = request_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(request, field, value)
    
    # Add history entry
    history = RequestHistory(
        request_id=request.id,
        action="updated",
        status_to=request.status,
        performed_by=request.requested_by,
        notes="Request updated"
    )
    db.add(history)
    await db.commit()
    await db.refresh(request)
    
    # Refresh with eager loading
    result = await db.execute(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == request.id)
        .options(selectinload(PurchaseRequest.history))
    )
    request = result.scalar_one()
    
    return request

@router.post("/{request_id}/approve", response_model=PurchaseRequestResponse)
async def approve_request(
    request_id: int,
    approve_data: RequestApprove,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == request_id)
        .options(selectinload(PurchaseRequest.history))
    )
    request = result.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != RequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending requests can be approved")
    
    status_from = request.status
    request.status = RequestStatus.APPROVED
    request.approved_by = approve_data.approved_by
    request.approved_at = datetime.utcnow()
    if approve_data.notes:
        request.notes = approve_data.notes
    
    # Add history entry
    history = RequestHistory(
        request_id=request.id,
        action="approved",
        status_from=status_from,
        status_to=RequestStatus.APPROVED,
        notes=approve_data.notes,
        performed_by=approve_data.approved_by
    )
    db.add(history)
    await db.commit()
    await db.refresh(request)
    
    # Refresh with eager loading
    result = await db.execute(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == request.id)
        .options(selectinload(PurchaseRequest.history))
    )
    request = result.scalar_one()
    
    # Send notification (don't let it fail the request)
    try:
        await NotificationService.send_notification(
            "request_approved",
            f"Request approved: {request.title}",
            request.id
        )
    except Exception as e:
        print(f"⚠️ Notification failed: {e}")
    
    return request

@router.post("/{request_id}/reject", response_model=PurchaseRequestResponse)
async def reject_request(
    request_id: int,
    reject_data: RequestReject,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == request_id)
        .options(selectinload(PurchaseRequest.history))
    )
    request = result.scalar_one_or_none()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != RequestStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending requests can be rejected")
    
    status_from = request.status
    request.status = RequestStatus.REJECTED
    request.rejection_reason = reject_data.reason
    request.approved_by = reject_data.rejected_by
    
    # Add history entry
    history = RequestHistory(
        request_id=request.id,
        action="rejected",
        status_from=status_from,
        status_to=RequestStatus.REJECTED,
        notes=reject_data.reason,
        performed_by=reject_data.rejected_by
    )
    db.add(history)
    await db.commit()
    await db.refresh(request)
    
    # Refresh with eager loading
    result = await db.execute(
        select(PurchaseRequest)
        .where(PurchaseRequest.id == request.id)
        .options(selectinload(PurchaseRequest.history))
    )
    request = result.scalar_one()
    
    # Send notification (don't let it fail the request)
    try:
        await NotificationService.send_notification(
            "request_rejected",
            f"Request rejected: {request.title}",
            request.id
        )
    except Exception as e:
        print(f"⚠️ Notification failed: {e}")
    
    return request

@router.get("/{request_id}/history", response_model=List[RequestHistoryResponse])
async def get_request_history(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(RequestHistory)
        .where(RequestHistory.request_id == request_id)
        .order_by(desc(RequestHistory.created_at))
    )
    return result.scalars().all()