from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
import pymongo
import json
import time
from app.database import get_db, DatabaseConnector
from app.models import DatabaseConnection, QueryHistory
from app.schemas import (
    QueryExecuteRequest,
    QueryExecuteResponse,
    QueryHistoryResponse,
    ExportRequest,
)
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/queries", tags=["queries"])


def execute_sql_query(connection_config: dict, query: str) -> tuple:
    """Execute SQL query and return results"""
    try:
        connection_string = DatabaseConnector.get_connection_string(connection_config)
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()
            data = [dict(row) for row in rows]
            
        return data, list(columns), None
    
    except Exception as e:
        return None, None, str(e)


def execute_mongodb_query(connection_config: dict, query: str) -> tuple:
    """Execute MongoDB query and return results"""
    try:
        client = pymongo.MongoClient(
            f"mongodb://{connection_config['host']}:{connection_config.get('port', 27017)}"
        )
        db = client[connection_config['database']]
        
        # Parse the query as JSON to get collection and operations
        query_obj = json.loads(query)
        collection_name = query_obj.get('collection')
        operation = query_obj.get('operation', 'find')
        
        if not collection_name:
            raise ValueError("Collection name required in query")
        
        collection = db[collection_name]
        
        if operation == 'find':
            filter_query = query_obj.get('filter', {})
            projection = query_obj.get('projection', None)
            results = list(collection.find(filter_query, projection))
        else:
            raise ValueError(f"Operation {operation} not supported")
        
        # Convert ObjectId to string for JSON serialization
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        
        columns = list(results[0].keys()) if results else []
        return results, columns, None
    
    except Exception as e:
        return None, None, str(e)


@router.post("/execute", response_model=QueryExecuteResponse)
def execute_query(
    request: QueryExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute a query on a database connection"""
    # Get the connection
    connection = db.query(DatabaseConnection).filter(
        DatabaseConnection.id == request.connection_id
    ).first()
    
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )
    
    # Prepare connection config
    connection_config = {
        "type": connection.type,
        "host": connection.host,
        "port": connection.port,
        "user": connection.user,
        "password": connection.password,
        "database": connection.database,
        "path": connection.path,
    }
    
    # Execute query
    start_time = time.time()
    
    if connection.type.lower() in ["postgresql", "mysql", "sqlite"]:
        data, columns, error = execute_sql_query(connection_config, request.query)
    elif connection.type.lower() == "mongodb":
        data, columns, error = execute_mongodb_query(connection_config, request.query)
    else:
        error = f"Unsupported database type: {connection.type}"
        data, columns = None, None
    
    execution_time = int((time.time() - start_time) * 1000)  # milliseconds
    
    # Save to history
    history_status = "error" if error else "success"
    query_history = QueryHistory(
        connection_id=request.connection_id,
        query=request.query,
        result=json.dumps(data) if data else None,
        execution_time=execution_time,
        status=history_status,
        error_message=error
    )
    db.add(query_history)
    db.commit()
    
    if error:
        return QueryExecuteResponse(
            success=False,
            error=error,
            execution_time=execution_time,
            row_count=0
        )
    
    return QueryExecuteResponse(
        success=True,
        data=data,
        columns=columns,
        row_count=len(data) if data else 0,
        execution_time=execution_time
    )


@router.get("/history", response_model=List[QueryHistoryResponse])
def get_query_history(
    connection_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get query history"""
    query = db.query(QueryHistory).order_by(QueryHistory.created_at.desc())
    
    if connection_id:
        query = query.filter(QueryHistory.connection_id == connection_id)
    
    history = query.limit(limit).all()
    return history


@router.delete("/history/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    """Delete a query history entry"""
    history = db.query(QueryHistory).filter(
        QueryHistory.id == history_id
    ).first()
    
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History entry not found"
        )
    
    db.delete(history)
    db.commit()
    return {"message": "History entry deleted"}


@router.post("/export")
def export_data(request: ExportRequest):
    """Export query results to JSON or CSV"""
    try:
        if request.format.lower() == "json":
            return {
                "format": "json",
                "data": json.dumps(request.data, indent=2),
                "filename": f"{request.filename}.json"
            }
        
        elif request.format.lower() == "csv":
            import csv
            from io import StringIO
            
            if not request.data:
                return {"error": "No data to export"}
            
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=request.data[0].keys())
            writer.writeheader()
            writer.writerows(request.data)
            
            return {
                "format": "csv",
                "data": output.getvalue(),
                "filename": f"{request.filename}.csv"
            }
        
        else:
            raise ValueError("Unsupported format")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
