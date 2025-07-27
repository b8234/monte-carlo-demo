#!/bin/bash

# Comprehensive alignment check script for monte-carlo-demo
# This script validates that all components are properly configured and working

echo "🔍 Monte Carlo Demo - System Alignment Check"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

check_file() {
    if [ -f "$1" ]; then
        echo -e "✅ ${GREEN}$1 exists${NC}"
    else
        echo -e "❌ ${RED}$1 missing${NC}"
        ((ERRORS++))
    fi
}

check_directory() {
    if [ -d "$1" ]; then
        echo -e "✅ ${GREEN}$1/ directory exists${NC}"
    else
        echo -e "❌ ${RED}$1/ directory missing${NC}"
        ((ERRORS++))
    fi
}

check_python_import() {
    if python3 -c "import $1" 2>/dev/null; then
        echo -e "✅ ${GREEN}Python module '$1' can be imported${NC}"
    else
        echo -e "❌ ${RED}Python module '$1' cannot be imported${NC}"
        ((ERRORS++))
    fi
}

echo ""
echo "📁 Checking file structure..."
echo "------------------------------"

# Core files
check_file "README.md"
check_file "requirements.txt"
check_file "config.py"
check_file "dashboard.py"
check_file "load_csv.py"
check_file "setup.sh"
check_file ".env.example"

# Directories
check_directory "data"
check_directory "dbt_project"
check_directory "ai_layer"
check_directory "observability"
check_directory "tests"
check_directory ".github/workflows"

# Data files
check_file "data/raw_data.csv"
check_file "data/additional_data.csv"
check_file "data/enriched_data.csv"

# dbt files
check_file "dbt_project/dbt_project.yml"
check_file "dbt_project/models/summarize_model.sql"
check_file "dbt_project/models/schema.yml"

echo ""
echo "🐍 Checking Python dependencies..."
echo "-----------------------------------"

# Core dependencies
check_python_import "duckdb"
check_python_import "pandas"
check_python_import "streamlit"
check_python_import "openai"
check_python_import "dotenv"
check_python_import "pytest"

echo ""
echo "⚙️  Checking configuration..."
echo "-----------------------------"

# Test configuration
if python3 config.py > /dev/null 2>&1; then
    echo -e "✅ ${GREEN}Configuration validation script works${NC}"
else
    echo -e "❌ ${RED}Configuration validation script failed${NC}"
    ((ERRORS++))
fi

# Check dbt profile
if [ -f ~/.dbt/profiles.yml ]; then
    echo -e "✅ ${GREEN}dbt profile exists${NC}"
else
    echo -e "⚠️  ${YELLOW}dbt profile missing (will be created by setup.sh)${NC}"
fi

echo ""
echo "🗃️  Checking database..."
echo "------------------------"

if [ -f "monte-carlo.duckdb" ]; then
    echo -e "✅ ${GREEN}DuckDB database file exists${NC}"
    
    # Test database content
    if python3 -c "import duckdb; con=duckdb.connect('monte-carlo.duckdb'); print(f'Tables: {len(con.execute(\"SHOW TABLES\").fetchall())}')" 2>/dev/null; then
        echo -e "✅ ${GREEN}Database is accessible and contains tables${NC}"
    else
        echo -e "⚠️  ${YELLOW}Database exists but may be empty${NC}"
    fi
else
    echo -e "⚠️  ${YELLOW}DuckDB database missing (will be created by setup.sh)${NC}"
fi

echo ""
echo "🔨 Checking dbt..."
echo "-----------------"

# Find dbt executable
DBT_PATH=""
if command -v dbt &> /dev/null; then
    DBT_PATH="dbt"
    echo -e "✅ ${GREEN}dbt found in PATH${NC}"
elif [ -f "/home/codespace/.local/lib/python3.12/site-packages/bin/dbt" ]; then
    DBT_PATH="/home/codespace/.local/lib/python3.12/site-packages/bin/dbt"
    echo -e "✅ ${GREEN}dbt found at $DBT_PATH${NC}"
else
    echo -e "❌ ${RED}dbt not found${NC}"
    ((ERRORS++))
fi

if [ ! -z "$DBT_PATH" ]; then
    if cd dbt_project && $DBT_PATH debug --quiet > /dev/null 2>&1; then
        echo -e "✅ ${GREEN}dbt project configuration is valid${NC}"
    else
        echo -e "⚠️  ${YELLOW}dbt project needs configuration${NC}"
    fi
    cd ..
fi

echo ""
echo "🧪 Running tests..."
echo "------------------"

if python3 -m pytest tests/ -q > /dev/null 2>&1; then
    echo -e "✅ ${GREEN}All tests pass${NC}"
else
    echo -e "❌ ${RED}Some tests are failing${NC}"
    ((ERRORS++))
fi

echo ""
echo "📊 Summary"
echo "----------"

if [ $ERRORS -eq 0 ]; then
    echo -e "🎉 ${GREEN}All checks passed! System is properly aligned.${NC}"
    echo ""
    echo "Ready to run:"
    echo "  1. streamlit run dashboard.py"
    echo "  2. python observability/alerts.py"
    echo "  3. python ai_layer/summarize.py"
else
    echo -e "⚠️  ${YELLOW}Found $ERRORS issues that need attention.${NC}"
    echo ""
    echo "To fix issues, run: ./setup.sh"
fi

echo ""
echo "📚 For full setup instructions, see README.md"
