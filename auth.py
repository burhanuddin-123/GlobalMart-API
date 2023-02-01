## refer:- https://itsjoshcampos.codes/fast-api-api-key-authorization

import os
from dotenv import load_dotenv, find_dotenv
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends
from starlette.status import HTTP_403_FORBIDDEN

load_dotenv(find_dotenv())

API_KEY = os.environ.get("API_KEY")  ## user+password MD5 hash conversion

## Now fetch the api_key from the header
api_key_header = APIKeyHeader(name="access_token", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )