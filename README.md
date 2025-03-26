1. **Create a Virtual Environment**:  
   `python -m venv venv`  

2. **Activate the Virtual Environment**:  
   - Command Prompt (cmd): `venv\Scripts\activate`  
   - PowerShell: `venv\Scripts\activate.ps1`  

3. **Install Dependencies**:  
   `pip install -r requirements.txt`  

4. **Run the FastAPI Server**:  
   `uvicorn main:app --reload`
5. **Test the API:**
   - `Swagger UI: http://127.0.0.1:8000/docs`
   - `Redoc UI: http://127.0.0.1:8000/redoc`

**Happy Coding!😊**