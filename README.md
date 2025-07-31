# 🎯 Monte Carlo Data Observability Demo

> **Professional data quality monitoring platform demonstrating enterprise-grade data engineering patterns and best practices**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/duckdb-latest-yellow.svg)](https://duckdb.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Dashboard Capabilities](#-dashboard-capabilities)
- [Technical Implementation](#-technical-implementation)
- [Usage Examples](#-usage-examples)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## 🌟 Overview

This project demonstrates a **comprehensive learning platform** for data observability concepts inspired by Monte Carlo Data. Built with modern data stack technologies, it provides hands-on experience with enterprise-level data engineering patterns, real-time monitoring, and AI-powered analysis.

### Learning Objectives

- **Data Observability Mastery**: Understanding multi-dimensional quality scoring, anomaly detection, and monitoring patterns
- **Enterprise SDK Integration**: Hands-on experience with Monte Carlo's pycarlo SDK and API patterns
- **Modern Data Stack Proficiency**: Working with DuckDB, Streamlit, Python, and AI integration
- **Professional Development Practices**: Enterprise-style deployment, error handling, testing, and documentation
- **Real-time Systems Architecture**: File monitoring, live dashboards, and automated quality assessment

## ✨ Features

### 🎛️ Core Capabilities

- **Real-time Data Quality Monitoring** - Live quality scoring and anomaly detection
- **AI-Powered Analysis** - Natural language insights with OpenAI integration
- **File System Monitoring** - Automated validation and schema drift detection
- **Monte Carlo SDK Integration** - Enterprise-grade observability platform integration

### 🚀 Technical Highlights

- **Modern Data Stack**: DuckDB + Streamlit + Python 3.12+
- **Professional Deployment**: Automated setup with zero-configuration
- **Enterprise-style Patterns**: Comprehensive error handling and logging
- **Scalable Architecture**: Modular design with clear separation of concerns

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- Git
- 4GB+ available RAM
- Terminal/Command Line access

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/b8234/monte-carlo-demo.git
cd monte-carlo-demo

# Run automated setup and start dashboard
./setup.sh
```

The setup script will:
1. Create Python virtual environment
2. Install all dependencies
3. Configure environment variables
4. Load sample data
5. Start the dashboard at `http://localhost:8501`

### Alternative Setup Options

```bash
# Full setup without auto-start
./setup.sh setup

# Just start the dashboard
./setup.sh start

# Reset and restart (if needed)
./setup.sh reset

# Verify everything is working
./setup.sh verify

# Clean installation
./setup.sh clean
```

## 🏗️ Architecture

### System Design

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │     DuckDB       │    │   File System   │
│   Dashboard     │◄──►│   Analytics      │◄──►│   Monitoring    │
│                 │    │    Engine        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                        ▲                       ▲
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   OpenAI API    │    │  Monte Carlo     │    │   Sample Data   │
│   Integration   │    │   SDK Client     │    │   (20+ files)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive dashboard and visualization |
| **Database** | DuckDB | High-performance analytics engine |
| **Monitoring** | Watchdog | Real-time file system monitoring |
| **Integration** | Monte Carlo SDK | Enterprise observability platform |
| **AI Analysis** | OpenAI API | Natural language data insights |
| **Deployment** | Bash Scripts | Automated setup and process management |

## 📊 Dashboard Capabilities

### Tab 1: Data Quality Dashboard
- **Real-time Quality Metrics**: Live scoring with configurable thresholds
- **Historical Trend Analysis**: Quality degradation tracking over time
- **Multi-dimensional Scoring**: Completeness, consistency, timeliness, accuracy
- **Interactive Visualizations**: Charts and graphs with drill-down capabilities

### Tab 2: AI Analysis
- **Natural Language Insights**: AI-powered explanations of data patterns
- **Anomaly Detection**: Intelligent identification of quality issues
- **Predictive Analysis**: Forecasting potential data quality problems
- **Business Impact Assessment**: Analysis of quality issues on business metrics

### Tab 3: File Monitoring
- **Real-time File Detection**: Automatic monitoring of new data files
- **Schema Validation**: Immediate detection of schema changes
- **Quality Scoring**: Per-file quality assessment and reporting
- **Error Tracking**: Comprehensive logging of validation failures

### Tab 4: Monte Carlo SDK Integration
- **Overview Section**: Connection status and SDK capabilities
- **Quality Metrics**: Enterprise-grade rule management
- **Incident Management**: Alert configuration and resolution tracking
- **Rule Management**: Custom quality rule creation and monitoring
- **API Patterns**: Professional integration examples and patterns

## 🔧 Technical Implementation

### Project Structure

```
monte-carlo-demo/
├── src/
│   └── monte_carlo_dashboard.py    # Main application (40KB+ of code)
├── pycarlo_integration/            # Monte Carlo SDK implementation
│   ├── monte_carlo_client.py       # Core SDK client (700+ lines)
│   ├── demo.py                     # Demo scenarios
│   └── examples/                   # Integration examples
├── sample_data/                    # 20+ enterprise data scenarios
├── scripts/                        # CI/CD and utility scripts
├── tests/                          # Test suite
├── docs/                           # Documentation and Jekyll site
├── monte_carlo_dbt/               # dbt transformation models
├── setup.sh                       # Professional deployment automation
├── requirements.txt               # Dependency management
├── .env.example                   # Environment configuration template
└── personal.md                    # Technical presentation guide
```

### Key Design Decisions

**Database Choice**: DuckDB for columnar analytics performance without server overhead

**Architecture Pattern**: Modular monolith with clear separation of concerns

**Quality Algorithm**: Weighted multi-dimensional scoring based on industry best practices

**Integration Strategy**: Facade pattern for enterprise SDK complexity management

**Error Handling**: Defensive programming with graceful degradation

## 📈 Usage Examples

### Basic Quality Monitoring

1. **Start the dashboard**: `./setup.sh start`
2. **Open browser**: Navigate to `http://localhost:8501`
3. **View quality metrics**: Real-time scores and trend analysis
4. **Explore data**: Interactive charts and drill-down capabilities

### Live File Monitoring Demo

```bash
# Create a new data file while dashboard is running
cd sample_data
cat > new_customer_data_$(date +%Y%m%d).csv << EOF
customer_id,revenue,signup_date,status
1001,2500.00,2025-01-30,active
1002,1800.75,2025-01-30,pending
EOF

# Watch the File Monitoring tab for real-time detection
```

### Testing Data Quality Issues

```bash
# Create file with quality problems
cat > problematic_data_$(date +%Y%m%d).csv << EOF
customer_id,revenue,signup_date,email
1003,invalid_amount,2025-13-99,not-an-email
,1800.75,,incomplete@
EOF

# Observe quality score changes and validation alerts
```

### AI Analysis (with OpenAI configured)

1. Edit `.env` file with your OpenAI API key
2. Restart dashboard: `./setup.sh reset`
3. Navigate to AI Analysis tab
4. View natural language insights and recommendations

## 🛠️ Development

### Local Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/b8234/monte-carlo-demo.git
cd monte-carlo-demo

# Create development environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start in development mode
streamlit run src/monte_carlo_dashboard.py --server.fileWatcherType auto
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run comprehensive test suite
pytest tests/ -v --cov=src/

# Run specific test categories
pytest tests/test_basic.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## 🚀 Deployment

### Demo Deployment

> **Note**: This is a demonstration platform showcasing professional data engineering patterns. It is designed for learning, testing, and demonstrating capabilities rather than production workloads.

```bash
# Current deployment supports local/development environments
./setup.sh setup
./setup.sh start
```

### Future Production Considerations

For actual production deployment, additional considerations would include:

- Docker containerization for consistent deployment
- Load balancing and horizontal scaling
- Enhanced security hardening and authentication
- Comprehensive monitoring and alerting
- Database optimization for production workloads
- Full test coverage and performance testing

### Environment Configuration

Create `.env` file from template:

```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:

```bash
# Database Configuration
DUCKDB_PATH=monte_carlo_dbt/database/monte-carlo.duckdb

# Optional: OpenAI Integration
OPENAI_API_KEY=your-api-key-here

# Optional: Monte Carlo Integration  
MONTE_CARLO_API_KEY=your-monte-carlo-key
```

## 📊 Performance Benchmarks

| Metric | Performance |
|--------|-------------|
| **Dashboard Load Time** | < 3 seconds |
| **Quality Score Calculation** | < 2 seconds |
| **File Processing** | < 1 second per MB |
| **Database Queries** | < 500ms |
| **Memory Usage** | ~100-200MB |
| **Supported File Count** | 100+ files |
| **Database Scale** | GB-scale data |

## 🔒 Security & Compliance

- **Environment Variable Management**: Secure credential handling
- **Audit Logging**: Comprehensive activity tracking
- **Data Encryption**: Secure data handling practices
- **Access Controls**: Foundation for role-based permissions

> **Note**: This demo implements security best practices suitable for development and demonstration environments. Production deployment would require additional security hardening and compliance measures.

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Contribution Guidelines

- Follow existing code style and patterns
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📚 Documentation

- **[Technical Presentation Guide](personal.md)** - Comprehensive demo and architecture guide
- **[Documentation Site](docs/)** - Jekyll-powered documentation website

## 🐛 Troubleshooting

### Common Issues

**Dashboard won't start**:
```bash
./setup.sh reset
./setup.sh start
```

**Database connection errors**:
```bash
./setup.sh data  # Reload data
./setup.sh verify  # Check status
```

**File monitoring not working**:
```bash
# Check sample_data directory permissions
ls -la sample_data/
chmod 755 sample_data/
```

**Performance issues**:
```bash
# Check system resources
./setup.sh verify
# Restart with clean state
./setup.sh clean && ./setup.sh setup
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Monte Carlo Data** - For the excellent data observability platform and SDK
- **DuckDB Team** - For the high-performance analytics engine
- **Streamlit Team** - For the intuitive dashboard framework
- **OpenAI** - For the powerful AI analysis capabilities

## 📞 Contact

**Developer**: GitHub @b8234
**Project Link**: [https://github.com/b8234/monte-carlo-demo](https://github.com/b8234/monte-carlo-demo)

---

*Built with ❤️ for enterprise data engineering excellence*

**Ready to demonstrate professional-level data engineering capabilities!** 🚀
