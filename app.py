from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from database import *

app = FastAPI(title="mystery")

origins = ["http://localhost:3000" "localhost:3000"]
