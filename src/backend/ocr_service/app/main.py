from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers import router
from tags import description, tags_metadata


app = FastAPI(
    title="ocr_service",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)