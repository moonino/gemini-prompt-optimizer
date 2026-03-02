import aiohttp
import json
from app.core.config import settings

class ForwarderService:
    async def forward_request(self, path: str, method: str, body: dict, headers: dict):
        url = f"{settings.OPENAI_BASE_URL}/{path}"
        
        # Remove host-specific headers and inject our API Key
        filtered_headers = {k: v for k, v in headers.items() if k.lower() not in ['host', 'content-length', 'authorization']}
        filtered_headers['Authorization'] = f"Bearer {settings.OPENAI_API_KEY}"
        filtered_headers['Content-Type'] = 'application/json'

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=filtered_headers,
                data=json.dumps(body)
            ) as response:
                return await response.json(), response.status

forwarder_service = ForwarderService()
