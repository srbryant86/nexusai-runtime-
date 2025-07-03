import Ajv from 'ajv';
import { v4 as uuidv4 } from 'uuid';

interface AgentContract {
  agentMetadata: {
    id: string;
    name: string;
    version: string;
    capabilities: string[];
    domain?: string;
  };
  role: 'PROCESSOR' | 'GENERATOR' | 'VALIDATOR' | 'ORCHESTRATOR' | 'MONITOR';
  endpoints?: {
    health: string;
    execute: string;
    status: string;
  };
  configuration?: Record<string, any>;
}

interface AgentRegistration {
  registrationId: string;
  contract: AgentContract;
  status: 'active' | 'inactive' | 'error';
  registeredAt: Date;
  lastHealthCheck?: Date;
  healthStatus?: 'healthy' | 'unhealthy' | 'unknown';
}

export class AgentRegistry {
  private agents: Map<string, AgentRegistration> = new Map();
  private ajv: Ajv;
  private schema: any;
  private monitoringActive: boolean = false;

  constructor() {
    this.ajv = new Ajv({ allErrors: true, verbose: true });
    this.loadSchema();
  }

  private loadSchema() {
    // Load the agent contract schema
    this.schema = {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "AgentContract",
      "type": "object",
      "properties": {
        "agentMetadata": {
          "type": "object",
          "properties": {
            "id": { "type": "string" },
            "name": { "type": "string" },
            "version": { "type": "string" },
            "capabilities": {
              "type": "array",
              "items": { "type": "string" }
            },
            "domain": { "type": "string" },
            "description": { "type": "string" },
            "author": { "type": "string" },
            "tags": {
              "type": "array",
              "items": { "type": "string" }
            }
          },
          "required": ["id", "name", "version", "capabilities"]
        },
        "role": {
          "type": "string",
          "enum": ["PROCESSOR", "GENERATOR", "VALIDATOR", "ORCHESTRATOR", "MONITOR"]
        },
        "endpoints": {
          "type": "object",
          "properties": {
            "health": { "type": "string" },
            "execute": { "type": "string" },
            "status": { "type": "string" },
            "metrics": { "type": "string" }
          }
        },
        "configuration": { "type": "object" },
        "requirements": {
          "type": "object",
          "properties": {
            "memory": { "type": "string" },
            "cpu": { "type": "string" },
            "dependencies": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        },
        "security": {
          "type": "object",
          "properties": {
            "permissions": {
              "type": "array",
              "items": { "type": "string" }
            },
            "authentication": {
              "type": "string",
              "enum": ["none", "api-key", "oauth", "certificate"]
            }
          }
        }
      },
      "required": ["agentMetadata", "role"]
    };

    this.ajv.addSchema(this.schema, 'agent-contract');
  }

  public registerAgent(contract: AgentContract): string {
    // Validate contract against schema
    const validate = this.ajv.getSchema('agent-contract');
    if (!validate || !validate(contract)) {
      throw new Error(`Invalid agent contract: ${this.ajv.errorsText(validate?.errors)}`);
    }

    // Generate registration ID
    const registrationId = uuidv4();

    // Create registration record
    const registration: AgentRegistration = {
      registrationId,
      contract,
      status: 'active',
      registeredAt: new Date(),
      healthStatus: 'unknown'
    };

    // Store in registry
    this.agents.set(registrationId, registration);

    console.log(`Agent registered: ${contract.agentMetadata.name} (${registrationId})`);
    return registrationId;
  }

  public getAgent(registrationId: string): AgentRegistration | undefined {
    return this.agents.get(registrationId);
  }

  public queryAgents(filters: {
    role?: string;
    domain?: string;
    capability?: string;
    status?: string;
  }): AgentRegistration[] {
    const results: AgentRegistration[] = [];

    for (const registration of this.agents.values()) {
      let matches = true;

      if (filters.role && registration.contract.role !== filters.role) {
        matches = false;
      }

      if (filters.domain && registration.contract.agentMetadata.domain !== filters.domain) {
        matches = false;
      }

      if (filters.capability && 
          !registration.contract.agentMetadata.capabilities.includes(filters.capability)) {
        matches = false;
      }

      if (filters.status && registration.status !== filters.status) {
        matches = false;
      }

      if (matches) {
        results.push(registration);
      }
    }

    return results;
  }

  public removeAgent(registrationId: string): boolean {
    return this.agents.delete(registrationId);
  }

  public startMonitoring(): void {
    this.monitoringActive = true;
    console.log('Agent monitoring started');
    
    // Start health check interval
    setInterval(() => {
      this.performHealthChecks();
    }, 30000); // Every 30 seconds
  }

  public stopMonitoring(): void {
    this.monitoringActive = false;
    console.log('Agent monitoring stopped');
  }

  private async performHealthChecks(): Promise<void> {
    if (!this.monitoringActive) return;

    for (const [id, registration] of this.agents.entries()) {
      try {
        const healthStatus = await this.checkAgentHealth(registration);
        registration.healthStatus = healthStatus;
        registration.lastHealthCheck = new Date();
        
        if (healthStatus === 'unhealthy') {
          registration.status = 'error';
          console.warn(`Agent ${registration.contract.agentMetadata.name} is unhealthy`);
        }
      } catch (error) {
        registration.healthStatus = 'unhealthy';
        registration.status = 'error';
        console.error(`Health check failed for agent ${id}:`, error);
      }
    }
  }

  private async checkAgentHealth(registration: AgentRegistration): Promise<'healthy' | 'unhealthy'> {
    // Simulate health check - in real implementation would call agent's health endpoint
    if (registration.contract.endpoints?.health) {
      // Would make HTTP request to health endpoint
      return Math.random() > 0.1 ? 'healthy' : 'unhealthy';
    }
    return 'healthy';
  }

  public getRegistryStats(): {
    totalAgents: number;
    activeAgents: number;
    agentsByRole: Record<string, number>;
    healthyAgents: number;
  } {
    const stats = {
      totalAgents: this.agents.size,
      activeAgents: 0,
      agentsByRole: {} as Record<string, number>,
      healthyAgents: 0
    };

    for (const registration of this.agents.values()) {
      if (registration.status === 'active') {
        stats.activeAgents++;
      }

      const role = registration.contract.role;
      stats.agentsByRole[role] = (stats.agentsByRole[role] || 0) + 1;

      if (registration.healthStatus === 'healthy') {
        stats.healthyAgents++;
      }
    }

    return stats;
  }
}

