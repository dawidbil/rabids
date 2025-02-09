from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .extension.manager import ExtensionManager


class Server:
    def __init__(self) -> None:
        self.extension_manager = ExtensionManager()
        self.app = Starlette(
            routes=[
                Route('/', self.home, methods=['GET']),
                Route('/extensions', self.list_extensions, methods=['GET']),
            ],
            on_startup=[self.startup],
            on_shutdown=[self.shutdown],
        )

    async def startup(self) -> None:
        """Initialize extensions on server startup."""
        await self.extension_manager.load_extensions()

    async def shutdown(self) -> None:
        """Cleanup when server shuts down."""
        for name in list(self.extension_manager.extensions.keys()):
            await self.extension_manager.unload_extension(name)

    async def home(self, request: Request) -> JSONResponse:
        return JSONResponse({'status': 'running'})

    async def list_extensions(self, request: Request) -> JSONResponse:
        return JSONResponse({'extensions': list(self.extension_manager.extensions.keys())})
