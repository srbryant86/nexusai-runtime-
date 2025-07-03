# NexusAI Runtime

Complete agent registry logic, contract enforcement schemas, orchestration methods, LiveShell preview interface, and structural documentation. This marks the baseline runtime deployment for NexusAI agent execution and validation.

## 🚀 Features

- **Agent Registry**: Complete TypeScript implementation with schema validation
- **Contract Enforcement**: JSON Schema validation with AJV
- **LiveShell Interface**: Real-time control panel for agent monitoring
- **REST API**: Full HTTP API for agent management
- **Health Monitoring**: Continuous agent health checks and status tracking

## 📦 Installation

### Dependencies

```bash
npm install ajv uuid
```

Required Node modules:
- `ajv` (JSON Schema validator)
- `uuid` (for registration ID generation)

### Setup

1. Clone this repository
2. Install dependencies: `npm install`
3. Build TypeScript: `npm run build`
4. Start the runtime: `npm start`

## 🔧 API Endpoints

- **POST /agents/register** - Register new agents
- **GET /agents/:id** - Get agent by ID
- **GET /agents/query** - Query agents with filters
- **DELETE /agents/:id** - Remove agents
- **GET /registry/stats** - Registry statistics
- **GET /health** - System health check
- **GET /schema** - Agent contract schema

## 🖥️ LiveShell Interface

Open `liveshell_preview_controlpanel_v2.html` in your browser for the real-time control interface.

## 📋 Agent Contract Schema

Agents must conform to the JSON schema defined in `agent-contract-schema.json`. Example:

```json
{
  "agentMetadata": {
    "id": "agent-001",
    "name": "Example Agent",
    "version": "1.0.0",
    "capabilities": ["processing", "analysis"],
    "domain": "data"
  },
  "role": "PROCESSOR",
  "endpoints": {
    "health": "/health",
    "execute": "/execute"
  }
}
```

## 🏗️ Architecture

- **AgentRegistry.ts**: Core registry implementation
- **runtime-server.ts**: HTTP server and API endpoints
- **agent-contract-schema.json**: Schema validation rules
- **bootstrap-agent.json**: Default system agent
- **src/main.py**: Flask wrapper for deployment

## 🌐 Deployment

The system includes both Node.js and Python Flask deployment options:

### Node.js (Development)
```bash
npm run dev
```

### Flask (Production)
```bash
python src/main.py
```

## 📊 Live Demo

**Permanent URL**: https://qjh9iecewogq.manus.space

## 🤖 Bootstrap Agent

The system automatically registers a bootstrap MONITOR agent for system initialization and health monitoring.

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Repository

https://github.com/srbryant86/nexusai-runtime-

