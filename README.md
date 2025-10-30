# 🚀 MCP Dynamic HTML App

A Python-based Model Context Protocol (MCP) server that demonstrates **dynamic HTML rendering with live data** for ChatGPT applications.

## 🎯 What This Does

This app showcases how to build a **dynamic ChatGPT app** where:
- HTML is rendered based on **live data** (not static assets)
- Data is fetched from a simulated database
- Content changes dynamically based on user queries
- Perfect for dashboards, reports, and data visualizations

## 🏗️ Architecture

Based on the **Server-Side Dynamic HTML Rendering** pattern:

```
ChatGPT → MCP Tool Call → Python Server → Fetch DB Data → Render HTML → Return to ChatGPT
```

## 📦 Features

✅ **Three Dynamic Tools:**
1. **`get_dynamic_dashboard`** - Live metrics dashboard with theme support
2. **`get_user_profile`** - User profile cards with real-time data
3. **`get_metrics_table`** - Interactive data tables (sales, performance, engagement)

✅ **Simulated Database** - No setup required, works out of the box

✅ **Beautiful HTML** - Modern, responsive designs with CSS

✅ **Easy Deployment** - Deploy to Railway, Render, or any Python hosting

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/vikkysarswat/mcp-dynamic-html-app.git
cd mcp-dynamic-html-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python server.py
```

## 🔧 How to Use

### With Claude Desktop (Recommended)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dynamic-html": {
      "command": "python",
      "args": ["/path/to/mcp-dynamic-html-app/server.py"]
    }
  }
}
```

### Example Prompts

```
"Show me the dashboard"
"Get user profile for user_001"
"Display sales metrics table"
"Show me performance metrics with dark theme"
```

## 📁 Project Structure

```
mcp-dynamic-html-app/
├── server.py           # Main MCP server with tool definitions
├── database.py         # Simulated database with sample data
├── html_renderer.py    # HTML rendering templates
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🛠️ Customization

### Add Your Own Data Source

Replace the simulated database in `database.py`:

```python
import sqlite3

async def get_user_data(user_id: str):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()
```

### Create Custom HTML Templates

Add new rendering functions in `html_renderer.py`:

```python
def render_custom_view(data):
    return f"""
    <!DOCTYPE html>
    <html>
        <!-- Your custom HTML -->
    </html>
    """
```

### Add New Tools

Extend the tools list in `server.py`:

```python
@server.list_tools()
async def handle_list_tools():
    return [
        # ... existing tools
        types.Tool(
            name="your_custom_tool",
            description="Your tool description",
            inputSchema={...}
        )
    ]
```

## 🚢 Deployment Options

### Deploy to Railway

1. Fork this repository
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Select this repository
5. Railway will auto-detect Python and deploy

### Deploy to Render

1. Go to [Render.com](https://render.com)
2. Click "New" → "Background Worker"
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python server.py`

### Deploy to Heroku

```bash
heroku create your-app-name
git push heroku main
```

## 📊 Example Use Cases

- **Business Dashboards** - Real-time KPIs and metrics
- **User Management** - Dynamic user profiles and lists
- **Data Reports** - Interactive tables and charts
- **Analytics Views** - Performance and engagement tracking
- **Admin Panels** - System monitoring and alerts

## 🧪 Testing

Test the tools directly:

```python
import asyncio
from database import get_user_data
from html_renderer import render_user_card

async def test():
    user = await get_user_data("user_001")
    html = render_user_card(user)
    print(html)

asyncio.run(test())
```

## 📚 Learn More

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Claude AI](https://claude.ai)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add new HTML templates
- Create additional tools
- Improve the database layer
- Add tests

## 📄 License

MIT License - feel free to use this in your projects!

## 🎉 Credits

Created by Nilesh Vikky based on MCP dynamic HTML rendering patterns.

---

**Happy Building! 🚀**

If you have questions or need help, open an issue or reach out!
