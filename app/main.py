from fastapi import FastAPI
import uvicorn

import models
from database import engine
from routers.user import router as user
from routers.phone_by_phone_id import router as phone_by_phone_id
from routers.phone_by_user_id import router as phone_by_user_id
from routers.email_by_email_id import router as email_by_email_id
from routers.email_by_user_id import router as email_by_user_id


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user, prefix="/user", tags=["user"])
app.include_router(phone_by_user_id, prefix="/user", tags=["user's phone"])
app.include_router(email_by_user_id, prefix="/user", tags=["user's email"])

app.include_router(phone_by_phone_id, prefix="/phone", tags=["phone"])
app.include_router(email_by_email_id, prefix="/email", tags=["email"])


if __name__ == "__main__":
    uvicorn.run(app)
