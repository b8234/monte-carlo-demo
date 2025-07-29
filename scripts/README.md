# Utility Scripts

This directory contains utility scripts for development, testing, and data generation.

## Data Generation Scripts

- `generate_fake_data.py` - Generate realistic sample data with quality issues
- `generate_sample_data.py` - Create clean sample datasets
- `build_demo_data.py` - Build comprehensive demo datasets
- `inject_errors.py` - Add intentional data quality issues for testing
- `quick_fake_data.py` - Quick data generation for demos

## Development Utilities

- `data_summary.py` - Analyze and summarize data in the database
- `explore_data.py` - Interactive data exploration tools
- `run_demo.py` - Alternative demo runner
- `setup.sh` - Environment setup script
- `check_alignment.sh` - Verify system alignment

## Quick Commands

- `quick_csv.sh` - Fast CSV operations

## Usage

Most scripts can be run directly from the project root:

```bash
# Generate demo data
python scripts/generate_fake_data.py

# Explore current data
python scripts/explore_data.py

# Check system status
bash scripts/check_alignment.sh
```
