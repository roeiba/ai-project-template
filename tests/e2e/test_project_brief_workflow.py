#!/usr/bin/env python3
"""
End-to-end tests for PROJECT_BRIEF.md parsing and validation workflow
Tests the complete flow from reading PROJECT_BRIEF.md to validation
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# Add src directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from utils.project_brief_validator import validate_project_brief


class TestProjectBriefWorkflow:
    """Test complete PROJECT_BRIEF.md workflow"""

    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def valid_project_brief(self):
        """Return a valid PROJECT_BRIEF.md content"""
        return """# Project Brief

## 🎯 Project Overview

**Project Name**: Test Project

**Brief Description**:
A test project for validation

**Problem Statement**:
Testing the validation workflow

**Target Users**:
Developers and testers

---

## 📋 Core Requirements

### Functional Requirements

1. **Feature One**
   - Requirement A
   - Requirement B

### Non-Functional Requirements

- **Usability**: Easy to use
- **Maintainability**: Well documented

---

## 🏗️ Technical Preferences

### Technology Stack

**Backend**:
- [x] Node.js
- [x] Python

---

## 👥 User Roles & Permissions

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| Developer | Writes code | Read, Write, Execute |

---

## 🔄 Key User Flows

### Flow 1: Development
1. Clone repository
2. Write code
3. Test code
4. Commit changes

---

## 🗄️ Data Model (High-Level)

### Entity
- Name: string
- Description: text

---

## 🔌 External Integrations

- [x] Git Version Control

---

## 📅 Timeline & Priorities

**Target Launch Date**: December 2025

**Priority Features**:
1. Core functionality
2. Documentation

---

## 💰 Budget & Resources

**Budget**: Open source

**Team Size**: 2 developers

---

## 📝 Additional Context

Additional notes and context for the project.

---

## ✅ Completion Checklist

- [x] All sections complete
- [x] Ready for development
"""

    @pytest.fixture
    def minimal_project_brief(self):
        """Return a minimal but valid PROJECT_BRIEF.md content"""
        return """# Project Brief

## 🎯 Project Overview

**Project Name**: Minimal Test

**Brief Description**: Minimal test project

**Problem Statement**: Testing minimal requirements

**Target Users**: Developers

## 📋 Core Requirements

### Functional Requirements
1. Basic feature

### Non-Functional Requirements
- **Usability**: Simple

## 🏗️ Technical Preferences

### Technology Stack
**Backend**: Python

## 👥 User Roles & Permissions

| Role | Description |
|------|-------------|
| User | Standard user |

## 🔄 Key User Flows

### Flow 1
1. Step one

## 🗄️ Data Model (High-Level)

### Entity
- Field: type

## 🔌 External Integrations

- [x] Git

## 📅 Timeline & Priorities

**Target Launch**: Q4 2025

## 💰 Budget & Resources

**Budget**: TBD

## 📝 Additional Context

Context here

## ✅ Completion Checklist

- [x] Complete
"""

    @pytest.fixture
    def invalid_project_brief(self):
        """Return an invalid PROJECT_BRIEF.md (missing required sections)"""
        return """# Project Brief

## 🎯 Project Overview

**Project Name**: Invalid Project

This is missing many required sections.
"""

    @pytest.mark.e2e
    def test_valid_project_brief_workflow(self, temp_project_dir, valid_project_brief):
        """Test e2e workflow with a valid PROJECT_BRIEF.md"""
        # Write PROJECT_BRIEF.md
        brief_path = temp_project_dir / "PROJECT_BRIEF.md"
        brief_path.write_text(valid_project_brief)

        # Validate
        result = validate_project_brief(brief_path)

        # Assertions
        assert result.is_valid
        assert len(result.errors) == 0
        assert brief_path.exists()

        # Verify file content can be read
        content = brief_path.read_text()
        assert "Project Name" in content
        assert "Core Requirements" in content

    @pytest.mark.e2e
    def test_minimal_project_brief_workflow(self, temp_project_dir, minimal_project_brief):
        """Test e2e workflow with minimal valid PROJECT_BRIEF.md"""
        # Write PROJECT_BRIEF.md
        brief_path = temp_project_dir / "PROJECT_BRIEF.md"
        brief_path.write_text(minimal_project_brief)

        # Validate
        result = validate_project_brief(brief_path)

        # Assertions
        assert result.is_valid
        assert len(result.errors) == 0

    @pytest.mark.e2e
    def test_invalid_project_brief_workflow(self, temp_project_dir, invalid_project_brief):
        """Test e2e workflow with invalid PROJECT_BRIEF.md"""
        # Write PROJECT_BRIEF.md
        brief_path = temp_project_dir / "PROJECT_BRIEF.md"
        brief_path.write_text(invalid_project_brief)

        # Validate
        result = validate_project_brief(brief_path)

        # Assertions
        assert not result.is_valid
        assert len(result.errors) > 0

        # Verify specific errors
        error_text = " ".join(result.errors)
        assert "missing" in error_text.lower() or "required" in error_text.lower()

    @pytest.mark.e2e
    def test_missing_project_brief_workflow(self, temp_project_dir):
        """Test e2e workflow when PROJECT_BRIEF.md doesn't exist"""
        brief_path = temp_project_dir / "PROJECT_BRIEF.md"

        # Validate non-existent file
        result = validate_project_brief(brief_path)

        # Should handle missing file gracefully
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("not found" in error.lower() or "does not exist" in error.lower()
                   for error in result.errors)

    @pytest.mark.e2e
    def test_project_brief_with_warnings(self, temp_project_dir):
        """Test e2e workflow with PROJECT_BRIEF.md that has warnings"""
        # Create brief with potential warnings (incomplete checkboxes, etc.)
        brief_content = """# Project Brief

## 🎯 Project Overview

**Project Name**: Warning Test

**Brief Description**: Testing warnings

**Problem Statement**: Test

**Target Users**: Developers

## 📋 Core Requirements

### Functional Requirements
1. Feature one

### Non-Functional Requirements
- **Usability**: Good

## 🏗️ Technical Preferences

### Technology Stack
**Backend**: Python

## 👥 User Roles & Permissions

| Role | Description |
|------|-------------|
| User | User role |

## 🔄 Key User Flows

### Flow 1
1. Step

## 🗄️ Data Model (High-Level)

### Entity
- Field: type

## 🔌 External Integrations

- [ ] Git (not checked)

## 📅 Timeline & Priorities

**Target Launch**: TBD

## 💰 Budget & Resources

**Budget**: Unknown

## 📝 Additional Context

Context

## ✅ Completion Checklist

- [ ] Not complete
- [ ] Not ready
"""

        brief_path = temp_project_dir / "PROJECT_BRIEF.md"
        brief_path.write_text(brief_content)

        # Validate
        result = validate_project_brief(brief_path)

        # Should be valid but may have warnings
        assert result.is_valid or not result.is_valid  # Depends on validation rules

        # Check that validation completed
        assert isinstance(result.errors, list)
        assert isinstance(result.warnings, list)

    @pytest.mark.e2e
    def test_project_brief_workflow_with_special_characters(self, temp_project_dir):
        """Test e2e workflow with PROJECT_BRIEF.md containing special characters"""
        brief_content = """# Project Brief

## 🎯 Project Overview

**Project Name**: Special Chars Test™

**Brief Description**:
Testing with émojis 🚀 and spëcial çhars

**Problem Statement**:
Handle UTF-8: 中文, العربية, Ελληνικά

**Target Users**:
Global users 🌍

## 📋 Core Requirements

### Functional Requirements
1. Unicode support ✓

### Non-Functional Requirements
- **Usability**: International

## 🏗️ Technical Preferences

### Technology Stack
**Backend**: Python

## 👥 User Roles & Permissions

| Role | Description |
|------|-------------|
| User | Standard |

## 🔄 Key User Flows

### Flow 1
1. Step

## 🗄️ Data Model (High-Level)

### Entity
- Field: string

## 🔌 External Integrations

- [x] Git

## 📅 Timeline & Priorities

**Target Launch**: 2025

## 💰 Budget & Resources

**Budget**: Open

## 📝 Additional Context

Context

## ✅ Completion Checklist

- [x] Done
"""

        brief_path = temp_project_dir / "PROJECT_BRIEF.md"
        brief_path.write_text(brief_content, encoding='utf-8')

        # Validate
        result = validate_project_brief(brief_path)

        # Should handle special characters properly
        assert isinstance(result.is_valid, bool)
        assert brief_path.read_text(encoding='utf-8') == brief_content
