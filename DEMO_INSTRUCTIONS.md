# 🎬 Live Demo Instructions

## 🚀 **Quick Start for Live Demo**

### **Option 1: Instant Demo with Pre-made Files**

1. **Start the live monitor:**
   ```bash
   python live_demo_monitor.py
   ```

2. **Open dashboard in browser:**
   ```bash
   python -m streamlit run dashboard.py
   ```
   Go to http://localhost:8501 and click "Live Demo Monitor" tab

3. **Add sample data during demo:**
   ```bash
   # Copy sample files to trigger live updates
   cp demo/sample_mixed_quality.csv demo/demo_file_1.csv
   cp demo/sample_critical_issues.csv demo/demo_file_2.csv  
   cp demo/sample_good_quality.csv demo/demo_file_3.csv
   ```

### **Option 2: Create Custom Demo Files**

Create CSV files with `title` and `description` columns in the `demo/` folder:

```csv
title,description
Critical Issue,This is a sample critical issue with detailed description
Empty Issue,
Short,Hi
```

## 🎯 **Demo Flow for Interviews**

### **1. Setup (30 seconds)**
- Show the dashboard: "This is our real-time data observability platform"
- Point to Live Demo Monitor tab: "Let me show you live data ingestion"

### **2. Live Data Ingestion (60 seconds)**
- Start live monitor in terminal
- Drop first CSV file: "Watch this - I'm adding new data with quality issues"
- Show dashboard updating in real-time
- Highlight metrics changing: "See the quality score dropping"

### **3. AI Quality Analysis (90 seconds)**
- Run AI analysis: `python ai_layer/summarize.py`
- Show comprehensive quality report
- Explain AI detection: "Our GPT-4 integration automatically identifies issues"

### **4. Technical Discussion Points**
- **Architecture**: "Centralized config, real-time monitoring, AI integration"
- **Scalability**: "File watcher handles multiple data sources"
- **Observability**: "Complete data lineage from ingestion to quality scoring"

## 📊 **Sample Demo Data Quality Scenarios**

### **File 1: Mixed Quality Data** (`sample_mixed_quality.csv`)
- NULL values in title column
- Empty descriptions  
- Good quality records mixed in
- **Expected**: Quality score ~60-70%

### **File 2: Critical Issues** (`sample_critical_issues.csv`)
- Security incidents
- Data breaches
- System failures
- **Expected**: All high-quality content, 100% score

### **File 3: Good Quality** (`sample_good_quality.csv`)
- Complete descriptions
- Proper formatting
- Business value content
- **Expected**: Perfect quality score

## 🛠 **Technical Features to Highlight**

1. **Real-time File Monitoring** - Watchdog library for live file detection
2. **Automatic Data Processing** - Pandas + DuckDB integration
3. **AI-Powered Quality Assessment** - OpenAI GPT-4 analysis
4. **Live Dashboard Updates** - Streamlit with auto-refresh
5. **Production Architecture** - Centralized config, error handling, logging

## 🎤 **Interview Talking Points**

**"Let me show you our data observability platform in action..."**

- **Business Value**: "This reduces manual data review by 90%"
- **Technical Excellence**: "Real-time processing with AI-powered insights"
- **Scalability**: "Handles multiple data sources with automatic quality scoring"
- **Production Ready**: "Complete monitoring, alerting, and reporting"

## 🔧 **Troubleshooting**

- **Dashboard not updating?** - Check if live monitor is running
- **File not processed?** - Ensure CSV has `title` and `description` columns
- **Database locked?** - Stop Streamlit dashboard temporarily
- **OpenAI errors?** - Check `.env` file has valid API key

Ready to impress! 🚀
