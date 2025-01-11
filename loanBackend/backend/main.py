from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import joblib
import numpy as np


app = FastAPI()

# Allow frontend to make requests to the backend (adjust if using different port or domain)
origins = [
    "http://localhost:8080",
    "http://18.133.30.151:8080",  # Frontend's origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("loan_approval_model.joblib")

if hasattr(model, "monotonic_cst"):
    del model.monotonic_cst

# Connect to the SQLite database (you can replace this with PostgreSQL)
def db_connect():
    conn = psycopg2.connect(
        host="db",
        database = "loan_db",
        port="5432",
        user = "postgres_admin",
        password = "password" )
    return conn

def create_table():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Run this once to create the table
create_table()

class SignupRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class EligibilityForm(BaseModel):
    gender: int
    married: int
    dependents: int
    education: int
    self_employed: int
    applicant_income: int
    coapplicant_income: int
    loan_amount: int
    loan_amount_term: int
    credit_history: float
    property_area: int

@app.post("/api/signup")
async def signup(request: SignupRequest):
    try:
        conn = db_connect()
        cursor = conn.cursor()
        print("Username:",request.username)
        print("Password: ", request.password)
        cursor.execute('SELECT * from users WHERE username = %s', (request.username,))
        print("1st Query done")
        user = cursor.fetchone()
        print(user)
        if user:
            cursor.close()
            conn.close()    
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            cursor.execute('INSERT INTO users (username, password) values (%s,%s)',(request.username,request.password))
            conn.commit()

            cursor.close()
            conn.close()

            return {"status": "success", "message": "User account created successfully"}
    except Exception as e:
        print("This Exception is coming: ", e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")





@app.post("/api/login")
async def login(request: LoginRequest):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * from users where username=%s AND password =%s',(request.username,request.password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    else:
        return { "status": "success", "message": "Login Successfull"}
    
@app.post("/api/eligibility_checker")
async def eligibity_check(data: EligibilityForm):
    try:
        
        # Prepare data for prediction
        values = [
            data.gender, data.married, data.dependents,
            data.education, data.self_employed, data.applicant_income,
            data.coapplicant_income, data.loan_amount, data.loan_amount_term,
            data.credit_history, data.property_area
        ]
        print(values)
        input_data = np.array(values).reshape(1, -1)
        
        # Predict eligibility
        prediction = model.predict(input_data)
        eligibility = "Eligible" if prediction[0] == 1 else "Not Eligible"

        # Return result as JSON
        return {
            "status": "success",
            "message" : eligibility,
            "data": {
                "Eligibility":eligibility,
                "loan_amount": data.loan_amount,
                "loan_term": data.loan_amount_term,
            }
        }
    except Exception as e:
        print("Exception occured when checking Eligibity : ",e)
        raise HTTPException(status_code=500, detail=str(e))


