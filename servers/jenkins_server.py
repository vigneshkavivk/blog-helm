import aiohttp
import base64
from typing import Dict, Any

class JenkinsServer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_url = config['base_url']
        self.auth = config['auth']
        self.session = None

    async def connect(self):
        auth_str = f"{self.auth['username']}:{self.auth['password']}"
        auth_bytes = auth_str.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            "Authorization": f"Basic {base64_auth}",
            "Content-Type": "application/json"
        }
        self.session = aiohttp.ClientSession(base_url=self.base_url, headers=headers)

    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        tool_config = next(t for t in self.config['tools'] if t['name'] == f"jenkins.{tool_name}")
        
        if tool_name == "get_jobs":
            async with self.session.get(tool_config['endpoint']) as resp:
                return await resp.json()
                
        elif tool_name == "trigger_build":
            job_name = args['job_name']
            endpoint = tool_config['endpoint'].format(job_name=job_name)
            async with self.session.post(endpoint) as resp:
                return {"status": resp.status, "message": "Build triggered"}
                
        raise ValueError(f"Unknown tool: {tool_name}")

    async def close(self):
        if self.session:
            await self.session.close()
