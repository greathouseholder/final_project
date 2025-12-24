from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    user_id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    telegram_id = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="user")
    is_paid = Column(Boolean, default=False)
    attempt_count = Column(Integer, default=0)


class CollectionModel(Base):
    __tablename__ = "collections"
    collection_id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    document_count = Column(Integer, default=0)
    owner_id = Column(SQLUUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DocumentModel(Base):
    __tablename__ = "documents"
    document_id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    collection_id = Column(SQLUUID(as_uuid=True), ForeignKey("collections.collection_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    path = Column(String)
    payload = Column(JSON, default=dict)