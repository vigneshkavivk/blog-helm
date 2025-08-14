from typing import Dict, Any
from pydantic import BaseModel

class GetPodsInput(BaseModel):
    namespace: str = "default"

class GetDeploymentsInput(BaseModel):
    namespace: str = "default"

KUBERNETES_TOOLS = [
    {
        "name": "k8s.get_pods",
        "description": "Get pods in a namespace",
        "inputSchema": GetPodsInput.schema(),
        "outputSchema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    },
    {
        "name": "k8s.get_deployments",
        "description": "Get deployments in a namespace",
        "inputSchema": GetDeploymentsInput.schema(),
        "outputSchema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    }
]
