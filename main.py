from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic model for user data
class User(BaseModel):
    id: int
    name: str
    phone_no: str
    address: str

# In-memory data storage
users_db = []

# Create a new user
@app.post("/users/", status_code=201)
async def create_user(user: User):
    for existing_user in users_db:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User ID already exists")
    users_db.append(user)
    return {"message": "User created successfully"}

@app.get("/users/search", response_model=List[User])
async def search_users(name: Optional[str] = Query(None)):
    if not name:
        raise HTTPException(status_code=400, detail="Name parameter is required")

    filtered_users = [user for user in users_db if name.lower() in user.name.lower()]
    return filtered_users

# Read user by ID
@app.get("/users/{id}", response_model=User)
async def get_user(id: int):
    for user in users_db:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# # Read users by name
# @app.get("/users/search", response_model=List[User])
# async def search_users(name: Optional[str] = None):
#     filtered_users = [user for user in users_db if user.name.lower() == name.lower()]
#     return filtered_users




# Update user details
@app.put("/users/{id}")
async def update_user(id: int, updated_data: User):
    for idx, user in enumerate(users_db):
        if user.id == id:
            users_db[idx] = updated_data
            return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Delete user by ID
@app.delete("/users/{id}")
async def delete_user(id: int):
    for idx, user in enumerate(users_db):
        if user.id == id:
            users_db.pop(idx)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
