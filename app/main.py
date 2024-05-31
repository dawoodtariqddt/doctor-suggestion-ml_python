#app/main.py
from fastapi import FastAPI, HTTPException
from .database import get_connection
import json
from .ml_model import DoctorSuggestionModel


app = FastAPI()
model = DoctorSuggestionModel()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": item[0]}


@app.get("/user/{id}")
async def get_user(id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE id = %s", (id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert tuple to dictionary for easier manipulation
        user_data = dict(zip(cursor.column_names, user))
        
        user_data['location'] = json.loads(user_data['location'])
        user_data['disability_related_to'] = json.loads(user_data['disability_related_to'])
        user_data['disability_with'] = json.loads(user_data['disability_with'])
        
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/suggest_doctor")
async def suggest_doctor(user_input: tuple):
    try:
        model.load_data()
        suggestion = model.predict_doctor(user_input)
        return suggestion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    