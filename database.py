from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection - UPDATE THESE WITH YOUR CREDENTIALS
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")  # Change to your password
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pdf_qa_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine with proper settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Check connection before using
    pool_recycle=3600,   # Recycle connections every hour
    echo=False           # Set to True to see SQL queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class QARecord(Base):
    __tablename__ = "qa_history"
    
    id = Column(Integer, primary_key=True, index=True)
    pdf_filename = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    user_rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PDFDocument(Base):
    __tablename__ = "pdf_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, nullable=False)
    file_path = Column(String(512), nullable=False)
    chunk_count = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Initialize database - creates tables if they don't exist"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ PostgreSQL database connected successfully!")
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("\n📝 Please check:")
        print("1. Is PostgreSQL running?")
        print("2. Are your credentials correct in .env file?")
        print("3. Does the database 'pdf_qa_db' exist?")
        raise