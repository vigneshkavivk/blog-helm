from typing import Dict, Any
from pydantic import BaseModel

class GetApplicationsInput(BaseModel):
    pass

class SyncApplicationInput(BaseModel):
    app_name: str

ARGOCD_TOOLS = [
    {
        "name": "argocd.get_applications",
        "description": "Get list of all ArgoCD applications",
        "inputSchema": GetApplicationsInput.schema(),
        "outputSchema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "metadata": {"type": "object"},
                            "status": {"type": "object"}
                        }
                    }
                }
            }
        }
    },
    {
        "name": "argocd.sync_application",
        "description": "Sync an ArgoCD application",
        "inputSchema": SyncApplicationInput.schema(),
        "outputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "message": {"type": "string"}
            }
        }
    }
]
