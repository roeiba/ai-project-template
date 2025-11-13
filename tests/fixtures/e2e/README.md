# E2E Test Fixtures

This directory contains fixtures and test data for end-to-end tests.

## Files

### sample_project_brief.md
A complete, valid PROJECT_BRIEF.md file used for testing:
- PROJECT_BRIEF.md parsing and validation
- Agent context understanding
- Documentation generation

### sample_issue.json
Sample GitHub issue data in JSON format:
- Issue analysis workflows
- Fix generation testing
- PR description generation

### sample_code.py
Well-structured Python code for testing:
- Code review workflows
- Documentation generation
- Code quality analysis
- Agent comprehension tests

### sample_broken_code.py
Python code with intentional bugs for testing:
- Bug detection workflows
- Fix suggestion generation
- Code repair validation
- Error handling in agent workflows

## Usage

These fixtures are used by e2e tests in `tests/e2e/` to simulate real-world scenarios
without requiring external dependencies or API calls during unit testing.

### In Tests

```python
import json
from pathlib import Path

# Load fixtures
fixtures_dir = Path(__file__).parent.parent / "fixtures" / "e2e"

# Load PROJECT_BRIEF.md
project_brief = (fixtures_dir / "sample_project_brief.md").read_text()

# Load issue data
with open(fixtures_dir / "sample_issue.json") as f:
    issue = json.load(f)

# Load code samples
sample_code = (fixtures_dir / "sample_code.py").read_text()
broken_code = (fixtures_dir / "sample_broken_code.py").read_text()
```

## Maintenance

When updating fixtures:
1. Ensure sample_project_brief.md passes validation
2. Keep sample_issue.json realistic and well-formatted
3. Maintain intentional bugs in sample_broken_code.py for fix testing
4. Update this README if adding new fixtures
