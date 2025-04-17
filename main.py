# This Project works ==> Approved
from fastapi import FastAPI, Request, status
from .database import engine, Base
from .routers import auth, notes, admin, users
#from NotesApp.database import engine, Base
#from NotesApp.routers import auth, notes, admin, users

#from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
#from NotesApp.routers import sample

app = FastAPI(title="React-FastAPI Secure Notes")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables
Base.metadata.create_all(bind=engine)

#templates = Jinja2Templates(directory="SecureNotesApp/templates")
#app.mount("/static", StaticFiles(directory="SecureNotesApp/static"), name="static")

@app.get("/")
def test(request: Request):
    #return templates.TemplateResponse("home.html", {"request": request})
    return RedirectResponse(url="/notes/note-page", status_code=status.HTTP_302_FOUND)

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(admin.router)
app.include_router(users.router)
