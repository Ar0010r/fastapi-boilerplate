from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from app.http.routes.v1 import product, user, auth
from app.core.database.postgres import db_creds
from app.core.exception import add as add_exception_handler
from app.http.routes import Route
from fastapi_responseschema import wrap_app_responses

app = FastAPI(debug=True)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=db_creds.get_pg_url(),
    engine_args=db_creds.engine_args,
    commit_on_exit=True
)

app.include_router(user.router)
app.include_router(product.router)
app.include_router(auth.router)
wrap_app_responses(app, route_class=Route)

add_exception_handler(app)


