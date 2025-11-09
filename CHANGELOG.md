# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-06

### Added
- Initial public release
- Complete data processing pipeline for MIMIC-IV refeeding syndrome analysis
- Five main processing scripts:
  - `01_extract_variables.py` - Extract clinical variables from MIMIC-IV
  - `02_merge_datasets.py` - Merge extracted variables
  - `03_calculate_scores.py` - Calculate SOFA and APACHE II scores
  - `04_create_sample.py` - Create sample datasets (optional)
  - `05_add_patient_info.py` - Add patient demographics
- Comprehensive documentation:
  - README with overview and usage instructions
  - Data dictionary with variable definitions
  - Methodology documentation
  - MIMIC-IV setup guide
- Configuration file template (`config.py`)
- Example pipeline execution script
- Python dependencies list (`requirements.txt`)
- MIT License with MIMIC-IV data use notice
- Contributing guidelines
- .gitignore for data protection

### Features
- Chunk-based processing for handling large MIMIC-IV files
- Efficient feather file format for intermediate storage
- Memory-optimized progressive merging
- Comprehensive SOFA score calculation (6 organ systems)
- Simplified APACHE II score calculation
- Medical history integration
- Reproducible random sampling
- Detailed logging and progress reporting

### Documentation
- Step-by-step setup instructions
- Complete variable definitions with MIMIC-IV itemid mappings
- Scoring methodology with clinical references
- Code availability statement for manuscript
- Troubleshooting guide

### Notes
- Complies with MIMIC-IV Data Use Agreement requirements
- Code made public to enable scientific transparency
- Designed for reproducible research

## [Unreleased]

### Planned Enhancements
- Expanded electrolyte monitoring (Na, K, Phos, Mg)
- Additional data quality checks
- Automated visualization tools
- Performance benchmarking
- Unit tests for scoring functions

### Under Consideration
- Support for MIMIC-III comparison
- Additional severity scores (SAPS II, MEWS)
- Batch processing for multiple cohorts
- Results validation utilities

---

## Version Numbering

- **Major version (X.0.0)**: Breaking changes to methodology or outputs
- **Minor version (0.X.0)**: New features, backward compatible
- **Patch version (0.0.X)**: Bug fixes, documentation updates

## How to Update This File

When making changes:
1. Add entry under [Unreleased] section
2. Categorize as: Added, Changed, Deprecated, Removed, Fixed, or Security
3. When releasing, move [Unreleased] items to new version section
4. Include date in YYYY-MM-DD format

---

**Maintained by:** James Green (jg1984@shp.rutgers.edu)
**Repository:** [GitHub URL will be added upon publication]
