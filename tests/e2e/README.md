# End-to-End Tests

This directory contains comprehensive end-to-end tests for multi-agent workflows, validating complete processes from PROJECT_BRIEF.md parsing through code generation and validation across both Claude and Gemini agents.

## Overview

End-to-end tests validate entire workflows rather than individual components:
- **PROJECT_BRIEF.md parsing and validation**
- **Complete Gemini agent workflows**
- **Complete Claude agent workflows**
- **Multi-agent collaboration (Claude + Gemini)**

## Test Files

### test_project_brief_workflow.py
Tests complete PROJECT_BRIEF.md workflow from parsing to validation.

**Test Coverage:**
- Valid PROJECT_BRIEF.md workflow (complete parsing and validation)
- Minimal PROJECT_BRIEF.md workflow (testing minimal requirements)
- Invalid PROJECT_BRIEF.md workflow (error handling and validation)
- Missing PROJECT_BRIEF.md workflow (graceful handling of missing files)
- PROJECT_BRIEF.md with warnings (validation with non-critical issues)
- PROJECT_BRIEF.md with special characters (UTF-8 and unicode support)

**Total: 6 tests**

### test_gemini_agent_workflow.py
Tests complete Gemini agent workflows from initialization through code generation.

**Test Coverage:**
- Initialization workflow (agent setup and configuration)
- Query workflow (complete query execution flow)
- Code review workflow (end-to-end code review process)
- Documentation generation workflow (doc generation from code)
- Batch processing workflow (processing multiple files)
- Error handling workflow (error recovery and handling)
- YOLO mode workflow (auto-approve operations)
- Include directories workflow (multi-directory context)
- Model selection workflow (using different AI models)
- Real API workflow (integration with real Gemini API)

**Total: 10 tests**

### test_claude_agent_workflow.py
Tests complete Claude agent workflows from initialization through code generation.

**Test Coverage:**
- Initialization workflow (agent setup and configuration)
- Query workflow (complete query execution flow)
- Code review workflow (end-to-end code review process)
- Fix code workflow (automated code fixing)
- Documentation generation workflow (doc generation from code)
- Batch processing workflow (processing multiple files)
- System prompt workflow (custom system prompts)
- Permission modes workflow (different permission settings)
- Tool restrictions workflow (limiting available tools)
- Continue conversation workflow (session management)
- Error handling workflow (error recovery)
- Stdin workflow (input via stdin)
- MCP configuration workflow (external tool integration)
- Real CLI workflow (integration with real Claude CLI)

**Total: 14 tests**

### test_multi_agent_workflow.py
Tests complete multi-agent workflows using both Claude and Gemini together.

**Test Coverage:**
- Multi-agent initialization (initialize both agents)
- Issue analysis workflow (Gemini analyzes issues)
- Code review workflow (Gemini reviews code)
- Fix validation workflow (Gemini validates Claude's fixes)
- PR description generation (generate PR descriptions)
- Documentation generation (generate docs from code)
- Complete issue resolution (full workflow from issue to PR)
- Error recovery workflow (handle failures between agents)
- Parallel operations workflow (concurrent agent operations)
- Context sharing workflow (share context between agents)
- Real multi-agent workflow (real API integration)
- Performance tracking workflow (monitor execution time)

**Total: 12 tests**

## Running E2E Tests

### Quick Start

```bash
# Run all e2e tests (fast, mocked)
pytest tests/e2e/ -v

# Run specific test file
pytest tests/e2e/test_multi_agent_workflow.py -v

# Run with markers
pytest tests/e2e/ -v -m e2e

# Run excluding integration tests
pytest tests/e2e/ -v -m "e2e and not integration"
```

### With Real APIs

```bash
# Set API keys
export GEMINI_API_KEY="your-gemini-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Run all tests including real API tests
pytest tests/e2e/ -v -m "e2e"

# Run only real API tests
pytest tests/e2e/ -v -m "e2e and integration"
```

### Coverage

```bash
# Run with coverage report
pytest tests/e2e/ --cov=src --cov-report=html -v

# View coverage
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Structure

### Fixtures

E2E tests use fixtures from `tests/fixtures/e2e/`:
- `sample_project_brief.md` - Valid PROJECT_BRIEF.md for testing
- `sample_issue.json` - Sample GitHub issue data
- `sample_code.py` - Well-structured code for testing
- `sample_broken_code.py` - Code with bugs for fix testing

### Markers

E2E tests use pytest markers:
- `@pytest.mark.e2e` - All e2e tests
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.integration` - Tests requiring real APIs
- `@pytest.mark.requires_api_key` - Tests requiring API keys

### Example Test

```python
@pytest.mark.e2e
@pytest.mark.slow
def test_complete_workflow(self, temp_workspace):
    """Test complete multi-agent workflow"""
    # Setup
    agent = MultiAgentWorkflow()

    # Execute workflow
    result = agent.analyze_issue(issue_description)

    # Verify
    assert result is not None
    assert "response" in result
```

## Best Practices

### Writing E2E Tests

1. **Test Complete Workflows**: Validate entire processes, not just individual steps
2. **Use Fixtures**: Leverage shared test data from `fixtures/e2e/`
3. **Mock by Default**: Use mocked API responses for fast execution
4. **Mark Real API Tests**: Use appropriate markers for tests requiring APIs
5. **Create Temporary Workspaces**: Use temp directories to avoid pollution
6. **Test Error Scenarios**: Include error handling and recovery
7. **Verify Complete State**: Check entire workflow completion

### Mocking API Calls

```python
with patch('subprocess.run') as mock_run:
    mock_run.return_value = Mock(
        returncode=0,
        stdout=json.dumps({"response": "Test response"}),
        stderr=""
    )

    result = agent.query("Test prompt")
    assert result is not None
```

### Temporary Workspaces

```python
@pytest.fixture
def temp_workspace(self):
    """Create temporary workspace for testing"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure paths are added to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
```

**API Key Issues**
```bash
# Skip tests if API keys not available
if not os.getenv("GEMINI_API_KEY"):
    pytest.skip("GEMINI_API_KEY not set")
```

**Mock Not Working**
```bash
# Ensure mock is patching the correct location
with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
    agent = GeminiAgent(api_key="test")
```

## CI/CD Integration

E2E tests run in CI/CD pipelines:
- Fast tests (mocked) run on every push/PR
- Slow tests run on schedule or manual trigger
- Real API tests run only when API keys are configured

See `.github/workflows/test-agents.yml` for configuration.

## Performance

**Test Execution Times:**
- Mocked e2e tests: ~5-10 seconds total
- Real API e2e tests: ~30-60 seconds total
- Complete test suite: ~1-2 minutes

## Contributing

When adding new e2e tests:

1. Follow the existing test structure
2. Use appropriate markers (`@pytest.mark.e2e`, etc.)
3. Create fixtures for reusable test data
4. Mock external dependencies by default
5. Add real API variant with `@pytest.mark.integration`
6. Update this README with test descriptions
7. Ensure tests are independent and can run in any order

## Documentation

- **Test Fixtures**: See [../fixtures/e2e/README.md](../fixtures/e2e/README.md)
- **Testing Guide**: See [../TESTING_GUIDE.md](../TESTING_GUIDE.md)
- **Integration Tests**: See [../INTEGRATION_TESTS.md](../INTEGRATION_TESTS.md)
