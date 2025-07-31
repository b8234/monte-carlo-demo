#!/usr/bin/env python3
"""
CSV Data Loader for Monte Carlo Demo CI Pipeline
===============================================

This script loads CSV test data into DuckDB for dbt testing in CI/CD pipelines.
It creates a 'raw_data' table by combining data from multiple CSV files in the
data/ and sample_data/ directories.

The script is designed to be used in CI workflows where a DuckDB database
needs to be populated with test data before running dbt models and tests.

Usage:
    python load_csv.py
    
Environment:
    - Creates database/monte-carlo.duckdb (or connects to existing)
    - Loads all CSV files from data/ and sample_data/ directories
    - Creates unified 'raw_data' table for dbt models
"""

import os
import pandas as pd
import duckdb
from pathlib import Path
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure we're working from the project root
PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)


class CSVLoader:
    """Loads CSV files into DuckDB for dbt testing"""
    
    def __init__(self, db_path: str = "database/monte-carlo.duckdb"):
        """Initialize the CSV loader with DuckDB connection"""
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        logger.info(f"Connected to DuckDB at {db_path}")
    
    def get_csv_files(self) -> List[Path]:
        """Find all CSV files in data/ and sample_data/ directories"""
        csv_files = []
        
        # Check data/ directory
        data_dir = Path("data")
        if data_dir.exists():
            csv_files.extend(data_dir.glob("*.csv"))
            logger.info(f"Found {len(list(data_dir.glob('*.csv')))} CSV files in data/")
        
        # Check sample_data/ directory
        sample_data_dir = Path("sample_data")
        if sample_data_dir.exists():
            csv_files.extend(sample_data_dir.glob("*.csv"))
            logger.info(f"Found {len(list(sample_data_dir.glob('*.csv')))} CSV files in sample_data/")
        
        return csv_files
    
    def load_csv_file(self, file_path: Path) -> pd.DataFrame:
        """Load a single CSV file and standardize its structure"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {file_path.name}: {len(df)} rows, {len(df.columns)} columns")
            
            # Ensure required columns exist
            required_columns = ['id', 'title', 'description']
            for col in required_columns:
                if col not in df.columns:
                    logger.warning(f"Missing '{col}' column in {file_path.name}, adding empty column")
                    df[col] = None
            
            # Add metadata columns
            df['source_file'] = file_path.name
            df['loaded_at'] = pd.Timestamp.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return pd.DataFrame()
    
    def combine_dataframes(self, dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        """Combine multiple dataframes into one standardized dataset"""
        if not dataframes:
            logger.warning("No dataframes to combine")
            return pd.DataFrame()
        
        # Filter out empty dataframes
        valid_dataframes = [df for df in dataframes if not df.empty]
        
        if not valid_dataframes:
            logger.warning("All dataframes are empty")
            return pd.DataFrame()
        
        # Combine all dataframes
        combined_df = pd.concat(valid_dataframes, ignore_index=True, sort=False)
        
        # Ensure consistent data types
        if 'id' in combined_df.columns:
            combined_df['id'] = combined_df['id'].astype(str)
        
        if 'title' in combined_df.columns:
            combined_df['title'] = combined_df['title'].fillna('').astype(str)
        
        if 'description' in combined_df.columns:
            combined_df['description'] = combined_df['description'].fillna('').astype(str)
        
        logger.info(f"Combined dataset: {len(combined_df)} total rows")
        return combined_df
    
    def create_raw_data_table(self, df: pd.DataFrame) -> None:
        """Create the raw_data table in DuckDB"""
        if df.empty:
            logger.error("Cannot create table from empty dataframe")
            return
        
        try:
            # Drop existing table if it exists
            self.conn.execute("DROP TABLE IF EXISTS raw_data")
            
            # Create table from dataframe
            self.conn.register('temp_df', df)
            self.conn.execute("CREATE TABLE raw_data AS SELECT * FROM temp_df")
            
            # Verify table creation
            row_count = self.conn.execute("SELECT COUNT(*) FROM raw_data").fetchone()[0]
            logger.info(f"Created raw_data table with {row_count} rows")
            
            # Show sample of the data
            sample = self.conn.execute("SELECT id, title, LEFT(description, 50) as description_preview FROM raw_data LIMIT 5").fetchdf()
            logger.info("Sample data:")
            logger.info(f"\n{sample.to_string(index=False)}")
            
        except Exception as e:
            logger.error(f"Error creating raw_data table: {e}")
            raise
    
    def validate_data(self) -> bool:
        """Validate the loaded data meets dbt model requirements"""
        try:
            # Check if table exists
            tables = self.conn.execute("SHOW TABLES").fetchdf()
            if 'raw_data' not in tables['name'].values:
                logger.error("raw_data table not found")
                return False
            
            # Check required columns exist
            columns = self.conn.execute("DESCRIBE raw_data").fetchdf()
            required_columns = ['id', 'title', 'description']
            existing_columns = columns['column_name'].values
            
            for col in required_columns:
                if col not in existing_columns:
                    logger.error(f"Required column '{col}' not found in raw_data table")
                    return False
            
            # Check for non-null ids
            null_ids = self.conn.execute("SELECT COUNT(*) FROM raw_data WHERE id IS NULL").fetchone()[0]
            if null_ids > 0:
                logger.warning(f"Found {null_ids} rows with NULL ids")
            
            # Check for non-null descriptions (required by dbt model)
            null_descriptions = self.conn.execute("SELECT COUNT(*) FROM raw_data WHERE description IS NULL OR description = ''").fetchone()[0]
            total_rows = self.conn.execute("SELECT COUNT(*) FROM raw_data").fetchone()[0]
            
            if null_descriptions > 0:
                logger.warning(f"Found {null_descriptions}/{total_rows} rows with empty descriptions")
            
            logger.info("Data validation completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            return False
    
    def close(self):
        """Close the database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()
            logger.info("Database connection closed")


def main():
    """Main execution function"""
    logger.info("Starting CSV data loading for Monte Carlo Demo CI")
    
    loader = None
    try:
        # Initialize loader
        loader = CSVLoader()
        
        # Find all CSV files
        csv_files = loader.get_csv_files()
        
        if not csv_files:
            logger.warning("No CSV files found in data/ or sample_data/ directories")
            # Create a minimal test dataset
            test_data = pd.DataFrame({
                'id': ['test1', 'test2', 'test3'],
                'title': ['Test Record 1', 'Test Record 2', 'Test Record 3'],
                'description': ['Test description 1', 'Test description 2', 'Test description 3'],
                'source_file': 'generated_test_data.csv',
                'loaded_at': pd.Timestamp.now()
            })
            logger.info("Created minimal test dataset")
            loader.create_raw_data_table(test_data)
        else:
            # Load all CSV files
            dataframes = []
            for csv_file in csv_files:
                df = loader.load_csv_file(csv_file)
                if not df.empty:
                    dataframes.append(df)
            
            # Combine and load data
            combined_df = loader.combine_dataframes(dataframes)
            loader.create_raw_data_table(combined_df)
        
        # Validate the loaded data
        if loader.validate_data():
            logger.info("✅ CSV data loading completed successfully!")
        else:
            logger.error("❌ Data validation failed")
            exit(1)
            
    except Exception as e:
        logger.error(f"❌ CSV loading failed: {e}")
        exit(1)
    
    finally:
        if loader:
            loader.close()


if __name__ == "__main__":
    main()
