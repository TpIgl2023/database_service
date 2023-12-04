from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from Models.AccountModel import Account
from database import get_db
from sqlalchemy.ext.declarative import declarative_base







app = FastAPI()
'''
@app.middleware("http")
async def parse_request_as_json(request: Request, call_next):
    try:
        print((await request.json())["taskId"])
        # Read the raw request body as bytes
        raw_body = await request.body()


        # Convert bytes to string (assuming it's UTF-8 encoded)
        raw_body_str = raw_body.decode("utf-8")

        # Parse the raw body as JSON
        json_data = json.loads(raw_body_str)



        # Attach the parsed JSON data to the request
        request.state.parsed_json = json_data
        request._body = json_data

        print(json_data["taskId"])

    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid JSON format in the request body")

    response = await call_next(request)
    return response
    '''

@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    print(body)
    account = Account(name=body["name"])
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

