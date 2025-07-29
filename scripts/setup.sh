#!/bin/bash

# Monte Carlo Demo Setup Script
# This script sets up the complete environment for the monte-carlo-demo project

set -e  # Exit on any error

echo "🚀 Setting up Monte Carlo Demo Environment..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if dbt is available
if ! command -v dbt &> /dev/null; then
    echo "⚠️  dbt not found. Installing..."
    pip3 install dbt-core dbt-duckdb
fi

echo "✅ dbt available"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your OpenAI credentials before continuing!"
    echo "   Required: OPENAI_API_KEY, OPENAI_ORGANIZATION, OPENAI_PROJECT"
fi

# Load initial data
echo "📊 Loading initial data..."
python3 load_csv.py

# Generate additional sample data for testing
echo "🎲 Generating sample data with quality issues..."
python3 scripts/generate_sample_data.py

# Reload data with new samples
echo "🔄 Reloading all data including generated samples..."
python3 load_csv.py

# Set up dbt profile directory
mkdir -p ~/.dbt

# Create dbt profiles.yml if it doesn't exist
if [ ! -f ~/.dbt/profiles.yml ]; then
    echo "🔧 Creating dbt profiles.yml..."
    cat > ~/.dbt/profiles.yml << 'EOF'
dbt_project:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: './monte-carlo.duckdb'
      threads: 4
EOF
    echo "✅ dbt profile created"
fi

# Run dbt models
echo "🔄 Running dbt transformations..."
cd dbt_project

# Find dbt executable - try multiple common locations
DBT_CMD=""
if command -v dbt &> /dev/null; then
    DBT_CMD="dbt"
elif [ -f "/home/codespace/.local/lib/python3.12/site-packages/bin/dbt" ]; then
    DBT_CMD="/home/codespace/.local/lib/python3.12/site-packages/bin/dbt"
elif [ -f "~/.local/bin/dbt" ]; then
    DBT_CMD="~/.local/bin/dbt"
else
    # Try to find dbt using Python
    DBT_CMD=$(python3 -c "import dbt; print('dbt')" 2>/dev/null || echo "")
    if [ -z "$DBT_CMD" ]; then
        echo "❌ Could not find dbt executable"
        exit 1
    fi
fi

echo "🔧 Using dbt: $DBT_CMD"
$DBT_CMD deps --quiet || true  # Install packages, ignore if none
$DBT_CMD run --quiet
$DBT_CMD test --quiet

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI credentials"
echo "2. Run the dashboard:"
echo "   python -m streamlit run dashboard.py"
echo "   Dashboard will be available at: http://localhost:8501"
echo "3. Check observability: python observability/alerts.py"
echo ""
echo "📚 See README.md for detailed usage instructions"
echo ""
echo "🚀 Quick Commands:"
echo "   • Run AI analysis: python ai_layer/summarize.py"
echo "   • Start dashboard: python -m streamlit run dashboard.py"
echo "   • Generate demo data: python scripts/generate_fake_data.py"
echo "   • Live demo: python interview_demo.py"

echo ""
echo "🎯 Would you like to start the system now? (y/n)"
read -r start_system

if [ "$start_system" = "y" ] || [ "$start_system" = "Y" ]; then
    echo ""
    echo "🔍 Choose an option:"
    echo "1) Start Dashboard (Streamlit)"
    echo "2) Run AI Analysis"
    echo "3) Run Interview Demo"
    echo "4) Generate New Sample Data"
    echo "5) Check System Status"
    echo "Enter your choice (1-5):"
    read -r choice
    
    case $choice in
        1)
            echo "🚀 Starting dashboard..."
            cd /workspaces/monte-carlo-demo
            python -m streamlit run dashboard.py
            ;;
        2)
            echo "🤖 Running AI analysis..."
            cd /workspaces/monte-carlo-demo
            python ai_layer/summarize.py
            ;;
        3)
            echo "🎬 Starting interview demo..."
            cd /workspaces/monte-carlo-demo
            python interview_demo.py
            ;;
        4)
            echo "🎲 Generating new sample data..."
            cd /workspaces/monte-carlo-demo
            python scripts/generate_fake_data.py
            echo "✅ New data generated! Run option 2 to analyze it."
            ;;
        5)
            echo "🔍 Checking system status..."
            cd /workspaces/monte-carlo-demo
            echo "Configuration:"
            python config.py
            echo ""
            echo "Database tables:"
            python check_tables.py || echo "ℹ️  Database is in use (this is normal if dashboard is running)"
            ;;
        *)
            echo "ℹ️  Setup complete. Use the commands above to operate your system."
            ;;
    esac
else
    echo "ℹ️  Setup complete. Use the commands above to operate your system."
fi
