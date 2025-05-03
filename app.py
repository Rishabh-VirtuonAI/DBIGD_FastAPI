from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from typing import List
from fastapi import Path

app = FastAPI()

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Linod+/+Mooxy/2021",
    "database": "chatbot_db"
}

# Pydantic model
class QAPair(BaseModel):
    question: str
    answer: str

class QAPairOut(QAPair):
    id: int

# Endpoint to insert a QA pair
@app.post("/insert_qa_pairs", response_model=QAPairOut)
def insert_qa_pair(qa: QAPair):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "INSERT INTO qa_pairs (question, answer) VALUES (%s, %s)"
        cursor.execute(query, (qa.question, qa.answer))
        conn.commit()
        inserted_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return QAPairOut(id=inserted_id, **qa.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve all QA pairs
@app.get("/get_qa_pairs", response_model=List[QAPairOut])
def get_all_qa_pairs():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, question, answer FROM qa_pairs"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# Endpoint to delete a QA pair by ID
@app.delete("/delete_qa_pairs/{id}", status_code=204)
def delete_qa_pair(id: int = Path(..., gt=0)):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Check if the record exists
        cursor.execute("SELECT * FROM qa_pairs WHERE id = %s", (id,))
        record = cursor.fetchone()
        if not record:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail=f"QA pair with id {id} not found.")

        # Delete the record
        cursor.execute("DELETE FROM qa_pairs WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

