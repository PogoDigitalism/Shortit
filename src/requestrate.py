import time
import math
from config import Config
from functools import wraps
from fastapi import Request, HTTPException

class requestRates:
    _D: dict[str, dict[str, dict[str,int]]] = dict() 
    
    @classmethod
    def __rateCredits(cls, client_info, e, c) -> None:
        print(cls._D[e][c])
        Factor = math.floor((time.time() - client_info['latestRequestUnix'])/Config.EndpointConstants()[e]['Cooldown'])

        cls._D[e][c]['Tokens'] = min(cls._D[e][c]['Tokens'] + Factor, Config.EndpointConstants()[e]['MaxTokens'])

    @classmethod
    def rateCheck(cls, endpoint_coro) -> bool:
        @wraps(endpoint_coro)
        async def wrapper(request: Request, *args, **kwargs):
            e = endpoint_coro.__name__
            c = f'{request.client.host}'
            s: bool
    
            print(e, c)
            
            if not cls._D.get(e):
                cls._D[e] = dict()
            if not cls._D[e].get(c):
                cls._D[e][c] = {
                    'latestRequestUnix': time.time(),
                    'Tokens': Config.EndpointConstants()[e]['MaxTokens']
                }

            client_info = cls._D[e][c]
            
            cls.__rateCredits(client_info, e, c)
            
            if cls._D[e][c]['Tokens'] > 0:
                cls._D[e][c]['latestRequestUnix'] = time.time()
                cls._D[e][c]['Tokens'] -= 1
                s = True
            else:
                s = False
            kwargs['Tokens'] = cls._D[e][c]['Tokens']

            if s:
                return await endpoint_coro(request, *args,  **kwargs)
            raise HTTPException(429, 'Refresh token limit reached.')
        
        return wrapper
        # @wraps(endpoint_coro)
        # def wrapper(*args, **kwargs):
        # # def wrapper(client_identifier: Request, *args, **kwargs):
        #     # print(client_identifier.client,  endpoint_coro.__name__)
        #     endpoint_identifier = endpoint_coro.__name__
        #     # client_info = cls._D[endpoint_identifier][client_identifier]
        #     # # lru, tokens = client_info['latestRequestUnix'], client_info['Tokens']
                    
        #     # cls.__rateCredits(client_info)
            
        #     # if cls._D[endpoint_identifier][client_identifier]['Tokens'] > 0:
        #     #     cls._D[endpoint_identifier][client_identifier]['Tokens'] -= 1
        #     #     return True
        #     # return False
            
        #     # client_identifier,
            
        #     return endpoint_coro(*args, **kwargs)
        # return wrapper
        endpoint_coro(endpoint_coro)