import asyncio
import logging
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.types import ASGIApp

from .llm.providers.openai import OpenAIProvider
from .log_config import load_api_keys, setup_logging


class CompletionRequest(BaseModel):
    prompt: str
    model: str = Field(default='gpt-3.5-turbo', validate_default=True)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)  # OpenAI API limits
    max_tokens: int = Field(default=1000, gt=0)

    @field_validator('model')
    @classmethod
    def validate_model(cls, v: str) -> str:
        if v not in OpenAIProvider.SUPPORTED_MODELS:
            raise ValueError(f'Unsupported model: {v}')
        return v


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions by returning JSON responses."""
    return JSONResponse(
        {'detail': exc.detail},
        status_code=exc.status_code,
    )


@asynccontextmanager
async def lifespan(app: ASGIApp) -> AsyncGenerator[None, None]:
    """Handle server lifespan events."""
    yield


class Server:
    def __init__(self) -> None:
        # Load env variables first
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(env_path)

        setup_logging()
        self.logger = logging.getLogger('rabids.server')

        self.api_keys = load_api_keys()
        self.llm_provider = OpenAIProvider()

        exception_handlers = {
            HTTPException: http_exception_handler,
            Exception: lambda r, e: http_exception_handler(
                r, HTTPException(status_code=500, detail=str(e))
            ),
        }

        self.app = Starlette(
            debug=True,
            routes=[
                Route('/', self.home, methods=['GET']),
                Route('/completion', self.get_completion, methods=['POST']),
            ],
            exception_handlers=exception_handlers,
            lifespan=lifespan,
        )
        # Initialize provider immediately since we're not using startup event
        asyncio.create_task(self.startup())

    async def startup(self) -> None:
        self.logger.info('Starting Rabids server')
        await self.llm_provider.initialize()

    async def home(self, request: Request) -> JSONResponse:
        return JSONResponse({'status': 'running'})

    async def verify_api_key(self, x_api_key: str | None) -> None:
        """Verify that the API key is valid."""
        if not x_api_key:
            raise HTTPException(status_code=401, detail='API key is required')

        if x_api_key not in self.api_keys:
            raise HTTPException(status_code=403, detail='Invalid API key')

    async def get_completion(self, request: Request) -> JSONResponse:
        # Verify API key first
        await self.verify_api_key(request.headers.get('x-api-key'))

        request_id = str(uuid.uuid4())
        logger = self.logger.getChild('completion')

        try:
            data = await request.json()
            completion_request = CompletionRequest(**data)

            logger.info(
                f'Processing completion request: model={completion_request.model} '
                f'temperature={completion_request.temperature} request_id={request_id}'
            )

            response = await self.llm_provider.generate(
                prompt=completion_request.prompt,
                model=completion_request.model,
                temperature=completion_request.temperature,
                max_tokens=completion_request.max_tokens,
            )

            logger.info(
                f'Successfully generated completion: length={len(response)} request_id={request_id}'
            )
            return JSONResponse({'completion': response})

        except ValueError as e:
            logger.warning(f'Invalid request data: {str(e)} request_id={request_id}')
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            logger.error(f'Internal server error: {str(e)} request_id={request_id}')
            raise HTTPException(status_code=500, detail=f'Internal server error: {str(e)}') from e
