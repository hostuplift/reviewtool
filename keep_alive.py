"""
Keep-alive script for Streamlit Cloud deployment
Run this script to periodically ping your app to keep it awake
"""
import requests
import time
import schedule

# Replace with your actual Streamlit Cloud URL
APP_URL = "https://reviewtool-app.streamlit.app"

def ping_app():
    """Ping the app to keep it awake"""
    try:
        response = requests.get(APP_URL, timeout=10)
        if response.status_code == 200:
            print(f"✅ App pinged successfully at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"⚠️ App responded with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error pinging app: {e}")

def main():
    print("🚀 Starting keep-alive service for ReviewTool...")
    print(f"📡 Monitoring: {APP_URL}")
    print("⏰ Pinging every 15 minutes...")
    
    # Schedule the ping every 15 minutes
    schedule.every(15).minutes.do(ping_app)
    
    # Initial ping
    ping_app()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
