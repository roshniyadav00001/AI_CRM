



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent
from tools import edit_interaction
from database import SessionLocal, Base, engine
from models import Interaction

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"msg": "Backend running"}

# ✅ CHAT API
@app.post("/chat")
def chat(data: dict):
    return run_agent(data.get("message"))

# ✅ FORM SAVE
@app.post("/add-form")
def add_form(data: dict):
    db = SessionLocal()

    obj = Interaction(
        hcp_name=data.get("hcp_name"),
        hospital=data.get("hospital"),
        notes=data.get("notes"),
        summary="Manual Entry",
        sentiment="N/A"
    )

    db.add(obj)
    db.commit()
    db.close()

    return {"msg": "Saved"}

# ✅ EDIT
@app.put("/edit")
def edit(data: dict):
    return edit_interaction(data["id"], data["text"])