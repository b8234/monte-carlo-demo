#!/usr/bin/env python3
"""
Configuration Validation Script for Monte Carlo Demo CI
======================================================

This script validates the configuration and environment setup for the 
Monte Carlo Demo application. It's designed to run in CI pipelines to
ensure that the application can start with test/dummy credentials.

Environment Variables Checked:
- OPENAI_API_KEY: Required for AI analysis features
- OPENAI_ORGANIZATION: Optional organization ID  
- OPENAI_PROJECT: Optional project ID

The script verifies that required dependencies are available and that
the basic configuration structure is valid for testing purposes.
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure we're working from the project root
PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)


def check_environment_variables():
    """Check that required environment variables are set"""
    logger.info("Checking environment variables...")
    
    required_vars = ['OPENAI_API_KEY']
    optional_vars = ['OPENAI_ORGANIZATION', 'OPENAI_PROJECT']
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            logger.info(f"✅ {var} is set")
    
    for var in optional_vars:
        if os.getenv(var):
            logger.info(f"✅ {var} is set (optional)")
        else:
            logger.info(f"ℹ️  {var} not set (optional)")
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        return False
    
    return True


def check_required_files():
    """Check that required application files exist"""
    logger.info("Checking required files...")
    
    required_files = [
        'requirements.txt',
        'src/monte_carlo_dashboard.py',
        'monte_carlo_dbt/dbt_project.yml',
        'scripts/load_csv.py'  # Updated path
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            logger.info(f"✅ {file_path} exists")
    
    if missing_files:
        logger.error(f"❌ Missing required files: {missing_files}")
        return False
    
    return True


def check_dependencies():
    """Check that key dependencies can be imported"""
    logger.info("Checking Python dependencies...")
    
    dependencies = {
        'streamlit': 'Streamlit dashboard framework',
        'duckdb': 'DuckDB database engine',
        'pandas': 'Data manipulation library',
        'openai': 'OpenAI API client',
        'watchdog': 'File system monitoring',
        'dotenv': 'Environment variable management'
    }
    
    failed_imports = []
    for module, description in dependencies.items():
        try:
            __import__(module)
            logger.info(f"✅ {module} - {description}")
        except ImportError as e:
            logger.error(f"❌ {module} - {description}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        logger.error(f"❌ Failed to import: {failed_imports}")
        return False
    
    return True


def validate_openai_config():
    """Validate OpenAI configuration (even with dummy values)"""
    logger.info("Validating OpenAI configuration...")
    
    try:
        from openai import OpenAI
        
        # Test with dummy credentials (should not make actual API calls)
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key and api_key.startswith('dummy'):
            logger.info("✅ Using dummy OpenAI credentials for testing")
            return True
        elif api_key:
            # In production, we'd test actual connectivity, but for CI just validate format
            if len(api_key) > 10:  # Basic sanity check
                logger.info("✅ OpenAI API key format appears valid")
                return True
            else:
                logger.error("❌ OpenAI API key appears too short")
                return False
        else:
            logger.error("❌ OPENAI_API_KEY not set")
            return False
            
    except Exception as e:
        logger.error(f"❌ OpenAI configuration validation failed: {e}")
        return False


def main():
    """Main validation function"""
    logger.info("🔍 Starting configuration validation for Monte Carlo Demo")
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("Required Files", check_required_files),
        ("Python Dependencies", check_dependencies),
        ("OpenAI Configuration", validate_openai_config),
    ]
    
    all_passed = True
    for check_name, check_function in checks:
        logger.info(f"\n📋 Running {check_name} check...")
        try:
            if not check_function():
                all_passed = False
                logger.error(f"❌ {check_name} check failed")
            else:
                logger.info(f"✅ {check_name} check passed")
        except Exception as e:
            logger.error(f"❌ {check_name} check failed with exception: {e}")
            all_passed = False
    
    if all_passed:
        logger.info("\n🎉 All configuration checks passed!")
        logger.info("✅ Monte Carlo Demo is ready for testing/deployment")
        sys.exit(0)
    else:
        logger.error("\n💥 Some configuration checks failed!")
        logger.error("❌ Please fix the issues above before proceeding")
        sys.exit(1)


if __name__ == "__main__":
    main()
