import os
import pkg_resources
from dotenv import load_dotenv
from fastapi import FastAPI

from resolverapi.config import Config
from resolverapi.routers import resolver

load_dotenv()

app = FastAPI(
    title="Resolver",
    description="The SAEON URL Resolver Service",
    version=pkg_resources.require('resolver')[0].version,
    openapi_prefix=os.getenv('PATH_PREFIX'),
    config=Config(),
)

app.include_router(
    resolver.router,
    prefix='',
    tags=['Resolver'],
)
