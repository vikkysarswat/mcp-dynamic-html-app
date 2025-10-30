#!/usr/bin/env python3
"""
HTTP Server Wrapper for MCP Dynamic HTML App

This version exposes the MCP functionality via HTTP endpoints
so it can be deployed to cloud platforms like Render, Railway, etc.
"""

import asyncio
import json
from typing import Any, Dict
import logging
from aiohttp import web

from database import get_user_data, get_metrics_data, get_dashboard_data
from html_renderer import render_dashboard, render_user_card, render_metrics_table

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-http-server")

app = web.Application()


async def health_check(request):
    """Health check endpoint."""
    return web.json_response({
        "status": "healthy",
        "service": "mcp-dynamic-html-app",
        "version": "1.0.0"
    })


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
            "name": "get_dynamic_dashboard",
            "description": "Fetches live metrics data and renders a dynamic HTML dashboard",
            "endpoint": "/api/dashboard",
            "parameters": {
                "theme": "light or dark (default: light)"
            }
        },
        {
            "name": "get_user_profile",
            "description": "Fetches user data and renders a dynamic user profile card",
            "endpoint": "/api/user/{user_id}",
            "parameters": {
                "user_id": "User ID (user_001, user_002, user_003)"
            }
        },
        {
            "name": "get_metrics_table",
            "description": "Fetches metrics data and renders an interactive HTML table",
            "endpoint": "/api/metrics",
            "parameters": {
                "type": "sales, performance, or engagement (default: sales)",
                "limit": "Number of rows (default: 10)"
            }
        }
    ]
    
    return web.json_response({"tools": tools})


async def index(request):
    """Home page with API documentation."""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP Dynamic HTML App - API</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 36px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 40px;
            font-size: 18px;
        }
        .status {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 30px;
        }
        .endpoint {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }
        .endpoint h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 20px;
        }
        .endpoint p {
            color: #666;
            margin-bottom: 15px;
            line-height: 1.6;
        }
        .method {
            display: inline-block;
            background: #3b82f6;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 10px;
        }
        .url {
            font-family: 'Courier New', monospace;
            background: #e5e7eb;
            padding: 8px 12px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 10px;
        }
        .params {
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-top: 10px;
        }
        .params h4 {
            font-size: 14px;
            margin-bottom: 10px;
            color: #333;
        }
        .param {
            margin-left: 20px;
            color: #666;
            font-size: 14px;
            margin-bottom: 5px;
        }
        .try-btn {
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
        }
        .try-btn:hover {
            background: #5568d3;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #888;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 MCP Dynamic HTML App</h1>
        <p class="subtitle">REST API for Dynamic HTML Rendering</p>
        <span class="status">✓ Service Running</span>
        
        <div class="endpoint">
            <h3>Health Check</h3>
            <p>Check if the service is running</p>
            <span class="method">GET</span>
            <span class="url">/health</span>
            <br>
            <a href="/health" class="try-btn" target="_blank">Try it →</a>
        </div>
        
        <div class="endpoint">
            <h3>List Tools</h3>
            <p>Get list of available tools and their endpoints</p>
            <span class="method">GET</span>
            <span class="url">/api/tools</span>
            <br>
            <a href="/api/tools" class="try-btn" target="_blank">Try it →</a>
        </div>
        
        <div class="endpoint">
            <h3>Dynamic Dashboard</h3>
            <p>Get a live dashboard with metrics and activity</p>
            <span class="method">GET</span>
            <span class="url">/api/dashboard</span>
            <div class="params">
                <h4>Query Parameters:</h4>
                <div class="param">• <strong>theme</strong>: light or dark (default: light)</div>
            </div>
            <a href="/api/dashboard" class="try-btn" target="_blank">Try Light Theme →</a>
            <a href="/api/dashboard?theme=dark" class="try-btn" target="_blank">Try Dark Theme →</a>
        </div>
        
        <div class="endpoint">
            <h3>User Profile</h3>
            <p>Get a user profile card with dynamic data</p>
            <span class="method">GET</span>
            <span class="url">/api/user/{user_id}</span>
            <div class="params">
                <h4>Path Parameters:</h4>
                <div class="param">• <strong>user_id</strong>: user_001, user_002, or user_003</div>
            </div>
            <a href="/api/user/user_001" class="try-btn" target="_blank">Try User 001 →</a>
            <a href="/api/user/user_002" class="try-btn" target="_blank">Try User 002 →</a>
        </div>
        
        <div class="endpoint">
            <h3>Metrics Table</h3>
            <p>Get an interactive metrics table</p>
            <span class="method">GET</span>
            <span class="url">/api/metrics</span>
            <div class="params">
                <h4>Query Parameters:</h4>
                <div class="param">• <strong>type</strong>: sales, performance, or engagement (default: sales)</div>
                <div class="param">• <strong>limit</strong>: number of rows (default: 10)</div>
            </div>
            <a href="/api/metrics?type=sales&limit=10" class="try-btn" target="_blank">Try Sales →</a>
            <a href="/api/metrics?type=performance&limit=7" class="try-btn" target="_blank">Try Performance →</a>
        </div>
        
        <div class="footer">
            <p>Built with Python + aiohttp | Deployed on Render</p>
        </div>
    </div>
</body>
</html>
    """
    return web.Response(text=html, content_type='text/html')


# Setup routes
app.router.add_get('/', index)
app.router.add_get('/health', health_check)
app.router.add_get('/api/tools', list_tools)
app.router.add_get('/api/dashboard', get_dashboard)
app.router.add_get('/api/user/{user_id}', get_user_profile)
app.router.add_get('/api/metrics', get_metrics)


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting HTTP server on port {port}...")
    web.run_app(app, host='0.0.0.0', port=port)
