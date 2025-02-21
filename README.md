# AI Orchestration System

A sophisticated AI orchestration system that dynamically assigns tasks to specialized AI agents, enabling efficient parallel execution and intelligent resource management.

## 🎯 Project Objectives

- Develop an AI orchestration system with specialized agent task assignment
- Utilize free/open-source models with high-quality verification
- Implement shared RAG (Retrieval-Augmented Generation) database
- Enable parallel task execution
- Provide web-based GUI for task management
- Ensure API/token cost control

## 🏗️ Architecture

### Backend
- **Python-based** using FastAPI
- **AI Framework**: LangChain, CrewAI
- **Task Queue**: Celery with Redis message broker
- **Vector Storage**: ChromaDB for shared RAG

### Frontend
- **Framework**: React
- **Styling**: TailwindCSS
- **Features**: Real-time progress tracking, task management UI

## 🔧 Core Features

### AI Orchestration
- Dynamic task assignment and model selection
- Specialized AI agents:
  - Coding Agent
  - Graphic Designer Agent
  - Marketing Manager Agent
- High-quality model verification system
- Parallel execution capabilities

### Knowledge Management
- Shared vector database (ChromaDB)
- Cross-agent knowledge storage and retrieval
- Efficient RAG implementation

### User Interface
- Intuitive AI Orchestration Dashboard
- Task type selection and prompt input
- Real-time execution monitoring
- Progress visualization

### Cost Management
- API call and token usage tracking
- Automatic execution pause at $5 threshold
- User confirmation for continued execution

## 🚀 Development Roadmap

1. ⏳ Backend System Development
   - FastAPI setup
   - LangChain integration
   - Celery configuration
   - Agent implementation

2. ⏳ AI Agent Creation
   - Coding agent development
   - Graphic design agent implementation
   - Marketing agent setup
   - Verification system integration

3. ⏳ Frontend Development
   - React/TailwindCSS setup
   - Dashboard implementation
   - Task management interface
   - Progress tracking system

4. ⏳ RAG Integration
   - ChromaDB setup
   - Knowledge storage system
   - Cross-agent retrieval implementation

5. ⏳ Testing & Optimization
   - Parallel execution testing
   - API cost monitoring
   - Performance optimization
   - System verification

## 💻 Setup Instructions

### Prerequisites

1. Install Podman:
   ```bash
   # macOS
   brew install podman
   podman machine init
   podman machine start

   # Linux (Ubuntu/Debian)
   sudo apt-get update
   sudo apt-get install -y podman podman-compose
   ```

2. Other requirements:
   - OpenAI API key (for AI model access)
   - Git (for version control)
   - 8GB RAM minimum (16GB recommended)
   - 20GB free disk space

3. Verify Podman installation:
   ```bash
   podman --version
   podman info
   ```

### Security Features

- Podman Security:
  - Daemonless container engine
  - Rootless container execution
  - SELinux integration
  - Network isolation
  - Stricter security defaults

- Chainguard Images:
  - Minimal attack surface through distroless images
  - Automatic security updates
  - Built-in software supply chain security
  - SBOM (Software Bill of Materials) support
  - Verified image signatures
  - Read-only root filesystem
  - No privilege escalation

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SplinteredSunlight/ai-orchestration-system.git
   cd ai-orchestration-system
   ```

2. Set up environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Edit backend/.env and configure:
   - OPENAI_API_KEY: Your OpenAI API key
   - SECRET_KEY: Generate a secure random key
   - COST_LIMIT: Set your preferred API cost limit
   - Other settings as needed

3. Install dependencies:
   ```bash
   # Install frontend dependencies
   cd frontend
   ./install-deps.sh
   cd ..

   # Install backend dependencies
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

4. Initialize ChromaDB:
   ```bash
   mkdir -p data/chromadb
   ```

### Development

1. Start the development environment:
   ```bash
   cd containers && ./start-dev.sh
   ```
   This will automatically:
   - Install Podman if not present
   - Pull and verify Chainguard images
   - Start all services with enhanced security
   - Display security status for each container
   - Show service logs

2. Access the services:
   - Frontend Dashboard: http://localhost:3000
   - Backend API & Docs: http://localhost:8000/docs
   - Redis: localhost:6379

3. View service status:
   ```bash
   # View running containers
   podman ps

   # View container logs
   podman-compose logs -f

   # View security info
   podman inspect <container-name>

   # View image signatures
   podman image verify cgr.dev/chainguard/python:latest-dev
   ```

4. Stop the environment:
   ```bash
   podman-compose down
   ```

### Troubleshooting

1. If services fail to start:
   ```bash
   podman-compose down -v
   podman-compose up -d
   ```

2. Clear ChromaDB data:
   ```bash
   rm -rf data/chromadb/*
   ```

3. View detailed logs:
   ```bash
   # All services
   podman-compose logs -f

   # Specific service
   podman logs -f <container-name>
   ```

4. Check container security:
   ```bash
   # View security info
   podman inspect <container-name> --format '{{.HostConfig.SecurityOpt}}'
   
   # View capabilities
   podman inspect <container-name> --format '{{.HostConfig.CapDrop}}'
   ```

5. Reset Podman:
   ```bash
   # On macOS
   podman machine stop
   podman machine rm
   podman machine init
   podman machine start

   # On Linux
   podman system reset
   ```

## 📁 Project Structure

```
ai-orchestration-system/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes and endpoints
│   │   ├── core/         # Core functionality and config
│   │   ├── agents/       # AI agent implementations
│   │   ├── models/       # Data models and schemas
│   │   └── utils/        # Utility functions
│   ├── tests/            # Backend tests
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── utils/        # Utility functions
│   └── package.json      # Frontend dependencies
└── docker/               # Docker configuration files
```

## 🛠️ Development Guidelines

1. **Code Style**
   - Backend: Follow PEP 8 guidelines
   - Frontend: Use Prettier and ESLint configs
   - Use TypeScript for type safety

2. **Git Workflow**
   - Create feature branches from `main`
   - Use descriptive commit messages
   - Submit PRs for review

3. **Testing**
   - Write unit tests for new features
   - Ensure all tests pass before committing
   - Test both frontend and backend changes

4. **Documentation**
   - Document new features and APIs
   - Update README when adding major features
   - Include inline documentation for complex logic

5. **Cost Management**
   - Monitor API usage in development
   - Use free/open-source models when possible
   - Test with small token limits first

## 📈 Project Status

Current Development Phase: Alpha

Completed Features:
- ✅ Project structure and architecture
- ✅ Basic frontend UI components
- ✅ Backend API endpoints
- ✅ AI agent framework
- ✅ Docker development environment

In Progress:
- 🔄 AI agent implementations
- 🔄 RAG system integration
- 🔄 Cost management system
- 🔄 Task execution engine

Upcoming:
- ⏳ Testing suite
- ⏳ Production deployment
- ⏳ Performance optimization
- ⏳ Documentation improvements

Next Milestone: Beta Release (Expected: March 2025)
- Feature-complete AI agents
- Full RAG system implementation
- Comprehensive testing
- Production deployment guide

## 🤝 Contributing

This project is currently in development. Contribution guidelines will be added soon.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
