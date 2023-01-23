from enum import Enum, IntEnum

from fastapi import FastAPI


class MLName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class IntMLName(IntEnum):
    zero = 0
    one = 1
    two = 2


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{pk}")
async def read_item(pk: int):
    print(type(pk))
    return {"pk": pk}


@app.get("/users/me")
async def read_user_me():
    return {"username": "current user"}


@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}


@app.get("/models/{model_name}")
async def read_model(model_name: MLName):
    return {"ur model": model_name}


@app.get("/models/int/{model_name}")
async def read_int_model(model_name: IntMLName):
    print(model_name.value, model_name)
    if model_name in list(IntMLName):
        print("이곳으로 통과")
    return {"ur model": model_name}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}