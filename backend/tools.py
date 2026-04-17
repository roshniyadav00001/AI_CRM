


from groq import Groq
import os, json, re
from dotenv import load_dotenv
from database import SessionLocal
from models import Interaction

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Helper: Clean JSON from LLM
def extract_json(text):
    try:
        # remove ```json ```
        text = re.sub(r"```json|```", "", text).strip()
        return json.loads(text)
    except:
        return {"summary": text}


#  LOG TOOL
def log_interaction(text):
    prompt = f"""
    Return ONLY valid JSON (no backticks, no explanation):

    {{
      "hcp_name": "",
      "hospital": "",
      "summary": "",
      "sentiment": ""
    }}

    Text: {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    clean = extract_json(raw)

    #  Save to DB safely
    db = SessionLocal()
    try:
        obj = Interaction(
            hcp_name=clean.get("hcp_name"),
            hospital=clean.get("hospital"),
            notes=text,
            summary=clean.get("summary"),
            sentiment=clean.get("sentiment")
        )
        db.add(obj)
        db.commit()
    except Exception as e:
        db.rollback()
        print("DB ERROR:", e)
    finally:
        db.close()

    return clean


#  SENTIMENT
def sentiment_tool(text):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Give sentiment in one word: {text}"}]
    )
    return res.choices[0].message.content


#  SUGGEST
def suggest_tool(text):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Suggest next sales action: {text}"}]
    )
    return res.choices[0].message.content


#  FETCH
def fetch_interactions():
    db = SessionLocal()
    data = db.query(Interaction).all()
    db.close()
    return [
        {
            "id": i.id,
            "hcp": i.hcp_name,
            "hospital": i.hospital,
            "notes": i.notes
        }
        for i in data
    ]


#  EDIT
def edit_interaction(id, new_text):
    db = SessionLocal()
    obj = db.query(Interaction).get(id)

    if obj:
        obj.notes = new_text
        db.commit()
        db.close()
        return "Updated successfully"

    db.close()
    return "Not found"