# 🚀 Monte Carlo Demo - Quick Setup Guide

## Prerequisites
- Python 3.9+
- OpenAI API key (for AI features)

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials:
# OPENAI_API_KEY=sk-your-key-here
# OPENAI_ORGANIZATION=org-your-org-here  
# OPENAI_PROJECT=proj-your-project-here
```

### 3. Load Sample Data
```bash
python monte_carlo_dashboard.py load_data
```

### 4. Setup dbt (Optional)
```bash
cd dbt_project
dbt run
dbt test
cd ..
```

### 5. Start Dashboard
```bash
streamlit run monte_carlo_dashboard.py
```

### 6. Open Browser
Navigate to: http://localhost:8501

## 🎬 Demo Features
- **🔴 Live Monitor**: Real-time data quality metrics
- **🤖 AI Analysis**: Intelligent quality assessment
- **📊 Data Overview**: Complete database statistics

## 💡 Pro Tips
- Drop CSV files in `demo/` folder for live ingestion
- Enable auto-refresh for real-time updates
- Use AI analysis to detect quality issues

## 🎯 Monte Carlo Value Demonstrated
✅ Real-time data quality monitoring  
✅ AI-powered anomaly detection  
✅ dbt pipeline observability  
✅ Live issue alerting  

**Everything in one powerful dashboard!** 🚀
