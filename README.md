# NexusAI Runtime

Complete agent runtime with LLM-powered contract enforcement, orchestration, metrics, and UI control panel.

## 🖥️ Desktop Application

Download the cross-platform NexusAI Runtime desktop client:

- **[Windows (.exe)](https://github.com/srbryant86/nexusai-runtime-/releases/latest/download/NexusAI-Runtime-Setup.exe)**
- **[macOS (.dmg)](https://github.com/srbryant86/nexusai-runtime-/releases/latest/download/NexusAI-Runtime.dmg)**
- **[Linux (.AppImage)](https://github.com/srbryant86/nexusai-runtime-/releases/latest/download/NexusAI-Runtime.AppImage)**
- **[Web Dashboard](https://nghki1c89y8v.manus.space)**

## ✨ Features

### 🤖 Cross-Platform AI Integrations
- **OpenAI** (GPT-4, DALL-E, Whisper)
- **Anthropic** (Claude-3 models)  
- **Google** (Gemini Pro)
- **Cohere** (Command models)
- **Hugging Face** (Open source models)
- **Local Models** (Ollama, custom endpoints)

### 🚀 True Creation Engine
- **Full-Stack Web Applications** - Complete with frontend, backend, database
- **Mobile Apps** - Cross-platform React Native applications
- **Landing Pages** - Professional responsive designs
- **AI Chatbots** - Intelligent conversational interfaces
- **E-commerce Stores** - Complete online shopping platforms
- **Data Dashboards** - Interactive analytics and visualization

### 🔧 Self-Healing System
- **Auto-fixes unresponsive buttons** - Immediate UI repair
- **Prevents empty agent creation** - Form validation and error prevention
- **Repairs failed uploads** - Alternative upload methods on failure
- **Heals API failures** - Retry with backoff + backup endpoints
- **Real-time diagnostics** - Continuous health monitoring

### 🎯 Agent Management
- **Create, edit, remove agents** with full validation
- **Role-based capabilities** (PROCESSOR, GENERATOR, VALIDATOR, etc.)
- **Asset upload and processing** with clear generation feedback
- **Performance monitoring** and health checks
- **Template system** for quick agent creation

## 🚀 Quick Start

### Desktop Application
1. Download the appropriate executable for your platform
2. Install and launch the application
3. Configure your AI providers (OpenAI, Anthropic, etc.)
4. Create your first agent or project
5. Start building with AI assistance!

### Web Dashboard
Visit [https://nghki1c89y8v.manus.space](https://nghki1c89y8v.manus.space) for the web interface.

### Build from Source
```bash
git clone https://github.com/srbryant86/nexusai-runtime-.git
cd nexusai-runtime-
npm install
npm start
```

See [BUILD.md](BUILD.md) for detailed build instructions.

## 📋 System Requirements

- **Windows**: Windows 10 or later
- **macOS**: macOS 10.14 or later  
- **Linux**: Ubuntu 18.04+ or equivalent
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB available space
- **Network**: Internet connection for AI provider access

## 🔑 Configuration

### AI Provider Setup
1. Open the application
2. Navigate to "AI Integrations"
3. Click on a provider to configure
4. Enter your API key and test the connection

### Environment Variables (Optional)
```bash
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

## 📖 Documentation

- **[Build Instructions](BUILD.md)** - How to build from source
- **[API Documentation](docs/api.md)** - REST API reference
- **[Agent Contracts](docs/contracts.md)** - Agent schema and validation
- **[Self-Healing Guide](docs/self-healing.md)** - Diagnostic and repair system

## 🛠️ Development

### Project Structure
```
nexusai-runtime/
├── src/                     # Source code
│   ├── main.js             # Electron main process
│   ├── app.js              # Application logic
│   ├── index.html          # UI interface
│   └── engines/            # Core engines
├── desktop/                # Built executables
├── docs/                   # Documentation
└── package.json
```

### Core Components
- **LLM Handshake Engine** - AI provider integration and communication
- **True Creation Engine** - Project generation and asset processing  
- **Self-Healing System** - Automatic error detection and repair
- **Agent Registry** - Agent lifecycle and contract management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/srbryant86/nexusai-runtime-/issues)
- **Self-Healing**: Built-in diagnostics and auto-repair
- **Documentation**: Comprehensive guides in the `docs/` directory

---

**NexusAI Runtime** - Empowering true creation with AI-driven automation and self-healing capabilities.

