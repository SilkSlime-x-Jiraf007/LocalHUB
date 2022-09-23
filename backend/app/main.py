from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.auth import authRouter
from app.routers import FilesRouter, CategoriesRouter, TagsRouter

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(FilesRouter, prefix="/files", tags=["files"])
app.include_router(CategoriesRouter, prefix="/categories", tags=["categories"])
app.include_router(TagsRouter, prefix="/tags", tags=["tags"])
