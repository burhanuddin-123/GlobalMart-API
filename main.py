## refer:- BasicAuth:- https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
# https://betterprogramming.pub/a-beginner-friendly-introduction-to-fastapi-security-d8f69a259804
# https://itsjoshcampos.codes/fast-api-api-key-authorization

import secrets
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status
from paginate import paginate
from pathlib import Path
# New Imports for app.py
from fastapi.security.api_key import APIKey
import auth

app = FastAPI()

# Lockedown Route
@app.get("/mentorskool/v1/sales")
async def read_current_user(api_key: APIKey = Depends(auth.get_api_key), start: Union[int, None] = None, limit: Union[int, None] = None):
    if not start:
        start = 1
    
    if limit is None:
        limit=30
    elif limit>100:
        limit=100
    
    if start < 0 or limit < 0:
        return {"message": "Pass the valid values for parameters"}
    final_data = paginate(start, limit)

    # return {"message": "Fetch successfully!!"}
    if final_data.get("message"):
        return final_data
    else:
        return final_data
