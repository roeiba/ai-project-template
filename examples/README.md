# AI Project Template - Example Projects

> **Real-world examples demonstrating how AI agents generate complete applications from PROJECT_BRIEF.md**

This directory contains complete demo projects showcasing the AI template's capabilities. Each example includes:

- ✅ **Original PROJECT_BRIEF.md** - The requirements document
- ✅ **Generated Code** - Complete, production-ready application
- ✅ **Tests** - Comprehensive test suites
- ✅ **Deployment Configs** - Docker, CI/CD, and infrastructure
- ✅ **Documentation** - API docs, architecture guides
- ✅ **Step-by-Step Guide** - How the project was generated

---

## 📚 Available Examples

### 1. TaskFlow API - Task Management System

**Location**: [`todo-api-demo/`](./todo-api-demo/)

**Description**: A complete RESTful API for task management with user authentication, task organization, and real-time notifications.

**Technology Stack**:
- Backend: Node.js, Express.js, TypeScript
- Database: PostgreSQL
- Cache: Redis
- Testing: Jest, Supertest
- Deployment: Docker, Docker Compose

**What You'll Learn**:
- REST API design patterns
- JWT authentication implementation
- Database modeling and relationships
- Testing strategies for APIs
- Docker multi-container deployment
- CI/CD pipeline configuration

**Quick Start**:
```bash
cd todo-api-demo
docker-compose up
```

**Read More**: [TaskFlow Demo README](./todo-api-demo/STEP_BY_STEP_GUIDE.md)

---

## 🎯 How to Use These Examples

### For Learning

1. **Study the PROJECT_BRIEF.md**
   - See how requirements are structured
   - Understand the level of detail needed
   - Learn how to specify technical preferences

2. **Explore Generated Code**
   - Review the project architecture
   - Study code patterns and conventions
   - See how requirements map to implementation

3. **Follow the Step-by-Step Guide**
   - Understand the AI generation workflow
   - Learn prompt engineering techniques
   - See decision-making process

### For Your Own Projects

1. **Use as a Template**
   ```bash
   # Copy example PROJECT_BRIEF.md
   cp examples/todo-api-demo/PROJECT_BRIEF.md ./PROJECT_BRIEF.md

   # Modify for your needs
   vim PROJECT_BRIEF.md
   ```

2. **Adapt the Structure**
   - Copy directory structure
   - Reuse configuration files
   - Follow naming conventions

3. **Learn from Tests**
   - Copy test patterns
   - Adapt to your use cases
   - Maintain code coverage standards

---

## 📖 What Each Example Demonstrates

### TaskFlow API Example

#### Requirements Gathering
- ✅ Comprehensive PROJECT_BRIEF.md structure
- ✅ Functional and non-functional requirements
- ✅ User roles and permissions
- ✅ Data model specifications
- ✅ Timeline and priorities

#### Architecture & Code
- ✅ Clean architecture with separation of concerns
- ✅ MVC pattern implementation
- ✅ Service layer for business logic
- ✅ Middleware for cross-cutting concerns
- ✅ TypeScript for type safety

#### Testing
- ✅ Unit tests for business logic
- ✅ Integration tests for API endpoints
- ✅ Test fixtures and factories
- ✅ 80%+ code coverage
- ✅ CI integration

#### Deployment
- ✅ Multi-stage Docker builds
- ✅ Docker Compose orchestration
- ✅ Environment configuration
- ✅ Health checks and monitoring
- ✅ Production-ready setup

#### Documentation
- ✅ Complete API documentation
- ✅ Architecture diagrams
- ✅ Setup instructions
- ✅ Deployment guides
- ✅ Troubleshooting tips

---

## 🚀 Running the Examples

### Prerequisites

- Docker and Docker Compose installed
- Node.js 20+ (for local development)
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/roeiba/ai-project-template.git
cd ai-project-template/examples

# Run TaskFlow API example
cd todo-api-demo
docker-compose up

# API will be available at http://localhost:3000
# API Documentation at http://localhost:3000/api-docs
```

### Local Development

```bash
# Install dependencies
cd todo-api-demo
npm install

# Set up environment variables
cp .env.example .env
vim .env

# Run database migrations
npm run migrate

# Start development server
npm run dev

# Run tests
npm test
```

---

## 📊 Project Statistics

### TaskFlow API Demo

| Metric | Value |
|--------|-------|
| Lines of Code | ~3,000+ |
| Number of Files | 45+ |
| Test Coverage | 85%+ |
| API Endpoints | 15+ |
| Generation Time | ~30 minutes |
| Human Time Saved | ~2-3 weeks |

---

## 🎓 Learning Paths

### For Beginners

1. Start with **PROJECT_BRIEF.md**
   - Read the requirements carefully
   - Understand the structure
   - See what details are needed

2. Explore **Basic Code Files**
   - `src/models/Task.ts` - Data models
   - `src/server.ts` - Application setup
   - `package.json` - Dependencies

3. Review **Documentation**
   - API_DOCUMENTATION.md
   - STEP_BY_STEP_GUIDE.md

### For Intermediate Developers

1. Study **Architecture Patterns**
   - Controllers and services separation
   - Middleware implementation
   - Error handling strategies

2. Analyze **Testing Approach**
   - Integration test structure
   - Mocking strategies
   - Test coverage goals

3. Review **Deployment Setup**
   - Dockerfile best practices
   - Docker Compose configuration
   - Environment management

### For Advanced Users

1. Examine **Code Generation Patterns**
   - How AI structures code
   - Naming conventions used
   - Design patterns applied

2. Study **Prompt Engineering**
   - Effective PROJECT_BRIEF writing
   - Specification techniques
   - Requirement clarity

3. Customize and Extend
   - Add new features
   - Modify architecture
   - Implement custom patterns

---

## 🔧 Customization Guide

### Adapting Examples for Your Project

1. **Copy the PROJECT_BRIEF.md**
   ```bash
   cp examples/todo-api-demo/PROJECT_BRIEF.md ./my-project-brief.md
   ```

2. **Modify Requirements**
   - Update project overview
   - Change technology stack
   - Adjust data models
   - Define your user flows

3. **Generate Your Project**
   Use this prompt with an AI assistant:
   ```
   I've filled out PROJECT_BRIEF.md with my requirements.
   Please generate a complete project following the structure
   shown in examples/todo-api-demo/. Use the same patterns
   for code organization, testing, and documentation.
   ```

4. **Review and Iterate**
   - Check generated code
   - Request modifications
   - Add custom features
   - Run tests

---

## 📝 Example Comparison

### What's Included vs Typical Boilerplate

| Feature | Typical Boilerplate | AI Template Example |
|---------|-------------------|-------------------|
| Project Structure | ✅ Basic folders | ✅ Complete architecture |
| Application Code | ❌ Minimal | ✅ Full implementation |
| Authentication | ❌ Usually missing | ✅ JWT auth included |
| Database Setup | ❌ Schema only | ✅ Models + migrations |
| API Endpoints | ❌ 1-2 examples | ✅ Complete CRUD |
| Tests | ❌ Rarely included | ✅ 80%+ coverage |
| Docker Setup | ❌ Basic Dockerfile | ✅ Multi-stage + compose |
| Documentation | ❌ README only | ✅ Complete API docs |
| CI/CD | ❌ Not included | ✅ GitHub Actions |
| Error Handling | ❌ Basic | ✅ Comprehensive |

**Time Savings**: 2-3 weeks of development time

---

## 🤝 Contributing Examples

Want to add your own example project? Great!

### Guidelines

1. **Include All Components**
   - Complete PROJECT_BRIEF.md
   - Full source code
   - Comprehensive tests
   - Deployment configs
   - Documentation

2. **Follow Structure**
   ```
   your-example/
   ├── PROJECT_BRIEF.md
   ├── STEP_BY_STEP_GUIDE.md
   ├── src/
   ├── tests/
   ├── deployment/
   └── docs/
   ```

3. **Document the Process**
   - How you wrote the brief
   - AI prompts used
   - Customizations made
   - Lessons learned

4. **Submit a PR**
   - Add your example
   - Update this README
   - Include screenshots/demos

---

## 🎯 Future Examples (Coming Soon)

### Planned Examples

- [ ] **E-commerce API** - Product catalog, shopping cart, payments
- [ ] **Blog Platform** - CMS with authentication and comments
- [ ] **Chat Application** - Real-time messaging with WebSockets
- [ ] **Analytics Dashboard** - Data processing and visualization
- [ ] **Mobile Backend** - BaaS with push notifications
- [ ] **Microservices Example** - Multi-service architecture

### Vote for Examples

Have a project type you'd like to see? [Open an issue](https://github.com/roeiba/ai-project-template/issues) and let us know!

---

## 📚 Additional Resources

### Documentation

- [Main README](../README.md) - Template overview
- [QUICKSTART](../QUICKSTART.md) - Getting started guide
- [PROJECT_BRIEF Template](../PROJECT_BRIEF.md) - Blank template

### Guides

- [How to Write a PROJECT_BRIEF](../docs/writing-project-briefs.md)
- [AI Prompt Engineering](../docs/prompt-engineering.md)
- [Testing Strategies](../docs/testing-guide.md)

### Community

- [Discussions](https://github.com/roeiba/ai-project-template/discussions)
- [Issues](https://github.com/roeiba/ai-project-template/issues)
- [Contributing](../CONTRIBUTING.md)

---

## 💡 Tips for Success

### Writing Effective PROJECT_BRIEFs

1. **Be Specific**: "User authentication with JWT" beats "add login"
2. **Include Data Models**: Define your database schema
3. **Specify Tech Stack**: Choose your frameworks and tools
4. **Define Success**: What does "done" look like?
5. **Prioritize**: Mark must-have vs nice-to-have features

### Working with AI Agents

1. **Review Generated Code**: Don't blindly accept everything
2. **Iterate**: Request changes and improvements
3. **Test Thoroughly**: Run the test suite, add more tests
4. **Understand Patterns**: Learn from the generated code
5. **Customize**: Make it yours, don't just copy

### Best Practices

1. **Start Small**: Begin with a simple example
2. **Build Incrementally**: Add features one at a time
3. **Document Changes**: Keep track of customizations
4. **Share Learnings**: Contribute back to the community
5. **Have Fun**: Experiment and explore!

---

## 🐛 Troubleshooting

### Common Issues

**"Docker containers won't start"**
- Check if ports are already in use
- Verify Docker is running
- Check environment variables in .env

**"Tests are failing"**
- Ensure database is running
- Check test environment configuration
- Review test logs for specific errors

**"AI generated incorrect code"**
- Review PROJECT_BRIEF.md for clarity
- Provide more specific requirements
- Use better examples in the brief

**"How do I customize the example?"**
- Read the STEP_BY_STEP_GUIDE.md
- Study the generated code
- Make incremental changes
- Test after each modification

---

## 📞 Support

Need help with the examples?

- **General Questions**: [GitHub Discussions](https://github.com/roeiba/ai-project-template/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/roeiba/ai-project-template/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/roeiba/ai-project-template/issues)

---

<div align="center">

**Happy Building!** 🚀

[← Back to Main README](../README.md) | [View TaskFlow Demo →](./todo-api-demo/)

---

*Examples maintained by the AI Project Template community*

</div>
