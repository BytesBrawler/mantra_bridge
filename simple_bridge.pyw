from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import sys

class ProxyHandler(BaseHTTPRequestHandler):
    
    # Override to handle ANY method name
    def handle_one_request(self):
        """Override to accept any HTTP method"""
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                return
            
            # Route all methods to our handler
            self.handle_request()
            
        except Exception as e:
            pass  # Silent in background
    
    def handle_request(self):
        """Handle any HTTP method"""
        # Show status page for GET /
        if self.command == 'GET' and self.path in ['/', '']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<head>
    <title>Mantra Bridge - Running</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 900px; 
            margin: 50px auto; 
            padding: 20px; 
            background: #f5f5f5; 
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .status { 
            padding: 20px; 
            border-radius: 8px; 
            margin: 20px 0; 
            background: white; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        }
        .running { 
            border-left: 4px solid #28a745; 
        }
        .downloads {
            border-left: 4px solid #007bff;
        }
        .instructions {
            border-left: 4px solid #ffc107;
        }
        h1 { 
            color: #333; 
            margin: 0;
        }
        h2 {
            color: #333;
            font-size: 20px;
            margin-top: 0;
        }
        .badge { 
            background: #28a745; 
            color: white; 
            padding: 6px 12px; 
            border-radius: 4px; 
            font-size: 14px;
            font-weight: bold;
        }
        .download-btn {
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            margin: 10px 10px 10px 0;
            font-weight: bold;
            transition: background 0.3s;
        }
        .download-btn:hover {
            background: #0056b3;
        }
        .download-item {
            background: #f8f9fa;
            padding: 15px;
            margin: 15px 0;
            border-radius: 6px;
            border: 1px solid #dee2e6;
        }
        .download-item h3 {
            margin: 0 0 8px 0;
            color: #333;
            font-size: 16px;
        }
        .download-item p {
            margin: 0 0 10px 0;
            color: #666;
            font-size: 14px;
        }
        .step-number {
            display: inline-block;
            background: #007bff;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            margin-right: 10px;
        }
        ol {
            padding-left: 20px;
        }
        li {
            margin: 10px 0;
            line-height: 1.6;
        }
        .note {
            background: #fff3cd;
            border: 1px solid #ffeeba;
            padding: 12px;
            border-radius: 6px;
            margin: 15px 0;
        }
        .note strong {
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔐 SV Recharge - Mantra Bridge</h1>
    </div>

    <div class="status running">
        <h2><span class="badge">✅ RUNNING</span> Bridge Status</h2>
        <p>Bridge is active on port 8765 and ready to connect your biometric device with svrecharge.in</p>
        <p><strong>Running in background - No window needed!</strong></p>
    </div>

    <div class="status downloads">
        <h2>📥 Required Downloads</h2>
        <p>Before using your biometric device, please install these components:</p>
        
        <div class="download-item">
            <h3><span class="step-number">1</span>MFS110 Device Driver</h3>
            <p>Install this driver first to enable your computer to recognize the Mantra fingerprint device.</p>
            <a href="https://www.mantratec.com/Download/Uploads/Setup/MFS110Driver_2.0.0.0.exe" 
               class="download-btn" 
               target="_blank">
                ⬇️ Download Driver (MFS110Driver_2.0.0.0.exe)
            </a>
        </div>

        <div class="download-item">
            <h3><span class="step-number">2</span>Mantra RD Service</h3>
            <p>Install this service to communicate with your fingerprint device. Must be running while using the device.</p>
            <a href="https://www.mantratec.com/Download/Uploads/Setup/MantraL1RDService_1.4.1.exe" 
               class="download-btn" 
               target="_blank">
                ⬇️ Download RD Service (MantraL1RDService_1.4.1.exe)
            </a>
        </div>

        <div class="note">
            <strong>⚠️ Note:</strong> You already have the Mantra Bridge installed. Just download and install the two files above if you haven't already.
        </div>
    </div>

    <div class="status instructions">
        <h2>📋 Setup Instructions</h2>
        <ol>
            <li><strong>Install Driver:</strong> Download and run MFS110Driver_2.0.0.0.exe</li>
            <li><strong>Install RD Service:</strong> Download and run MantraL1RDService_1.4.1.exe</li>
            <li><strong>Connect Device:</strong> Plug in your Mantra fingerprint device via OTG cable</li>
            <li><strong>Start RD Service:</strong> Open "Mantra RD Service" app from Start Menu</li>
            <li><strong>Wait for Green Status:</strong> All checks in the RD Service app should show GREEN/READY</li>
            <li><strong>Bridge Runs in Background:</strong> No window needed - runs automatically!</li>
            <li><strong>Use Website:</strong> Open <strong>svrecharge.in</strong> in Chrome or Edge</li>
            <li><strong>Start Using:</strong> Your biometric device will now work with the website!</li>
        </ol>
    </div>

    <div class="status">
        <h2>🔧 Troubleshooting</h2>
        <ul>
            <li><strong>Device not detected?</strong> Make sure driver is installed and device is plugged in</li>
            <li><strong>RD Service shows red?</strong> Restart the RD Service app after installing driver</li>
            <li><strong>Website can't connect?</strong> Make sure MantraBridge.exe is running (check Task Manager)</li>
            <li><strong>Still having issues?</strong> Try restarting your computer after installing everything</li>
        </ul>
    </div>

    <div class="status" style="text-align: center; color: #666;">
        <p>Bridge Server: <code>http://127.0.0.1:8765</code> | Mantra Service: <code>http://127.0.0.1:11100</code></p>
        <p style="font-size: 12px; margin-top: 10px;">Bridge runs in background - check Task Manager to see if running</p>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
            
        # Handle OPTIONS (CORS preflight)
        elif self.command == 'OPTIONS':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.end_headers()
            
        # Forward everything else to Mantra RD Service
        else:
            self.proxy_request()
    
    def proxy_request(self):
        try:
            url = f"http://127.0.0.1:11100{self.path}"
            
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
                
        except urllib.error.URLError as e:
            self.send_response(503)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<body style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px;">
    <h2 style="color: #dc3545;">⚠️ Cannot Connect to Mantra RD Service</h2>
    <p>Please ensure:</p>
    <ol>
        <li><strong>Driver is installed:</strong> <a href="https://www.mantratec.com/Download/Uploads/Setup/MFS110Driver_2.0.0.0.exe">Download Driver</a></li>
        <li><strong>RD Service is installed:</strong> <a href="https://www.mantratec.com/Download/Uploads/Setup/MantraL1RDService_1.4.1.exe">Download RD Service</a></li>
        <li><strong>RD Service app is running</strong> (open from Start Menu)</li>
        <li><strong>Device is connected</strong> via OTG cable</li>
        <li><strong>Service shows READY status</strong> (green indicators)</li>
    </ol>
    <p><a href="/">← Back to Bridge Home</a></p>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
    
    def log_message(self, format, *args):
        """Disable console logging"""
        pass

if __name__ == '__main__':
    try:
        server = HTTPServer(('127.0.0.1', 8765), ProxyHandler)
        server.serve_forever()
    except:
        sys.exit(1)