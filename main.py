#точка входа FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ExcuseFlow API")

# ================= AUTH MODULE =================
@app.post("/api/auth/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# ================= EXCUSE MODULE =================
@app.post("/api/excuses", response_model=schemas.ExcuseResponse)
def create_excuse(excuse: schemas.ExcuseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_excuse = models.Excuse(text=excuse.text, category=excuse.category)
    db.add(new_excuse)
    db.commit()
    db.refresh(new_excuse)
    return new_excuse

@app.get("/api/excuses", response_model=List[schemas.ExcuseResponse])
def get_excuses(category: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Excuse)
    if category:
        query = query.filter(models.Excuse.category == category)
    return query.all()

@app.post("/api/excuses/{id}/rate")
def rate_excuse(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    excuse = db.query(models.Excuse).filter(models.Excuse.id == id).first()
    if not excuse:
        raise HTTPException(status_code=404, detail="Excuse not found")
    excuse.rating += 1
    db.commit()
    return {"message": "Rating updated", "new_rating": excuse.rating}

# ================= VIOLATION MODULE =================
@app.post("/api/violations", response_model=schemas.ViolationResponse)
def create_violation(violation: schemas.ViolationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_violation = models.Violation(title=violation.title, description=violation.description, employee_id=violation.employee_id)
    db.add(new_violation)
    db.commit()
    db.refresh(new_violation)
    return new_violation

@app.get("/api/violations", response_model=List[schemas.ViolationResponse])
def get_violations(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Violation).all()

@app.patch("/api/violations/{id}/status")
def update_status(id: int, status_update: schemas.StatusUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    violation = db.query(models.Violation).filter(models.Violation.id == id).first()
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    
    # Проверка запрещенных переходов (упрощенно)
    if violation.status == "closed" and status_update.status != "closed":
        raise HTTPException(status_code=400, detail="Cannot change status from closed")
    
    violation.status = status_update.status
    db.commit()
    return {"message": "Status updated", "new_status": violation.status}

@app.post("/api/violations/{v_id}/excuses/{e_id}")
def link_excuse(v_id: int, e_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    violation = db.query(models.Violation).filter(models.Violation.id == v_id).first()
    excuse = db.query(models.Excuse).filter(models.Excuse.id == e_id).first()
    if not violation or not excuse:
        raise HTTPException(status_code=404, detail="Violation or Excuse not found")
    
    violation.excuses.append(excuse)
    db.commit()
    return {"message": "Excuse linked to violation"}

# ================= REPORT MODULE =================
@app.get("/api/reports/top-excuses")
def get_top_excuses(db: Session = Depends(get_db)):
    # Сортируем по рейтингу по убыванию, берем топ-10
    return db.query(models.Excuse).order_by(models.Excuse.rating.desc()).limit(10).all()
