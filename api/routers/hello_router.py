from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def say_hello():
    return {"message": "Hello, World! -  running on /hello"}


@router.get("/joke")
async def say_hello():
    return {"message": "This is a joke endpoint - running on /joke"}
@router.get("/goodbye")
async def say_goodbye():
    return {"message": "Goodbye, World! - running on /goodbye"}     

