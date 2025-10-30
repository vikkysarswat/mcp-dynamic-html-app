#!/usr/bin/env python3
"""
HTTP Server for ChatGPT Custom Actions

This version exposes the functionality via REST API with OpenAPI spec
for ChatGPT GPT/Actions integration.
"""

import asyncio
import json
from typing import Any, Dict
import logging
from aiohttp import web
import os

from database import get_user_data, get_metrics_data, get_dashboard_data
from html_renderer import render_dashboard, render_user_card, render_metrics_table

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chatgpt-http-server")

app = web.Application()


async def health_check(request):
    """Health check endpoint."""
    return web.json_response({
        "status": "healthy",
        "service": "mcp-dynamic-html-app",
        "version": "1.0.0"
    })


async def openapi_spec(request):
    """OpenAPI specification for ChatGPT Actions."""
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "Dynamic HTML Rendering API",
            "description": "API for generating dashboards, profiles, and metrics tables. Returns HTML for browsers and JSON for ChatGPT Actions.",
            "version": "1.1.0"
        },
        "servers": [
            {"url": "https://mcp-dynamic-html-app.onrender.com", "description": "Production server"}
        ],
        "paths": {
            "/api/dashboard": {
                "get": {
                    "operationId": "getDynamicDashboard",
                    "summary": "Get a dynamic dashboard",
                    "parameters": [
                        {
                            "name": "theme",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "enum": ["light", "dark"], "default": "light"},
                            "description": "Dashboard theme color"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Dashboard rendered successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"html": {"type": "string", "description": "HTML content of dashboard"}}
                                    }
                                },
                                "text/html": {"schema": {"type": "string"}}
                            }
                        }
                    }
                }
            },
            "/api/user/{user_id}": {
                "get": {
                    "operationId": "getUserProfile",
                    "summary": "Get user profile card",
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "User ID (e.g., user_001)"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "User profile rendered successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"html": {"type": "string", "description": "HTML for user card"}}
                                    }
                                },
                                "text/html": {"schema": {"type": "string"}}
                            }
                        },
                        "404": {"description": "User not found"}
                    }
                }
            },
            "/api/metrics": {
                "get": {
                    "operationId": "getMetricsTable",
                    "summary": "Get metrics table",
                    "parameters": [
                        {
                            "name": "type",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "enum": ["sales", "performance", "engagement"], "default": "sales"},
                            "description": "Metrics category"
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 10, "minimum": 1, "maximum": 30},
                            "description": "Number of rows"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Metrics table rendered successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"html": {"type": "string", "description": "HTML of metrics table"}}
                                    }
                                },
                                "text/html": {"schema": {"type": "string"}}
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {}
        }
    }

    return web.Response(
        text=json.dumps(spec, indent=2),
        content_type="application/json"
    )




async def get_dashboard(request):
    """Get dynamic dashboard endpoint."""
    try:
        theme = request.query.get('theme', 'light')
        data = await get_dashboard_data()
        html = render_dashboard(data, theme)
        
        return web.Response(
            text=html,
            content_type='text/html'
        )
    except Exception as e:
        logger.error(f"Error in get_dashboard: {str(e)}")
        return web.json_response(
            {"error": str(e)},
            status=500
        )


async def get_user_profile(request):
    """Get user profile endpoint."""
    try:
        user_id = request.match_info.get('user_id')
        if not user_id:
            return web.json_response(
                {"error": "user_id is required"},
                status=400
            )
        
        user_data = await get_user_data(user_id)
        html = render_user_card(user_data)
        
        return web.Response(
            text=html,
            content_type='text/html'
        )
    except ValueError as e:
        return web.json_response(
            {"error": str(e)},
            status=404
        )
    except Exception as e:
        logger.error(f"Error in get_user_profile: {str(e)}")
        return web.json_response(
            {"error": str(e)},
            status=500
        )


async def get_metrics(request):
    """Get metrics table endpoint."""
    try:
        metric_type = request.query.get('type', 'sales')
        limit = int(request.query.get('limit', '10'))
        
        # Validate limit
        if limit < 1 or limit > 30:
            limit = 10
        
        metrics = await get_metrics_data(metric_type, limit)
        html = render_metrics_table(metrics, metric_type)
        
        return web.Response(
            text=html,
            content_type='text/html'
        )
    except Exception as e:
        logger.error(f"Error in get_metrics: {str(e)}")
        return web.json_response(
            {"error": str(e)},
            status=500
        )


async def list_tools(request):
    """List available tools endpoint."""
    tools = [
        {
            "name": "getDynamicDashboard",
            "description": "Get a live dashboard with metrics and activity",
            "endpoint": "/api/dashboard",
            "parameters": {
                "theme": "light or dark (default: light)"
            }
        },
        {
            "name": "getUserProfile",
            "description": "Get a user profile card with dynamic data",
            "endpoint": "/api/user/{user_id}",
            "parameters": {
                "user_id": "User ID (user_001, user_002, user_003)"
            }
        },
        {
            "name": "getMetricsTable",
            "description": "Get an interactive metrics table",
            "endpoint": "/api/metrics",
            "parameters": {
                "type": "sales, performance, or engagement (default: sales)",
                "limit": "Number of rows (default: 10)"
            }
        }
    ]
    
    return web.json_response({"tools": tools})


async def index(request):
    """Home page with API documentation and ChatGPT setup instructions."""
    host = request.host
    protocol = "https" if "localhost" not in host else "http"
    base_url = f"{protocol}://{host}"
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT Dynamic HTML API</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 36px;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 18px;
        }}
        .status {{
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 30px;
        }}
        .setup-box {{
            background: #f0f9ff;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin: 30px 0;
            border-radius: 8px;
        }}
        .setup-box h2 {{
            color: #1e40af;
            margin-bottom: 15px;
            font-size: 24px;
        }}
        .setup-box ol {{
            margin-left: 20px;
        }}
        .setup-box li {{
            margin: 10px 0;
            line-height: 1.6;
        }}
        .code-box {{
            background: #1e293b;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            overflow-x: auto;
            margin: 10px 0;
        }}
        .endpoint {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }}
        .endpoint h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 20px;
        }}
        .method {{
            display: inline-block;
            background: #3b82f6;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 10px;
        }}
        .url {{
            font-family: 'Courier New', monospace;
            background: #e5e7eb;
            padding: 8px 12px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 10px;
        }}
        .try-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            margin-top: 10px;
            text-decoration: none;
            display: inline-block;
        }}
        .try-btn:hover {{
            background: #5568d3;
        }}
        .warning {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 ChatGPT Dynamic HTML API</h1>
        <p class="subtitle">REST API with OpenAPI Spec for ChatGPT Custom Actions</p>
        <span class="status">✓ Service Running</span>
        
        <div class="setup-box">
            <h2>🚀 Setup ChatGPT Custom GPT</h2>
            <ol>
                <li>Go to <a href="https://chat.openai.com/" target="_blank">ChatGPT</a></li>
                <li>Click your profile → <strong>My GPTs</strong> → <strong>Create a GPT</strong></li>
                <li>In the <strong>Configure</strong> tab, scroll to <strong>Actions</strong></li>
                <li>Click <strong>Create new action</strong></li>
                <li>Click <strong>Import from URL</strong> and paste:</li>
            </ol>
            <div class="code-box">{base_url}/.well-known/openapi.json</div>
            <p style="margin-top: 15px;"><strong>Or manually paste the OpenAPI spec from:</strong></p>
            <div class="code-box">{base_url}/.well-known/openapi.json</div>
        </div>

        <div class="warning">
            <strong>⚠️ CORS Notice:</strong> If testing locally, you may need to enable CORS for ChatGPT to access your API.
            For production deployment on Render/Railway, CORS is automatically handled.
        </div>
        
        <div class="endpoint">
            <h3>OpenAPI Specification</h3>
            <p>Get the OpenAPI 3.1 spec for ChatGPT Actions</p>
            <span class="method">GET</span>
            <span class="url">/.well-known/openapi.json</span>
            <br>
            <a href="/.well-known/openapi.json" class="try-btn" target="_blank">View Spec →</a>
        </div>
        
        <div class="endpoint">
            <h3>Health Check</h3>
            <p>Check if the service is running</p>
            <span class="method">GET</span>
            <span class="url">/health</span>
            <br>
            <a href="/health" class="try-btn" target="_blank">Try it →</a>
        </div>
        
        <div class="endpoint">
            <h3>Dynamic Dashboard</h3>
            <p>Get a live dashboard with metrics and activity</p>
            <span class="method">GET</span>
            <span class="url">/api/dashboard</span>
            <br>
            <a href="/api/dashboard" class="try-btn" target="_blank">Light Theme →</a>
            <a href="/api/dashboard?theme=dark" class="try-btn" target="_blank">Dark Theme →</a>
        </div>
        
        <div class="endpoint">
            <h3>User Profile</h3>
            <p>Get a user profile card with dynamic data</p>
            <span class="method">GET</span>
            <span class="url">/api/user/{{user_id}}</span>
            <br>
            <a href="/api/user/user_001" class="try-btn" target="_blank">User 001 →</a>
            <a href="/api/user/user_002" class="try-btn" target="_blank">User 002 →</a>
        </div>
        
        <div class="endpoint">
            <h3>Metrics Table</h3>
            <p>Get an interactive metrics table</p>
            <span class="method">GET</span>
            <span class="url">/api/metrics</span>
            <br>
            <a href="/api/metrics?type=sales&limit=10" class="try-btn" target="_blank">Sales →</a>
            <a href="/api/metrics?type=performance&limit=7" class="try-btn" target="_blank">Performance →</a>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #888; font-size: 14px;">
            <p>Built for ChatGPT Custom Actions | Python + aiohttp</p>
        </div>
    </div>
</body>
</html>
    """
    return web.Response(text=html, content_type='text/html')


# Enable CORS for ChatGPT
@web.middleware
async def cors_middleware(request, handler):
    """Add CORS headers for ChatGPT compatibility."""
    if request.method == "OPTIONS":
        response = web.Response()
    else:
        response = await handler(request)
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# Setup routes
app.router.add_get('/', index)
app.router.add_get('/health', health_check)
app.router.add_get('/.well-known/openapi.json', openapi_spec)
app.router.add_get('/api/tools', list_tools)
app.router.add_get('/api/dashboard', get_dashboard)
app.router.add_get('/api/user/{user_id}', get_user_profile)
app.router.add_get('/api/metrics', get_metrics)

# Add CORS middleware
app.middlewares.append(cors_middleware)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting HTTP server on port {port}...")
    logger.info("OpenAPI spec available at: /.well-known/openapi.json")
    web.run_app(app, host='0.0.0.0', port=port)
