import json
import os
from typing import Dict, Any

async def load_server_configs(self, config_dir: str = "config/servers"):
    """Load server configurations from JSON files"""
    server_configs = {}
    
    for filename in os.listdir(config_dir):
        if filename.endswith('.json'):
            server_name = filename[:-5]  # Remove .json
            with open(os.path.join(config_dir, filename)) as f:
                server_configs[server_name] = json.load(f)
                
    return server_configs

async def initialize_servers(self):
    """Initialize servers based on loaded configurations"""
    server_configs = await self.load_server_configs()
    
    for server_name, config in server_configs.items():
        if server_name == "argocd":
            from .servers.argocd_server import ArgoCDServer
            server = ArgoCDServer(config)
        elif server_name == "jenkins":
            from .servers.jenkins_server import JenkinsServer
            server = JenkinsServer(config)
        elif server_name == "kubernetes":
            from .servers.kubernetes_server import KubernetesServer
            server = KubernetesServer(config)
        else:
            continue
            
        await server.connect()
        self.sessions[server_name] = {
            "session": server,
            "config": config
        }
        
        # Register tools
        for tool in config.get('tools', []):
            self.tool_manager.register_tool(tool)
