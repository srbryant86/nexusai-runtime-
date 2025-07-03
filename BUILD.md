# NexusAI Runtime – Build Instructions

## Desktop Application Build

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Git

### Quick Start
```bash
# Clone the repository
git clone https://github.com/srbryant86/nexusai-runtime-.git
cd nexusai-runtime-

# Install dependencies
npm install

# Start development mode
npm start

# Build for production
npm run build
```

### Development Mode
```bash
npm start
```
This starts the Electron application in development mode with hot reload.

### Production Build
```bash
npm run build
```
This creates platform-specific executables in the `dist/` directory.

### Platform-Specific Builds

#### Windows
```bash
npm run build-win
```
Creates: `dist/NexusAI Runtime Setup.exe`

#### macOS
```bash
npm run build-mac
```
Creates: `dist/NexusAI Runtime.dmg`

#### Linux
```bash
npm run build-linux
```
Creates: `dist/NexusAI Runtime.AppImage`

## Features

### ✅ Complete Desktop Application
- **Native Windows/Mac/Linux executable**
- **Professional UI with dark theme**
- **Self-healing capabilities**
- **Real-time monitoring**

### ✅ Cross-Platform AI Integrations
- **OpenAI** (GPT-4, DALL-E, Whisper)
- **Anthropic** (Claude-3 models)
- **Google** (Gemini Pro)
- **Cohere** (Command models)
- **Hugging Face** (Open source models)
- **Local Models** (Ollama, custom endpoints)

### ✅ True Creation Engine
- **Full-Stack Web Applications**
- **Mobile Apps** (React Native)
- **Landing Pages**
- **AI Chatbots**
- **E-commerce Stores**
- **Data Analysis Dashboards**

### ✅ Self-Healing System
- **Auto-fixes unresponsive buttons**
- **Prevents empty agent creation**
- **Repairs failed uploads**
- **Heals API failures**
- **Real-time diagnostics**

### ✅ Agent Management
- **Create, edit, remove agents**
- **Role-based capabilities**
- **Asset upload and processing**
- **Performance monitoring**

## Configuration

### AI Provider Setup
1. Open the application
2. Navigate to "AI Integrations"
3. Click on a provider to configure
4. Enter your API key
5. Test the connection

### Environment Variables
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
COHERE_API_KEY=your_cohere_key
HUGGINGFACE_API_KEY=your_hf_key
```

## Troubleshooting

### Build Issues
- Ensure Node.js 18+ is installed
- Clear node_modules: `rm -rf node_modules && npm install`
- Update Electron: `npm update electron`

### Runtime Issues
- Check the self-healing diagnostics page
- Restart the application
- Clear application data (Settings > Reset)

### AI Integration Issues
- Verify API keys are correct
- Check internet connection
- Review provider status in AI Integrations page

## Development

### Project Structure
```
nexusai-runtime/
├── src/
│   ├── main.js              # Electron main process
│   ├── app.js               # Main application logic
│   ├── index.html           # UI interface
│   ├── llm-handshake-engine.js    # AI integration engine
│   ├── true-creation-engine.js    # Project generation engine
│   ├── self-healing-system.js     # Self-healing capabilities
│   └── preload.js           # Secure IPC bridge
├── desktop/                 # Built executables
├── package.json
└── README.md
```

### Adding New AI Providers
1. Update `getAIProviders()` in `app.js`
2. Add handshake logic in `llm-handshake-engine.js`
3. Test integration and capabilities

### Adding New Project Templates
1. Update `getCreationTemplates()` in `app.js`
2. Add generation logic in `true-creation-engine.js`
3. Test project creation workflow

## Support

For issues, feature requests, or contributions:
- GitHub Issues: https://github.com/srbryant86/nexusai-runtime-/issues
- Documentation: See README.md
- Self-Healing: Built-in diagnostics and auto-repair

## License

MIT License - see LICENSE file for details.

