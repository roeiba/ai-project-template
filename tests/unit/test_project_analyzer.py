#!/usr/bin/env python3
"""
Unit tests for Project Analyzer
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agents.project_analyzer import ProjectAnalyzer


class TestProjectAnalyzer:
    """Test suite for ProjectAnalyzer"""

    @pytest.fixture
    def mock_repo(self):
        """Create a mock GitHub repository"""
        repo = Mock()
        repo.full_name = "test/repo"
        return repo

    @pytest.fixture
    def analyzer(self, mock_repo):
        """Create a ProjectAnalyzer instance with mock repo"""
        return ProjectAnalyzer(mock_repo)

    def test_init(self, mock_repo):
        """Test ProjectAnalyzer initialization"""
        analyzer = ProjectAnalyzer(mock_repo)
        assert analyzer.repo == mock_repo

    def test_analyze_directory_structure_basic(self, analyzer, mock_repo):
        """Test basic directory structure analysis"""
        # Mock contents
        mock_dir = Mock()
        mock_dir.type = "dir"
        mock_dir.path = "src"
        mock_dir.name = "src"

        mock_file = Mock()
        mock_file.type = "file"
        mock_file.name = "README.md"

        mock_repo.get_contents.return_value = [mock_dir, mock_file]

        result = analyzer._analyze_directory_structure()

        assert "total_directories" in result
        assert "top_level_dirs" in result
        assert "has_src" in result
        assert result["has_src"] is True

    def test_analyze_directory_structure_error_handling(self, analyzer, mock_repo):
        """Test directory structure analysis handles errors gracefully"""
        mock_repo.get_contents.side_effect = Exception("API Error")

        result = analyzer._analyze_directory_structure()

        assert "error" in result

    def test_analyze_file_types_basic(self, analyzer, mock_repo):
        """Test file type analysis"""
        # Mock Python file
        mock_py_file = Mock()
        mock_py_file.type = "file"
        mock_py_file.name = "main.py"

        # Mock JavaScript file
        mock_js_file = Mock()
        mock_js_file.type = "file"
        mock_js_file.name = "app.js"

        mock_repo.get_contents.return_value = [mock_py_file, mock_js_file]

        result = analyzer._analyze_file_types()

        assert "total_files" in result
        assert "file_types" in result
        assert "primary_language" in result
        assert result["total_files"] == 2

    def test_determine_primary_language_python(self, analyzer):
        """Test primary language detection for Python"""
        file_types = {".py": 10, ".md": 5, ".txt": 2}
        result = analyzer._determine_primary_language(file_types)
        assert result == "Python"

    def test_determine_primary_language_javascript(self, analyzer):
        """Test primary language detection for JavaScript"""
        file_types = {".js": 15, ".json": 5, ".md": 2}
        result = analyzer._determine_primary_language(file_types)
        assert result == "JavaScript"

    def test_determine_primary_language_unknown(self, analyzer):
        """Test primary language detection for unknown types"""
        file_types = {".txt": 10, ".md": 5}
        result = analyzer._determine_primary_language(file_types)
        assert result == "Unknown"

    def test_detect_technology_stack_package_json(self, analyzer, mock_repo):
        """Test technology stack detection with package.json"""
        # Mock package.json
        mock_package = Mock()
        mock_package.name = "package.json"
        mock_package.type = "file"
        mock_package.decoded_content.decode.return_value = """{
            "dependencies": {
                "react": "^18.0.0",
                "express": "^4.18.0"
            }
        }"""

        mock_repo.get_contents.side_effect = [
            [mock_package],  # Root contents
            mock_package,  # Direct package.json read
        ]

        result = analyzer._detect_technology_stack()

        assert "package_managers" in result
        assert "Node.js/npm" in result["package_managers"]
        assert "frameworks" in result
        assert "React" in result["frameworks"]
        assert "Express" in result["frameworks"]

    def test_detect_technology_stack_requirements_txt(self, analyzer, mock_repo):
        """Test technology stack detection with requirements.txt"""
        # Mock requirements.txt
        mock_requirements = Mock()
        mock_requirements.name = "requirements.txt"
        mock_requirements.type = "file"
        mock_requirements.decoded_content.decode.return_value = """django==4.0.0
flask==2.0.0
fastapi==0.95.0"""

        mock_repo.get_contents.side_effect = [
            [mock_requirements],  # Root contents
            Exception("No package.json"),  # No package.json
            mock_requirements,  # Direct requirements.txt read
        ]

        result = analyzer._detect_technology_stack()

        assert "package_managers" in result
        assert "Python/pip" in result["package_managers"]

    def test_analyze_code_patterns_basic(self, analyzer, mock_repo):
        """Test code pattern analysis"""
        # Mock Python file with various patterns
        mock_py_file = Mock()
        mock_py_file.type = "file"
        mock_py_file.name = "test_module.py"
        mock_py_file.path = "src/test_module.py"
        mock_py_file.decoded_content.decode.return_value = """
class MyClass:
    async def my_method(self):
        pass

def test_something():
    assert True
"""

        mock_repo.get_contents.side_effect = [
            [mock_py_file],  # Root contents
            mock_py_file,  # File read
        ]

        result = analyzer._analyze_code_patterns()

        assert "has_classes" in result
        assert "has_functions" in result
        assert "has_async" in result
        assert "has_tests" in result

    def test_analyze_documentation_complete(self, analyzer, mock_repo):
        """Test documentation analysis with complete docs"""
        mock_readme = Mock()
        mock_readme.type = "file"
        mock_readme.name = "README.md"

        mock_contributing = Mock()
        mock_contributing.type = "file"
        mock_contributing.name = "CONTRIBUTING.md"

        mock_changelog = Mock()
        mock_changelog.type = "file"
        mock_changelog.name = "CHANGELOG.md"

        mock_license = Mock()
        mock_license.type = "file"
        mock_license.name = "LICENSE"

        mock_docs_dir = Mock()
        mock_docs_dir.type = "dir"
        mock_docs_dir.name = "docs"

        mock_repo.get_contents.return_value = [
            mock_readme,
            mock_contributing,
            mock_changelog,
            mock_license,
            mock_docs_dir,
        ]

        result = analyzer._analyze_documentation()

        assert result["has_readme"] is True
        assert result["has_contributing"] is True
        assert result["has_changelog"] is True
        assert result["has_license"] is True
        assert result["has_docs_folder"] is True

    def test_analyze_testing_setup_with_pytest(self, analyzer, mock_repo):
        """Test testing setup analysis with pytest"""
        mock_test_dir = Mock()
        mock_test_dir.type = "dir"
        mock_test_dir.name = "tests"

        mock_pytest_ini = Mock()
        mock_pytest_ini.type = "file"
        mock_pytest_ini.name = "pytest.ini"

        mock_coveragerc = Mock()
        mock_coveragerc.type = "file"
        mock_coveragerc.name = ".coveragerc"

        mock_repo.get_contents.return_value = [
            mock_test_dir,
            mock_pytest_ini,
            mock_coveragerc,
        ]

        result = analyzer._analyze_testing_setup()

        assert result["has_test_directory"] is True
        assert "pytest" in result["test_frameworks"]
        assert result["test_coverage"] is True

    def test_analyze_ci_cd_github_actions(self, analyzer, mock_repo):
        """Test CI/CD analysis with GitHub Actions"""
        mock_workflow = Mock()
        mock_workflow.type = "file"
        mock_workflow.name = "ci.yml"
        mock_workflow.decoded_content.decode.return_value = """
name: CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
  deploy:
    runs-on: ubuntu-latest
"""

        def get_contents_side_effect(path):
            if path == ".github/workflows":
                return [mock_workflow]
            elif path == "":
                mock_github_dir = Mock()
                mock_github_dir.type = "dir"
                mock_github_dir.name = ".github"
                return [mock_github_dir]
            raise Exception("Not found")

        mock_repo.get_contents.side_effect = get_contents_side_effect

        result = analyzer._analyze_ci_cd()

        assert result["has_ci"] is True
        assert "GitHub Actions" in result["platforms"]
        assert result["has_deployment"] is True

    def test_generate_context_summary_complete(self, analyzer):
        """Test context summary generation with complete analysis"""
        analysis = {
            "directory_structure": {
                "total_directories": 10,
                "top_level_dirs": ["src", "tests", "docs"],
                "key_directories": {"src": True, "tests": True},
            },
            "file_types": {
                "total_files": 50,
                "primary_language": "Python",
                "file_types": {".py": 30, ".md": 10, ".json": 5},
            },
            "technology_stack": {
                "package_managers": ["Python/pip"],
                "frameworks": ["FastAPI", "pytest"],
                "tools": ["Docker", "GitHub Actions"],
            },
            "code_patterns": {
                "has_classes": True,
                "has_async": True,
                "has_tests": True,
                "architectural_patterns": ["Factory Pattern"],
            },
            "documentation": {
                "has_readme": True,
                "has_contributing": True,
                "has_docs_folder": True,
            },
            "testing": {
                "has_test_directory": True,
                "test_frameworks": ["pytest"],
                "test_coverage": True,
            },
            "ci_cd": {
                "has_ci": True,
                "platforms": ["GitHub Actions"],
                "has_deployment": True,
            },
        }

        result = analyzer.generate_context_summary(analysis)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Directory Structure:" in result
        assert "File Analysis:" in result
        assert "Technology Stack:" in result
        assert "Code Patterns:" in result
        assert "Documentation:" in result
        assert "Testing:" in result
        assert "CI/CD:" in result

    def test_generate_context_summary_minimal(self, analyzer):
        """Test context summary generation with minimal analysis"""
        analysis = {
            "directory_structure": {"error": "Could not access"},
            "file_types": {"error": "Could not access"},
            "technology_stack": {},
            "code_patterns": {},
            "documentation": {},
            "testing": {},
            "ci_cd": {},
        }

        result = analyzer.generate_context_summary(analysis)

        assert isinstance(result, str)
        # Should handle empty/error data gracefully

    def test_analyze_project_integration(self, analyzer, mock_repo):
        """Test full project analysis integration"""
        # Mock minimal repository
        mock_file = Mock()
        mock_file.type = "file"
        mock_file.name = "README.md"

        mock_repo.get_contents.return_value = [mock_file]

        result = analyzer.analyze_project()

        assert "directory_structure" in result
        assert "file_types" in result
        assert "technology_stack" in result
        assert "code_patterns" in result
        assert "documentation" in result
        assert "testing" in result
        assert "ci_cd" in result
