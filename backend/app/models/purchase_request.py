from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class Department(str, enum.Enum):
    PURCHASE = "purchase"
    ACCOUNT = "account"
    HR = "hr"

class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    department = Column(Enum(Department), nullable=False)
    requested_by = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String(50), nullable=False)
    vendor = Column(String(255), nullable=True)
    priority = Column(String(20), default="medium")
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_by = Column(String(100), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Relationships
    history = relationship("RequestHistory", back_populates="request", cascade="all, delete-orphan")

class RequestHistory(Base):
    __tablename__ = "request_history"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("purchase_requests.id"), nullable=False)
    action = Column(String(50), nullable=False)
    status_from = Column(Enum(RequestStatus), nullable=True)
    status_to = Column(Enum(RequestStatus), nullable=True)
    notes = Column(Text, nullable=True)
    performed_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    request = relationship("PurchaseRequest", back_populates="history")
