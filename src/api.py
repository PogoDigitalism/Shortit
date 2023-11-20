from typing import Any, Callable, Coroutine, Dict, List, Optional, Sequence, Type, Union
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse, Response, HTMLResponse, FileResponse
import asyncio
import uvicorn
from config import Config
from requestrate import requestRates
from functools import wraps

        # self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.ConnectionSRV())
        # self.db: motor.motor_asyncio.AsyncIOMotorDatabase = self.client['MyUGC']
        
class mainAPI():
    def __init__(self):
        self.version = "0.0.1"

        url = "https://stackoverflow.com/q/65446591/5538913"
        self.app = FastAPI()
        self.serving_task: Optional[asyncio.Task] = None


    async def serve(self):
        @self.app.exception_handler(404)
        async def _404(request, _):
            return HTMLResponse(Config.HTML_404(), 404)
        
        @self.app.exception_handler(429)
        async def _429(request, exception):
            return JSONResponse({'Status': exception.status_code, 'Description': exception.detail})
   
        # API ENDPOINTS:     

        @self.app.get("/profile", include_in_schema=False)
        @requestRates.rateCheck
        async def _get_profile(request: Request, *args, **kwargs) -> JSONResponse:
            return JSONResponse({"MyClass version": self.version, "FastAPI version": self.app.version})

        # CONTENT SERVERS:

        self.app.mount("/", StaticFiles(directory="static", html = True), name="static")
        @self.app.get("/", include_in_schema=False)
        @requestRates.rateCheck
        async def _get_root(request: Request, success: Optional[bool] = False, Tokens: Optional[int] = None) -> JSONResponse:
            return JSONResponse({'tokens': Tokens})
            # return HTMLResponse('<meta http-equiv="Refresh" content="0; url=\'/docs\'" />')


        self.app.mount("/test", StaticFiles(directory="static/test", html= True), name="test")
        @self.app.get("/test", include_in_schema=False)
        @requestRates.rateCheck
        async def _get_version() -> JSONResponse:
            return JSONResponse({'test': 'test'}, 200)

        # @requestRates.rateCheck
        # def hi():
        #     print('hellooooo')
        #// serve
        config = uvicorn.Config(self.app, host="127.0.0.1", port=8000)
        server = uvicorn.Server(config)
        await server.serve()
        