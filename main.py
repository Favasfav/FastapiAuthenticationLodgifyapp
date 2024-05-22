from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging
import models, schemas, crud, database, auth
from sqlalchemy.sql import text
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
logging.basicConfig(level=logging.INFO)
import uvicorn

app = FastAPI()


# CORS SETUP
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# serves as a dependency that provides a SQLAlchemy database session 
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


#for checking database connection
@app.get("/healthcheck")
async def healthcheck(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM accounts_customuser"))
        users = result.fetchall()
        users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        return {"status": "Database connection successful", "users": users_list}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    



# for sign up
@app.post("/signup", response_model=schemas.User, status_code=201)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# get any user by id 
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(id:int ,db: Session = Depends(get_db)):
    user=crud.get_user_by_id(db,id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} is not available")
    return user


# login or get token
@app.post("/login",tags=['Login'])
def login_for_access(request:schemas.Login,db:Session=Depends(get_db)):
    user=crud.get_user_by_email(db,email=request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"invalid credentials")
    
    if not auth.verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"invalid credentials")
    payload = {
                "email": user.email,
                "username": user.username,  
                "role": user.role,          
                "user_id": user.id          
            } 
    access_token = auth.create_access_token(
        data=payload
    )
    return {"access":access_token, "token_type":"bearer"}
   
    
