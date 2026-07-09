from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime


# Database Connection Schemas
class DatabaseConnectionCreate(BaseModel):
    name: str
    type: str  # postgresql, mysql, sqlite, mongodb
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    path: Optional[str] = None


class DatabaseConnectionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    path: Optional[str] = None


class DatabaseConnectionResponse(BaseModel):
    id: int
    name: str
    type: str
    host: Optional[str]
    port: Optional[int]
    database: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Query Schemas
class QueryExecuteRequest(BaseModel):
    connection_id: int
    query: str


class QueryExecuteResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    columns: Optional[List[str]] = None
    row_count: int = 0
    execution_time: int  # milliseconds
    error: Optional[str] = None


class QueryHistoryResponse(BaseModel):
    id: int
    connection_id: int
    query: str
    status: str
    execution_time: int
    created_at: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


# Export Schemas
class ExportRequest(BaseModel):
    format: str  # json, csv
    data: List[Dict[str, Any]]
    filename: Optional[str] = "export"


# Health Check
class HealthResponse(BaseModel):
    status: str
    message: str
