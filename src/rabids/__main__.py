import uvicorn

from .server import Server


def main() -> None:
    server = Server()
    uvicorn.run(server.app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
