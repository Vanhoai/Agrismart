import uvicorn

def main():
    uvicorn.run("agrismart.main:app", port=8080, host="0.0.0.0", reload=True)
