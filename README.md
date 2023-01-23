# FastAPI 가이드

## 첫걸음
- Hello World, OpenAPI, 스키마

<details>
<summary>Hello FastAPI</summary> 
<div markdown ="1">

`pip install fastapi`
`pip install uvicorn`
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```
`uvicorn main:app --reload`
- uvicorn: ASGI web server
- main: main.py(파이썬 "모듈", 파일 이름)
- app: main.py 내부의 app = FastAPI() 줄에서 생성한 오브젝트.
- --reload: 코드 변경 후 서버 재시작. 개발시에만 사용
> http://127.0.0.1:8000
- 대화형 API 문서: /docs
- 대안 API 문서: /redoc
- JSON 스키마: /openapi.json
- FastAPI는 API를 정의하기 위한 OpenAPI 표준을 사용한다. API를 이용해 "스키마"를 생성한다.
- "스키마"는 무언가의 정의 또는 설명이다. 코드가 아니라 추상적인 설명일 뿐이다.
- 데이터 "스키마"는 JSON처럼 어떤 데이터의 형채를 나타낼 수도 있다.

</div>    
</details>

## 경로 매개변수
- 매개 변수의 타입을 제한할 수 있다. 타입을 지정하지 않는다면 str값으로 인식한다.
- 경로 동작(API)을 만들 때 고정 경로를 갖고 있는 상황에는 순서를 먼저 지정함으로써 해결할 수 있다.
- Enum 클래스를 생성하여 들어올 수 있는 매개변수를 정의할 수 있다.
- :path를 경로에 지정함으로써 path전체를 가져올 수 있다.
- 데이터 검증, API 주석과 자동완성, 데이터 파싱 등 한번에 선언으로 도와준다.

<details>
<summary>설명 예제</summary> 
<div markdown ="1">

### 타입 지정

```python
@app.get("/items/{pk}")
async def read_item_1(pk: int):
    print(type(pk)) # int
    return {"pk": pk}


@app.get("/items/{pk}")
async def read_item_2(pk):
    print(type(pk)) # str
    return {"pk": pk}
```
- 데이터 검증은 Pydantic에 의해 이뤄진다.
- 매개 변수에 타입을 지정함으로써 들어오는 값에 대한 제한을 둘 수 있다. str, float, bool 외 다른 복잡한 데이터 타입을 선언 가능하다.
- 지정하지 않는다면 아무 값(any)이 들어 올 수 있고 str값으로 인식된다.

### 동일 경로의 순서

```python
@app.get("/users/me")
async def read_user_me():
    return {"username": "current user"}


@app.get("/users/{username}")
async def read_user(username: str):
    return {"username": username}
```

`/users/me` 경로에 요청 시, 위에서부터 순차적으로 읽어 read_user_me()가 실행된다. read_user()가 위에 있다면 'me'또한 username이라고 판단하여 실행된다.

### Enum 클래스 생성
- 미리 정의한 경로 매개변수 값을 원한다면 파이썬 표준 Enum을 사용할 수 있다.
- 간단하게 열거 가능한, iterable한 객체를 만든다고 생각하면 좋겠다.

```python
class MLName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def read_model(model_name: MLName):
    return {"ur model": model_name}
```
- 경로 매개 변수 model_name에는 미리 정의한 MLName의 멤버 값(속성 값)들만 들어올 수 있다.
- Enum에 들어오는 타입을 지정할 수 있다.

```python
from enum import Enum

class IntMLName(int, Enum): # 요류
    zero = 0
    one = 1
    two = 2


@app.get("/models/{model_name}")
async def read_int_model(model_name: IntMLName):
    return {"ur int model": model_name}
```
- 하지만 위와 같은 int 타입을 넣고 '/models/0'으로 요청을 하게되면 유효하지 않다는 422에러가 뜨게 된다.
- 이유는 starlette(fastapi가 상속하는 클래스)에서 경로 매개 변수가 처리 될 때, 먼저 사전 값을 가져오고 {"model_name": "0"} 그 다음 pydantic(fastapi 데이터 검증)에서 유효성 검사를 체크할 때 int의 변환 시도를 먼저하는 것이 아닌, Enum을 통해 값을 가져오기 때문에 발생하는 것으로 판단됩니다.
- 두가지의 해결 방법
```python
from enum import IntEnum

class IntMLName(IntEnum): # 요류
    zero = 0
    one = 1
    two = 2


@app.get("/models/{model_name:int}")
async def read_int_model(model_name: IntMLName):
    return {"ur int model": model_name}
```
1. 경로에 직접 타입을 지정하는 것 ({model_name:int})
2. IntEnum을 상속 받는것 (class IntMLName(IntEnum))


### 경로 변환기:path
- /files/{file_path}가 있는 경로에서 home/useranem/my.txt 처럼 path에 들어있는 file_path자체가 필요할 때, /files/home/username/my.txt
- Starlette의 내부 도구 중 하나를 사용하여 가져올 수 있다.

```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```
- 매개변수가 /home/username/my.txt를 갖고 있어 슬래시로 시작(/)해야 할 수 있다.

- 이 경우 URL은: /files//home/username/my.txt이며 files과 home 사이에 이중 슬래시(//)가 생긴다.

</div>    
</details>