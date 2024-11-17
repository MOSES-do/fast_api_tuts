Activate vurtual environment
venv\Scripts\activate.bat

FLask library
pip install fastapi[all]
uvicorn main:app --reload (To start fastAPI)
uvicorn app.main:app --reload

# The login info sent from the frontend is stored in the OAuth2PasswordRequestForm which has only two fields username and password, therefore if a user sends email and password it's stored as username and password in OAuth2PasswordRequestForm. To retrieve the email we would have to reference username, tricky but must be understood
