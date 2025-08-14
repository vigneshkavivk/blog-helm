from typing import Dict, Any
from pydantic import BaseModel

class GetJobsInput(BaseModel):
    pass

class TriggerBuildInput(BaseModel):
    job_name: str

JENKINS_TOOLS = [
    {
        "name": "jenkins.get_jobs",
        "description": "Get list of all Jenkins jobs",
        "inputSchema": GetJobsInput.schema(),
        "outputSchema": {
            "type": "object",
            "properties": {
                "jobs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "url": {"type": "string"}
                        }
                    }
                }
            }
        }
    },
    {
        "name": "jenkins.trigger_build",
        "description": "Trigger a Jenkins build",
        "inputSchema": TriggerBuildInput.schema(),
        "outputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "integer"},
                "message": {"type": "string"}
            }
        }
    }
]
