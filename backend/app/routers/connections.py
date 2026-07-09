from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, DatabaseConnector
from app.models import DatabaseConnection
from app.schemas import (
    DatabaseConnectionCreate,
    DatabaseConnectionResponse,
    DatabaseConnectionUpdate,
)
from typing import List

router = APIRouter(prefix="/api/connections", tags=["connections"])


@router.post("", response_model=DatabaseConnectionResponse)
def create_connection(
    connection: DatabaseConnectionCreate, db: Session = Depends(get_db)
):
    """Create a new database connection"""
    # Check if connection name already exists
    existing = db.query(DatabaseConnection).filter(
        DatabaseConnection.name == connection.name
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Connection name already exists"
        )
    
    db_connection = DatabaseConnection(
        name=connection.name,
        type=connection.type,
        host=connection.host,
        port=connection.port,
        user=connection.user,
        password=connection.password,
        database=connection.database,
        path=connection.path,
        config="{}"
    )
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


@router.get("", response_model=List[DatabaseConnectionResponse])
def list_connections(db: Session = Depends(get_db)):
    """List all database connections"""
    connections = db.query(DatabaseConnection).all()
    return connections


@router.get("/{connection_id}", response_model=DatabaseConnectionResponse)
def get_connection(connection_id: int, db: Session = Depends(get_db)):
    """Get a specific database connection"""
    connection = db.query(DatabaseConnection).filter(
        DatabaseConnection.id == connection_id
    ).first()
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )
    return connection


@router.put("/{connection_id}", response_model=DatabaseConnectionResponse)
def update_connection(
    connection_id: int,
    connection_update: DatabaseConnectionUpdate,
    db: Session = Depends(get_db)
):
    """Update a database connection"""
    connection = db.query(DatabaseConnection).filter(
        DatabaseConnection.id == connection_id
    ).first()
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )
    
    update_data = connection_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(connection, field, value)
    
    db.commit()
    db.refresh(connection)
    return connection


@router.delete("/{connection_id}")
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    """Delete a database connection"""
    connection = db.query(DatabaseConnection).filter(
        DatabaseConnection.id == connection_id
    ).first()
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )
    
    db.delete(connection)
    db.commit()
    return {"message": "Connection deleted successfully"}


@router.post("/{connection_id}/test")
def test_connection(connection_id: int, db: Session = Depends(get_db)):
    """Test a database connection"""
    connection = db.query(DatabaseConnection).filter(
        DatabaseConnection.id == connection_id
    ).first()
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )
    
    connection_config = {
        "type": connection.type,
        "host": connection.host,
        "port": connection.port,
        "user": connection.user,
        "password": connection.password,
        "database": connection.database,
        "path": connection.path,
    }
    
    result = DatabaseConnector.test_connection(connection_config)
    return result
