from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to my FastAPI app!"}

@app.get("/hello")
def hello():
    return {"message": "Hello, FastAPI is awesome!"}

@app.get("/goodbye")
def goodbye():
    return {"message": "Goodbye, see you later!"}
