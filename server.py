#!/usr/bin/env python3
"""
MCP Server for Dynamic HTML Rendering with Live Data

This server demonstrates how to create a ChatGPT app that:
- Fetches data from a simulated database
- Renders dynamic HTML based on user queries
- Returns structured HTML responses via MCP protocol
"""

import asyncio
import json
from datetime import datetime
from typing import Any
import logging

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from database import get_user_data, get_metrics_data, get_dashboard_data
from html_renderer import render_dashboard, render_user_card, render_metrics_table

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-dynamic-html")

# Create MCP server instance
server = Server("dynamic-html-app")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for dynamic HTML rendering."""
    return [
        types.Tool(
            name="get_dynamic_dashboard",
            description="Fetches live metrics data and renders a dynamic HTML dashboard",
            inputSchema={
                "type": "object",
                "properties": {
                    "theme": {
                        "type": "string",
                        "description": "Dashboard theme (light or dark)",
                        "enum": ["light", "dark"],
                        "default": "light"
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="get_user_profile",
            description="Fetches user data and renders a dynamic user profile card in HTML",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID to fetch profile for"
                    }
                },
                "required": ["user_id"]
            },
        ),
        types.Tool(
            name="get_metrics_table",
            description="Fetches metrics data and renders an interactive HTML table",
            inputSchema={
                "type": "object",
                "properties": {
                    "metric_type": {
                        "type": "string",
                        "description": "Type of metrics to display",
                        "enum": ["sales", "performance", "engagement"],
                        "default": "sales"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of rows to return",
                        "default": 10
                    }
                },
                "required": []
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls and return dynamic HTML."""
    
    if not arguments:
        arguments = {}
    
    try:
        if name == "get_dynamic_dashboard":
            theme = arguments.get("theme", "light")
            data = await get_dashboard_data()
            html = render_dashboard(data, theme)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Dynamic Dashboard (Theme: {theme})\n\n{html}"
                )
            ]
        
        elif name == "get_user_profile":
            user_id = arguments.get("user_id")
            if not user_id:
                raise ValueError("user_id is required")
            
            user_data = await get_user_data(user_id)
            html = render_user_card(user_data)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"User Profile for {user_id}\n\n{html}"
                )
            ]
        
        elif name == "get_metrics_table":
            metric_type = arguments.get("metric_type", "sales")
            limit = arguments.get("limit", 10)
            
            metrics = await get_metrics_data(metric_type, limit)
            html = render_metrics_table(metrics, metric_type)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Metrics Table ({metric_type.title()})\n\n{html}"
                )
            ]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error handling tool call {name}: {str(e)}")
        return [
            types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        ]


async def main():
    """Run the MCP server."""
    logger.info("Starting MCP Dynamic HTML Server...")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dynamic-html-app",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
