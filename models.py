from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="violator") # admin, inspector, violator

class Violation(Base):
    __tablename__ = "violations"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="fixed") # fixed, under_review, closed
    employee_id = Column(Integer, ForeignKey("users.id"))
    
    # Связь многие-ко-многим через промежуточную таблицу
    excuses = relationship("Excuse", secondary="violation_excuses", back_populates="violations")

class Excuse(Base):
    __tablename__ = "excuses"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    category = Column(String) # dumb, medium, creative, super_creative
    rating = Column(Integer, default=0)
    
    violations = relationship("Violation", secondary="violation_excuses", back_populates="excuses")

class ViolationExcuse(Base):
    __tablename__ = "violation_excuses"
    violation_id = Column(Integer, ForeignKey("violations.id"), primary_key=True)
    excuse_id = Column(Integer, ForeignKey("excuses.id"), primary_key=True)
