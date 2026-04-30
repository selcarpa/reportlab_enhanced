# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.0.1] - 2026-02-12

### Added
- Complete CI/CD automation workflow for GitHub Actions
  - Automatic GitHub Pages deployment on master push
  - Automatic PyPI publishing on release tags
  - Version verification against pyproject.toml
  - Dry-run mode support for workflow testing
- Version management refactored to use pyproject.toml as single source of truth

### Changed
- pyproject.toml: Complete reconfiguration with static version
- setup.py: Simplified to retain only dynamic build logic
- src/reportlab/__init__.py: Now uses importlib.metadata for version resolution

## [0.0.0] - 2025-02-12

### Added
- Initial fork from ReportLab
- Based on ReportLab version 3.6.13

This version represents the starting point of the reportlab-enhanced fork,
containing all the features and fixes from the upstream ReportLab 3.6.13 release.
