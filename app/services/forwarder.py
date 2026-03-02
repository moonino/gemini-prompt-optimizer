import aiohttp
import json
from app.core.config import settings

class ForwarderService:
    async def forward_request(self, path: str, method: str, body: dict, headers: dict):
        url = f"{settings.GEMINI_BASE_URL}/{path}"
        
        # Inject Gemini API Key for the native Gemini API
        filtered_headers = {k: v for k, v in headers.items() if k.lower() not in ['host', 'content-length', 'authorization', 'x-goog-api-key']}
        filtered_headers['x-goog-api-key'] = settings.GEMINI_API_KEY
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
