from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import json

# SQLAlchemy database setup for internal app DB
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database connection manager for external databases
class DatabaseConnector:
    """Manages connections to external databases"""
    
    @staticmethod
    def get_connection_string(connection_config: dict) -> str:
        """Build connection string from config"""
        db_type = connection_config.get("type", "").lower()
        
        if db_type == "postgresql":
            return f"postgresql://{connection_config['user']}:{connection_config['password']}@{connection_config['host']}:{connection_config.get('port', 5432)}/{connection_config['database']}"
        
        elif db_type == "mysql":
            return f"mysql+pymysql://{connection_config['user']}:{connection_config['password']}@{connection_config['host']}:{connection_config.get('port', 3306)}/{connection_config['database']}"
        
        elif db_type == "sqlite":
            return f"sqlite:///{connection_config['path']}"
        
        elif db_type == "mongodb":
            return f"mongodb://{connection_config['host']}:{connection_config.get('port', 27017)}/{connection_config['database']}"
        
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    @staticmethod
    def test_connection(connection_config: dict) -> dict:
        """Test a database connection"""
        try:
            db_type = connection_config.get("type", "").lower()
            
            if db_type in ["postgresql", "mysql", "sqlite"]:
                from sqlalchemy import create_engine, text
                connection_string = DatabaseConnector.get_connection_string(connection_config)
                engine = create_engine(connection_string)
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                return {"success": True, "message": "Connection successful"}
            
            elif db_type == "mongodb":
                import pymongo
                client = pymongo.MongoClient(
                    f"mongodb://{connection_config['host']}:{connection_config.get('port', 27017)}"
                )
                client.admin.command('ping')
                return {"success": True, "message": "Connection successful"}
            
            else:
                return {"success": False, "message": f"Unsupported database type: {db_type}"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
