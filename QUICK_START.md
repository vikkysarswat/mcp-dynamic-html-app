# ⚡ Quick Reference - ChatGPT Setup

## 🚀 3-Minute Setup

### 1️⃣ Deploy to Render
- Visit: https://render.com
- New → Web Service → Connect this GitHub repo
- Wait 2 minutes ⏱️
- Copy your URL: `https://your-app.onrender.com`

### 2️⃣ Test OpenAPI Endpoint
Visit in browser:
```
https://your-app.onrender.com/.well-known/openapi.json
```
✅ Should return JSON

### 3️⃣ Create ChatGPT Custom GPT
1. Go to: https://chat.openai.com
2. Profile → My GPTs → Create
3. Configure tab → Actions → Create new action
4. Import from URL:
```
https://your-app.onrender.com/.well-known/openapi.json
```
5. Save!

### 4️⃣ Test It!
```
"Show me a dashboard"
"Get user profile for user_001"  
"Display sales metrics"
```

---

## 🔧 If You Get Errors

### "Failed to build actions from MCP endpoint"
✅ **Fixed!** Use the OpenAPI URL:
```
https://your-app.onrender.com/.well-known/openapi.json
```
NOT the base URL.

### "Cannot reach server"
- Check your Render deployment is running
- Visit the URL in browser first
- Make sure you're using `https://` not `http://`

### Still Not Working?
1. Visit your homepage: `https://your-app.onrender.com/`
2. Copy the OpenAPI spec from: `/.well-known/openapi.json`
3. In ChatGPT Actions, **paste the JSON directly** instead of importing

---

## 📋 Your Deployed Endpoints

| URL | What it does |
|-----|--------------|
| `/.well-known/openapi.json` | OpenAPI spec (use this in ChatGPT) |
| `/api/dashboard?theme=light` | Dashboard HTML |
| `/api/user/user_001` | User profile HTML |
| `/api/metrics?type=sales&limit=10` | Metrics table HTML |

---

## 💬 Example ChatGPT Prompts

Once your GPT is set up:

```
"Show me a dark theme dashboard"
"Create a profile card for user_002"
"Display performance metrics for the last 7 days"
"Show me engagement metrics"
"Get sales data table"
```

---

## 🎯 Full Documentation

- **ChatGPT Setup**: See `CHATGPT_SETUP.md`
- **README**: See `README.md`
- **GitHub Repo**: https://github.com/vikkysarswat/mcp-dynamic-html-app

---

**That's it! Your ChatGPT Custom Action is ready!** 🎉
