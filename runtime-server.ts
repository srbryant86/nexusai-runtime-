import express from 'express';
import cors from 'cors';
import { AgentRegistry } from './AgentRegistry';
import * as fs from 'fs';
import * as path from 'path';

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Agent Registry
const registry = new AgentRegistry();

// API Routes

// Register a new agent
app.post('/agents/register', (req, res) => {
  try {
    const contract = req.body;
    const registrationId = registry.registerAgent(contract);
    
    res.status(201).json({
      success: true,
      registrationId,
      message: 'Agent registered successfully'
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: error instanceof Error ? error.message : 'Registration failed'
    });
  }
});

// Get agent by ID
app.get('/agents/:id', (req, res) => {
  const { id } = req.params;
  const agent = registry.getAgent(id);
  
  if (!agent) {
    return res.status(404).json({
      success: false,
      error: 'Agent not found'
    });
  }
  
  return res.json({
    success: true,
    agent
  });
});

// Query agents with filters
app.get('/agents/query', (req, res) => {
  const filters = {
    role: req.query.role as string,
    domain: req.query.domain as string,
    capability: req.query.capability as string,
    status: req.query.status as string
  };
  
  // Remove undefined filters
  Object.keys(filters).forEach(key => {
    if (filters[key as keyof typeof filters] === undefined) {
      delete filters[key as keyof typeof filters];
    }
  });
  
  const agents = registry.queryAgents(filters);
  
  return res.json({
    success: true,
    count: agents.length,
    agents
  });
});

// Remove agent
app.delete('/agents/:id', (req, res) => {
  const { id } = req.params;
  const removed = registry.removeAgent(id);
  
  if (!removed) {
    return res.status(404).json({
      success: false,
      error: 'Agent not found'
    });
  }
  
  return res.json({
    success: true,
    message: 'Agent removed successfully'
  });
});

// Get registry statistics
app.get('/registry/stats', (req, res) => {
  const stats = registry.getRegistryStats();
  
  res.json({
    success: true,
    stats
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '0.1.0',
    registry: 'active'
  });
});

// Get schema
app.get('/schema', (req, res) => {
  try {
    const schemaPath = path.join(__dirname, 'agent-contract-schema.json');
    const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
    
    res.json({
      success: true,
      schema
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Failed to load schema'
    });
  }
});

// Bootstrap function
async function bootstrap() {
  try {
    // Start monitoring
    registry.startMonitoring();
    
    // Load and register bootstrap agent if it exists
    const bootstrapPath = path.join(__dirname, 'bootstrap-agent.json');
    if (fs.existsSync(bootstrapPath)) {
      const bootstrapAgent = JSON.parse(fs.readFileSync(bootstrapPath, 'utf8'));
      const registrationId = registry.registerAgent(bootstrapAgent);
      
      console.log(`Bootstrap agent registered with ID: ${registrationId}`);
      
      return {
        registrationId,
        status: 'active'
      };
    }
    
    return {
      registrationId: null,
      status: 'no-bootstrap-agent'
    };
  } catch (error) {
    console.error('Bootstrap failed:', error);
    return {
      registrationId: null,
      status: 'error',
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

// Start server
app.listen(port, async () => {
  console.log(`NexusAI Runtime Server running on port ${port}`);
  
  // Perform bootstrap
  const bootstrapResult = await bootstrap();
  
  // Log deployment confirmation
  const deploymentInfo = {
    status: "deployed",
    registry: "active",
    agentsReady: registry.getRegistryStats().totalAgents,
    version: "0.1.0",
    source: "nexusai-runtime.zip",
    bootstrap: bootstrapResult
  };
  
  console.log('Deployment Confirmation:', JSON.stringify(deploymentInfo, null, 2));
});

export { app, registry };

