# Retry Logic and Exponential Backoff Implementation

## Overview

This document describes the retry logic and exponential backoff implementation added to AutoGrow to handle API call failures gracefully and prevent cascading failures across all three agents.

## Issue Addressed

**Issue #21**: API calls to Anthropic and GitHub have no retry logic. Any network failure crashes workflows. This implementation adds exponential backoff with jitter and rate limit handling.

## Implementation Details

### 1. Retry Utility Module (`src/utils/retry_utils.py`)

A comprehensive retry utility module providing:

- **Exponential Backoff with Jitter**: Prevents thundering herd problem
- **Rate Limit Detection**: Automatically detects and handles rate limit errors
- **Retryable Error Detection**: Identifies transient vs. permanent errors
- **Specialized Decorators**: Separate decorators for Anthropic and GitHub API calls
- **Configurable Parameters**: Max retries, base delay, max delay, jitter control

#### Key Functions

##### `exponential_backoff_with_jitter(attempt, base_delay, max_delay, jitter)`
Calculates delay with exponential backoff: `delay = min(base_delay * 2^attempt, max_delay)`
- Optional jitter randomizes delay between 0 and calculated delay
- Prevents synchronized retry storms

##### `is_rate_limit_error(exception)`
Detects rate limit errors by:
- Exception type (RateLimitExceededException)
- Error message keywords (rate limit, 429, quota exceeded, throttle)

##### `is_retryable_error(exception)`
Identifies retryable errors:
- Rate limit errors
- Connection/timeout errors
- 5xx server errors
- Network failures

Non-retryable errors (4xx client errors, authentication failures) fail immediately.

##### `retry_with_exponential_backoff(max_retries, base_delay, ...)`
Main retry decorator with:
- Configurable retry attempts (default: 3)
- Exponential backoff (default base: 2.0s, max: 60.0s)
- Optional jitter (default: enabled)
- Verbose logging of retry attempts
- Special handling for rate limits (minimum 30s delay)

##### `retry_anthropic_api_call(max_retries, base_delay, max_delay)`
Specialized decorator for Anthropic API:
- Handles Anthropic-specific exceptions (APIError, RateLimitError, etc.)
- Default: 3 retries, 2s base delay, 120s max delay
- Automatically imported if anthropic library available

##### `retry_github_api_call(max_retries, base_delay, max_delay)`
Specialized decorator for GitHub API:
- Handles PyGithub exceptions (GithubException, RateLimitExceededException)
- Default: 3 retries, 2s base delay, 120s max delay
- Automatically imported if github library available

### 2. Updated Agent Files

#### `src/agents/issue_generator.py`

**GitHub API Calls with Retry:**
- `_get_open_issues_with_retry()`: Get open issues
- `_get_readme_with_retry()`: Get README content
- `_get_commits_with_retry()`: Get recent commits
- `_create_issue_with_retry()`: Create new issues

**Anthropic API Calls with Retry:**
- `_call_anthropic_api()`: Call Claude API for issue generation
- Decorated with `@retry_anthropic_api_call(max_retries=3, base_delay=2.0)`

#### `src/agents/issue_resolver.py`

**GitHub API Calls with Retry:**
- `_get_issue_with_retry()`: Get specific issue
- `_get_issues_with_retry()`: Get issue list
- `_get_readme_with_retry()`: Get README
- `_create_comment_with_retry()`: Create issue comments
- `_add_label_with_retry()`: Add labels to issues
- `_remove_label_with_retry()`: Remove labels from issues
- `_create_pull_request_with_retry()`: Create pull requests

**Note:** Claude CLI Agent calls are not wrapped with retry decorators as the CLI itself handles subprocess-level retries.

#### `src/agents/qa_agent.py`

**GitHub API Calls with Retry:**
- `_get_issues_with_retry()`: Get issues for review
- `_get_pulls_with_retry()`: Get pull requests
- `_get_commits_with_retry()`: Get recent commits
- `_create_issue_with_retry()`: Create QA report issues

**Anthropic API Calls with Retry:**
- `_call_anthropic_api()`: Call Claude API for QA analysis
- Decorated with `@retry_anthropic_api_call(max_retries=3, base_delay=2.0)`

#### `src/agentic_workflow.py`

**GitHub API Calls with Retry:**
- `_get_repo_with_retry()`: Get repository object
- `_get_issues_with_retry()`: Get issue list
- `_get_issue_with_retry()`: Get specific issue
- `_create_pull_with_retry()`: Create pull request

**Anthropic API Calls with Retry:**
- `_call_anthropic_with_retry()`: Call Claude API for fix generation
- Decorated with `@retry_anthropic_api_call(max_retries=3, base_delay=2.0, verbose=False)`
- Logging handled by workflow logger instead of retry verbose output

### 3. Dependencies Added

Updated `src/claude-agent/requirements.txt`:
```
anthropic>=0.18.0  # Added explicit dependency
```

All retry logic is implemented without external retry libraries (tenacity, backoff) to minimize dependencies.

## Retry Behavior Examples

### Example 1: Transient Network Error
```
⚠️  ConnectionError: Connection timeout
🔄 Retrying in 1.5s (attempt 1/3)...
⚠️  ConnectionError: Connection timeout
🔄 Retrying in 3.2s (attempt 2/3)...
✅ Success on attempt 3
```

### Example 2: Rate Limit Hit
```
⏳ Rate limit detected, waiting 30.0s before retry 1/3
⏳ Rate limit detected, waiting 45.0s before retry 2/3
✅ Success on attempt 3
```

### Example 3: Non-Retryable Error
```
❌ Non-retryable error: AuthenticationError: Invalid API key
[Fails immediately without retry]
```

## Configuration

### Default Retry Settings

- **Max Retries**: 3 attempts
- **Base Delay**: 2.0 seconds
- **Max Delay**: 60-120 seconds (API-dependent)
- **Jitter**: Enabled (randomizes delay)
- **Rate Limit Min Delay**: 30 seconds

### Customization

To adjust retry parameters, modify the decorator arguments:

```python
@retry_anthropic_api_call(
    max_retries=5,      # More retry attempts
    base_delay=3.0,     # Longer initial delay
    max_delay=180.0     # Higher maximum delay
)
def _call_api():
    ...
```

## Error Handling Strategy

### Retryable Errors (Will Retry)
- Rate limit errors (429)
- Connection errors
- Timeout errors
- 5xx server errors
- Network unavailable
- Service temporarily unavailable

### Non-Retryable Errors (Fail Fast)
- Authentication errors (401, 403)
- Invalid request errors (400)
- Resource not found (404)
- Validation errors
- Permission denied

## Benefits

1. **Resilience**: Handles transient network failures gracefully
2. **Rate Limit Protection**: Automatically backs off when hitting API limits
3. **Cascading Failure Prevention**: Jitter prevents synchronized retry storms
4. **Better User Experience**: Workflows complete successfully despite temporary issues
5. **Cost Optimization**: Avoids wasted API calls on repeated failures
6. **Observability**: Verbose logging helps debug API issues

## Testing Recommendations

1. **Unit Tests**: Mock API failures and verify retry behavior
2. **Integration Tests**: Test with rate limit scenarios
3. **Chaos Testing**: Inject network failures to validate resilience
4. **Monitoring**: Track retry rates and success/failure metrics

## Future Enhancements

Potential improvements for future iterations:

1. **Circuit Breaker Pattern**: Stop retrying after sustained failures
2. **Adaptive Backoff**: Adjust delays based on error patterns
3. **Retry Metrics**: Collect and report retry statistics
4. **Per-Endpoint Configuration**: Different retry settings per API endpoint
5. **Distributed Rate Limiting**: Coordinate retries across multiple workflow instances

## Related Files

- `src/utils/retry_utils.py` - Core retry implementation
- `src/agents/issue_generator.py` - Issue generator with retry
- `src/agents/issue_resolver.py` - Issue resolver with retry
- `src/agents/qa_agent.py` - QA agent with retry
- `src/agentic_workflow.py` - Agentic workflow with retry
- `src/claude-agent/requirements.txt` - Updated dependencies

## References

- [Exponential Backoff Algorithm](https://en.wikipedia.org/wiki/Exponential_backoff)
- [Anthropic API Documentation](https://docs.anthropic.com/claude/reference)
- [GitHub API Rate Limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [PyGithub Library](https://pygithub.readthedocs.io/)
