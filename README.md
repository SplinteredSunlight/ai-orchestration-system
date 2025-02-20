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

- Docker and Docker Compose
- Node.js (v18 or later)
- Python 3.11 or later
- OpenAI API key

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SplinteredSunlight/ai-orchestration-system.git
   cd ai-orchestration-system
   ```

2. Set up environment variables:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your OpenAI API key and other settings
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   ./install-deps.sh
   cd ..
   ```

### Development

Start the development environment:
```bash
./start-dev.sh
```

This will start:
- Frontend at http://localhost:3000
- Backend API at http://localhost:8000
- Redis at localhost:6379
- ChromaDB with persistence

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

Currently in initial development phase. Check back for regular updates on progress and milestones.

## 🤝 Contributing

This project is currently in development. Contribution guidelines will be added soon.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
