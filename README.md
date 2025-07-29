# 🎯 Monte Carlo Data Observability Demo

> **Production-ready data observability platform showcasing real-time monitoring, AI-powered analysis, and dbt integration - exactly what Monte Carlo delivers.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![dbt](https://img.shields.io/badge/dbt-1.10.5-orange.svg)](https://www.getdbt.com/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.47.1-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)

## 🚀 **One-Command Demo Setup**

```bash
python clean-setup.py
```

**Then start the demo:**
```bash
# Terminal 1: Live file monitoring
python monte_carlo_dashboard.py monitor

# Terminal 2: Dashboard
streamlit run monte_carlo_dashboard.py
```

**Demo URL:** http://localhost:8501

---

## 🎯 **What This Demonstrates for Monte Carlo**

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

## 🎬 **Live Demo Flow**

### **1. Start Systems**
```bash
python clean-setup.py                # One-time setup
python monte_carlo_dashboard.py monitor          # Terminal 1
streamlit run monte_carlo_dashboard.py           # Terminal 2
```

### **2. Dashboard Features**
- **🔴 Live Monitor Tab** - Real-time metrics with auto-refresh
- **📊 Data Analysis Tab** - Quality scoring and issue detection  
- **📋 Full Report Tab** - AI analysis + dbt test results

### **3. Live Demonstration**
```bash
# Drop demo files to trigger live updates
cp demo/sample_*.csv data/

# Watch dashboard update in real-time
# See quality scores, AI analysis, issue detection
```

---

## 🏗️ **Project Structure**

```
monte-carlo-demo/
├── 📊 dashboard.py              # Main Streamlit app (KEEP - POWERFUL!)
├── 🔄 live_demo_monitor.py     # Real-time file monitoring
├── 🤖 ai_layer/summarize.py    # AI-powered analysis
├── 🔧 dbt_project/             # Data transformations
├── 📁 data/                    # Source data
├── 🎯 demo/                    # Demo files for live updates
├── ⚙️ config.py                # Centralized configuration
└── 🧪 tests/                   # Unit tests
```

### **Core Files (Keep All)**
- `dashboard.py` - **Multi-tab dashboard with live monitoring**
- `live_demo_monitor.py` - **Real-time file watching system**  
- `ai_layer/summarize.py` - **GPT-4 powered quality analysis**
- `dbt_project/` - **Data transformations and testing**
- `config.py` - **Centralized environment management**

---

## ⚙️ **Simple Configuration**

### **Essential Dependencies** (`requirements-simple.txt`)
```
streamlit==1.47.1          # Dashboard
duckdb==1.3.2              # Database  
dbt-core==1.10.5           # Transformations
dbt-duckdb==1.9.4          # dbt adapter
openai==1.97.1             # AI analysis
python-dotenv==1.0.1       # Environment
pandas==2.3.1             # Data processing
watchdog==6.0.0            # File monitoring
pytest==8.3.4             # Testing
```

### **Environment Variables** (`.env`)
```bash
OPENAI_API_KEY=your_key_here      # For AI features
OPENAI_ORGANIZATION=your_org      # Optional
OPENAI_PROJECT=your_project       # Optional
```

---

## 🎯 **Monte Carlo Value Proposition**

### **For Data Engineering Teams**
- **Eliminates Manual Monitoring** - Automated quality checks replace manual SQL queries
- **Real-time Issue Detection** - Catch problems before they impact downstream systems
- **dbt Pipeline Observability** - Monitor transformation health and test failures
- **Executive Reporting** - Quality scores and trends for leadership

### **For AI/ML Teams** 
- **ML-Powered Anomaly Detection** - AI identifies subtle quality issues humans miss
- **Intelligent Alerting** - Reduces false positives with smart analysis
- **Content Quality Assessment** - Validates data suitable for ML training

### **Business Impact**
- **Prevent Data Incidents** - Stop bad data before it reaches dashboards
- **Increase Data Trust** - Teams confidence in data quality
- **Reduce Engineering Time** - Automated monitoring vs. manual checks
- **Faster Issue Resolution** - Instant alerts with root cause analysis

---

## 🚀 **Quick Commands**

```bash
# Complete setup and demo
python clean-setup.py

# Start live monitoring
python monte_carlo_dashboard.py monitor

# Start dashboard
streamlit run monte_carlo_dashboard.py

# Run AI analysis manually  
python ai_layer/summarize.py

# Test data quality
cd dbt_project && dbt test

# Generate new demo data
python scripts/generate_fake_data.py
```

---

## 🏆 **Interview Success Points**

This demo showcases exactly what Monte Carlo provides:

✅ **Real-time Data Observability** - Live monitoring dashboard  
✅ **AI-Powered Quality Detection** - Intelligent anomaly identification  
✅ **dbt Pipeline Monitoring** - Transform and test observability  
✅ **Production Architecture** - Scalable, maintainable system design  
✅ **Executive Visibility** - Quality metrics and trend reporting  
✅ **Developer Experience** - Easy setup, clear documentation  

**Built for Monte Carlo technical interviews - demonstrates deep understanding of data observability challenges and solutions.**

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) for details.
