import subprocess
import requests
import time
import random
import sys

def get_xbogus(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"  

    # Run Node.js script and capture X-Bogus output
    result = subprocess.run(
        ["node", "test_xbogus.js", url, user_agent], 
        capture_output=True, text=True
    )
    
    return result.stdout.strip().split(": ")[1]  

def report_tiktok_video(video_url, report_count):
    for i in range(report_count):
        xbogus = get_xbogus(video_url)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": video_url,
            "X-Bogus": xbogus,
        }

        # Define the TikTok Report API (Modify with real API if needed)
        report_url = "https://www.tiktok.com/api/report"

        # Report payload (choosing the most severe category)
        payload = {
            "video_url": video_url,
            "reason": "minor_safety",  # 🚨 Most drastic reason
            "details": "This video contains content that endangers minors.",
        }

        response = requests.post(report_url, headers=headers, json=payload)

        if response.status_code == 200:
            print(f"✅ Report {i+1}/{report_count} sent successfully!")
        else:
            print(f"❌ Report {i+1}/{report_count} failed | Error: {response.text}")

        # Random delay to avoid detection
        delay = random.uniform(3, 10)  # Wait between 3-10 seconds
        print(f"⏳ Waiting {round(delay, 2)} seconds before next report...")
        time.sleep(delay)

# VPN Check
vpn_check = input("🚨 Have you turned on your VPN? (yes/no): ").strip().lower()
if vpn_check != "yes":
    print("❌ Please turn on your VPN before running this script! Exiting now...")
    sys.exit()

# Get user input for mass reporting
tiktok_url = input("Enter the TikTok video URL: ")
report_count = int(input("How many times do you want to report this video? "))

# Run mass reports
report_tiktok_video(tiktok_url, report_count)
