#!/usr/bin/env python3
"""Local testing script for the MCP Dynamic HTML App."""

import asyncio
from database import get_user_data, get_metrics_data, get_dashboard_data
from html_renderer import render_dashboard, render_user_card, render_metrics_table


async def test_dashboard():
    """Test dashboard rendering."""
    print("\n" + "="*50)
    print("Testing Dashboard Rendering...")
    print("="*50)
    
    data = await get_dashboard_data()
    html = render_dashboard(data, "light")
    
    # Save to file for viewing
    with open("test_dashboard.html", "w") as f:
        f.write(html)
    
    print("✅ Dashboard HTML generated!")
    print("📄 Open 'test_dashboard.html' in your browser to view")
    print(f"📊 Stats: {data['stats']}")


async def test_user_profile():
    """Test user profile rendering."""
    print("\n" + "="*50)
    print("Testing User Profile Rendering...")
    print("="*50)
    
    user = await get_user_data("user_001")
    html = render_user_card(user)
    
    # Save to file for viewing
    with open("test_user_profile.html", "w") as f:
        f.write(html)
    
    print("✅ User profile HTML generated!")
    print("📄 Open 'test_user_profile.html' in your browser to view")
    print(f"👤 User: {user['name']} ({user['role']})")


async def test_metrics_table():
    """Test metrics table rendering."""
    print("\n" + "="*50)
    print("Testing Metrics Table Rendering...")
    print("="*50)
    
    metrics = await get_metrics_data("sales", 10)
    html = render_metrics_table(metrics, "sales")
    
    # Save to file for viewing
    with open("test_metrics_table.html", "w") as f:
        f.write(html)
    
    print("✅ Metrics table HTML generated!")
    print("📄 Open 'test_metrics_table.html' in your browser to view")
    print(f"📈 Generated {len(metrics)} rows of sales data")


async def main():
    """Run all tests."""
    print("\n🚀 MCP Dynamic HTML App - Local Testing")
    print("="*50)
    
    try:
        await test_dashboard()
        await test_user_profile()
        await test_metrics_table()
        
        print("\n" + "="*50)
        print("✨ All tests completed successfully!")
        print("="*50)
        print("\nNext steps:")
        print("1. Open the generated HTML files in your browser")
        print("2. Configure Claude Desktop with this MCP server")
        print("3. Try prompts like 'Show me the dashboard'")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
