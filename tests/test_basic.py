"""
Unit tests for the monte-carlo-demo project.
Run with: python -m pytest tests/
"""

import pytest
import pandas as pd
import duckdb
from pathlib import Path
import tempfile
import os


class TestLoadCSV:
    """Test the data loading functionality."""
    
    def test_csv_loading(self):
        """Test that CSV data can be loaded correctly."""
        # Create temporary CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("id,title,description\n")
            f.write("1,Test,This is a test description\n")
            csv_path = f.name
        
        try:
            # Load CSV
            df = pd.read_csv(csv_path)
            
            # Assertions
            assert len(df) == 1
            assert df.iloc[0]['id'] == 1
            assert df.iloc[0]['title'] == 'Test'
            assert 'description' in df.columns
            
        finally:
            os.unlink(csv_path)


class TestDuckDBOperations:
    """Test DuckDB database operations."""
    
    def test_duckdb_connection(self):
        """Test DuckDB connection and basic operations."""
        with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=True) as f:
            db_path = f.name
        
        try:
            # Connect and create test table
            con = duckdb.connect(db_path)
            con.execute("CREATE TABLE test_table (id INTEGER, name VARCHAR)")
            con.execute("INSERT INTO test_table VALUES (1, 'test')")
            
            # Query data
            result = con.execute("SELECT * FROM test_table").fetchall()
            
            # Assertions
            assert len(result) == 1
            assert result[0][0] == 1
            assert result[0][1] == 'test'
            
            con.close()
            
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)


class TestConfiguration:
    """Test configuration management."""
    
    def test_config_validation(self):
        """Test configuration validation logic."""
        from config import Config
        
        # Test with missing environment variables
        config = Config()
        validation = config.validate()
        
        # Should be a dictionary with validation results
        assert isinstance(validation, dict)
        assert 'openai_api_key' in validation
        assert 'duckdb_path' in validation


if __name__ == "__main__":
    pytest.main([__file__])
