#!/usr/bin/env python3
"""
Project Analyzer - Enhanced Context Analysis for Issue Generation

Provides comprehensive project structure and code pattern analysis
to help the issue generator make better suggestions.
"""

import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class ProjectAnalyzer:
    """Analyzes project structure, files, and code patterns"""

    def __init__(self, repo):
        """
        Initialize the Project Analyzer

        Args:
            repo: PyGithub Repository object
        """
        self.repo = repo

    def analyze_project(self) -> Dict:
        """
        Perform comprehensive project analysis

        Returns:
            Dict containing project structure, file types, and code patterns
        """
        print("🔍 Starting comprehensive project analysis...")

        analysis = {
            "directory_structure": self._analyze_directory_structure(),
            "file_types": self._analyze_file_types(),
            "technology_stack": self._detect_technology_stack(),
            "code_patterns": self._analyze_code_patterns(),
            "documentation": self._analyze_documentation(),
            "testing": self._analyze_testing_setup(),
            "ci_cd": self._analyze_ci_cd(),
        }

        print("✅ Project analysis complete")
        return analysis

    def _analyze_directory_structure(self) -> Dict:
        """Analyze the directory structure of the repository"""
        print("📁 Analyzing directory structure...")

        try:
            contents = self.repo.get_contents("")
            dirs = []
            key_dirs = {
                "src": False,
                "tests": False,
                "docs": False,
                "scripts": False,
                ".github": False,
                "config": False,
            }

            def traverse_dir(items, path="", depth=0, max_depth=3):
                """Recursively traverse directories"""
                if depth > max_depth:
                    return

                for item in items:
                    if item.type == "dir":
                        dir_name = item.path
                        dirs.append(dir_name)

                        # Check if it's a key directory
                        base_name = os.path.basename(dir_name)
                        if base_name in key_dirs:
                            key_dirs[base_name] = True

                        # Recurse into subdirectories
                        try:
                            subdirs = self.repo.get_contents(item.path)
                            if isinstance(subdirs, list):
                                traverse_dir(subdirs, item.path, depth + 1)
                        except:
                            pass  # Skip if we can't access

            traverse_dir(contents)

            return {
                "total_directories": len(dirs),
                "top_level_dirs": [d for d in dirs if "/" not in d],
                "key_directories": {k: v for k, v in key_dirs.items() if v},
                "has_src": key_dirs["src"],
                "has_tests": key_dirs["tests"],
                "has_docs": key_dirs["docs"],
            }

        except Exception as e:
            print(f"⚠️  Error analyzing directory structure: {e}")
            return {"error": str(e)}

    def _analyze_file_types(self) -> Dict:
        """Analyze file types and count them"""
        print("📄 Analyzing file types...")

        try:
            file_counts = defaultdict(int)
            total_files = 0

            contents = self.repo.get_contents("")

            def count_files(items, depth=0, max_depth=3):
                """Recursively count file types"""
                nonlocal total_files
                if depth > max_depth:
                    return

                for item in items:
                    if item.type == "file":
                        total_files += 1
                        ext = Path(item.name).suffix.lower()
                        if ext:
                            file_counts[ext] += 1
                        else:
                            file_counts["[no extension]"] += 1
                    elif item.type == "dir":
                        try:
                            subdirs = self.repo.get_contents(item.path)
                            if isinstance(subdirs, list):
                                count_files(subdirs, depth + 1)
                        except:
                            pass

            count_files(contents)

            # Sort by count
            sorted_types = sorted(
                file_counts.items(), key=lambda x: x[1], reverse=True
            )

            return {
                "total_files": total_files,
                "file_types": dict(sorted_types[:10]),  # Top 10 file types
                "primary_language": self._determine_primary_language(dict(sorted_types)),
            }

        except Exception as e:
            print(f"⚠️  Error analyzing file types: {e}")
            return {"error": str(e)}

    def _determine_primary_language(self, file_types: Dict) -> str:
        """Determine primary programming language from file types"""
        language_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".jsx": "JavaScript (React)",
            ".tsx": "TypeScript (React)",
            ".go": "Go",
            ".java": "Java",
            ".rb": "Ruby",
            ".php": "PHP",
            ".rs": "Rust",
            ".cpp": "C++",
            ".c": "C",
            ".cs": "C#",
        }

        for ext, count in file_types.items():
            if ext in language_map:
                return language_map[ext]

        return "Unknown"

    def _detect_technology_stack(self) -> Dict:
        """Detect technology stack from key files"""
        print("🔧 Detecting technology stack...")

        tech_stack = {
            "languages": [],
            "frameworks": [],
            "tools": [],
            "package_managers": [],
        }

        try:
            # Check for key configuration files
            key_files = {
                "package.json": "Node.js/npm",
                "requirements.txt": "Python/pip",
                "Pipfile": "Python/pipenv",
                "pyproject.toml": "Python/poetry",
                "go.mod": "Go modules",
                "Cargo.toml": "Rust/Cargo",
                "pom.xml": "Java/Maven",
                "build.gradle": "Java/Gradle",
                "composer.json": "PHP/Composer",
                "Gemfile": "Ruby/Bundler",
            }

            # Check for CI/CD files
            ci_files = {
                ".github/workflows": "GitHub Actions",
                ".gitlab-ci.yml": "GitLab CI",
                ".travis.yml": "Travis CI",
                "Jenkinsfile": "Jenkins",
            }

            # Check for containerization
            container_files = {
                "Dockerfile": "Docker",
                "docker-compose.yml": "Docker Compose",
                "kubernetes": "Kubernetes",
            }

            contents = self.repo.get_contents("")

            def check_files(items):
                """Check for key technology indicator files"""
                for item in items:
                    if item.type == "file":
                        if item.name in key_files:
                            tech_stack["package_managers"].append(key_files[item.name])
                        if item.name in container_files:
                            tech_stack["tools"].append(container_files[item.name])
                    elif item.type == "dir":
                        if item.name in ci_files:
                            tech_stack["tools"].append(ci_files[item.name])
                        # Check subdirectories for CI/CD
                        try:
                            if item.name == ".github":
                                subdirs = self.repo.get_contents(item.path)
                                if isinstance(subdirs, list):
                                    for subitem in subdirs:
                                        if (
                                            subitem.type == "dir"
                                            and subitem.name == "workflows"
                                        ):
                                            tech_stack["tools"].append("GitHub Actions")
                                            break
                        except:
                            pass

            check_files(contents)

            # Try to read package.json or requirements.txt for framework detection
            try:
                package_json = self.repo.get_contents("package.json")
                import json

                data = json.loads(package_json.decoded_content.decode("utf-8"))
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

                # Detect frameworks
                if "react" in deps:
                    tech_stack["frameworks"].append("React")
                if "next" in deps:
                    tech_stack["frameworks"].append("Next.js")
                if "vue" in deps:
                    tech_stack["frameworks"].append("Vue.js")
                if "angular" in deps or "@angular/core" in deps:
                    tech_stack["frameworks"].append("Angular")
                if "express" in deps:
                    tech_stack["frameworks"].append("Express")
                if "fastify" in deps:
                    tech_stack["frameworks"].append("Fastify")

            except:
                pass

            try:
                requirements = self.repo.get_contents("requirements.txt")
                content = requirements.decoded_content.decode("utf-8")

                # Detect Python frameworks
                if "django" in content.lower():
                    tech_stack["frameworks"].append("Django")
                if "flask" in content.lower():
                    tech_stack["frameworks"].append("Flask")
                if "fastapi" in content.lower():
                    tech_stack["frameworks"].append("FastAPI")

            except:
                pass

        except Exception as e:
            print(f"⚠️  Error detecting technology stack: {e}")

        return tech_stack

    def _analyze_code_patterns(self) -> Dict:
        """Analyze common code patterns in the repository"""
        print("🔍 Analyzing code patterns...")

        patterns = {
            "has_classes": False,
            "has_functions": False,
            "has_tests": False,
            "has_async": False,
            "architectural_patterns": [],
        }

        try:
            # Sample some Python files to detect patterns
            contents = self.repo.get_contents("")

            def analyze_python_file(file_path):
                """Analyze a Python file for patterns"""
                try:
                    file_content = self.repo.get_contents(file_path)
                    code = file_content.decoded_content.decode("utf-8")

                    if "class " in code:
                        patterns["has_classes"] = True
                    if "def " in code:
                        patterns["has_functions"] = True
                    if "async def" in code or "await " in code:
                        patterns["has_async"] = True
                    if "test_" in code or "Test" in code:
                        patterns["has_tests"] = True

                    # Check for architectural patterns
                    if "Factory" in code or "factory" in code:
                        if "Factory" not in patterns["architectural_patterns"]:
                            patterns["architectural_patterns"].append("Factory Pattern")
                    if "Singleton" in code:
                        if "Singleton" not in patterns["architectural_patterns"]:
                            patterns["architectural_patterns"].append(
                                "Singleton Pattern"
                            )
                    if "Observer" in code or "observer" in code:
                        if "Observer" not in patterns["architectural_patterns"]:
                            patterns["architectural_patterns"].append(
                                "Observer Pattern"
                            )

                except:
                    pass

            # Sample a few Python files
            py_files_checked = 0
            max_files = 5

            def check_py_files(items, depth=0, max_depth=2):
                """Check Python files for patterns"""
                nonlocal py_files_checked
                if depth > max_depth or py_files_checked >= max_files:
                    return

                for item in items:
                    if py_files_checked >= max_files:
                        break

                    if item.type == "file" and item.name.endswith(".py"):
                        analyze_python_file(item.path)
                        py_files_checked += 1
                    elif item.type == "dir" and not item.name.startswith("."):
                        try:
                            subdirs = self.repo.get_contents(item.path)
                            if isinstance(subdirs, list):
                                check_py_files(subdirs, depth + 1)
                        except:
                            pass

            check_py_files(contents)

        except Exception as e:
            print(f"⚠️  Error analyzing code patterns: {e}")

        return patterns

    def _analyze_documentation(self) -> Dict:
        """Analyze documentation coverage"""
        print("📚 Analyzing documentation...")

        docs = {
            "has_readme": False,
            "has_contributing": False,
            "has_changelog": False,
            "has_license": False,
            "has_docs_folder": False,
            "doc_files": [],
        }

        try:
            contents = self.repo.get_contents("")

            for item in contents:
                name_lower = item.name.lower()
                if name_lower == "readme.md" or name_lower == "readme":
                    docs["has_readme"] = True
                elif name_lower == "contributing.md":
                    docs["has_contributing"] = True
                elif name_lower == "changelog.md":
                    docs["has_changelog"] = True
                elif name_lower.startswith("license"):
                    docs["has_license"] = True
                elif item.type == "dir" and name_lower == "docs":
                    docs["has_docs_folder"] = True
                elif item.type == "file" and name_lower.endswith(".md"):
                    docs["doc_files"].append(item.name)

        except Exception as e:
            print(f"⚠️  Error analyzing documentation: {e}")

        return docs

    def _analyze_testing_setup(self) -> Dict:
        """Analyze testing infrastructure"""
        print("🧪 Analyzing testing setup...")

        testing = {
            "has_test_directory": False,
            "has_test_files": False,
            "test_frameworks": [],
            "test_coverage": False,
        }

        try:
            contents = self.repo.get_contents("")

            for item in contents:
                name_lower = item.name.lower()
                if item.type == "dir" and ("test" in name_lower or name_lower == "spec"):
                    testing["has_test_directory"] = True

            # Check for test framework config files
            test_configs = {
                "pytest.ini": "pytest",
                "setup.cfg": "pytest/unittest",
                "jest.config.js": "Jest",
                "karma.conf.js": "Karma",
                ".coveragerc": "Coverage",
                "coverage": "Coverage",
            }

            for item in contents:
                if item.name in test_configs:
                    framework = test_configs[item.name]
                    if framework == "Coverage":
                        testing["test_coverage"] = True
                    elif framework not in testing["test_frameworks"]:
                        testing["test_frameworks"].append(framework)

        except Exception as e:
            print(f"⚠️  Error analyzing testing setup: {e}")

        return testing

    def _analyze_ci_cd(self) -> Dict:
        """Analyze CI/CD setup"""
        print("🚀 Analyzing CI/CD configuration...")

        ci_cd = {
            "has_ci": False,
            "platforms": [],
            "has_deployment": False,
        }

        try:
            # Check for .github/workflows
            try:
                workflows = self.repo.get_contents(".github/workflows")
                if workflows:
                    ci_cd["has_ci"] = True
                    ci_cd["platforms"].append("GitHub Actions")

                    # Check if any workflow has deployment steps
                    if isinstance(workflows, list):
                        for workflow in workflows:
                            if workflow.type == "file":
                                content = workflow.decoded_content.decode("utf-8")
                                if "deploy" in content.lower():
                                    ci_cd["has_deployment"] = True
                                    break
            except:
                pass

            # Check for other CI platforms
            try:
                contents = self.repo.get_contents("")
                for item in contents:
                    if item.name == ".gitlab-ci.yml":
                        ci_cd["has_ci"] = True
                        ci_cd["platforms"].append("GitLab CI")
                    elif item.name == ".travis.yml":
                        ci_cd["has_ci"] = True
                        ci_cd["platforms"].append("Travis CI")
                    elif item.name == "Jenkinsfile":
                        ci_cd["has_ci"] = True
                        ci_cd["platforms"].append("Jenkins")
            except:
                pass

        except Exception as e:
            print(f"⚠️  Error analyzing CI/CD: {e}")

        return ci_cd

    def generate_context_summary(self, analysis: Dict) -> str:
        """
        Generate a human-readable summary of the project analysis

        Args:
            analysis: The analysis dictionary from analyze_project()

        Returns:
            str: Formatted context summary
        """
        lines = []

        # Directory structure
        dir_info = analysis.get("directory_structure", {})
        if not dir_info.get("error"):
            lines.append("Directory Structure:")
            lines.append(
                f"  - Total directories: {dir_info.get('total_directories', 0)}"
            )
            lines.append(
                f"  - Top-level: {', '.join(dir_info.get('top_level_dirs', [])[:5])}"
            )
            key_dirs = dir_info.get("key_directories", {})
            if key_dirs:
                lines.append(f"  - Key directories: {', '.join(key_dirs.keys())}")

        # File types
        file_info = analysis.get("file_types", {})
        if not file_info.get("error"):
            lines.append(f"\nFile Analysis:")
            lines.append(f"  - Total files: {file_info.get('total_files', 0)}")
            lines.append(
                f"  - Primary language: {file_info.get('primary_language', 'Unknown')}"
            )
            file_types = file_info.get("file_types", {})
            if file_types:
                top_types = list(file_types.items())[:3]
                lines.append(
                    f"  - Main file types: {', '.join([f'{k}({v})' for k, v in top_types])}"
                )

        # Technology stack
        tech = analysis.get("technology_stack", {})
        if tech.get("package_managers"):
            lines.append(f"\nTechnology Stack:")
            lines.append(f"  - Package managers: {', '.join(tech['package_managers'])}")
        if tech.get("frameworks"):
            lines.append(f"  - Frameworks: {', '.join(tech['frameworks'])}")
        if tech.get("tools"):
            lines.append(f"  - Tools: {', '.join(tech['tools'])}")

        # Code patterns
        patterns = analysis.get("code_patterns", {})
        if patterns:
            lines.append(f"\nCode Patterns:")
            features = []
            if patterns.get("has_classes"):
                features.append("OOP/Classes")
            if patterns.get("has_async"):
                features.append("Async")
            if patterns.get("has_tests"):
                features.append("Tests")
            if features:
                lines.append(f"  - Features: {', '.join(features)}")
            if patterns.get("architectural_patterns"):
                lines.append(
                    f"  - Patterns: {', '.join(patterns['architectural_patterns'])}"
                )

        # Documentation
        docs = analysis.get("documentation", {})
        doc_status = []
        if docs.get("has_readme"):
            doc_status.append("README")
        if docs.get("has_contributing"):
            doc_status.append("CONTRIBUTING")
        if docs.get("has_changelog"):
            doc_status.append("CHANGELOG")
        if docs.get("has_docs_folder"):
            doc_status.append("docs/")
        if doc_status:
            lines.append(f"\nDocumentation: {', '.join(doc_status)}")

        # Testing
        testing = analysis.get("testing", {})
        if testing.get("has_test_directory") or testing.get("test_frameworks"):
            lines.append(f"\nTesting:")
            if testing.get("test_frameworks"):
                lines.append(f"  - Frameworks: {', '.join(testing['test_frameworks'])}")
            if testing.get("test_coverage"):
                lines.append(f"  - Coverage tracking: Yes")

        # CI/CD
        ci_cd = analysis.get("ci_cd", {})
        if ci_cd.get("has_ci"):
            lines.append(f"\nCI/CD:")
            lines.append(f"  - Platforms: {', '.join(ci_cd['platforms'])}")
            if ci_cd.get("has_deployment"):
                lines.append(f"  - Deployment configured: Yes")

        return "\n".join(lines)
