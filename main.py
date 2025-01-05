from fastapi import FastAPI, Depends, HTTPException, status
from auth import verify_password, hash_password, create_access_token
from schemas import UserCreate, UserBase, Token, ProjectCreate, Project as PydanticProject, TokenData, TokenRequest
from models import User, Project as MongoProject
from utils import get_current_user, role_required
from mongoengine import connect
from dotenv import load_dotenv
import os
from typing import List


load_dotenv()
MONGODB_DATABASE = os.environ['MONGODB_DATABASE']
MONGODB_USERNAME = os.environ['MONGODB_USERNAME']
MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']

connect(
    db=MONGODB_DATABASE,
    host=f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@assignment-user-cluster.12fvl.mongodb.net/?retryWrites=true&w=majority&appName=assignment-user-cluster',
)

app = FastAPI()


@app.post("/register", response_model=UserBase)
def register_user(user: UserCreate):
    if User.objects(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        role=user.role,
    )
    new_user.save()
    return UserBase(username=user.username, role=user.role)


@app.post("/login", response_model=Token)
def login_for_access_token(form_data: TokenRequest):
    user = User.objects(username=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/projects", response_model=list[PydanticProject])  
def get_projects(current_user: TokenData = Depends(get_current_user)):
    projects = MongoProject.objects() 
    return [PydanticProject(id=str(project.id), name=project.name, description=project.description, created_by=project.created_by) for project in projects]


@app.post("/projects", response_model=PydanticProject)
def create_project(project: ProjectCreate, current_user: TokenData = Depends(get_current_user), role: str = Depends(role_required("admin"))):
    new_project = MongoProject(
        name=project.name,
        description=project.description,
        created_by=current_user.username
    )
    new_project.save()
    return PydanticProject(id=str(new_project.id), name=new_project.name, description=new_project.description, created_by=new_project.created_by)
