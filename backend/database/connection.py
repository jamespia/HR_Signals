"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from models.database import Base

# Create database engine
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize database, create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_initial_data() -> None:
    """Seed initial data (themes, sectors)"""
    db = SessionLocal()
    try:
        from models.database import Theme, Sector

        # Check if data already exists
        if db.query(Theme).count() > 0:
            print("Database already seeded")
            return

        # Seed themes
        themes_data = [
            {
                "name": "Workforce Transformation",
                "description": "Changes in workforce structure, hybrid work, and organizational models",
                "keywords": ["workforce", "transformation", "hybrid", "remote", "flexible work"],
                "color": "#3B82F6"
            },
            {
                "name": "AI Governance",
                "description": "AI ethics, regulation, and responsible AI practices",
                "keywords": ["AI governance", "ethics", "responsible AI", "regulation", "compliance"],
                "color": "#8B5CF6"
            },
            {
                "name": "Skills and Capability",
                "description": "Upskilling, reskilling, and capability development",
                "keywords": ["skills", "upskilling", "reskilling", "learning", "capability"],
                "color": "#10B981"
            },
            {
                "name": "HR Technology",
                "description": "HRIS, talent tech, and people analytics platforms",
                "keywords": ["HR tech", "HRIS", "people analytics", "talent tech", "automation"],
                "color": "#F59E0B"
            },
            {
                "name": "Policy and Regulation",
                "description": "Labor laws, employment regulations, and compliance",
                "keywords": ["policy", "regulation", "compliance", "labor law", "employment law"],
                "color": "#EF4444"
            },
            {
                "name": "Future of Work",
                "description": "Long-term trends shaping the workplace",
                "keywords": ["future of work", "trends", "innovation", "digital transformation"],
                "color": "#06B6D4"
            },
            {
                "name": "Employee Experience",
                "description": "Engagement, wellbeing, and employee satisfaction",
                "keywords": ["employee experience", "engagement", "wellbeing", "satisfaction", "culture"],
                "color": "#EC4899"
            },
            {
                "name": "Talent Acquisition",
                "description": "Recruitment, hiring, and talent sourcing",
                "keywords": ["recruitment", "hiring", "talent acquisition", "sourcing", "employer brand"],
                "color": "#6366F1"
            },
            {
                "name": "Diversity and Inclusion",
                "description": "DEI initiatives and workplace equity",
                "keywords": ["diversity", "inclusion", "equity", "DEI", "belonging"],
                "color": "#14B8A6"
            },
            {
                "name": "Organizational Culture",
                "description": "Culture transformation and values",
                "keywords": ["culture", "values", "leadership", "change management", "transformation"],
                "color": "#F97316"
            }
        ]

        for theme_data in themes_data:
            theme = Theme(**theme_data)
            db.add(theme)

        # Seed sectors
        sectors_data = [
            {"name": "Technology", "description": "Software, hardware, and tech services"},
            {"name": "Financial Services", "description": "Banking, insurance, and investment"},
            {"name": "Healthcare", "description": "Hospitals, pharmaceuticals, and health services"},
            {"name": "Manufacturing", "description": "Industrial production and manufacturing"},
            {"name": "Retail", "description": "Retail and consumer goods"},
            {"name": "Professional Services", "description": "Consulting, legal, and professional services"},
            {"name": "Public Sector", "description": "Government and public administration"},
            {"name": "Education", "description": "Schools, universities, and education services"},
            {"name": "Energy", "description": "Oil, gas, and renewable energy"},
            {"name": "General", "description": "Cross-industry and general topics"}
        ]

        for sector_data in sectors_data:
            sector = Sector(**sector_data)
            db.add(sector)

        db.commit()
        print("Initial data seeded successfully")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_initial_data()
