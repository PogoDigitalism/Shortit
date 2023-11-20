from api import mainAPI
import asyncio

if __name__ == "__main__":
    instance = mainAPI()
    asyncio.run(instance.serve())