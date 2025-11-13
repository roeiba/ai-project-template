# Tests

This directory contains tests for the project.

## Structure

```
tests/
├── unit/                      # Unit tests
│   ├── test_gemini_agent.py  # GeminiAgent tests
│   ├── test_claude_cli_agent.py  # ClaudeAgent tests
│   └── __init__.py
├── integration/               # Integration tests
│   ├── test_gemini_agent_integration.py
│   ├── test_claude_cli_agent_integration.py
│   └── __init__.py
├── e2e/                      # End-to-end tests
│   ├── test_project_brief_workflow.py    # PROJECT_BRIEF.md workflow
│   ├── test_gemini_agent_workflow.py     # Gemini agent workflows
│   ├── test_claude_agent_workflow.py     # Claude agent workflows
│   ├── test_multi_agent_workflow.py      # Multi-agent workflows
│   └── __init__.py
├── fixtures/                 # Test fixtures and data
│   └── e2e/                  # E2E test fixtures
│       ├── sample_project_brief.md
│       ├── sample_issue.json
│       ├── sample_code.py
│       ├── sample_broken_code.py
│       └── README.md
├── conftest.py               # Pytest configuration and fixtures
├── pytest.ini                # Pytest settings
├── requirements.txt          # Test dependencies
├── run_tests.sh             # Test runner script
└── README.md                # This file
```

## Current Test Coverage

### GeminiAgent Tests (`unit/test_gemini_agent.py`)
Comprehensive tests for the Gemini CLI Python wrapper:

- ✅ **Initialization** (7 tests)
  - API key handling (env var, explicit, missing)
  - Model and format configuration
  - Debug mode
  - Installation check

- ✅ **Installation Check** (3 tests)
  - Detection when installed
  - Detection when not found
  - Error handling

- ✅ **Query Method** (10 tests)
  - Basic queries
  - Include directories
  - YOLO mode
  - Custom models
  - Debug mode
  - Text vs JSON format
  - Error handling
  - API key in environment

- ✅ **Query with File** (3 tests)
  - File input handling
  - File not found errors
  - Custom model selection

- ✅ **Code Review** (1 test)
  - Review functionality and prompts

- ✅ **Generate Docs** (1 test)
  - Documentation generation

- ✅ **Analyze Logs** (2 tests)
  - Default and custom focus

- ✅ **Batch Process** (3 tests)
  - Success scenarios
  - Error handling
  - Custom file patterns

- ✅ **Integration Tests** (1 test)
  - Real API calls (requires API key)

**Total: 31 tests**

### ClaudeAgent Tests (`unit/test_claude_cli_agent.py`)
Comprehensive tests for the Claude Code CLI Python wrapper:

- ✅ **Initialization** (6 tests)
  - Default and custom parameters
  - Tool restrictions
  - Permission modes
  - Installation check

- ✅ **Installation Check** (3 tests)
  - Detection when installed
  - Detection when not found
  - Error handling

- ✅ **Command Building** (6 tests)
  - Basic command structure
  - Verbose mode
  - Tool restrictions
  - Permission modes
  - Additional arguments

- ✅ **Query Method** (6 tests)
  - Basic queries
  - System prompts
  - MCP configuration
  - Text vs JSON format
  - Error handling

- ✅ **Query with Stdin** (2 tests)
  - Stdin input handling
  - System prompt integration

- ✅ **Continue Conversation** (2 tests)
  - Continue most recent
  - Resume specific session

- ✅ **Code Review** (2 tests)
  - Review functionality
  - File not found errors

- ✅ **Generate Docs** (1 test)
  - Documentation generation

- ✅ **Fix Code** (1 test)
  - Code fixing functionality

- ✅ **Batch Process** (2 tests)
  - Success scenarios
  - Error handling

- ✅ **Integration Tests** (1 test)
  - Real CLI calls (requires installation)

**Total: 32 tests**

### End-to-End Tests (`e2e/`)
Comprehensive tests for complete multi-agent workflows:

#### PROJECT_BRIEF.md Workflow (`test_project_brief_workflow.py`)
- ✅ **Valid PROJECT_BRIEF.md workflow** - Complete parsing and validation
- ✅ **Minimal PROJECT_BRIEF.md workflow** - Testing minimal requirements
- ✅ **Invalid PROJECT_BRIEF.md workflow** - Error handling and validation
- ✅ **Missing PROJECT_BRIEF.md workflow** - Graceful handling of missing files
- ✅ **PROJECT_BRIEF.md with warnings** - Validation with non-critical issues
- ✅ **PROJECT_BRIEF.md with special characters** - UTF-8 and unicode support

**Total: 6 tests**

#### Gemini Agent Workflow (`test_gemini_agent_workflow.py`)
- ✅ **Initialization workflow** - Agent setup and configuration
- ✅ **Query workflow** - Complete query execution flow
- ✅ **Code review workflow** - End-to-end code review process
- ✅ **Documentation generation workflow** - Doc generation from code
- ✅ **Batch processing workflow** - Processing multiple files
- ✅ **Error handling workflow** - Error recovery and handling
- ✅ **YOLO mode workflow** - Auto-approve operations
- ✅ **Include directories workflow** - Multi-directory context
- ✅ **Model selection workflow** - Using different AI models
- ✅ **Real API workflow** - Integration with real Gemini API

**Total: 10 tests**

#### Claude Agent Workflow (`test_claude_agent_workflow.py`)
- ✅ **Initialization workflow** - Agent setup and configuration
- ✅ **Query workflow** - Complete query execution flow
- ✅ **Code review workflow** - End-to-end code review process
- ✅ **Fix code workflow** - Automated code fixing
- ✅ **Documentation generation workflow** - Doc generation from code
- ✅ **Batch processing workflow** - Processing multiple files
- ✅ **System prompt workflow** - Custom system prompts
- ✅ **Permission modes workflow** - Different permission settings
- ✅ **Tool restrictions workflow** - Limiting available tools
- ✅ **Continue conversation workflow** - Session management
- ✅ **Error handling workflow** - Error recovery
- ✅ **Stdin workflow** - Input via stdin
- ✅ **MCP configuration workflow** - External tool integration
- ✅ **Real CLI workflow** - Integration with real Claude CLI

**Total: 14 tests**

#### Multi-Agent Workflow (`test_multi_agent_workflow.py`)
- ✅ **Multi-agent initialization** - Initialize both agents
- ✅ **Issue analysis workflow** - Gemini analyzes issues
- ✅ **Code review workflow** - Gemini reviews code
- ✅ **Fix validation workflow** - Gemini validates Claude's fixes
- ✅ **PR description generation** - Generate PR descriptions
- ✅ **Documentation generation** - Generate docs from code
- ✅ **Complete issue resolution** - Full workflow from issue to PR
- ✅ **Error recovery workflow** - Handle failures between agents
- ✅ **Parallel operations workflow** - Concurrent agent operations
- ✅ **Context sharing workflow** - Share context between agents
- ✅ **Real multi-agent workflow** - Real API integration
- ✅ **Performance tracking workflow** - Monitor execution time

**Total: 12 tests**

### Combined Test Coverage

**Unit Tests** (mocked, fast):
- **GeminiAgent**: 31 tests
- **ClaudeAgent**: 32 tests
- **Subtotal**: 63 tests

**Integration Tests** (real APIs, slow):
- **GeminiAgent**: 15 tests
- **ClaudeAgent**: 17 tests
- **Subtotal**: 32 tests

**End-to-End Tests** (complete workflows):
- **PROJECT_BRIEF.md workflow**: 6 tests
- **Gemini agent workflow**: 10 tests
- **Claude agent workflow**: 14 tests
- **Multi-agent workflow**: 12 tests
- **Subtotal**: 42 tests

**Total**: 137 tests (63 unit + 32 integration + 42 e2e)

## Running Tests

### Quick Start with Make (Recommended)
```bash
# Install dependencies
make install-test-deps

# Run unit tests only (fast, no API keys needed)
make test

# Run integration tests (requires API keys)
export GEMINI_API_KEY="your-key"
make test-integration

# Run all tests
make test-all

# Run with coverage
make test-coverage
```

### Manual Setup
```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run unit tests only (fast, no API keys needed)
cd tests
./run_tests.sh

# Run with coverage
./run_tests.sh --coverage

# Run including integration tests (requires API keys)
./run_tests.sh --integration

# Run e2e tests only
pytest tests/e2e/ -v

# Run specific test file
./run_tests.sh unit/test_gemini_agent.py

# Run with verbose output
./run_tests.sh --verbose
```

### Python Tests (Manual)
```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests (unit + integration + e2e)
pytest

# Run only unit tests (fast, mocked)
pytest tests/unit/ -v

# Run only integration tests (slow, real APIs)
pytest tests/integration/ -v -m integration

# Run only e2e tests (complete workflows)
pytest tests/e2e/ -v -m e2e

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_gemini_agent.py

# Run only unit tests (skip integration and e2e)
pytest -m "not integration and not e2e"

# Run with verbose output
pytest -vv

# Run e2e tests with specific workflow
pytest tests/e2e/test_multi_agent_workflow.py -v
```

### JavaScript/TypeScript Tests
```bash
# Install jest
npm install --save-dev jest

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Writing Tests

### Python Example
```python
# tests/unit/test_example.py
import pytest
from src.module import function

def test_function():
    result = function(input)
    assert result == expected
```

### JavaScript Example
```javascript
// tests/unit/example.test.js
const { function } = require('../src/module');

test('function works correctly', () => {
  const result = function(input);
  expect(result).toBe(expected);
});
```

## Test Types

### Unit Tests (`unit/`)
- **Fast**: Run in < 1 second per test
- **Mocked**: No real API calls
- **Always run**: Part of CI/CD
- **No API keys needed**
- **Scope**: Individual functions and classes

### Integration Tests (`integration/`)
- **Slow**: Run in ~45 seconds total
- **Real APIs**: Actual API calls
- **Run selectively**: Manual trigger in CI
- **API keys required**
- **Scope**: Agent CLI integration with real services

### End-to-End Tests (`e2e/`)
- **Medium speed**: Run in ~10-30 seconds (with mocks)
- **Workflow testing**: Complete multi-step processes
- **Mocked by default**: Fast execution without API keys
- **Real API variants**: Optional integration tests marked with `@pytest.mark.integration`
- **Scope**: Complete workflows from PROJECT_BRIEF.md parsing through code generation and validation

## Best Practices

### Unit Tests
1. **Organize by type**: Unit, integration, and e2e tests in separate directories
2. **Name clearly**: Use descriptive test names that explain what is being tested
3. **One assertion per test**: Keep tests focused and simple
4. **Use fixtures**: Share test data and setup code
5. **Mock external dependencies**: Isolate the code under test
6. **Test edge cases**: Include boundary conditions and error cases
7. **Keep tests fast**: Unit tests should run quickly

### Integration Tests
1. **Mark with `@pytest.mark.integration`**
2. **Mark slow tests with `@pytest.mark.slow`**
3. **Handle API errors gracefully**
4. **Use temporary files**
5. **Document API costs**
6. **Skip if API keys not set**

### End-to-End Tests
1. **Mark with `@pytest.mark.e2e`**
2. **Test complete workflows**: Validate entire processes, not just individual steps
3. **Use fixtures for test data**: Leverage `tests/fixtures/e2e/` for consistent test data
4. **Mock by default**: Use mocked API responses for fast execution
5. **Mark real API tests**: Use `@pytest.mark.integration` and `@pytest.mark.requires_api_key` for real API tests
6. **Create temporary workspaces**: Use temp directories to avoid polluting the project
7. **Test error scenarios**: Include tests for error handling and recovery
8. **Verify complete state**: Check that entire workflow completed successfully, not just parts

## Documentation

- **Unit Tests**: This file (README.md)
- **Integration Tests**: See [INTEGRATION_TESTS.md](INTEGRATION_TESTS.md)
- **End-to-End Tests**: See [e2e/](e2e/) and [fixtures/e2e/README.md](fixtures/e2e/README.md)
- **Testing Guide**: See [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Makefile Guide**: See [../MAKEFILE_GUIDE.md](../MAKEFILE_GUIDE.md)

## CI/CD Integration

Tests are automatically run in CI/CD pipelines. See `.github/workflows/test-agents.yml` for configuration.

**GitHub Actions Workflow**:
- Runs unit tests on push/PR
- Runs on multiple OS (Ubuntu, macOS)
- Runs on multiple Python versions (3.9, 3.10, 3.11)
- Integration tests via manual trigger
- Coverage reports uploaded to Codecov
