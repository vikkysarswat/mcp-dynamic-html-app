# 🤖 ChatGPT Setup Guide

## ✅ FIXED: "Failed to build actions from MCP endpoint"

The error is now resolved! The server has been updated with proper OpenAPI specification for ChatGPT Custom Actions.

---

## 🚀 Quick Setup for ChatGPT

### Step 1: Deploy Your Server

First, deploy your server to a public URL (Render recommended):

1. Go to [Render.com](https://render.com)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository: `vikkysarswat/mcp-dynamic-html-app`
4. Render will auto-detect the configuration
5. Click **"Create Web Service"**
6. Wait 2-3 minutes for deployment
7. Copy your deployment URL (e.g., `https://your-app.onrender.com`)

### Step 2: Test Your Server

Visit your deployed URL in a browser:
```
https://your-app.onrender.com/
```

You should see a beautiful homepage with API documentation.

**Test the OpenAPI spec:**
```
https://your-app.onrender.com/.well-known/openapi.json
```

This should return a JSON OpenAPI specification.

### Step 3: Create ChatGPT Custom GPT

1. Go to [ChatGPT](https://chat.openai.com/)
2. Click on your profile picture (top-right)
3. Select **"My GPTs"**
4. Click **"Create a GPT"**
5. Click on **"Configure"** tab

### Step 4: Configure the GPT

**Name:**
```
Dynamic HTML Dashboard
```

**Description:**
```
Generates beautiful HTML dashboards, user profiles, and metrics tables with live data
```

**Instructions:**
```
You are a helpful assistant that can generate dynamic HTML visualizations. You have access to tools that:

1. Generate live dashboards with metrics and activity feeds
2. Create user profile cards with avatars and details
3. Build interactive data tables for sales, performance, and engagement metrics

When a user asks for visualizations, use the appropriate tool and present the HTML output. Always explain what the visualization shows.
```

### Step 5: Add Actions

In the **Configure** tab, scroll down to **Actions** section:

1. Click **"Create new action"**
2. Click **"Import from URL"**
3. Paste your OpenAPI URL:
   ```
   https://your-app.onrender.com/.well-known/openapi.json
   ```
4. Click **"Import"**
5. ChatGPT will automatically load all three actions ✅

**You should now see:**
- ✅ getDynamicDashboard
- ✅ getUserProfile
- ✅ getMetricsTable

### Step 6: Configure Authentication

Set authentication to **"None"** (API key not required for this demo)

### Step 7: Test Your GPT!

Click **"Save"** and try these prompts:

```
"Show me a dashboard"
"Create a user profile for user_001"
"Display sales metrics for the last 10 days"
"Show me a dark theme dashboard"
"Get performance metrics"
```

---

## 🔧 Troubleshooting

### Error: "Failed to build actions from MCP endpoint"

**Solution:** Make sure you're using the OpenAPI URL, not the base URL:

✅ **Correct:**
```
https://your-app.onrender.com/.well-known/openapi.json
```

❌ **Wrong:**
```
https://your-app.onrender.com
```

### Error: "Cannot reach the server"

**Causes:**
1. Server not deployed yet (wait 2-3 minutes after deploying on Render)
2. Server crashed (check Render logs)
3. Wrong URL

**Solution:**
1. Visit your URL in browser to confirm it's working
2. Check that you can access `/.well-known/openapi.json`
3. Make sure URL has `https://` not `http://`

### Error: "OpenAPI spec invalid"

**Solution:** 
1. Visit `https://your-app.onrender.com/.well-known/openapi.json` in browser
2. Copy the JSON
3. In ChatGPT Actions, instead of "Import from URL", paste the JSON directly

### CORS Errors

The server now includes CORS headers, but if you still see errors:

**For local testing:**
```bash
# The server already includes CORS middleware
# Just make sure you're running: python server_http.py
```

**For production:**
- CORS is automatically handled ✅

---

## 📱 Using Your ChatGPT

Once configured, you can:

1. **Generate Dashboards:**
   ```
   "Show me a dashboard with dark theme"
   "Create a metrics dashboard"
   ```

2. **View User Profiles:**
   ```
   "Get profile for user_001"
   "Show me information about user_002"
   ```

3. **Display Metrics:**
   ```
   "Show sales metrics for the last 10 days"
   "Display performance metrics"
   "Create an engagement metrics table"
   ```

---

## 🌐 Available Endpoints

Your deployed server exposes:

| Endpoint | Description |
|----------|-------------|
| `/` | Homepage with documentation |
| `/health` | Health check |
| `/.well-known/openapi.json` | OpenAPI spec for ChatGPT |
| `/api/dashboard` | Dynamic dashboard HTML |
| `/api/user/{user_id}` | User profile card HTML |
| `/api/metrics` | Metrics table HTML |

---

## 🎯 What Changed

The fix included:

1. ✅ Added OpenAPI 3.1 specification endpoint
2. ✅ Added CORS middleware for ChatGPT compatibility
3. ✅ Proper operationId for each endpoint
4. ✅ Clear parameter descriptions and enums
5. ✅ Response schemas defined
6. ✅ Beautiful homepage with setup instructions

---

## ✨ Next Steps

1. **Deploy to Render** (if not done already)
2. **Test the OpenAPI endpoint** in your browser
3. **Create your Custom GPT** in ChatGPT
4. **Import the OpenAPI spec** 
5. **Start using it!** 🎉

---

## 💡 Tips

- Share your GPT with others by making it public
- You can customize the instructions to change how the GPT behaves
- Add more endpoints by editing `server_http.py`
- Connect to a real database instead of the simulated one

---

**Your ChatGPT Custom Action is now ready to use!** 🚀
