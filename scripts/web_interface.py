#!/usr/bin/env python3
"""
Bittensor Subnet Updater Web Interface

A simple web interface to view subnet data and profiles locally.
Run this script and visit http://localhost:8000 to view the subnet information.
"""

import json
import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import threading
import time

# File paths
SUBNETS_JSON = Path("data/subnets.json")
PROFILES_DIR = Path("data/profiles")
OUTPUT_DIR = Path("web_output")
OUTPUT_DIR.mkdir(exist_ok=True)

def create_index_html():
    """Create the main index.html file for the web interface."""
    
    # Read subnet data
    if not SUBNETS_JSON.exists():
        return create_error_html("No subnet data found. Please run 'python scripts/fetch_subnets_bt.py' first.")
    
    with open(SUBNETS_JSON, 'r') as f:
        data = json.load(f)
    
    subnets = data.get("subnets", [])
    
    # Create HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bittensor Subnet Updater</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .subnets-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .subnet-card {{
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .subnet-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .subnet-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .subnet-id {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }}
        .status {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        .status.active {{
            background: #d4edda;
            color: #155724;
        }}
        .status.inactive {{
            background: #f8d7da;
            color: #721c24;
        }}
        .status.unknown {{
            background: #fff3cd;
            color: #856404;
        }}
        .subnet-info {{
            font-size: 0.9em;
            color: #666;
        }}
        .subnet-info div {{
            margin: 5px 0;
        }}
        .price {{
            font-weight: bold;
            color: #28a745;
        }}
        .owner {{
            font-family: monospace;
            font-size: 0.8em;
            word-break: break-all;
        }}
        .view-profile {{
            margin-top: 15px;
        }}
        .view-profile a {{
            display: inline-block;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.9em;
            transition: background 0.2s;
        }}
        .view-profile a:hover {{
            background: #5a6fd8;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        .refresh-btn {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            font-size: 0.9em;
        }}
        .refresh-btn:hover {{
            background: #218838;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Bittensor Subnet Updater</h1>
            <p>Live subnet data from the Bittensor blockchain</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(subnets)}</div>
                <div class="stat-label">Total Subnets</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(1 for s in subnets if s.get('is_active') is True)}</div>
                <div class="stat-label">Active Subnets</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(1 for s in subnets if s.get('is_active') is False)}</div>
                <div class="stat-label">Inactive Subnets</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{data.get('timestamp', 'N/A')}</div>
                <div class="stat-label">Last Updated</div>
            </div>
        </div>
        
        <div class="subnets-grid">
"""
    
    # Add subnet cards
    for subnet in subnets:
        subnet_id = subnet.get("id", "Unknown")
        name = subnet.get("name", f"Subnet {subnet_id}")
        is_active = subnet.get("is_active")
        price = subnet.get("price", 0)
        owner = subnet.get("owner_hotkey", "Unknown")
        
        # Determine status
        if is_active is True:
            status_class = "active"
            status_text = "✅ Active"
        elif is_active is False:
            status_class = "inactive"
            status_text = "⚠️ Inactive"
        else:
            status_class = "unknown"
            status_text = "🔄 Unknown"
        
        html_content += f"""
            <div class="subnet-card">
                <div class="subnet-header">
                    <div class="subnet-id">{name}</div>
                    <div class="status {status_class}">{status_text}</div>
                </div>
                <div class="subnet-info">
                    <div><strong>ID:</strong> {subnet_id}</div>
                    <div><strong>Price:</strong> <span class="price">{price:.6f} TAO</span></div>
                    <div><strong>Owner:</strong> <span class="owner">{owner}</span></div>
                    <div><strong>Exists:</strong> {subnet.get('exists', 'Unknown')}</div>
                </div>
                <div class="view-profile">
                    <a href="profiles/{subnet_id}_subnet-{subnet_id}.html" target="_blank">View Profile</a>
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>Data source: Bittensor Subtensor SDK (Finney network) - Public data only</p>
            <p>Generated on: """ + time.strftime('%Y-%m-%d %H:%M:%S') + """</p>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
</body>
</html>
"""
    
    return html_content

def create_profile_html(subnet_id, profile_content):
    """Convert Markdown profile to HTML."""
    
    # Better Markdown to HTML conversion
    html_content = profile_content
    
    # Convert headers
    html_content = html_content.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
    html_content = html_content.replace('## ', '<h2>').replace('\n', '</h2>\n')
    html_content = html_content.replace('### ', '<h3>').replace('\n', '</h3>\n')
    
    # Convert bold text (handle multiple instances)
    import re
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    
    # Convert lists - wrap in <ul> tags
    lines = html_content.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    html_content = '\n'.join(result_lines)
    
    # Convert code blocks
    html_content = html_content.replace('`', '<code>').replace('`', '</code>')
    
    # Convert line breaks
    html_content = html_content.replace('\n', '<br>\n')
    
    # Wrap in HTML structure
    full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subnet {subnet_id} Profile</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        h1 {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        h3 {{ color: #666; }}
        code {{ background: #f8f9fa; padding: 2px 4px; border-radius: 3px; font-family: monospace; }}
        ul {{ margin: 10px 0; padding-left: 20px; }}
        li {{ margin: 5px 0; }}
        .back-btn {{
            display: inline-block;
            margin-bottom: 20px;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }}
        .back-btn:hover {{ background: #5a6fd8; }}
        .placeholder {{ 
            color: #999; 
            font-style: italic; 
            background: #f8f9fa; 
            padding: 2px 4px; 
            border-radius: 3px; 
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-btn">← Back to Subnet List</a>
        {html_content}
    </div>
</body>
</html>
"""
    
    return full_html

def create_error_html(message):
    """Create an error page."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Bittensor Subnet Updater</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .error-container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
        }}
        h1 {{ color: #dc3545; }}
        p {{ color: #666; margin: 20px 0; }}
        .code {{
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <h1>⚠️ Error</h1>
        <p>{message}</p>
        <div class="code">python scripts/fetch_subnets_bt.py</div>
        <p>Then refresh this page.</p>
    </div>
</body>
</html>
"""

def generate_web_files():
    """Generate all web files."""
    print("Generating web interface...")
    
    # Create profiles subdirectory
    profiles_output_dir = OUTPUT_DIR / "profiles"
    profiles_output_dir.mkdir(exist_ok=True)
    
    # Create main index.html
    index_html = create_index_html()
    with open(OUTPUT_DIR / "index.html", 'w') as f:
        f.write(index_html)
    
    # Convert profile files to HTML
    if PROFILES_DIR.exists():
        for profile_file in PROFILES_DIR.glob("*.md"):
            with open(profile_file, 'r') as f:
                profile_content = f.read()
            
            # Extract subnet ID from filename
            subnet_id = profile_file.stem.split('_')[0]
            
            # Convert to HTML
            html_content = create_profile_html(subnet_id, profile_content)
            
            # Save HTML file in profiles subdirectory
            html_filename = profile_file.stem + ".html"
            with open(profiles_output_dir / html_filename, 'w') as f:
                f.write(html_content)
    
    print(f"Web interface generated in {OUTPUT_DIR}/")
    print("Files created:")
    print(f"  - index.html")
    if profiles_output_dir.exists():
        for file in profiles_output_dir.glob("*.html"):
            print(f"  - profiles/{file.name}")

def start_server():
    """Start the local web server."""
    os.chdir(OUTPUT_DIR)
    
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print(f"\n🌐 Web interface is running at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    # Open browser automatically
    threading.Timer(1.0, lambda: webbrowser.open('http://localhost:8000')).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        httpd.shutdown()

def main():
    """Main function."""
    print("🚀 Starting Bittensor Subnet Updater Web Interface")
    
    # Generate web files
    generate_web_files()
    
    # Start web server
    start_server()

if __name__ == "__main__":
    main()
