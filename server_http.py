#!/usr/bin/env python3
"""
Dynamic HTML MCP Server
-----------------------
Exposes interactive dashboard, metrics, and user card tools
via the Model Context Protocol (MCP) for ChatGPT integration.
"""

from __future__ import annotations
import json
from copy import deepcopy
from typing import Any, Dict, List

import mcp.types as types
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

# --- Imports from your existing app ---
from database import get_user_data, get_metrics_data, get_dashboard_data
from html_renderer import render_dashboard, render_user_card, render_metrics_table

# ------------------------------------------------------
#  MCP Server Setup
# ------------------------------------------------------

mcp = FastMCP(
    name="mcp-dynamic-html-app",
    stateless_http=True,  # allows simple HTTP hosting (Render-compatible)
)

# MIME type for embedded HTML widgets
MIME_TYPE = "text/html+skybridge"


# ------------------------------------------------------
#  Tool Input Schemas
# ------------------------------------------------------

class DashboardInput(BaseModel):
    theme: str = Field("light", description="Dashboard theme: 'light' or 'dark'")


class MetricsInput(BaseModel):
    type: str = Field("sales", description="Metric type: sales, performance, or engagement")
    limit: int = Field(10, description="Number of rows to return (1–30)", ge=1, le=30)


class UserInput(BaseModel):
    user_id: str = Field(..., description="User ID, e.g. user_001")


# ------------------------------------------------------
#  Helpers
# ------------------------------------------------------

def make_html_resource(name: str, title: str, html: str) -> types.EmbeddedResource:
    """Wrap HTML as an MCP-embeddable widget resource."""
    uri = f"ui://widget/{name}.html"
    return types.EmbeddedResource(
        type="resource",
        resource=types.TextResourceContents(
            uri=uri,
            mimeType=MIME_TYPE,
            text=html,
            title=title,
        ),
    )


# ------------------------------------------------------
#  Tools
# ------------------------------------------------------

@mcp.tool()
async def getDynamicDashboard(theme: str = "light") -> types.CallToolResult:
    """Render a dynamic dashboard with live metrics."""
    try:
        data = await get_dashboard_data()
        html = render_dashboard(data, theme)
        resource = make_html_resource("dashboard", "Dynamic Dashboard", html)

        meta = {
            "openai.com/widget": resource.model_dump(mode="json"),
            "openai/outputTemplate": "ui://widget/dashboard.html",
            "openai/widgetAccessible": True,
            "openai/resultCanProduceWidget": True,
        }

        return types.CallToolResult(
            content=[types.TextContent(type="text", text="Rendered dashboard")],
            structuredContent={"html": html, "theme": theme},
            _meta=meta,
        )
    except Exception as e:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True,
        )


@mcp.tool()
async def getUserProfile(user_id: str) -> types.CallToolResult:
    """Render a user profile card for a given user ID."""
    try:
        user_data = await get_user_data(user_id)
        html = render_user_card(user_data)
        resource = make_html_resource("user", f"User {user_id}", html)

        meta = {
            "openai.com/widget": resource.model_dump(mode="json"),
            "openai/outputTemplate": "ui://widget/user.html",
            "openai/widgetAccessible": True,
            "openai/resultCanProduceWidget": True,
        }

        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"User {user_id} card rendered")],
            structuredContent={"html": html, "user_id": user_id},
            _meta=meta,
        )
    except Exception as e:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True,
        )


@mcp.tool()
async def getMetricsTable(type: str = "sales", limit: int = 10) -> types.CallToolResult:
    """Render an interactive metrics table."""
    try:
        data = await get_metrics_data(type, limit)
        html = render_metrics_table(data, type)
        resource = make_html_resource("metrics", f"{type.title()} Metrics", html)

        meta = {
            "openai.com/widget": resource.model_dump(mode="json"),
            "openai/outputTemplate": "ui://widget/metrics.html",
            "openai/widgetAccessible": True,
            "openai/resultCanProduceWidget": True,
        }

        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"{type.title()} metrics rendered")],
            structuredContent={"html": html, "type": type, "limit": limit},
            _meta=meta,
        )
    except Exception as e:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True,
        )


# ------------------------------------------------------
#  Resources (for the widgets)
# ------------------------------------------------------

@mcp._mcp_server.list_resources()
async def list_resources() -> List[types.Resource]:
    """Expose basic resources for UI hydration."""
    return [
        types.Resource(
            name="Dynamic Dashboard",
            title="Dynamic Dashboard",
            uri="ui://widget/dashboard.html",
            mimeType=MIME_TYPE,
            description="Dashboard HTML template",
        ),
        types.Resource(
            name="Metrics Table",
            title="Metrics Table",
            uri="ui://widget/metrics.html",
            mimeType=MIME_TYPE,
            description="Metrics table template",
        ),
        types.Resource(
            name="User Profile Card",
            title="User Profile Card",
            uri="ui://widget/user.html",
            mimeType=MIME_TYPE,
            description="User profile HTML card",
        ),
    ]


# ------------------------------------------------------
#  HTTP App (Render-compatible)
# ------------------------------------------------------

app = mcp.streamable_http_app()

try:
    from starlette.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
    )
except Exception:
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0")
