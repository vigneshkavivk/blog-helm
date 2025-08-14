import aiohttp
import json
from typing import Dict, Any

class ArgoCDServer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_url = config['base_url']
        self.auth = config['auth']
        self.session = None

    async def connect(self):
        headers = {
            "Authorization": f"Bearer {self.auth['token']}",
            "Content-Type": "application/json"
        }
        self.session = aiohttp.ClientSession(base_url=self.base_url, headers=headers)

    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        tool_config = next(t for t in self.config['tools'] if t['name'] == f"argocd.{tool_name}")
        
        if tool_name == "get_applications":
            async with self.session.get(tool_config['endpoint']) as resp:
                return await resp.json()
                
        elif tool_name == "sync_application":
            app_name = args['app_name']
            endpoint = tool_config['endpoint'].format(app_name=app_name)
            async with self.session.post(endpoint) as resp:
                return await resp.json()
                
        raise ValueError(f"Unknown tool: {tool_name}")

    async def close(self):
        if self.session:
            await self.session.close()
