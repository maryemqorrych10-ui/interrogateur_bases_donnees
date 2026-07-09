from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime
import json

Base = declarative_base()


class DatabaseConnection(Base):
    __tablename__ = "database_connections"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    type = Column(String(50))  # postgresql, mysql, sqlite, mongodb
    host = Column(String(255), nullable=True)
    port = Column(Integer, nullable=True)
    user = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    database = Column(String(255), nullable=True)
    path = Column(String(255), nullable=True)  # For SQLite
    config = Column(Text)  # Store additional config as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class QueryHistory(Base):
    __tablename__ = "query_history"
    
    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, index=True)
    query = Column(Text)
    result = Column(Text)  # Store result as JSON
    execution_time = Column(Integer)  # in milliseconds
    status = Column(String(50))  # success, error
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
