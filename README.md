# Monte Carlo Data Observability Demo

A demonstration of modern data observability patterns using AI-powered quality monitoring, data pipeline orchestration, and real-time alerting.

## 🎯 Overview

This project showcases a complete data observability stack that monitors data quality through AI-powered content validation and traditional dbt testing. It simulates Monte Carlo-style observability by detecting data anomalies, AI hallucinations, and pipeline failures.

## 🏗️ Architecture

```
├── data/                   # Raw data sources
├── dbt_project/           # dbt models and tests
├── ai_layer/              # AI summarization and validation
├── observability/         # Monitoring and alerting logic
├── dashboard.py           # Streamlit dashboard
└── load_csv.py           # Data ingestion script
```

## 🚀 Features

- **AI Quality Monitoring**: Detects hallucinations and generic responses in AI-generated summaries
- **dbt Data Testing**: Validates data integrity with not_null and uniqueness constraints
- **Real-time Dashboard**: Streamlit interface showing data quality metrics and alerts
- **Alerting System**: Automated detection of data quality issues and pipeline failures
- **Modern Data Stack**: DuckDB for analytics, OpenAI for AI processing, dbt for transformations

## 🛠️ Tech Stack

- **Database**: DuckDB
- **Transformations**: dbt
- **AI**: OpenAI GPT-4
- **Frontend**: Streamlit
- **Language**: Python 3.8+

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- dbt installed globally (`pip install dbt-core dbt-duckdb`)

## 🔧 Setup

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd monte-carlo-demo
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   # Create .env file with:
   OPENAI_ORGANIZATION=your_org_id
   OPENAI_PROJECT=your_project_id  
   OPENAI_API_KEY=your_api_key
   DUCKDB_PATH=monte-carlo.duckdb
   ```

3. **Load initial data:**
   ```bash
   python load_csv.py
   ```

4. **Generate additional sample data (optional):**
   ```bash
   python generate_sample_data.py
   python load_csv.py  # Reload with new data
   ```

4. **Configure dbt profile:**
   ```bash
   mkdir -p ~/.dbt
   # Add profiles.yml configuration (see dbt_project/README.md)
   ```

5. **Run dbt models:**
   ```bash
   cd dbt_project
   dbt run
   dbt test
   ```

## 🎮 Usage

1. **Launch the dashboard:**
   ```bash
   python -m streamlit run dashboard.py
   ```

2. **Monitor data quality:**
   - View AI summary quality issues
   - Check dbt test failures
   - Monitor data pipeline health

3. **Run observability checks:**
   ```bash
   python observability/alerts.py
   python observability/ai_alerts.py
   ```

## 📊 Demo Scenarios

The project demonstrates several observability scenarios using comprehensive sample datasets:

### Data Quality Issues Included:
- **Empty/Null Values**: Records with missing descriptions to trigger data quality alerts
- **Short Content**: Minimal text that produces poor AI summaries  
- **Special Characters**: Unicode, emojis, and edge cases for robust processing
- **Long Text**: Extremely long descriptions to test processing limits
- **Generic Responses**: Content likely to trigger AI hallucination detection
- **Malformed Data**: Inconsistent formatting and data types

### Sample Data Files:
- `raw_data.csv`: Base dataset with 20 records including edge cases
- `additional_data.csv`: Extended dataset with 10 more records
- `enriched_data.csv`: Enhanced data with priority, department, and date fields
- `generated_sample.csv`: 100 programmatically generated records with quality issues
- `timestamped_events.csv`: Time-series data with event types and severity
- `problematic_data.csv`: Focused dataset of problematic records for testing

### Observability Scenarios:
1. **AI Hallucination Detection**: Identifies when AI generates generic or invalid summaries
2. **Data Quality Failures**: Shows dbt test failures for null values or constraint violations  
3. **Pipeline Monitoring**: Tracks data freshness and processing metrics
4. **Automated Alerting**: Triggers alerts when quality thresholds are breached
5. **Edge Case Handling**: Processes special characters, long text, and malformed data

## 🧪 Testing

- dbt tests validate data constraints
- AI quality checks detect poor summaries
- Integration tests ensure end-to-end functionality

## 🔮 Future Enhancements

- [ ] Add data lineage tracking
- [ ] Implement anomaly detection for numerical metrics
- [ ] Create Slack/email alert integrations
- [ ] Add data profiling and drift detection
- [ ] Expand AI quality metrics beyond text summarization

## 📝 Implementation Notes

This demo simulates production observability patterns at scale. In a real environment, you would:
- Use production databases (PostgreSQL, Snowflake, etc.)
- Implement proper secret management
- Add comprehensive logging and monitoring
- Set up CI/CD for dbt deployments
- Scale AI validation across larger datasets

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the demonstration.

## 📄 License

MIT License - see LICENSE file for details.
