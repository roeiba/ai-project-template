#!/usr/bin/env python3
"""
End-to-end tests for Gemini Agent workflow
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
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "gemini-agent"))

from gemini_agent import GeminiAgent


class TestGeminiAgentWorkflow:
    """Test complete Gemini agent workflows"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def mock_gemini_api_key(self, monkeypatch):
        """Mock Gemini API key"""
        monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")
        return "test-key-123"

    @pytest.fixture
    def sample_code_file(self, temp_workspace):
        """Create a sample code file for testing"""
        code_file = temp_workspace / "sample.py"
        code_file.write_text("""
def hello_world():
    '''Print hello world'''
    print('Hello, World!')

if __name__ == '__main__':
    hello_world()
""")
        return code_file

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_agent_initialization_workflow(self, mock_gemini_api_key):
        """Test complete workflow of initializing Gemini agent"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            # Initialize agent
            agent = GeminiAgent(api_key=mock_gemini_api_key)

            # Verify initialization
            assert agent.api_key == mock_gemini_api_key
            assert agent.model == "gemini-2.5-pro"
            assert agent.output_format == "json"

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_agent_query_workflow(self, mock_gemini_api_key, temp_workspace):
        """Test complete workflow of querying Gemini agent"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            agent = GeminiAgent(api_key=mock_gemini_api_key)

            # Mock subprocess response
            mock_response = {
                "response": "This is a test response",
                "model": "gemini-2.5-pro",
                "finish_reason": "STOP"
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
                assert "response" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_code_review_workflow(self, mock_gemini_api_key, sample_code_file):
        """Test complete workflow of code review with Gemini"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            agent = GeminiAgent(api_key=mock_gemini_api_key)

            # Mock subprocess response
            mock_response = {
                "response": "Code looks good. Well structured.",
                "model": "gemini-2.5-pro"
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
                assert "response" in result
                mock_run.assert_called_once()

                # Verify the file path was used
                call_args = mock_run.call_args
                assert str(sample_code_file) in str(call_args)

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_documentation_generation_workflow(self, mock_gemini_api_key, sample_code_file):
        """Test complete workflow of generating documentation with Gemini"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            agent = GeminiAgent(api_key=mock_gemini_api_key)

            # Mock subprocess response
            mock_response = {
                "response": "# Documentation\n\n## hello_world\nPrints hello world message.",
                "model": "gemini-2.5-pro"
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
                assert "response" in result
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_batch_processing_workflow(self, mock_gemini_api_key, temp_workspace):
        """Test complete workflow of batch processing multiple files"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            agent = GeminiAgent(api_key=mock_gemini_api_key)

            # Create multiple test files
            file1 = temp_workspace / "file1.py"
            file2 = temp_workspace / "file2.py"
            file1.write_text("# File 1")
            file2.write_text("# File 2")

            files = [str(file1), str(file2)]
            prompt = "Review these files"

            # Mock subprocess responses
            mock_responses = [
                Mock(returncode=0, stdout=json.dumps({"response": "File 1 OK"}), stderr=""),
                Mock(returncode=0, stdout=json.dumps({"response": "File 2 OK"}), stderr="")
            ]

            with patch('subprocess.run', side_effect=mock_responses):
                # Execute batch processing
                results = agent.batch_process(files, prompt)

                # Verify workflow
                assert len(results) == 2
                assert all("response" in r for r in results)

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_error_handling_workflow(self, mock_gemini_api_key):
        """Test complete workflow with error handling"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            agent = GeminiAgent(api_key=mock_gemini_api_key)

            # Mock subprocess error
            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.CalledProcessError(
                    1, "gemini", stderr="API error"
                )

                # Execute query and expect error handling
                with pytest.raises(RuntimeError):
                    agent.query("Test prompt")

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_yolo_mode_workflow(self, mock_gemini_api_key, temp_workspace):
        """Test complete workflow with YOLO mode (auto-approve)"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            agent = GeminiAgent(api_key=mock_gemini_api_key)

            mock_response = {
                "response": "Changes applied automatically",
                "model": "gemini-2.5-pro"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute with YOLO mode
                result = agent.query("Make changes", yolo=True)

                # Verify workflow
                assert result is not None
                mock_run.assert_called_once()

                # Verify YOLO flag was passed
                call_args = mock_run.call_args
                assert "--yolo" in str(call_args) or "yolo" in str(call_args).lower()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_include_directories_workflow(self, mock_gemini_api_key, temp_workspace):
        """Test complete workflow with including additional directories"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            agent = GeminiAgent(api_key=mock_gemini_api_key)

            # Create additional directories
            src_dir = temp_workspace / "src"
            tests_dir = temp_workspace / "tests"
            src_dir.mkdir()
            tests_dir.mkdir()

            (src_dir / "main.py").write_text("# Main")
            (tests_dir / "test.py").write_text("# Test")

            mock_response = {
                "response": "Analyzed all directories",
                "model": "gemini-2.5-pro"
            }

            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=0,
                    stdout=json.dumps(mock_response),
                    stderr=""
                )

                # Execute with include directories
                result = agent.query(
                    "Analyze codebase",
                    include_directories=[str(src_dir), str(tests_dir)]
                )

                # Verify workflow
                assert result is not None
                mock_run.assert_called_once()

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_gemini_model_selection_workflow(self, mock_gemini_api_key):
        """Test complete workflow with different model selection"""
        with patch.object(GeminiAgent, '_is_gemini_installed', return_value=True):
            # Test with different models
            models = ["gemini-2.5-pro", "gemini-2.5-flash"]

            for model in models:
                agent = GeminiAgent(api_key=mock_gemini_api_key, model=model)

                mock_response = {
                    "response": f"Response from {model}",
                    "model": model
                }

                with patch('subprocess.run') as mock_run:
                    mock_run.return_value = Mock(
                        returncode=0,
                        stdout=json.dumps(mock_response),
                        stderr=""
                    )

                    # Execute query
                    result = agent.query("Test prompt", model=model)

                    # Verify workflow
                    assert result is not None
                    assert result.get("model") == model

    @pytest.mark.e2e
    @pytest.mark.slow
    @pytest.mark.integration
    @pytest.mark.requires_api_key
    def test_gemini_real_api_workflow(self):
        """Test complete workflow with real Gemini API (requires API key)"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            pytest.skip("GEMINI_API_KEY not set - skipping real API test")

        try:
            # Initialize with real API
            agent = GeminiAgent(api_key=api_key, model="gemini-2.5-flash")

            # Execute simple query
            result = agent.query("Say 'Hello from Gemini'")

            # Verify workflow completed
            assert result is not None
            assert "response" in result
            assert len(result["response"]) > 0

        except Exception as e:
            # If gemini CLI is not installed, skip
            if "not installed" in str(e).lower():
                pytest.skip("Gemini CLI not installed")
            raise
