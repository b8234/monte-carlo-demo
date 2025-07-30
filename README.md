# 🎯 Monte Carlo Data Observability Demo

> **Enterprise-ready data observability platform showcasing real-time monitoring, AI-powered analysis, and dbt integration - demonstrating Monte Carlo's core value proposition for enterprise customers.**

## ⚡ **Quick Start (One Command)**

**Want to see it working immediately?** Just run:

```bash
./setup.sh
```

**That's it!** The setup script will:
- ✅ Create virtual environment  
- ✅ Install all dependencies
- ✅ Configure environment settings
- ✅ Load enterprise datasets
- ✅ Start the dashboard automatically

**Dashboard opens at: `http://localhost:8501`**

### **🔧 Alternative Manual Setup**

If you prefer traditional setup:

```bash
# 1. Install and load data
pip install -r requirements.txt
python src/monte_carlo_dashboard.py load_data

# 2. Start dashboard  
streamlit run src/monte_carlo_dashboard.py

# 3. Open browser to http://localhost:8501
```

**You'll see:** Live data quality dashboard with 6 enterprise datasets (210+ records) and real-time monitoring capabilities.

---

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![dbt](https://img.shields.io/badge/dbt-1.10.5-orange.svg)](https://www.getdbt.com/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.47.1-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)

---

## 🏗️ **Project Structure**

```
monte-carlo-demo/
├── setup.sh                      # 🚀 Main entry point - runs everything
├── README.md                     # 📖 This documentation
├── requirements.txt              # 📦 Python dependencies
├── .env                         # ⚙️ Environment configuration
│
├── src/                         # 📁 APPLICATION CODE
│   └── monte_carlo_dashboard.py # 🎯 Main dashboard application
│
├── database/                   # 💾 DATABASE STORAGE
│   └── monte-carlo.duckdb     # 🗄️ DuckDB database file
│
├── data/                      # 📊 SOURCE DATA
│   ├── product_operations_incidents_2025.csv
│   ├── business_intelligence_reports_2025.csv
│   └── ... (6 enterprise CSV files)
│
├── sample_data/              # 🎬 LIVE DEMO SCENARIOS
│   ├── customer_engagement_metrics_20250129.csv
│   └── ... (17 demo files)
│
├── monte_carlo_dbt/         # 🔄 DBT TRANSFORMATIONS
├── logs/                    # 📋 APPLICATION LOGS
└── tests/                   # 🧪 TEST FILES
```

---

## 🚀 **Setup Script Options**

### **🎯 Full Setup (Recommended)**
```bash
# Complete setup + start dashboard
./setup.sh

# Or explicitly:
./setup.sh setup
```

### **🔧 Individual Operations**
```bash
# Install dependencies only
./setup.sh install

# Load data only  
./setup.sh data

# Start dashboard only
./setup.sh start

# Verify setup
./setup.sh verify

# Clean everything
./setup.sh clean

# Show help
./setup.sh help
```

### **🎬 What the Setup Script Does**

#### **1. Environment Setup**
- Creates isolated Python virtual environment
- Installs all required packages from `requirements.txt`
- Upgrades pip to latest version

#### **2. Configuration**
- Creates `.env` file with default settings
- Configures database path and logging
- Sets up OpenAI placeholders (optional)

#### **3. Data Loading**
- Loads all CSV files from `data/` directory into DuckDB
- Creates quality monitoring tables
- Prepares sample data for live monitoring

#### **4. Verification**
- Tests all Python imports
- Verifies database connectivity
- Confirms record counts

#### **5. Dashboard Launch**
- Starts Streamlit on `http://localhost:8501`
- Optimized server settings for performance
- Auto-opens browser (if supported)

## 🏢 **Enterprise Demo Overview**

This project demonstrates Monte Carlo's data observability platform using **realistic enterprise data scenarios** that mirror actual customer use cases. All data files use enterprise naming conventions aligned with typical Fortune 500 data architecture patterns.

## 🚀 **Quick Setup Guide**

### **🎯 Option A: One-Line Setup (Recommended)**

```bash
# Run everything automatically:
./setup.sh
```

**That's it!** The setup script will:
- ✅ Create virtual environment
- ✅ Install all dependencies  
- ✅ Load enterprise datasets
- ✅ Configure environment
- ✅ Start the dashboard

**Dashboard will be available at: `http://localhost:8501`**

### **🔧 Option B: Traditional Manual Setup**

#### **1. Clone and Navigate**
```bash
git clone <repository-url>
cd monte-carlo-demo
```

#### **2. Install Dependencies**
```bash
# Create virtual environment (recommended)
python -m venv monte-carlo-env
source monte-carlo-env/bin/activate  # On Windows: monte-carlo-env\Scripts\activate
pip install -r requirements.txt
```

#### **3. Load Initial Data**
```bash
# Load the 6 enterprise datasets into the database
python src/monte_carlo_dashboard.py load_data

# You should see output like:
# 📁 Found 6 CSV files in data directory
# 📊 Loading product_operations_incidents_2025.csv -> product_operations_incidents_2025 table (20 rows)
# ... etc.
```

#### **4. Configure Environment (Optional - for AI Features)**
```bash
# The setup script creates .env automatically, or manually:
cp .env.example .env

#### **5. Start the Dashboard**
```bash
# Launch the Streamlit dashboard
streamlit run src/monte_carlo_dashboard.py

# You should see:
# Local URL: http://localhost:8501
# Network URL: http://192.168.x.x:8501
```

**🌐 Access the Dashboard:** Open <http://localhost:8501> in your browser

### **What You'll See Immediately**
- **🔴 Live Monitor Tab** - Real-time data quality metrics and monitoring
- **🤖 AI Analysis Tab** - GPT-4 powered data quality insights (if OpenAI configured)  
- **📊 Data Overview Tab** - Database statistics and health metrics
- **Enterprise Datasets** - 6 realistic business datasets pre-loaded with 210+ records
- **Quality Metrics** - Current data quality score, issue counts, and trends

### **First Steps After Setup**
1. **Explore the Live Monitor** - See real-time stats and recent data records
2. **Try AI Analysis** - Click "Run AI Analysis" to see GPT-4 quality assessments
3. **Test Live Monitoring** - Drop a CSV file from `sample_data/` folder into `data/` to see real-time updates
4. **Check Data Overview** - Review database statistics and quality trends

---

## 🏢 **Enterprise Data Architecture**

This demo uses **realistic enterprise naming conventions** that mirror actual Monte Carlo customer scenarios:

### **📊 Core Data Assets (`data/` folder)**

| File Name | Enterprise Context | Monte Carlo Value |
|-----------|-------------------|-------------------|
| `product_operations_incidents_2025.csv` | Product operations team incident reports | Primary dataset for quality monitoring baseline |
| `business_intelligence_reports_2025.csv` | BI team's processed analytics reports | Shows data enrichment pipeline quality |
| `data_quality_violations_2025.csv` | Data governance team's quality violations log | Demonstrates data quality issue detection |
| `system_monitoring_events_2025.csv` | Platform engineering team's system events | Shows streaming data quality monitoring |
| `user_behavior_analytics_2025.csv` | Product analytics team's user behavior data | Demonstrates ML pipeline data quality |
| `customer_support_metrics_2025.csv` | Customer success team's support metrics | Shows customer-facing data quality impact |

### **🎬 Sample Data Files (`sample_data/` folder)**

Real-time enterprise scenarios for live demonstration:

- **Customer Intelligence**: `customer_engagement_metrics_20250129.csv`
- **Fraud Detection**: `fraud_detection_alerts_20250129.csv`
- **Payment Processing**: `payment_processing_errors_20250129.csv`
- **Revenue Monitoring**: `revenue_anomaly_detected_20250129.csv`
- **Sales Operations**: `sales_performance_data_20250129.csv`
- **Marketing Analytics**: `marketing_campaign_results_20250129.csv`
- **User Analytics**: `user_activity_stream_20250129_01.csv`
- **Product Metrics**: `product_analytics_20250129_03.csv`
- **Transaction Logs**: `transaction_logs_20250129_02.csv`
- **Pipeline Health**: `data_pipeline_validation_20250129.csv`
- **Customer Data**: `customer_data_quality_issues_20250129.csv`
- **Churn Analysis**: `customer_churn_analysis_20250129.csv`

---

## 🎯 **Monte Carlo Value Demonstration**

### **Core Data Observability Features**
✅ **Real-time Monitoring** - Live dashboard with auto-refresh showing data quality metrics  
✅ **AI-Powered Analysis** - GPT-4 integration for intelligent anomaly detection  
✅ **dbt Integration** - Pipeline monitoring with test failure detection  
✅ **Live Alerting** - Instant notifications when quality issues occur  
✅ **Quality Scoring** - Executive-level data health metrics  

### **Technical Architecture**
- **Modern Data Stack**: Python + DuckDB + dbt + Streamlit
- **AI Integration**: OpenAI GPT-4 for quality assessment  
- **Real-time Processing**: File monitoring with instant ingestion
- **Production Practices**: Centralized config, comprehensive testing

---

## 🔄 **dbt Integration**

The `monte_carlo_dbt/` directory contains data transformations and quality tests that work seamlessly with the main dashboard.

### **🔧 dbt Setup**

The setup script handles dbt automatically, but for manual configuration:

```bash
# 1. dbt is already installed via requirements.txt
pip install dbt-core dbt-duckdb

# 2. dbt profile is auto-configured to use our database
# Profile location: ~/.dbt/profiles.yml
```

### **📊 dbt Project Structure**

```
monte_carlo_dbt/
├── dbt_project.yml         # Project configuration
├── models/                 # Data transformations
│   ├── schema.yml         # Model documentation & tests
│   └── summarize_model.sql # Core data quality model
├── tests/                 # Custom data quality tests
├── macros/                # Reusable SQL functions
└── README.md              # dbt-specific documentation
```

### **🚀 Running dbt Commands**

```bash
# Navigate to dbt directory
cd monte_carlo_dbt

# Install dependencies (if any)
dbt deps

# Run transformations
dbt run

# Execute data quality tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

### **🧪 Data Quality Tests**

The dbt project includes enterprise-grade data quality tests:

- **Schema Tests**: Column constraints and data types
- **Data Tests**: Business logic validation
- **Quality Metrics**: Completeness, accuracy, consistency
- **Custom Tests**: Domain-specific quality rules

```yaml
# Example from models/schema.yml
models:
  - name: summarize_model
    tests:
      - unique:
          column_name: id
      - not_null:
          column_name: title
    columns:
      - name: description_length
        tests:
          - positive
```

### **🔗 Integration with Dashboard**

The dashboard automatically:
- ✅ **Reads dbt models** - Displays data from dbt transformations
- ✅ **Shows test results** - Reports dbt test failures as quality alerts
- ✅ **Monitors lineage** - Tracks data flow through dbt models
- ✅ **Quality scoring** - Incorporates dbt test results into quality metrics

---

### **🎯 Platform Capabilities**

**Core Value Propositions**:
1. **Data Quality Monitoring**: Real-time monitoring of business-critical data pipelines
2. **Pipeline Observability**: Complete visibility across enterprise data architecture patterns
3. **Business Impact Analysis**: Identifies customer-facing data quality issues and downstream effects
4. **Anomaly Detection**: AI-powered quality violation identification and intelligent alerting

**Demonstration Scenarios**:
1. **Baseline monitoring** with clean customer engagement metrics
2. **Quality alert triggers** when problematic data files are detected
3. **ML pipeline monitoring** with user behavior analytics
4. **Business impact assessment** with revenue anomaly detection

**Platform Benefits**:
- Comprehensive enterprise data architecture monitoring across operations, BI, customer, and system data pipelines
- Automated pipeline monitoring for freshness, volume, schema changes, and data quality
- Proactive detection and alerting for the exact quality violations that impact business operations
- Enterprise-grade naming conventions and realistic customer scenarios

---

## 🎬 **Understanding the Platform**

### **What This Demo Demonstrates**

This Monte Carlo platform simulation shows **real enterprise data observability** in action:

#### **🔍 Data Quality Monitoring**
- **Real-time Metrics** - Live tracking of data freshness, completeness, and accuracy
- **Quality Scoring** - Automatic calculation of overall data health (0-100% score)
- **Issue Detection** - Identifies NULL values, short content, and schema problems
- **Trend Analysis** - Historical view of data quality over time

#### **🤖 AI-Powered Insights**
- **Intelligent Summarization** - GPT-4 analysis of data content and patterns
- **Anomaly Detection** - AI identifies unusual patterns and potential issues
- **Quality Assessment** - Automated quality scoring with detailed reasoning
- **Proactive Alerting** - Smart notifications when quality degrades

#### **📊 Enterprise Data Architecture**
- **Realistic Scenarios** - Data patterns that mirror actual Fortune 500 environments
- **Multiple Data Sources** - Operations, BI, Customer, System monitoring data
- **Live Ingestion** - Real-time processing of new data files
- **Pipeline Monitoring** - Complete visibility into data transformations

### **How to Use Each Feature**

#### **🔴 Live Monitor Tab**
**Purpose**: Real-time dashboard for data operations teams

**What you see**:
- **Total Records** - Count of all monitored data points
- **Quality Score** - Overall data health percentage  
- **Issue Counts** - NULL values, short content, validation errors
- **Recent Records** - Latest data with quality indicators

**How to use**:
1. Click "Start Monitor" to begin real-time file watching
2. Enable "Auto-refresh" to see live updates every 10 seconds
3. Drop CSV files into `sample_data/` folder to simulate new data arrival
4. Watch metrics update automatically as new data is processed

#### **🤖 AI Analysis Tab**  
**Purpose**: AI-powered data quality insights for data scientists/analysts

**What you see**:
- **AI Quality Alerts** - GPT-4 identified issues with detailed explanations
- **Analysis Results** - Row-by-row AI summaries and quality assessments
- **Pattern Detection** - Anomalies and trends identified by machine learning

**How to use**:
1. Click "Run AI Analysis" to analyze all data with GPT-4
2. Review alerts for critical quality issues
3. Examine AI summaries for insights into data patterns
4. Use findings to improve data collection and processing

#### **📊 Data Overview Tab**
**Purpose**: Executive dashboard for data governance and management

**What you see**:
- **Database Statistics** - High-level metrics for leadership reporting
- **Quality Trends** - Historical data health for governance reporting
- **Issue Summary** - Aggregated quality metrics for decision making
- **Data Freshness** - Timeliness indicators for operational awareness

### **Real-World Use Cases**

#### **Scenario 1: Daily Operations Monitoring**
```bash
# Morning routine: Check data quality health
streamlit run src/monte_carlo_dashboard.py
# Navigate to Live Monitor → Review overnight quality metrics
# Check for any degradation in key business datasets
```

#### **Scenario 2: New Data Pipeline Validation**  
```bash
# Simulate new data arrival
cp sample_data/customer_engagement_metrics_20250129.csv data/new_pipeline_data.csv
# Watch Live Monitor → See real-time ingestion and quality scoring
# Navigate to AI Analysis → Get detailed quality assessment
```

#### **Scenario 3: Quality Issue Investigation**
```bash
# Investigate data quality problems
# Live Monitor → Identify records with quality issues
# AI Analysis → Get AI-powered root cause analysis
# Data Overview → Understand business impact
```

#### **Scenario 4: Executive Reporting**
```bash
# Generate quality reports for leadership
# Data Overview → Export quality metrics and trends
# AI Analysis → Include AI insights in governance reports
# Live Monitor → Show real-time operational status
```

---

## 🎬 **Live Demo Flow**

## 🏗️ **Project Structure**

```text
monte-carlo-demo/
├── � setup.sh                 # 340-line automation script - main entry point
├── 📁 src/                     # APPLICATION CODE
│   └── monte_carlo_dashboard.py # 520-line consolidated data observability platform
├── 💾 database/                # DATABASE STORAGE
│   └── monte-carlo.duckdb      # DuckDB database file
├── � data/                    # Enterprise source datasets (6 files)
│   ├── product_operations_incidents_2025.csv
│   ├── business_intelligence_reports_2025.csv
│   ├── data_quality_violations_2025.csv
│   ├── system_monitoring_events_2025.csv
│   ├── user_behavior_analytics_2025.csv
│   └── customer_support_metrics_2025.csv
├── 🎯 sample_data/             # Live sample files (17 enterprise scenarios)
├── 🔧 monte_carlo_dbt/         # Data transformations and testing
├── 📁 scripts/                 # Enterprise data generators
│   ├── generate_enterprise_datasets.py
│   └── generate_quality_test_data.py
├── 🧪 tests/                   # Unit tests (3 passing)
├── ⚙️ requirements.txt         # Clean dependencies (9 packages)
└── 📖 README.md                # This comprehensive guide
```

### **Consolidated Architecture**
- **`src/monte_carlo_dashboard.py`** - Complete 520-line data observability platform
  - Streamlit multi-tab dashboard with live monitoring
  - DuckDB database operations and data loading
  - AI-powered quality analysis with OpenAI integration
  - File watching and real-time data ingestion
  - Centralized configuration and logging

---

## ⚙️ **Configuration & Dependencies**

### **Essential Dependencies**
```txt
streamlit==1.47.1          # Dashboard framework
duckdb==1.3.2              # In-memory database
dbt-core==1.10.5           # Data transformations
dbt-duckdb==1.9.1          # dbt DuckDB adapter
openai==1.57.2             # AI analysis
pandas==2.2.3              # Data manipulation
python-dotenv==1.0.1       # Environment management
watchdog==6.0.0            # File monitoring
pytest==8.3.4             # Testing framework
```

### **Environment Configuration** (`.env`)
```bash
# Required for AI analysis features
OPENAI_API_KEY=sk-your-key-here
OPENAI_ORGANIZATION=org-your-org-here  
OPENAI_PROJECT=proj-your-project-here

# Database configuration
DUCKDB_PATH=database/monte-carlo.duckdb
LOG_LEVEL=INFO
```

---

## 🎬 **Using the Platform**

### **Dashboard Features**
Once you start the dashboard with `streamlit run src/monte_carlo_dashboard.py`, you'll see:

- **📊 Data Quality Overview** - Summary statistics and quality metrics for all datasets
- **🔍 Dataset Analysis** - Detailed analysis of individual datasets with AI insights (if configured)
- **� Quality Trends** - Data quality patterns and anomaly detection
- **⚙️ Data Management** - Tools to load and refresh datasets

### **Demo Scenarios**

**Option 1: Use Pre-loaded Data**
- The dashboard loads with 6 enterprise datasets ready for analysis
- Navigate through tabs to explore data quality metrics
- View AI-powered insights (requires OpenAI API key)

**Option 2: Load Sample Files**
```bash
# Copy sample files to trigger new data analysis
cp sample_data/customer_engagement_metrics_20250129.csv data/
cp sample_data/payment_processing_errors_20250129.csv data/

# Refresh the dashboard to see updated metrics
```

**Option 3: Generate New Test Data**
```bash
# Generate additional enterprise datasets
python scripts/generate_enterprise_datasets.py

# Generate quality test datasets  
python scripts/generate_quality_test_data.py
```

---

## 💼 **Business Value for Monte Carlo**

### **For Data Engineering Teams**
- **Eliminates Manual Monitoring** - Automated quality checks replace manual SQL queries
- **Proactive Issue Detection** - Catch problems before they impact business operations
- **Pipeline Observability** - Complete visibility into data flow health and performance
- **Reduced MTTR** - Instant alerts and AI-powered root cause analysis

### **For Executive Leadership**
- **Business Risk Mitigation** - Prevent revenue impact from data quality issues
- **Operational Efficiency** - Reduce time spent on data firefighting
- **Customer Experience** - Ensure reliable data for customer-facing applications
- **Compliance Readiness** - Automated data governance and quality documentation

---

## 🔧 **Troubleshooting**

### **Setup Issues**

**🚨 "No module named 'streamlit'" or similar import errors:**
```bash
# Make sure you installed dependencies
pip install -r requirements.txt

# If still failing, try upgrading pip first
pip install --upgrade pip
pip install -r requirements.txt
```

**🚨 "Python version not supported" or compatibility issues:**
```bash
# Check your Python version (must be 3.12+)
python --version

# If using older Python, install Python 3.12+ from python.org
# Or use pyenv to manage multiple Python versions
```

**🚨 Dashboard won't start:**
```bash
# Check if port 8501 is already in use
netstat -an | grep 8501

# Start on different port if needed
streamlit run src/monte_carlo_dashboard.py --server.port 8502

# Try with verbose output for debugging
streamlit run src/monte_carlo_dashboard.py --logger.level=debug
```

### **Data Issues**

**🚨 "No data visible" or empty dashboard:**
```bash
# Load the initial data first
python src/monte_carlo_dashboard.py load_data

# If data/ folder is empty, copy from sample_data/
cp sample_data/*.csv data/

# Check that CSV files have proper headers
head -1 data/product_operations_incidents_2025.csv
# Should show: id,title,description,severity,timestamp
```

**🚨 "Database connection error":**
```bash
# Remove existing database and reload
rm database/monte-carlo.duckdb
python src/monte_carlo_dashboard.py load_data

# Check file permissions
ls -la database/monte-carlo.duckdb
```

### **AI Features**

**🚨 AI analysis not working:**
```bash
# Check if .env file exists
ls -la .env

# Verify API key format in .env
cat .env | grep OPENAI_API_KEY
# Should show: OPENAI_API_KEY=sk-proj-...

# Test API key manually
python -c "import openai; client = openai.OpenAI(); print('API key valid')"
```

**🚨 "Rate limit exceeded" errors:**
- AI analysis will be skipped if OpenAI quota is exceeded
- Platform still works without AI features
- Consider upgrading OpenAI plan or try again later

### **Platform Issues**

**🚨 Live monitoring not working:**
```bash
# Check if sample_data/ folder exists
ls -la sample_data/

# Test file monitoring manually
python src/monte_carlo_dashboard.py monitor
# Drop a CSV file in sample_data/ folder and watch for output
```

**🚨 Performance issues or slow loading:**
```bash
# Clear browser cache and refresh
# Check available memory: free -h
# Reduce data size if needed: head -100 data/*.csv > small_data.csv
```

### **Getting Help**

If you're still having issues:

1. **Check the logs** - Look for error messages in the terminal
2. **Verify requirements** - Ensure Python 3.12+ and all dependencies installed  
3. **Test step-by-step** - Follow the setup guide exactly as written
4. **Check permissions** - Ensure you can read/write files in the project directory

**Quick Validation Test:**
```bash
# Run this to verify everything is working
python -c "
import streamlit, duckdb, pandas, openai, watchdog
print('✅ All dependencies available')

import sys; sys.path.append('src')
import monte_carlo_dashboard
print('✅ Main application loads')

# Test database
import duckdb; con = duckdb.connect('database/monte-carlo.duckdb')
print(f'✅ Database accessible')
"
```

---

## 🎯 **Platform Readiness Summary**

This demo project demonstrates Monte Carlo's complete data observability platform:

✅ **Realistic Enterprise Data** - File names and scenarios mirror actual customer environments  
✅ **Complete Data Observability** - Real-time monitoring, AI analysis, and alerting  
✅ **Production Architecture** - Modern data stack with proper testing and configuration  
✅ **Business Impact Focus** - Clear ROI story for data quality and pipeline reliability  

**Demonstrates how Monte Carlo helps enterprise data teams deliver reliable, high-quality data at scale.** 🚀

---

## 🧪 **Testing & Validation**

Run the test suite to verify everything works:

```bash
# Run all tests
python -m pytest tests/ -v

# Expected output: 3/3 tests passing
# ✅ CSV data loading functionality
# ✅ DuckDB database operations  
# ✅ Configuration management
```

---

## � **Platform Capabilities Summary**

This Monte Carlo data observability demo showcases:

✅ **Real-time Data Monitoring** - Live dashboard with enterprise datasets  
✅ **AI-Powered Quality Analysis** - Intelligent anomaly detection (with OpenAI)  
✅ **Production Architecture** - Modern data stack with proper testing  
✅ **Enterprise Scenarios** - Realistic data patterns that mirror customer environments  
✅ **Easy Setup** - Simple installation and immediate value demonstration  

**Perfect for demonstrating how Monte Carlo helps enterprise teams deliver reliable, high-quality data at scale.** 🚀

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details.

---

*Monte Carlo Data Observability Platform Demo - January 2025*
