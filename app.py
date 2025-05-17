# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import mysql.connector
# from typing import List
# from fastapi import Path

# app = FastAPI()

# # Database configuration
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "Linod+/+Mooxy/2021",
#     "database": "chatbot_db"
# }

# # Pydantic model
# class QAPair(BaseModel):
#     question: str
#     answer: str

# class QAPairOut(QAPair):
#     id: int

# # Endpoint to insert a QA pair
# @app.post("/insert_qa_pairs", response_model=QAPairOut)
# def insert_qa_pair(qa: QAPair):
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#         query = "INSERT INTO qa_pairs (question, answer) VALUES (%s, %s)"
#         cursor.execute(query, (qa.question, qa.answer))
#         conn.commit()
#         inserted_id = cursor.lastrowid
#         cursor.close()
#         conn.close()
#         return QAPairOut(id=inserted_id, **qa.dict())
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Endpoint to retrieve all QA pairs
# @app.get("/get_qa_pairs", response_model=List[QAPairOut])
# def get_all_qa_pairs():
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor(dictionary=True)
#         query = "SELECT id, question, answer FROM qa_pairs"
#         cursor.execute(query)
#         results = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return results
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    


# # Endpoint to delete a QA pair by ID
# @app.delete("/delete_qa_pairs/{id}", status_code=204)
# def delete_qa_pair(id: int = Path(..., gt=0)):
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#         # Check if the record exists
#         cursor.execute("SELECT * FROM qa_pairs WHERE id = %s", (id,))
#         record = cursor.fetchone()
#         if not record:
#             cursor.close()
#             conn.close()
#             raise HTTPException(status_code=404, detail=f"QA pair with id {id} not found.")

#         # Delete the record
#         cursor.execute("DELETE FROM qa_pairs WHERE id = %s", (id,))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

# # Endpoint to update a QA pair
# @app.post("/update_qa_pair", response_model=QAPairOut)
# def update_qa_pair(id: int, qa: QAPair):
#     try:
#         conn = mysql.connector.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#         query = """
#             UPDATE qa_pairs 
#             SET question = %s, answer = %s 
#             WHERE id = %s
#         """
#         cursor.execute(query, (qa.question, qa.answer, id))
#         conn.commit()

#         # Check if a record was updated
#         if cursor.rowcount == 0:
#             raise HTTPException(status_code=404, detail="QA Pair not found")

#         cursor.close()
#         conn.close()

#         return QAPairOut(id=id, **qa.dict())
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from typing import List

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:3000",  
    "http://65.0.34.207",     
    "http://example.com"      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "%V:rorRawr=kZsm#60dF",
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

# Endpoint to update a QA pair (using PUT method)
@app.put("/update_qa_pair/{id}", response_model=QAPairOut)
def update_qa_pair(id: int, qa: QAPair):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            UPDATE qa_pairs 
            SET question = %s, answer = %s 
            WHERE id = %s
        """
        cursor.execute(query, (qa.question, qa.answer, id))
        conn.commit()

        # Check if a record was updated
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"QA Pair with id {id} not found")

        cursor.close()
        conn.close()

        return QAPairOut(id=id, **qa.dict())
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

