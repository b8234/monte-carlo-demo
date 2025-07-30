#!/bin/bash

# =====================================
# Monte Carlo Data Observability Demo
# Automated Setup & Launch Script
# =====================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"
DASHBOARD_FILE="$SCRIPT_DIR/src/monte_carlo_dashboard.py"
ENV_FILE="$SCRIPT_DIR/.env"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "\n${PURPLE}=== $1 ===${NC}\n"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to cleanup any running Streamlit processes
cleanup_streamlit() {
    print_status "Checking for running Streamlit processes..."
    
    # Find Streamlit processes
    STREAMLIT_PIDS=$(pgrep -f "streamlit.*monte_carlo_dashboard" 2>/dev/null || true)
    
    if [ -n "$STREAMLIT_PIDS" ]; then
        print_warning "Found running Streamlit processes. Stopping them..."
        echo "$STREAMLIT_PIDS" | while read -r pid; do
            if [ -n "$pid" ]; then
                print_status "Stopping Streamlit process (PID: $pid)..."
                kill "$pid" 2>/dev/null || true
                sleep 1
                # Force kill if still running
                if kill -0 "$pid" 2>/dev/null; then
                    print_warning "Force stopping process $pid..."
                    kill -9 "$pid" 2>/dev/null || true
                fi
            fi
        done
        
        # Wait a moment for processes to fully terminate
        sleep 2
        print_success "Streamlit processes stopped"
    else
        print_status "No running Streamlit processes found"
    fi
    
    # Also check for any processes using the target ports
    for port in 8501 8502 8503; do
        if command_exists lsof; then
            PORT_PID=$(lsof -ti:$port 2>/dev/null || true)
            if [ -n "$PORT_PID" ]; then
                print_warning "Port $port is in use by process $PORT_PID. Stopping..."
                kill "$PORT_PID" 2>/dev/null || true
                sleep 1
            fi
        fi
    done
}

# Function to detect Python command
detect_python() {
    if command_exists python3; then
        echo "python3"
    elif command_exists python; then
        # Check if it's Python 3
        if python --version 2>&1 | grep -q "Python 3"; then
            echo "python"
        else
            print_error "Python 3 is required but not found"
            exit 1
        fi
    else
        print_error "Python 3 is required but not found"
        exit 1
    fi
}

# Function to setup virtual environment
setup_venv() {
    print_header "Setting Up Python Virtual Environment"
    
    PYTHON_CMD=$(detect_python)
    print_status "Using Python command: $PYTHON_CMD"
    
    if [ ! -d "$VENV_DIR" ]; then
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        print_success "Virtual environment created at $VENV_DIR"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    print_success "Virtual environment ready"
}

# Function to install dependencies
install_dependencies() {
    print_header "Installing Python Dependencies"
    
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        print_error "requirements.txt not found at $REQUIREMENTS_FILE"
        exit 1
    fi
    
    print_status "Installing packages from requirements.txt..."
    pip install -r "$REQUIREMENTS_FILE"
    
    print_success "All dependencies installed successfully"
}

# Function to setup environment variables
setup_env() {
    print_header "Setting Up Environment Configuration"
    
    if [ ! -f "$ENV_FILE" ]; then
        print_status "Creating .env file with default configuration..."
        cat > "$ENV_FILE" << 'EOF'
# Monte Carlo Demo Configuration
# ==============================

# Database Configuration
DUCKDB_PATH=database/monte-carlo.duckdb

# Logging Configuration  
LOG_LEVEL=INFO

# OpenAI Configuration (Optional - for AI features)
# Uncomment and set your OpenAI API key to enable AI analysis
# OPENAI_API_KEY=sk-proj-your-api-key-here
# OPENAI_ORGANIZATION=your-org-id
# OPENAI_PROJECT=your-project-id

# Demo Configuration
DEMO_DATA_DIR=sample_data
WATCH_DIR=sample_data
EOF
        print_success "Created .env file with default configuration"
        print_warning "To enable AI features, edit .env and add your OpenAI API key"
    else
        print_status ".env file already exists"
    fi
}

# Function to load initial data
load_data() {
    print_header "Loading Initial Data"
    
    if [ ! -f "$DASHBOARD_FILE" ]; then
        print_error "Dashboard file not found at $DASHBOARD_FILE"
        exit 1
    fi
    
    print_status "Loading CSV data into DuckDB..."
    python "$DASHBOARD_FILE" load_data
    print_success "Initial data loaded successfully"
}

# Function to verify setup
verify_setup() {
    print_header "Verifying Setup"
    
    # Check Python imports
    print_status "Checking Python imports..."
    python -c "
import streamlit
import duckdb  
import pandas
import openai
import watchdog
print('✅ All required packages can be imported')
"
    
    # Check database
    if [ -f "database/monte-carlo.duckdb" ]; then
        print_status "Checking database..."
        python -c "
import duckdb
con = duckdb.connect('database/monte-carlo.duckdb')
tables = con.execute('SHOW TABLES').fetchall()
record_count = con.execute('SELECT COUNT(*) FROM summarize_model').fetchone()[0] if tables else 0
con.close()
print(f'✅ Database ready with {record_count} records')
"
    fi
    
    print_success "Setup verification completed"
}

# Function to start the dashboard
start_dashboard() {
    print_header "Starting Monte Carlo Dashboard"
    
    # Clean up any existing Streamlit processes first
    cleanup_streamlit
    
    print_status "Dashboard will be available at: http://localhost:8501"
    print_status "Press Ctrl+C to stop the dashboard"
    echo
    print_status "Starting Streamlit dashboard..."
    
    # Start Streamlit with optimized settings
    python -m streamlit run "$DASHBOARD_FILE" \
        --server.port=8501 \
        --server.address=0.0.0.0 \
        --browser.gatherUsageStats=false \
        --server.fileWatcherType=none
}

# Function to show usage
show_usage() {
    echo "Monte Carlo Data Observability Demo - Setup Script"
    echo
    echo "Usage: $0 [OPTION]"
    echo
    echo "Options:"
    echo "  setup     - Full setup (venv, dependencies, data loading)"
    echo "  install   - Install dependencies only"
    echo "  data      - Load data only"
    echo "  start     - Start dashboard only"
    echo "  reset     - Stop any running processes and restart dashboard"
    echo "  verify    - Verify setup only"
    echo "  clean     - Clean virtual environment"
    echo "  help      - Show this help message"
    echo
    echo "Default (no option): Full setup + start dashboard"
}

# Function to clean setup
clean_setup() {
    print_header "Cleaning Setup"
    
    if [ -d "$VENV_DIR" ]; then
        print_status "Removing virtual environment..."
        rm -rf "$VENV_DIR"
        print_success "Virtual environment removed"
    fi
    
    if [ -f "database/monte-carlo.duckdb" ]; then
        print_status "Removing database file..."
        rm -f "database/monte-carlo.duckdb"
        print_success "Database file removed"
    fi
    
    print_success "Cleanup completed"
}

# Function to run full setup
full_setup() {
    print_header "Monte Carlo Data Observability Demo - Full Setup"
    
    setup_venv
    install_dependencies
    setup_env
    load_data
    verify_setup
    
    print_success "Setup completed successfully!"
    echo
    print_status "🎯 Your Monte Carlo demo is ready!"
    print_status "🚀 Dashboard features:"
    print_status "   • Real-time data quality monitoring"
    print_status "   • AI-powered analysis (if OpenAI configured)"
    print_status "   • Live file monitoring"
    print_status "   • Enterprise data scenarios"
    echo
}

# Main script logic
main() {
    case "${1:-}" in
        "setup")
            full_setup
            ;;
        "install")
            setup_venv
            install_dependencies
            ;;
        "data")
            if [ -d "$VENV_DIR" ]; then
                source "$VENV_DIR/bin/activate"
            fi
            load_data
            ;;
        "start")
            if [ -d "$VENV_DIR" ]; then
                source "$VENV_DIR/bin/activate"
            fi
            start_dashboard
            ;;
        "reset")
            print_header "Resetting Dashboard"
            cleanup_streamlit
            if [ -d "$VENV_DIR" ]; then
                source "$VENV_DIR/bin/activate"
            fi
            print_success "Dashboard reset complete"
            echo
            read -p "Press Enter to start the dashboard (or Ctrl+C to exit)..."
            start_dashboard
            ;;
        "verify")
            if [ -d "$VENV_DIR" ]; then
                source "$VENV_DIR/bin/activate"
            fi
            verify_setup
            ;;
        "clean")
            clean_setup
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        "")
            # Default: full setup + start
            full_setup
            echo
            read -p "Press Enter to start the dashboard (or Ctrl+C to exit)..."
            start_dashboard
            ;;
        *)
            print_error "Unknown option: $1"
            echo
            show_usage
            exit 1
            ;;
    esac
}

# Trap to handle interruption
trap 'echo -e "\n${YELLOW}Setup interrupted by user${NC}"; exit 130' INT

# Check if we're in the right directory
if [ ! -f "$DASHBOARD_FILE" ]; then
    print_error "Please run this script from the monte-carlo-demo directory"
    print_error "Expected file: $DASHBOARD_FILE"
    exit 1
fi

# Show banner
echo -e "${PURPLE}"
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🎯 Monte Carlo Data Observability Demo Setup               ║  
║                                                               ║
║   Enterprise-ready data quality monitoring platform          ║
║   • Real-time monitoring & AI-powered insights               ║
║   • Live file monitoring & quality scoring                   ║
║   • Professional demo with enterprise datasets               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# Run main function
main "$@"
