from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import engine, SessionLocal 
from sqlalchemy.orm import Session
import models
import database

# models에 정의한 모든 클래스, 연결한 DB엔진에 테이블로 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# html 파일(템플릿) 파일 위치
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home(request: Request, db: Session = Depends(database.get_db)):
    # todos 테이블의 모든 레코드 가져오기
    todos = db.query(models.Todo).order_by(models.Todo.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add")
def add(request : Request, task : str = Form(...), db: Session = Depends(database.get_db)):
    # form 데이터를 db의 todos 테이블에 저장
    todo = models.Todo(task=task)
    db.add(todo)
    db.commit()
    # print(todo)
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/edit/{todo_id}")
def edit_todo(request: Request, todo_id: int, db: Session = Depends(database.get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo})

@app.post("/edit/{todo_id}")
def update_todo(request: Request, todo_id: int, task: str = Form(...), completed: bool = Form(False), db: Session = Depends(database.get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.task = task
    todo.completed = completed
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
    
@app.get("/delete/{todo_id}")
async def add(request: Request, todo_id: int, db: Session = Depends(database.get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)