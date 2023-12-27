from fastapi import FastAPI

from app import FastApiBuilder

fb = FastApiBuilder('/api')
app: FastAPI = fb.create_app()
