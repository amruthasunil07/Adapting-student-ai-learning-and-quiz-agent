from auth import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from database import SessionLocal
from models import Student

token = create_access_token({"sub": "2"})
print("Generated token:", token)

payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print("Decoded payload:", payload)

db = SessionLocal()
s = db.query(Student).filter(Student.id == int(payload.get("sub"))).first()
print("Found student in DB:", s.id if s else None, s.name if s else None)
db.close()
