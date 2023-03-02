from fastapi import FastAPI
app = FastAPI()

@app.get("/hi")
def hello():
  return {"Hello world!"}