from kubernetes_asyncio import client, config
from typing import Dict, Any

class KubernetesServer:
    def __init__(self, config_data: Dict[str, Any]):
        self.config = config_data
        self.api_client = None

    async def connect(self):
        await config.load_kube_config(config_file=self.config['config_path'], context=self.config['context'])
        self.api_client = client.ApiClient()

    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        tool_config = next(t for t in self.config['tools'] if t['name'] == f"k8s.{tool_name}")
        
        if tool_name == "get_pods":
            namespace = args.get('namespace', tool_config.get('namespace', 'default'))
            v1 = client.CoreV1Api(self.api_client)
            pods = await v1.list_namespaced_pod(namespace)
            return {"items": [p.metadata.name for p in pods.items]}
            
        elif tool_name == "get_deployments":
            namespace = args.get('namespace', tool_config.get('namespace', 'default'))
            apps_v1 = client.AppsV1Api(self.api_client)
            deployments = await apps_v1.list_namespaced_deployment(namespace)
            return {"items": [d.metadata.name for d in deployments.items]}
            
        raise ValueError(f"Unknown tool: {tool_name}")

    async def close(self):
        if self.api_client:
            await self.api_client.close()
