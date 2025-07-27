"""
Configuration management for the monte-carlo-demo project.
Centralizes environment variable loading and validation.
"""

import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for the monte-carlo-demo project."""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration with optional custom .env file."""
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to find .env file in project root
            project_root = Path(__file__).parent
            env_path = project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path)
    
    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key."""
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return key
    
    @property
    def openai_organization(self) -> str:
        """Get OpenAI organization ID."""
        org = os.getenv("OPENAI_ORGANIZATION")
        if not org:
            raise ValueError("OPENAI_ORGANIZATION environment variable is required")
        return org
    
    @property
    def openai_project(self) -> str:
        """Get OpenAI project ID."""
        project = os.getenv("OPENAI_PROJECT")
        if not project:
            raise ValueError("OPENAI_PROJECT environment variable is required")
        return project
    
    @property
    def duckdb_path(self) -> str:
        """Get DuckDB database path."""
        return os.getenv("DUCKDB_PATH", "monte-carlo.duckdb")
    
    @property
    def log_level(self) -> str:
        """Get logging level."""
        return os.getenv("LOG_LEVEL", "INFO")
    
    def validate(self) -> Dict[str, bool]:
        """Validate all required configuration values."""
        validation_results = {}
        
        try:
            self.openai_api_key
            validation_results["openai_api_key"] = True
        except ValueError:
            validation_results["openai_api_key"] = False
        
        try:
            self.openai_organization
            validation_results["openai_organization"] = True
        except ValueError:
            validation_results["openai_organization"] = False
        
        try:
            self.openai_project
            validation_results["openai_project"] = True
        except ValueError:
            validation_results["openai_project"] = False
        
        # DuckDB path is optional, just check if file exists or can be created
        duckdb_path = Path(self.duckdb_path)
        validation_results["duckdb_path"] = (
            duckdb_path.exists() or duckdb_path.parent.exists()
        )
        
        return validation_results
    
    def is_valid(self) -> bool:
        """Check if all required configuration is valid."""
        return all(self.validate().values())


# Global configuration instance
config = Config()


if __name__ == "__main__":
    """Command-line configuration validator."""
    print("🔧 Monte Carlo Demo Configuration Validator")
    print("=" * 50)
    
    validation = config.validate()
    
    for key, is_valid in validation.items():
        status = "✅" if is_valid else "❌"
        print(f"{status} {key}: {'Valid' if is_valid else 'Invalid/Missing'}")
    
    print("=" * 50)
    
    if config.is_valid():
        print("🎉 All configuration is valid!")
    else:
        print("⚠️  Some configuration is missing. Please check your .env file.")
        print("   Copy .env.example to .env and fill in the required values.")
