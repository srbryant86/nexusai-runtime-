from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import subprocess
import requests
import json
import os
import signal
import atexit
import time
import threading

app = Flask(__name__)
CORS(app)

# Global variable to track Node.js process
node_process = None
node_port = 3002

def start_node_server():
    """Start the Node.js NexusAI Runtime server"""
    global node_process
    try:
        # Kill any existing process on the port
        subprocess.run(['pkill', '-f', 'runtime-server.js'], capture_output=True)
        time.sleep(1)
        
        # Start the Node.js server
        env = os.environ.copy()
        env['PORT'] = str(node_port)
        
        node_process = subprocess.Popen(
            ['node', 'dist/runtime-server.js'],
            cwd='/home/ubuntu/nexusai-runtime-deploy',
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test if server is running
        try:
            response = requests.get(f'http://localhost:{node_port}/health', timeout=5)
            if response.status_code == 200:
                print(f"NexusAI Runtime started successfully on port {node_port}")
                return True
        except:
            pass
            
        print("Failed to start NexusAI Runtime")
        return False
        
    except Exception as e:
        print(f"Error starting Node.js server: {e}")
        return False

def stop_node_server():
    """Stop the Node.js server"""
    global node_process
    if node_process:
        try:
            node_process.terminate()
            node_process.wait(timeout=5)
        except:
            try:
                node_process.kill()
            except:
                pass
        node_process = None

# Register cleanup function
atexit.register(stop_node_server)

# Proxy function to forward requests to Node.js server
def proxy_to_node(path, method='GET', data=None):
    """Proxy requests to the Node.js NexusAI Runtime"""
    try:
        url = f'http://localhost:{node_port}{path}'
        
        if method == 'GET':
            response = requests.get(url, params=request.args, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data or request.get_json(), timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=10)
        else:
            return jsonify({'error': 'Method not supported'}), 405
            
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'NexusAI Runtime unavailable',
            'details': str(e)
        }), 503

# Flask routes that proxy to Node.js

@app.route('/health')
def health():
    return proxy_to_node('/health')

@app.route('/agents/register', methods=['POST'])
def register_agent():
    return proxy_to_node('/agents/register', 'POST')

@app.route('/agents/<agent_id>')
def get_agent(agent_id):
    return proxy_to_node(f'/agents/{agent_id}')

@app.route('/agents/query')
def query_agents():
    return proxy_to_node('/agents/query')

@app.route('/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    return proxy_to_node(f'/agents/{agent_id}', 'DELETE')

@app.route('/registry/stats')
def registry_stats():
    return proxy_to_node('/registry/stats')

@app.route('/schema')
def get_schema():
    return proxy_to_node('/schema')

@app.route('/')
def index():
    return jsonify({
        'name': 'NexusAI Runtime API',
        'version': '0.1.0',
        'status': 'deployed',
        'registry': 'active',
        'endpoints': {
            'health': '/health',
            'register': 'POST /agents/register',
            'get_agent': 'GET /agents/:id',
            'query': 'GET /agents/query',
            'delete': 'DELETE /agents/:id',
            'stats': '/registry/stats',
            'schema': '/schema'
        },
        'documentation': 'https://github.com/nexusai/runtime'
    })

# Start Node.js server in a separate thread
def init_runtime():
    """Initialize the NexusAI Runtime"""
    print("Initializing NexusAI Runtime...")
    success = start_node_server()
    if success:
        print("NexusAI Runtime initialized successfully")
    else:
        print("Failed to initialize NexusAI Runtime")

# Start the runtime when Flask starts
threading.Thread(target=init_runtime, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)

