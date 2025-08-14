from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import Optional
import asyncio
from .client import MCPClient

class MCPUI:
    def __init__(self, client: MCPClient):
        self.client = client
        self.console = Console()
        
    async def run(self):
        self.console.print(Panel(
            Text.from_markup("[bold green]MCP Client for DevOps[/bold green]", justify="center"),
            expand=True,
            border_style="green"
        ))
        
        while True:
            query = await self.client.get_user_input()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
                
            response = await self.client.process_query(query)
            self.console.print(Panel(
                Markdown(response),
                title="Response",
                border_style="blue"
            ))
