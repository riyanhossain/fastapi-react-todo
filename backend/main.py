from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}
