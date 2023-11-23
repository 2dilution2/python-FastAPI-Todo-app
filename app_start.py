import uvicorn

# cli 실행 : uvicorn main:app [--port=8000] --reload

if __name__ == "__main__":
  uvicorn.run('main:app', host='localhost', port=8000, reload=True)