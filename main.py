from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import database
from passlib.context import CryptContext

app = FastAPI()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User Model (Pydantic for validation)
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    account_type: str

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Test Database Connection
@app.get("/test-db")
def test_db():
    conn = database.get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    return {"message": "Database connected successfully"}

# Register New User
@app.post("/register")
def register(user: User):
    conn = database.get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()
    hashed_password = hash_password(user.password)

    try:
        cursor.execute(
            "INSERT INTO Users (Username, Email, PasswordHash, AccountType) VALUES (?, ?, ?, ?)",
            (user.username, user.email, hashed_password, user.account_type)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

    return {"message": "User registered successfully"}

# User Login
@app.post("/login")
def login(username: str, password: str):
    conn = database.get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()
    cursor.execute("SELECT UserID, PasswordHash FROM Users WHERE Username = ?", (username,))
    user = cursor.fetchone()

    if not user or not pwd_context.verify(password, user[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user[0]}

# Fetch All Users
@app.get("/users")
def get_users():
    conn = database.get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Username, Email FROM Users")
    users = cursor.fetchall()

    user_list = [{"id": user[0], "username": user[1], "email": user[2]} for user in users]

    cursor.close()
    conn.close()
    return user_list

# Fetch User by ID
@app.get("/users/{id}")
def get_user(id: int):
    conn = database.get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Username, Email FROM Users WHERE UserID = ?", (id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user[0], "username": user[1], "email": user[2]}

# Update User Details
@app.put("/users/{id}")
def update_user(id: int, user: User):
    conn = database.get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()
    hashed_password = hash_password(user.password)

    cursor.execute(
        "UPDATE Users SET Username = ?, Email = ?, PasswordHash = ?, AccountType = ? WHERE UserID = ?",
        (user.username, user.email, hashed_password, user.account_type, id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "User updated successfully"}

# Delete User
@app.delete("/users/{id}")
def delete_user(id: int):
    conn = database.get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE UserID = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "User deleted successfully"}
