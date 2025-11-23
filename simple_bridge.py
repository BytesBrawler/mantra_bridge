from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import sys

class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), format % args))
    
    def do_GET(self):
        if self.path == '/' or self.path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<head>
    <title>Mantra Bridge - Running</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        .status { padding: 20px; border-radius: 8px; margin: 20px 0; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .running { border-left: 4px solid #28a745; }
        h1 { color: #333; }
        .badge { background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <h1>SV Recharge - Mantra Bridge</h1>
    <div class="status running">
        <strong><span class="badge">RUNNING</span></strong>
        <p>Bridge is active on port 8765</p>
    </div>
    <div class="status">
        <h3>Instructions:</h3>
        <ol>
            <li>Keep this bridge running</li>
            <li>Open Mantra RD Service app</li>
            <li>Connect biometric device</li>
            <li>Open <strong>svrecharge.in</strong></li>
        </ol>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
        else:
            self.proxy_request()
    
    def do_POST(self):
        self.proxy_request()
    
    def do_RDSERVICE(self):
        self.proxy_request()
    
    def do_DEVICEINFO(self):
        self.proxy_request()
    
    def do_CAPTURE(self):
        self.proxy_request()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
    
    def proxy_request(self):
        try:
            url = f"http://127.0.0.1:11100{self.path}"
            print(f"Proxying {self.command} -> {url}")
            
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len) if content_len > 0 else None
            
            req = urllib.request.Request(url, data=body, method=self.command)
            for key, value in self.headers.items():
                if key.lower() not in ['host', 'connection']:
                    req.add_header(key, value)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                self.send_response(response.status)
                for key, value in response.headers.items():
                    self.send_header(key, value)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', '*')
                self.send_header('Access-Control-Allow-Headers', '*')
                self.end_headers()
                self.wfile.write(response.read())
                print(f"Response: {response.status}")
                
        except urllib.error.URLError as e:
            print(f"Cannot connect to Mantra RD Service: {e}")
            self.send_response(503)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<body>
    <h2>Cannot Connect to Mantra RD Service</h2>
    <p>Please ensure:</p>
    <ol>
        <li>Mantra RD Service app is running</li>
        <li>Device is connected</li>
        <li>Service shows READY status</li>
    </ol>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
        except Exception as e:
            print(f"Error: {str(e)}")
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))

def print_banner():
    print("\n" + "="*60)
    print("  SV Recharge - Mantra Biometric Bridge")
    print("="*60)
    print("  Bridge Server: http://127.0.0.1:8765")
    print("  Mantra Service: http://127.0.0.1:11100")
    print("="*60)
    print("\n  Ready to accept requests from svrecharge.in")
    print("  Test in browser: http://127.0.0.1:8765")
    print("  Keep this window open while using the website\n")
    print("="*60 + "\n")

if __name__ == '__main__':
    print_banner()
    try:
        server = HTTPServer(('127.0.0.1', 8765), ProxyHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nMantra Bridge stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\nFailed to start server: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
