from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

# In-memory agent registry for deployment
class SimpleAgentRegistry:
    def __init__(self):
        self.agents = {}
        self.stats = {
            'totalAgents': 0,
            'activeAgents': 0,
            'agentsByRole': {},
            'healthyAgents': 0
        }
    
    def register_agent(self, contract):
        agent_id = str(uuid.uuid4())
        registration = {
            'registrationId': agent_id,
            'contract': contract,
            'status': 'active',
            'registeredAt': datetime.now().isoformat(),
            'healthStatus': 'healthy'
        }
        self.agents[agent_id] = registration
        self._update_stats()
        return agent_id
    
    def get_agent(self, agent_id):
        return self.agents.get(agent_id)
    
    def query_agents(self, filters):
        results = []
        for registration in self.agents.values():
            matches = True
            
            if filters.get('role') and registration['contract']['role'] != filters['role']:
                matches = False
            if filters.get('domain') and registration['contract']['agentMetadata'].get('domain') != filters['domain']:
                matches = False
            if filters.get('status') and registration['status'] != filters['status']:
                matches = False
            if filters.get('capability'):
                capabilities = registration['contract']['agentMetadata'].get('capabilities', [])
                if filters['capability'] not in capabilities:
                    matches = False
            
            if matches:
                results.append(registration)
        
        return results
    
    def remove_agent(self, agent_id):
        if agent_id in self.agents:
            del self.agents[agent_id]
            self._update_stats()
            return True
        return False
    
    def _update_stats(self):
        self.stats = {
            'totalAgents': len(self.agents),
            'activeAgents': sum(1 for a in self.agents.values() if a['status'] == 'active'),
            'agentsByRole': {},
            'healthyAgents': sum(1 for a in self.agents.values() if a['healthStatus'] == 'healthy')
        }
        
        for registration in self.agents.values():
            role = registration['contract']['role']
            self.stats['agentsByRole'][role] = self.stats['agentsByRole'].get(role, 0) + 1

# Initialize registry
registry = SimpleAgentRegistry()

# Bootstrap agent registration
bootstrap_agent = {
    "agentMetadata": {
        "id": "bootstrap-agent-001",
        "name": "NexusAI Bootstrap Agent",
        "version": "1.0.0",
        "capabilities": ["system-initialization", "health-monitoring", "basic-processing"],
        "domain": "system",
        "description": "Bootstrap agent for initial system validation and testing",
        "author": "NexusAI Runtime"
    },
    "role": "MONITOR",
    "endpoints": {
        "health": "/bootstrap/health",
        "execute": "/bootstrap/execute",
        "status": "/bootstrap/status"
    },
    "configuration": {
        "monitoringInterval": 10000,
        "autoStart": True,
        "logLevel": "info"
    }
}

# Register bootstrap agent
bootstrap_id = registry.register_agent(bootstrap_agent)

# Flask API routes

@app.route('/self-healing.js')
def self_healing_js():
    with open('src/templates/self-healing.js', 'r') as f:
        content = f.read()
    return content, 200, {'Content-Type': 'application/javascript'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api_info():
    return jsonify({
        'name': 'NexusAI Runtime API',
        'version': '0.1.0',
        'status': 'deployed',
        'registry': 'active',
        'agentsReady': registry.stats['totalAgents'],
        'bootstrapAgent': bootstrap_id,
        'endpoints': {
            'health': '/health',
            'register': 'POST /agents/register',
            'get_agent': 'GET /agents/:id',
            'query': 'GET /agents/query',
            'delete': 'DELETE /agents/:id',
            'stats': '/registry/stats',
            'schema': '/schema'
        },
        'documentation': 'https://github.com/srbryant86/nexusai-runtime-'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '0.1.0',
        'registry': 'active',
        'agentsReady': registry.stats['totalAgents']
    })

@app.route('/agents/register', methods=['POST'])
def register_agent():
    try:
        contract = request.get_json()
        if not contract:
            return jsonify({'success': False, 'error': 'No contract provided'}), 400
        
        # Basic validation
        if 'agentMetadata' not in contract or 'role' not in contract:
            return jsonify({'success': False, 'error': 'Invalid contract format'}), 400
        
        registration_id = registry.register_agent(contract)
        
        return jsonify({
            'success': True,
            'registrationId': registration_id,
            'message': 'Agent registered successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/agents/<agent_id>')
def get_agent(agent_id):
    agent = registry.get_agent(agent_id)
    
    if not agent:
        return jsonify({
            'success': False,
            'error': 'Agent not found'
        }), 404
    
    return jsonify({
        'success': True,
        'agent': agent
    })

@app.route('/agents/query')
def query_agents():
    filters = {
        'role': request.args.get('role'),
        'domain': request.args.get('domain'),
        'capability': request.args.get('capability'),
        'status': request.args.get('status')
    }
    
    # Remove None filters
    filters = {k: v for k, v in filters.items() if v is not None}
    
    agents = registry.query_agents(filters)
    
    return jsonify({
        'success': True,
        'count': len(agents),
        'agents': agents
    })

@app.route('/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    removed = registry.remove_agent(agent_id)
    
    if not removed:
        return jsonify({
            'success': False,
            'error': 'Agent not found'
        }), 404
    
    return jsonify({
        'success': True,
        'message': 'Agent removed successfully'
    })

@app.route('/registry/stats')
def registry_stats():
    return jsonify({
        'success': True,
        'stats': registry.stats
    })

@app.route('/schema')
def get_schema():
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "AgentContract",
        "type": "object",
        "properties": {
            "agentMetadata": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "version": {"type": "string"},
                    "capabilities": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "domain": {"type": "string"}
                },
                "required": ["id", "name", "version", "capabilities"]
            },
            "role": {
                "type": "string",
                "enum": ["PROCESSOR", "GENERATOR", "VALIDATOR", "ORCHESTRATOR", "MONITOR"]
            }
        },
        "required": ["agentMetadata", "role"]
    }
    
    return jsonify({
        'success': True,
        'schema': schema
    })

if __name__ == '__main__':
    print(f"NexusAI Runtime initialized with bootstrap agent: {bootstrap_id}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)

