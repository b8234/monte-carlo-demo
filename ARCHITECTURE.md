# Project Structure

This document explains the organization and purpose of each component in the monte-carlo-demo project.

## 📁 Directory Structure

```
monte-carlo-demo/
├── README.md                    # Project overview and setup instructions
├── requirements.txt             # Python dependencies
├── dashboard.py                 # Streamlit web interface
├── load_csv.py                 # Data ingestion script
├── check_tables.py             # Database inspection utility
├── monte-carlo.duckdb          # DuckDB database file
├── data/                       # Raw data sources
│   └── raw_data.csv            # Sample dataset
├── dbt_project/                # dbt transformation layer
│   ├── dbt_project.yml         # dbt configuration
│   ├── models/                 # Data models
│   │   ├── schema.yml          # Model tests and documentation
│   │   └── summarize_model.sql # Main transformation model
│   ├── analyses/               # Ad-hoc analyses
│   ├── macros/                 # Reusable SQL macros
│   ├── seeds/                  # Static data files
│   ├── snapshots/              # SCD Type 2 tables
│   └── tests/                  # Custom data tests
├── ai_layer/                   # AI processing components
│   └── summarize.py            # OpenAI integration for text summarization
├── observability/              # Monitoring and alerting
│   ├── alerts.py               # dbt test failure detection
│   └── ai_alerts.py           # AI quality monitoring
└── logs/                       # Application logs
    └── dbt.log                 # dbt execution logs
```

## 🔄 Data Flow

1. **Ingestion**: `load_csv.py` loads raw data into DuckDB
2. **Transformation**: dbt models clean and enrich the data
3. **AI Processing**: `ai_layer/summarize.py` generates content summaries
4. **Quality Monitoring**: `observability/` components check for issues
5. **Visualization**: `dashboard.py` presents results and alerts

## 🧩 Component Details

### Core Scripts
- **dashboard.py**: Streamlit application providing real-time monitoring interface
- **load_csv.py**: Simple ETL script to populate the database from CSV
- **check_tables.py**: Utility to inspect database schema and contents

### dbt Project
- **models/summarize_model.sql**: Core transformation adding description length metrics
- **models/schema.yml**: Data quality tests (not_null, unique constraints)
- **dbt_project.yml**: Project configuration and materialization settings

### AI Layer
- **summarize.py**: Integrates with OpenAI API to generate text summaries
- Includes validation logic to detect hallucinations and poor quality outputs

### Observability
- **alerts.py**: Monitors dbt test execution and captures failures
- **ai_alerts.py**: Evaluates AI-generated content for quality issues
- Simulates Monte Carlo-style data observability patterns

## 🔧 Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Database | DuckDB | Analytics database with SQL interface |
| Transformations | dbt | Data modeling and testing framework |
| AI | OpenAI GPT-4 | Text summarization and content generation |
| Frontend | Streamlit | Interactive dashboard and visualization |
| Orchestration | Python | Glue code and workflow management |

## 🎯 Design Principles

1. **Separation of Concerns**: Each layer has a distinct responsibility
2. **Testability**: dbt tests ensure data quality at the model level
3. **Observability**: Multiple monitoring layers catch different types of issues
4. **Modularity**: Components can be developed and tested independently
5. **Scalability**: Architecture patterns support growth to production scale
