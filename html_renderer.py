"""HTML rendering utilities for dynamic content."""

from typing import Dict, List, Any


def render_dashboard(data: Dict[str, Any], theme: str = "light") -> str:
    """Render a complete dashboard with live data."""
    bg_color = "#ffffff" if theme == "light" else "#1a1a1a"
    text_color = "#333333" if theme == "light" else "#f0f0f0"
    card_bg = "#f8f9fa" if theme == "light" else "#2d2d2d"
    
    stats = data["stats"]
    recent_activity = data["recent_activity"]
    alerts = data["alerts"]
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: {bg_color};
            color: {text_color};
            padding: 20px;
        }}
        .dashboard {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .timestamp {{
            color: #888;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: {card_bg};
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
            opacity: 0.7;
        }}
        .stat-card .value {{
            font-size: 36px;
            font-weight: bold;
            color: #3b82f6;
        }}
        .section {{
            background: {card_bg};
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            font-size: 20px;
            margin-bottom: 20px;
        }}
        .activity-item {{
            padding: 15px;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }}
        .activity-item:last-child {{
            border-bottom: none;
        }}
        .activity-user {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .activity-time {{
            color: #888;
            font-size: 12px;
        }}
        .alert {{
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 14px;
        }}
        .alert.info {{
            background: #dbeafe;
            color: #1e40af;
        }}
        .alert.warning {{
            background: #fef3c7;
            color: #92400e;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🚀 Dynamic Dashboard</h1>
            <div class="timestamp">Last updated: {data['timestamp']}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Users</h3>
                <div class="value">{stats['total_users']}</div>
            </div>
            <div class="stat-card">
                <h3>Active Sessions</h3>
                <div class="value">{stats['active_sessions']}</div>
            </div>
            <div class="stat-card">
                <h3>Revenue Today</h3>
                <div class="value">${stats['revenue_today']:,}</div>
            </div>
            <div class="stat-card">
                <h3>Orders Today</h3>
                <div class="value">{stats['orders_today']}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Recent Activity</h2>
"""
    
    for activity in recent_activity:
        html += f"""
            <div class="activity-item">
                <div class="activity-user">{activity['user']}</div>
                <div>{activity['action']}</div>
                <div class="activity-time">{activity['time']}</div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="section">
            <h2>System Alerts</h2>
"""
    
    for alert in alerts:
        html += f"""<div class="alert {alert['level']}">{alert['message']}</div>"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html


def render_user_card(user: Dict[str, Any]) -> str:
    """Render a user profile card."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Profile</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .user-card {{
            background: white;
            border-radius: 16px;
            padding: 40px;
            max-width: 400px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .avatar {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin: 0 auto 20px;
            overflow: hidden;
        }}
        .avatar img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .name {{
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .role {{
            color: #666;
            font-size: 16px;
            margin-bottom: 20px;
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-top: 1px solid #eee;
        }}
        .info-label {{
            color: #888;
            font-size: 14px;
        }}
        .info-value {{
            font-weight: 500;
        }}
        .status {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            background: #10b981;
            color: white;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="user-card">
        <div class="avatar">
            <img src="{user['avatar']}" alt="{user['name']}">
        </div>
        <div class="name">{user['name']}</div>
        <div class="role">{user['role']}</div>
        <div class="info-row">
            <span class="info-label">Email:</span>
            <span class="info-value">{user['email']}</span>
        </div>
        <div class="info-row">
            <span class="info-label">User ID:</span>
            <span class="info-value">{user['id']}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Joined:</span>
            <span class="info-value">{user['joined']}</span>
        </div>
        <div class="status">{user['status'].upper()}</div>
    </div>
</body>
</html>
"""


def render_metrics_table(metrics: List[Dict[str, Any]], metric_type: str) -> str:
    """Render an interactive metrics table."""
    
    # Determine column headers based on metric type
    if metric_type == "sales":
        headers = ["Date", "Revenue", "Orders", "Avg Order Value"]
        row_template = lambda m: f"<td>{m['date']}</td><td>${m['revenue']:,}</td><td>{m['orders']}</td><td>${m['avg_order_value']}</td>"
    elif metric_type == "performance":
        headers = ["Date", "Response Time (ms)", "Requests", "Error Rate (%)"]
        row_template = lambda m: f"<td>{m['date']}</td><td>{m['response_time']}</td><td>{m['requests']:,}</td><td>{m['error_rate']}%</td>"
    else:  # engagement
        headers = ["Date", "Active Users", "Page Views", "Avg Session (s)"]
        row_template = lambda m: f"<td>{m['date']}</td><td>{m['active_users']:,}</td><td>{m['page_views']:,}</td><td>{m['avg_session_duration']}</td>"
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metrics Table - {metric_type.title()}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            margin-bottom: 25px;
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #3b82f6;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 {metric_type.title()} Metrics</h1>
        <table>
            <thead>
                <tr>
"""
    
    for header in headers:
        html += f"                    <th>{header}</th>\n"
    
    html += """
                </tr>
            </thead>
            <tbody>
"""
    
    for metric in metrics:
        html += f"                <tr>{row_template(metric)}</tr>\n"
    
    html += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    
    return html
