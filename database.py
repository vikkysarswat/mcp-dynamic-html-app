"""Simulated database for demo purposes."""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Simulated database
USERS_DB = {
    "user_001": {
        "id": "user_001",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "role": "Product Manager",
        "joined": "2023-01-15",
        "status": "active",
        "avatar": "https://i.pravatar.cc/150?img=1"
    },
    "user_002": {
        "id": "user_002",
        "name": "Bob Smith",
        "email": "bob@example.com",
        "role": "Software Engineer",
        "joined": "2022-06-20",
        "status": "active",
        "avatar": "https://i.pravatar.cc/150?img=2"
    },
    "user_003": {
        "id": "user_003",
        "name": "Carol Davis",
        "email": "carol@example.com",
        "role": "UX Designer",
        "joined": "2023-03-10",
        "status": "active",
        "avatar": "https://i.pravatar.cc/150?img=3"
    },
}


async def get_user_data(user_id: str) -> Dict[str, Any]:
    """Fetch user data from simulated database."""
    if user_id not in USERS_DB:
        raise ValueError(f"User {user_id} not found")
    return USERS_DB[user_id]


async def get_metrics_data(metric_type: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Generate simulated metrics data."""
    base_date = datetime.now() - timedelta(days=limit)
    metrics = []
    
    for i in range(limit):
        date = base_date + timedelta(days=i)
        
        if metric_type == "sales":
            metrics.append({
                "date": date.strftime("%Y-%m-%d"),
                "revenue": random.randint(5000, 25000),
                "orders": random.randint(50, 200),
                "avg_order_value": round(random.uniform(80, 150), 2)
            })
        elif metric_type == "performance":
            metrics.append({
                "date": date.strftime("%Y-%m-%d"),
                "response_time": random.randint(50, 500),
                "requests": random.randint(10000, 50000),
                "error_rate": round(random.uniform(0.1, 2.5), 2)
            })
        elif metric_type == "engagement":
            metrics.append({
                "date": date.strftime("%Y-%m-%d"),
                "active_users": random.randint(1000, 5000),
                "page_views": random.randint(50000, 200000),
                "avg_session_duration": random.randint(120, 600)
            })
    
    return metrics


async def get_dashboard_data() -> Dict[str, Any]:
    """Generate comprehensive dashboard data."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stats": {
            "total_users": len(USERS_DB),
            "active_sessions": random.randint(10, 50),
            "revenue_today": random.randint(5000, 15000),
            "orders_today": random.randint(50, 150)
        },
        "recent_activity": [
            {"user": "Alice Johnson", "action": "Completed order #1234", "time": "2 minutes ago"},
            {"user": "Bob Smith", "action": "Updated profile", "time": "15 minutes ago"},
            {"user": "Carol Davis", "action": "Viewed dashboard", "time": "1 hour ago"},
        ],
        "alerts": [
            {"level": "info", "message": "System running smoothly"},
            {"level": "warning", "message": "Database backup pending"},
        ]
    }
