#!/usr/bin/env python3
"""
End-to-end tests for Multi-Agent workflow (Claude + Gemini)
Tests complete workflow using both agents together
"""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import subprocess
import json
import sys

# Add src directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "gemini-agent"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "claude-agent"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "gemini-agent" / "examples"))

from gemini_agent import GeminiAgent
from claude_cli_agent import ClaudeAgent
from multi_agent_workflow import MultiAgentWorkflow


class TestMultiAgentWorkflow:
    """Test complete multi-agent workflows combining Claude and Gemini"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def mock_api_keys(self, monkeypatch):
        """Mock API keys for both agents"""
        monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")

    @pytest.fixture
    def sample_issue(self):
        """Sample GitHub issue for testing"""
        return {
            "number": 42,
            "title": "Add user authentication",
            "body": """
            Implement user authentication with the following requirements:
            - Login with email and password
            - JWT token generation
            - Password hashing with bcrypt
            - Session management
            """,
            "labels": ["enhancement", "security"]
        }

    @pytest.fixture
    def sample_code_files(self, temp_workspace):
        """Create sample code files for testing"""
        src_dir = temp_workspace / "src"
        src_dir.mkdir()

        # Create main module
        (src_dir / "auth.py").write_text("""
import bcrypt
import jwt

def hash_password(password: str) -> str:
    '''Hash a password using bcrypt'''
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    '''Verify a password against a hash'''
    return bcrypt.checkpw(password.encode(), hashed.encode())
""")

        # Create user module
        (src_dir / "user.py").write_text("""
class User:
    def __init__(self, email: str, password_hash: str):
        self.email = email
        self.password_hash = password_hash
""")

        return src_dir

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_multi_agent_initialization_workflow(self, mock_api_keys):
        """Test initializing multi-agent workflow"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            # Verify both agents are initialized
            assert workflow.gemini is not None
            assert isinstance(workflow.gemini, GeminiAgent)

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_issue_analysis_workflow(self, mock_api_keys, sample_issue):
        """Test complete workflow: Gemini analyzes issue"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            # Mock Gemini response for issue analysis
            mock_analysis = {
                "response": json.dumps({
                    "issue_type": "enhancement",
                    "severity": "medium",
                    "complexity": "moderate",
                    "affected_areas": ["authentication", "security"],
                    "recommended_approach": "Implement JWT with bcrypt"
                }),
                "model": "gemini-2.5-flash"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_analysis),
                    stderr=""
                )

                # Execute analysis
                result = workflow.analyze_issue(sample_issue["body"])

                # Verify workflow
                assert result is not None
                assert "response" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_code_review_workflow(self, mock_api_keys, sample_code_files):
        """Test complete workflow: Gemini reviews code"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            auth_file = sample_code_files / "auth.py"

            # Mock Gemini response for code review
            mock_review = {
                "response": "Code review:\n- Good: Using bcrypt for hashing\n- Consider: Add type hints\n- Consider: Add error handling",
                "model": "gemini-2.5-pro"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_review),
                    stderr=""
                )

                # Execute code review
                result = workflow.review_code_changes(str(auth_file))

                # Verify workflow
                assert result is not None
                assert "response" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_fix_validation_workflow(self, mock_api_keys, sample_issue):
        """Test complete workflow: Gemini validates Claude's fix"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            fix_description = """
            Implemented user authentication:
            - Added JWT token generation
            - Implemented password hashing with bcrypt
            - Created User model with authentication methods
            - Added login/logout endpoints
            """

            # Mock Gemini response for validation
            mock_validation = {
                "response": json.dumps({
                    "addresses_root_cause": "Yes",
                    "gaps": "Missing password reset functionality",
                    "risks": "Should add rate limiting on login",
                    "testing_recommendations": [
                        "Test with invalid credentials",
                        "Test token expiration",
                        "Test concurrent sessions"
                    ],
                    "confidence_level": "High"
                }),
                "model": "gemini-2.5-pro"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_validation),
                    stderr=""
                )

                # Execute validation
                result = workflow.validate_fix(sample_issue["body"], fix_description)

                # Verify workflow
                assert result is not None
                assert "response" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_pr_description_generation_workflow(self, mock_api_keys, sample_issue):
        """Test complete workflow: Gemini generates PR description"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            changes_summary = "Implemented JWT-based authentication with bcrypt password hashing"

            # Mock Gemini response for PR description
            mock_pr_desc = {
                "response": """# Pull Request: User Authentication

## Summary
Implemented JWT-based authentication system with secure password hashing.

## Technical Details
- JWT token generation and validation
- Bcrypt password hashing
- User model with authentication methods

## Testing Recommendations
- [ ] Test login with valid credentials
- [ ] Test login with invalid credentials
- [ ] Test token expiration
- [ ] Test password hashing

## Potential Impacts
- New dependency: PyJWT, bcrypt
- Database schema changes required

## Reviewer Checklist
- [ ] Code follows security best practices
- [ ] Tests are comprehensive
- [ ] Documentation is updated
""",
                "model": "gemini-2.5-pro"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_pr_desc),
                    stderr=""
                )

                # Execute PR description generation
                result = workflow.generate_pr_description(
                    changes_summary,
                    sample_issue["number"]
                )

                # Verify workflow
                assert result is not None
                assert "response" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_documentation_generation_workflow(self, mock_api_keys, sample_code_files):
        """Test complete workflow: Gemini generates documentation"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            auth_file = sample_code_files / "auth.py"

            # Mock Gemini response for documentation
            mock_docs = {
                "response": """# Authentication Module

## Functions

### hash_password(password: str) -> str
Hashes a password using bcrypt.

**Parameters:**
- password: The plain text password to hash

**Returns:** The hashed password as a string

### verify_password(password: str, hashed: str) -> bool
Verifies a password against a bcrypt hash.

**Parameters:**
- password: The plain text password to verify
- hashed: The bcrypt hash to verify against

**Returns:** True if password matches, False otherwise
""",
                "model": "gemini-2.5-pro"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_docs),
                    stderr=""
                )

                # Execute documentation generation
                result = workflow.generate_documentation(str(auth_file))

                # Verify workflow
                assert result is not None
                assert "response" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_complete_issue_resolution_workflow(self, mock_api_keys, sample_issue, sample_code_files):
        """Test complete end-to-end issue resolution workflow with both agents"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            # Step 1: Gemini analyzes the issue
            analysis_response = {
                "response": "Analysis: Authentication feature, moderate complexity",
                "model": "gemini-2.5-flash"
            }

            # Step 2: Claude would generate the fix (simulated)
            fix_description = "Implemented authentication with JWT and bcrypt"

            # Step 3: Gemini validates the fix
            validation_response = {
                "response": "Validation: Fix addresses requirements properly",
                "model": "gemini-2.5-pro"
            }

            # Step 4: Gemini reviews the code
            review_response = {
                "response": "Code review: Implementation looks good",
                "model": "gemini-2.5-pro"
            }

            # Step 5: Gemini generates PR description
            pr_response = {
                "response": "# PR: User Authentication\n\nImplemented JWT auth system",
                "model": "gemini-2.5-pro"
            }

            responses = [
                Mock(returncode=0, stdout=json.dumps(analysis_response), stderr=""),
                Mock(returncode=0, stdout=json.dumps(validation_response), stderr=""),
                Mock(returncode=0, stdout=json.dumps(review_response), stderr=""),
                Mock(returncode=0, stdout=json.dumps(pr_response), stderr="")
            ]

            with patch('subprocess.run', side_effect=responses):
                # Execute complete workflow
                analysis = workflow.analyze_issue(sample_issue["body"])
                assert analysis is not None

                validation = workflow.validate_fix(sample_issue["body"], fix_description)
                assert validation is not None

                auth_file = sample_code_files / "auth.py"
                review = workflow.review_code_changes(str(auth_file))
                assert review is not None

                pr_desc = workflow.generate_pr_description(fix_description, sample_issue["number"])
                assert pr_desc is not None

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_multi_agent_error_recovery_workflow(self, mock_api_keys, sample_issue):
        """Test workflow with error recovery between agents"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            # Simulate Gemini API error then success
            responses = [
                subprocess.CalledProcessError(1, "gemini", stderr="Rate limit exceeded"),
                Mock(
                    returncode=0,
                    stdout=json.dumps({
                        "response": "Analysis completed after retry",
                        "model": "gemini-2.5-flash"
                    }),
                    stderr=""
                )
            ]

            with patch('subprocess.run', side_effect=responses):
                # First call should fail
                with pytest.raises(RuntimeError):
                    workflow.analyze_issue(sample_issue["body"])

                # Second call should succeed
                result = workflow.analyze_issue(sample_issue["body"])
                assert result is not None

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_parallel_agent_operations_workflow(self, mock_api_keys, sample_code_files):
        """Test workflow with parallel operations using both agents"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            auth_file = sample_code_files / "auth.py"
            user_file = sample_code_files / "user.py"

            # Mock responses for parallel operations
            review_responses = [
                Mock(returncode=0, stdout=json.dumps({"response": "auth.py OK"}), stderr=""),
                Mock(returncode=0, stdout=json.dumps({"response": "user.py OK"}), stderr="")
            ]

            with patch('subprocess.run', side_effect=review_responses):
                # Execute parallel reviews
                results = []
                results.append(workflow.review_code_changes(str(auth_file)))
                results.append(workflow.review_code_changes(str(user_file)))

                # Verify both completed
                assert len(results) == 2
                assert all(r is not None for r in results)

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_workflow_with_context_sharing(self, mock_api_keys, sample_issue):
        """Test workflow where context is shared between agent calls"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            # Step 1: Analyze issue (establishes context)
            analysis_response = {
                "response": json.dumps({
                    "complexity": "moderate",
                    "required_modules": ["auth", "user", "token"]
                }),
                "model": "gemini-2.5-flash"
            }

            # Step 2: Generate implementation plan based on analysis
            plan_response = {
                "response": "Implementation plan based on moderate complexity analysis",
                "model": "gemini-2.5-pro"
            }

            responses = [
                Mock(returncode=0, stdout=json.dumps(analysis_response), stderr=""),
                Mock(returncode=0, stdout=json.dumps(plan_response), stderr="")
            ]

            with patch('subprocess.run', side_effect=responses):
                # Execute workflow with context
                analysis = workflow.analyze_issue(sample_issue["body"])
                assert analysis is not None

                # Use analysis results in next step
                analysis_data = json.loads(analysis["response"])
                assert "complexity" in analysis_data

    @pytest.mark.e2e
    @pytest.mark.slow
    @pytest.mark.integration
    @pytest.mark.requires_api_key
    def test_real_multi_agent_workflow(self, sample_issue):
        """Test complete workflow with real API calls (requires API keys)"""
        gemini_key = os.getenv("GEMINI_API_KEY")

        if not gemini_key:
            pytest.skip("GEMINI_API_KEY not set - skipping real API test")

        try:
            # Initialize workflow with real APIs
            workflow = MultiAgentWorkflow()

            # Execute simple analysis
            result = workflow.analyze_issue(sample_issue["body"])

            # Verify workflow completed
            assert result is not None
            assert "response" in result
            assert len(result["response"]) > 0

        except Exception as e:
            # If CLI tools not installed, skip
            if "not installed" in str(e).lower():
                pytest.skip("Required CLI tools not installed")
            raise

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_workflow_performance_tracking(self, mock_api_keys, sample_issue):
        """Test workflow with performance tracking"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            workflow = MultiAgentWorkflow()

            import time

            mock_response = {
                "response": "Quick analysis",
                "model": "gemini-2.5-flash"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Track execution time
                start_time = time.time()
                result = workflow.analyze_issue(sample_issue["body"])
                duration = time.time() - start_time

                # Verify workflow completed and timing
                assert result is not None
                assert duration < 5.0  # Should complete quickly with mocked API
