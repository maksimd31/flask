# filename hm5
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = []

templates = Jinja2Templates(directory="templates")


@app.post("/users/")
async def create_user(user: User):
    users.append(user.dict())
    return user


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    for u in users:
        if u["id"] == user_id:
            u.update(user.dict())
            return u
    return {"error": "User not found"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u["id"] == user_id:
            del users[i]
            return {"success": f"User with id {user_id} deleted."}
    return {"error": "User not found"}


@app.get("/users/")
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
