from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import schemas
from auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Expense Tracker API")


@app.get("/")
def home():
    return {"message": "Personal Expense Tracker API. Visit /docs to test."}


@app.post(
    "/auth/register",
    response_model=schemas.UserResponse,   # hashed_password
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    existing_email = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/auth/login", response_model=schemas.Token, tags=["Authentication"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .first()
    )

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



@app.post(
    "/transactions",
    response_model=schemas.TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Transactions"],
)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_transaction = models.Transaction(
        title=transaction.title,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        date=transaction.date,
        owner_id=current_user.id,      
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@app.get(
    "/transactions",
    response_model=List[schemas.TransactionResponse],
    tags=["Transactions"],
)
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.owner_id == current_user.id)
        .all()
    )

@app.get(
    "/transactions/filter",
    response_model=List[schemas.TransactionResponse],
    tags=["Transactions"],
)
def filter_transactions(
    type: Optional[str] = Query(None, description="income or expense"),
    category: Optional[str] = Query(None),
    minimum_amount: Optional[float] = Query(None),
    maximum_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    query = db.query(models.Transaction).filter(
        models.Transaction.owner_id == current_user.id
    )

    
    if type is not None:
        query = query.filter(models.Transaction.type == type)

    if category is not None:
        query = query.filter(models.Transaction.category == category)

    if minimum_amount is not None:
        query = query.filter(models.Transaction.amount >= minimum_amount)

    if maximum_amount is not None:
        query = query.filter(models.Transaction.amount <= maximum_amount)

    return query.all()


@app.get(
    "/transactions/{transaction_id}",
    response_model=schemas.TransactionResponse,
    tags=["Transactions"],
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    transaction = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == current_user.id,
        )
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {transaction_id} not found",
        )

    return transaction


@app.put(
    "/transactions/{transaction_id}",
    response_model=schemas.TransactionResponse,
    tags=["Transactions"],
)
def update_transaction(
    transaction_id: int,
    updated: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    transaction = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == current_user.id,
        )
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {transaction_id} not found",
        )

    transaction.title = updated.title
    transaction.amount = updated.amount
    transaction.type = updated.type
    transaction.category = updated.category
    transaction.date = updated.date

    db.commit()
    db.refresh(transaction)
    return transaction


@app.delete("/transactions/{transaction_id}", tags=["Transactions"])
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    transaction = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.owner_id == current_user.id,
        )
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {transaction_id} not found",
        )

    db.delete(transaction)
    db.commit()
    return {"message": f"Transaction {transaction_id} deleted successfully"}