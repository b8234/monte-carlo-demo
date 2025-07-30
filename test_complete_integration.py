#!/usr/bin/env python3
"""
Comprehensive Test Suite for Monte Carlo Demo with pycarlo 0.10.51
================================================================

This script validates all components of the Monte Carlo demo project:
- Basic dependencies and imports
- pycarlo SDK integration (version 0.10.51)
- Monte Carlo client functionality
- Dashboard components
- Data loading and management
- Configuration management

Run with: python test_complete_integration.py
"""

import sys
import os
from pathlib import Path

# Add paths for imports
sys.path.append('src')
sys.path.append('pycarlo_integration')

def test_imports():
    """Test all critical imports."""
    print("🧪 Testing imports...")
    
    # Test core dependencies
    try:
        import pandas as pd
        print("✅ pandas imported")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import duckdb
        print("✅ duckdb imported")
    except ImportError as e:
        print(f"❌ duckdb import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ streamlit imported")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ openai imported")
    except ImportError as e:
        print(f"❌ openai import failed: {e}")
        return False
    
    # Test pycarlo 0.10.51
    try:
        import pycarlo
        print(f"✅ pycarlo imported (version check needed)")
    except ImportError as e:
        print(f"❌ pycarlo import failed: {e}")
        return False
    
    return True

def test_pycarlo_version():
    """Test pycarlo version specifically."""
    print("\n🧪 Testing pycarlo version...")
    
    try:
        import subprocess
        result = subprocess.run(['pip', 'show', 'pycarlo'], capture_output=True, text=True)
        if '0.10.51' in result.stdout:
            print("✅ pycarlo version 0.10.51 confirmed")
            return True
        else:
            print(f"❌ pycarlo version mismatch. Output: {result.stdout}")
            return False
    except Exception as e:
        print(f"❌ pycarlo version check failed: {e}")
        return False

def test_monte_carlo_integration():
    """Test Monte Carlo SDK integration."""
    print("\n🧪 Testing Monte Carlo integration...")
    
    try:
        from monte_carlo_client import MonteCarloIntegration
        
        # Test demo mode
        client = MonteCarloIntegration(demo_mode=True)
        print("✅ Monte Carlo client initialized")
        
        # Test connection
        status = client.client.test_connection()
        if status['status'] == 'connected':
            print("✅ Connection test passed")
        else:
            print(f"❌ Connection test failed: {status}")
            return False
            
        # Test account info
        account_info = client.client.get_account_info()
        if account_info.get('account_name'):
            print("✅ Account info retrieved")
        else:
            print("❌ Account info retrieval failed")
            return False
            
        # Test quality metrics
        metrics = client.client.get_quality_metrics()
        if 'overall_score' in metrics:
            print("✅ Quality metrics retrieved")
        else:
            print("❌ Quality metrics retrieval failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Monte Carlo integration test failed: {e}")
        return False

def test_dashboard_components():
    """Test dashboard components."""
    print("\n🧪 Testing dashboard components...")
    
    try:
        from monte_carlo_dashboard import Config, DataManager, AIAnalyzer
        
        # Test configuration
        config = Config()
        print("✅ Config initialized")
        
        # Test DataManager
        dm = DataManager(config.duckdb_path)
        print("✅ DataManager initialized")
        
        # Test AIAnalyzer (without OpenAI key requirement)
        try:
            ai = AIAnalyzer(config)
            print("✅ AIAnalyzer initialized")
        except ValueError:
            # Expected if no OpenAI key is set
            print("✅ AIAnalyzer initialized (no API key)")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard components test failed: {e}")
        return False

def test_data_operations():
    """Test basic data operations."""
    print("\n🧪 Testing data operations...")
    
    try:
        import tempfile
        import pandas as pd
        import duckdb
        
        # Create temporary test data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("id,title,description\n")
            f.write("1,Test Title,This is a test description for quality scoring\n")
            f.write("2,Another Test,Short\n")
            f.write("3,Third Test,\n")
            csv_path = f.name
        
        try:
            # Test CSV loading
            df = pd.read_csv(csv_path)
            assert len(df) == 3
            print("✅ CSV loading works")
            
            # Test DuckDB operations
            with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=False) as f:
                db_path = f.name
            
            con = duckdb.connect(db_path)
            con.register("test_df", df)
            con.execute("CREATE TABLE test_table AS SELECT *, LENGTH(description) as description_length FROM test_df")
            
            # Test quality scoring logic
            result = con.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN description IS NULL OR description = '' THEN 1 ELSE 0 END) as null_count,
                    SUM(CASE WHEN LENGTH(description) < 10 AND description IS NOT NULL THEN 1 ELSE 0 END) as short_count
                FROM test_table
            """).fetchone()
            
            total, null_count, short_count = result
            quality_score = ((total - null_count - short_count) / total * 100) if total > 0 else 0
            
            assert total == 3
            assert quality_score > 0  # Should have at least one good record
            print(f"✅ Quality scoring works (score: {quality_score:.1f}%)")
            
            con.close()
            os.unlink(db_path)
            
        finally:
            os.unlink(csv_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Data operations test failed: {e}")
        return False

def test_pycarlo_core_api():
    """Test pycarlo core API patterns."""
    print("\n🧪 Testing pycarlo core API patterns...")
    
    try:
        # Test that we can import the core classes
        from pycarlo.core import Client, Query, Mutation, Session
        print("✅ pycarlo.core classes imported")
        
        # Test that we can import error handling
        from pycarlo.common.errors import GqlError
        print("✅ pycarlo.common.errors imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ pycarlo core API test failed: {e}")
        return False

def run_all_tests():
    """Run all test suites."""
    print("🚀 Monte Carlo Demo - Complete Integration Test")
    print("=" * 60)
    
    tests = [
        ("Basic Imports", test_imports),
        ("PycarloVersion", test_pycarlo_version),
        ("Pycarlo Core API", test_pycarlo_core_api),
        ("Monte Carlo Integration", test_monte_carlo_integration),
        ("Dashboard Components", test_dashboard_components),
        ("Data Operations", test_data_operations),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The Monte Carlo demo is working correctly with pycarlo 0.10.51")
        return True
    else:
        print("⚠️  Some tests failed. Please check the output above for details.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
