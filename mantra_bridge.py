from flask import Flask, request, Response
from flask_cors import CORS
import requests
import sys

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS", "RDSERVICE", "DEVICEINFO", "CAPTURE"],
        "allow_headers": ["Content-Type", "Accept", "Origin"]
    }
})

MANTRA_URL = "http://127.0.0.1:11100"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'RDSERVICE', 'DEVICEINFO', 'CAPTURE', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'RDSERVICE', 'DEVICEINFO', 'CAPTURE', 'OPTIONS'])
def proxy(path=''):
    """Proxy all requests to Mantra RD Service"""
    
    # Handle browser GET request to root - show status page
    if request.method == 'GET' and path == '':
        return Response("""
<!DOCTYPE html>
<html>
<head>
    <title>Mantra Bridge - Running</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .status { padding: 20px; border-radius: 8px; margin: 20px 0; }
        .running { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .info { background-color: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
        h1 { color: #333; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>🔐 SV Recharge - Mantra Bridge</h1>
    <div class="status running">
        <strong>✅ Bridge Status: RUNNING</strong>
        <p>The bridge is running on port 8765</p>
    </div>
    <div class="status info">
        <strong>ℹ️ Connection Info:</strong>
        <ul>
            <li>Bridge Server: <code>http://127.0.0.1:8765</code></li>
            <li>Mantra Service: <code>http://127.0.0.1:11100</code></li>
        </ul>
    </div>
    <div class="info">
        <h3>Instructions:</h3>
        <ol>
            <li>Keep this window running</li>
            <li>Open Mantra RD Service app</li>
            <li>Connect your biometric device</li>
            <li>Open svrecharge.in in your browser</li>
        </ol>
    </div>
</body>
</html>
        """, mimetype='text/html')
    
    try:
        # Handle preflight OPTIONS request
        if request.method == 'OPTIONS':
            response = Response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, RDSERVICE, DEVICEINFO, CAPTURE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
            return response
        
        # Build target URL
        url = f"{MANTRA_URL}/{path}" if path else MANTRA_URL
        
        print(f"📡 Proxying {request.method} -> {url}")
        
        # Forward the request to Mantra RD Service
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key.lower() not in ['host', 'connection']},
            data=request.get_data(),
            allow_redirects=False,
            timeout=30
        )
        
        # Create response with CORS headers
        response = Response(
            resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, RDSERVICE, DEVICEINFO, CAPTURE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
        
        print(f"✅ Response: {resp.status_code}")
        return response
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Mantra RD Service on port 11100")
        
        # Return HTML error page for browser, JSON for API calls
        if 'text/html' in request.headers.get('Accept', ''):
            return Response("""
<!DOCTYPE html>
<html>
<head>
    <title>Mantra Service Not Found</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .error { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="error">
        <h2>⚠️ Cannot Connect to Mantra RD Service</h2>
        <p>Please ensure:</p>
        <ol>
            <li>Mantra RD Service app is running</li>
            <li>Device is connected via OTG</li>
            <li>RD Service shows 'READY' status</li>
        </ol>
    </div>
</body>
</html>
            """, status=503, mimetype='text/html')
        else:
            return Response(
                "Cannot connect to Mantra RD Service. Please ensure:\n"
                "1. Mantra RD Service app is running\n"
                "2. Device is connected\n"
                "3. RD Service shows 'READY' status",
                status=503,
                headers={'Access-Control-Allow-Origin': '*'}
            )
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return Response(
            f"Error: {str(e)}",
            status=500,
            headers={'Access-Control-Allow-Origin': '*'}
        )

def check_mantra_service():
    """Check if Mantra RD Service is running"""
    try:
        resp = requests.get(f"{MANTRA_URL}", timeout=2)
        return True
    except:
        return False

def print_banner():
    """Print startup banner"""
    print("\n" + "="*60)
    print("  🔐 SV Recharge - Mantra Biometric Bridge")
    print("="*60)
    print(f"  Bridge Server: http://127.0.0.1:8765")
    print(f"  Mantra Service: {MANTRA_URL}")
    print("="*60)
    
    # Check Mantra service
    print("\n🔍 Checking Mantra RD Service...")
    if check_mantra_service():
        print("✅ Mantra RD Service is running!")
    else:
        print("⚠️  Mantra RD Service not detected")
        print("   Please start Mantra RD Service app")
    
    print("\n📱 Ready to accept requests from svrecharge.in")
    print("   Keep this window open while using the website")
    print("   Test in browser: http://127.0.0.1:8765")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    print_banner()
    
    try:
        # Run Flask server
        app.run(
            host='127.0.0.1',
            port=8765,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Mantra Bridge stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        input("Press Enter to exit...")
        sys.exit(1)