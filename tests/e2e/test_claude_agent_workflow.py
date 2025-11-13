#!/usr/bin/env python3
"""
End-to-end tests for Claude Agent workflow
Tests complete workflow from initialization through code generation
"""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess
import json
import sys

# Add src directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "claude-agent"))

from claude_cli_agent import ClaudeAgent


class TestClaudeAgentWorkflow:
    """Test complete Claude agent workflows"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def sample_code_file(self, temp_workspace):
        """Create a sample code file for testing"""
        code_file = temp_workspace / "sample.py"
        code_file.write_text("""
def calculate_sum(a, b):
    '''Calculate sum of two numbers'''
    return a + b

if __name__ == '__main__':
    result = calculate_sum(5, 3)
    print(f'Sum: {result}')
""")
        return code_file

    @pytest.fixture
    def sample_broken_code(self, temp_workspace):
        """Create a sample file with broken code"""
        code_file = temp_workspace / "broken.py"
        code_file.write_text("""
def broken_function():
    '''This function has a bug'''
    x = 10
    y = 0
    return x / y  # Division by zero error
""")
        return code_file

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_agent_initialization_workflow(self):
        """Test complete workflow of initializing Claude agent"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            # Initialize agent
            agent = ClaudeAgent(output_format="json")

            # Verify initialization
            assert agent.output_format == "json"
            assert agent.verbose is False

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_agent_query_workflow(self, temp_workspace):
        """Test complete workflow of querying Claude agent"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            # Mock subprocess response
            mock_response = {
                "content": "Here's a hello world function in Python:\n\n```python\ndef hello():\n    print('Hello, World!')\n```",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute query
                result = agent.query("Write a hello world function")

                # Verify workflow
                assert result is not None
                assert "content" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_code_review_workflow(self, sample_code_file):
        """Test complete workflow of code review with Claude"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            # Mock subprocess response
            mock_response = {
                "content": "Code review:\n- Good: Clear function name\n- Good: Docstring present\n- Consider: Add type hints",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute code review
                result = agent.code_review(str(sample_code_file))

                # Verify workflow
                assert result is not None
                assert "content" in result
                mock_run.assert_called_once()

                # Verify the file path was used
                call_args = mock_run.call_args
                assert str(sample_code_file) in str(call_args)

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_fix_code_workflow(self, sample_broken_code):
        """Test complete workflow of fixing code with Claude"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            # Mock subprocess response
            mock_response = {
                "content": "Fixed the division by zero error by adding a check",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute fix
                result = agent.fix_code(
                    str(sample_broken_code),
                    "Fix the division by zero error"
                )

                # Verify workflow
                assert result is not None
                assert "content" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_documentation_generation_workflow(self, sample_code_file):
        """Test complete workflow of generating documentation with Claude"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            # Mock subprocess response
            mock_response = {
                "content": "# Documentation\n\n## calculate_sum\nCalculates the sum of two numbers.\n\n**Parameters:**\n- a: First number\n- b: Second number\n\n**Returns:** Sum of a and b",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute documentation generation
                result = agent.generate_docs(str(sample_code_file))

                # Verify workflow
                assert result is not None
                assert "content" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_batch_processing_workflow(self, temp_workspace):
        """Test complete workflow of batch processing multiple files"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            # Create multiple test files
            file1 = temp_workspace / "module1.py"
            file2 = temp_workspace / "module2.py"
            file1.write_text("# Module 1")
            file2.write_text("# Module 2")

            files = [str(file1), str(file2)]
            prompt = "Review these modules"

            # Mock subprocess responses
            mock_responses = [
                Mock(returncode=0, stdout=json.dumps({"content": "Module 1 OK"}), stderr=""),
                Mock(returncode=0, stdout=json.dumps({"content": "Module 2 OK"}), stderr="")
            ]

            with patch('subprocess.run', side_effect=mock_responses):
                # Execute batch processing
                results = agent.batch_process(files, prompt)

                # Verify workflow
                assert len(results) == 2
                assert all("content" in r for r in results)

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_with_system_prompt_workflow(self):
        """Test complete workflow with custom system prompt"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            system_prompt = "You are a Python expert. Be concise."
            mock_response = {
                "content": "Brief Python code example",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute query with system prompt
                result = agent.query("Write code", system_prompt=system_prompt)

                # Verify workflow
                assert result is not None
                mock_run.assert_called_once()

                # Verify system prompt was used
                call_args = str(mock_run.call_args)
                assert "--system-prompt" in call_args or "system" in call_args.lower()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_permission_modes_workflow(self):
        """Test complete workflow with different permission modes"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            # Test with acceptEdits permission
            agent = ClaudeAgent(
                output_format="json",
                permission_mode="acceptEdits"
            )

            mock_response = {
                "content": "Edits applied automatically",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute query
                result = agent.query("Make changes to code")

                # Verify workflow
                assert result is not None
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_tool_restrictions_workflow(self):
        """Test complete workflow with tool restrictions"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            # Test with allowed tools
            agent = ClaudeAgent(
                output_format="json",
                allowed_tools=["Read", "Edit"]
            )

            mock_response = {
                "content": "Using only Read and Edit tools",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute query
                result = agent.query("Review and edit code")

                # Verify workflow
                assert result is not None
                mock_run.assert_called_once()

                # Verify tools restriction was applied
                call_args = str(mock_run.call_args)
                assert "allowedTools" in call_args or "allowed" in call_args.lower()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_continue_conversation_workflow(self):
        """Test complete workflow of continuing a conversation"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            mock_response = {
                "content": "Continuing from previous context",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute continue conversation
                result = agent.continue_conversation("Add more details")

                # Verify workflow
                assert result is not None
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_error_handling_workflow(self):
        """Test complete workflow with error handling"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            # Mock subprocess error
            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.CalledProcessError(
                    1, "claude", stderr="API error"
                )

                # Execute query and expect error handling
                with pytest.raises(RuntimeError):
                    agent.query("Test prompt")

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_stdin_workflow(self):
        """Test complete workflow with stdin input"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            stdin_content = "This is content from stdin"
            mock_response = {
                "content": "Processed stdin content",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute query with stdin
                result = agent.query_with_stdin(
                    "Process this content",
                    stdin_content
                )

                # Verify workflow
                assert result is not None
                mock_run.assert_called_once()

                # Verify stdin was used
                call_args = mock_run.call_args
                assert call_args.kwargs.get('input') == stdin_content

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_claude_mcp_configuration_workflow(self):
        """Test complete workflow with MCP configuration"""
        with patch.object(ClaudeAgent, '_is_claude_installed', return_value=True):
            agent = ClaudeAgent(output_format="json")

            mock_response = {
                "content": "Using MCP servers",
                "model": "claude-sonnet-4-5"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute query with MCP config
                result = agent.query(
                    "Use external tools",
                    mcp_config_path="/path/to/mcp.json"
                )

                # Verify workflow
                assert result is not None
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    @pytest.mark.integration
    @pytest.mark.requires_api_key
    def test_claude_real_cli_workflow(self):
        """Test complete workflow with real Claude CLI (requires installation)"""
        try:
            # Check if Claude CLI is installed
            subprocess.run(
                ["claude", "--version"],
                check=True,
                capture_output=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            pytest.skip("Claude CLI not installed")

        # Initialize with real CLI
        agent = ClaudeAgent(output_format="text")

        try:
            # Execute simple query
            result = agent.query("Say 'Hello from Claude'")

            # Verify workflow completed
            assert result is not None
            assert len(str(result)) > 0

        except Exception as e:
            # Handle potential errors gracefully
            if "authentication" in str(e).lower() or "api key" in str(e).lower():
                pytest.skip("Claude authentication not configured")
            raise
