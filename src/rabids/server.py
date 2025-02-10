import logging
import uuid
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .llm.base import LLMProvider
from .llm.providers.openai import OpenAIProvider
from .log_config import setup_logging


class CompletionRequest(BaseModel):
    prompt: str
    model: str = Field(default='gpt-3.5-turbo')
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)  # OpenAI API limits
    max_tokens: int = Field(default=1000, gt=0)


class Server:
    def __init__(self) -> None:
        # Load env variables first
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(env_path)

        setup_logging()
        self.logger = logging.getLogger('rabids.server')

        self.llm_providers: dict[str, LLMProvider] = {
            'openai': OpenAIProvider(),
        }

        self.app = Starlette(
            routes=[
                Route('/', self.home, methods=['GET']),
                Route('/completion', self.get_completion, methods=['POST']),
            ],
            on_startup=[self.startup],
        )

    async def startup(self) -> None:
        self.logger.info('Starting Rabids server')

        for provider_name, provider in self.llm_providers.items():
            self.logger.info(f'Initializing provider: {provider_name}')
            await provider.initialize()

    async def home(self, request: Request) -> JSONResponse:
        return JSONResponse({'status': 'running'})

    async def get_completion(self, request: Request) -> JSONResponse:
        request_id = str(uuid.uuid4())
        logger = self.logger.getChild('completion')

        try:
            data = await request.json()
            completion_request = CompletionRequest(**data)

            logger.info(
                f'Processing completion request: model={completion_request.model} '
                f'temperature={completion_request.temperature} request_id={request_id}'
            )

            provider_name = (
                'openai'
                if completion_request.model in OpenAIProvider.SUPPORTED_MODELS
                else 'unknown'
            )

            provider = self.llm_providers.get(provider_name)
            if not provider:
                logger.warning(
                    f'Unsupported model provider requested: {provider_name}',
                    extra={'request_id': request_id},
                )
                return JSONResponse(
                    {'error': f'Unsupported model provider: {provider_name}'},
                    status_code=400,
                )

            response = await provider.generate(
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
            return JSONResponse({'error': str(e)}, status_code=400)
        except Exception as e:
            logger.error(f'Internal server error: {str(e)} request_id={request_id}')
            return JSONResponse(
                {'error': f'Internal server error: {str(e)}'},
                status_code=500,
            )
