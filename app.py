from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/<package_name>")
def index(package_name:str):
    api_key = request.headers.get('key')
    
    if not api_key:
        return "API key is required", 401
    
    headers = {
        "X-API-Key": api_key
    }
    r = requests.get(f"https://api.pepy.tech/api/v2/projects/{package_name}", headers=headers)
    
    if r.status_code != 200:
        return "Invalid package", 404
    try:
        data = r.json()

        total_downloads = data["total_downloads"]
        
        last_day = list(data["downloads"].keys())[-1]
        last_day_downloads = sum(data["downloads"][last_day].values())
        
        return {
            "last_day_downloads": last_day_downloads,
            "total_downloads": total_downloads
        }
    except Exception as e:
        return f"ERROR: {e}", 500

if __name__ == "__main__":
    app.run()