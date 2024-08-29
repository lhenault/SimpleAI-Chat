import uvicorn
from simple_ai.server import app


def serve_app(app=app, host="0.0.0.0", port=80):
    uvicorn.run(app=app, host=host, port=port)


if __name__ == "__main__":
    serve_app()
