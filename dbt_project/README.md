# dbt Project Configuration

This directory contains the dbt project for the Monte Carlo demo, including data models, tests, and configuration.

## Setup

1. **Install dbt with DuckDB adapter:**
   ```bash
   pip install dbt-core dbt-duckdb
   ```

2. **Configure dbt profile** (`~/.dbt/profiles.yml`):
   ```yaml
   dbt_project:
     target: dev
     outputs:
       dev:
         type: duckdb
         path: './monte-carlo.duckdb'
         threads: 4
   ```

3. **Run dbt commands:**
   ```bash
   cd dbt_project
   dbt run      # Execute models
   dbt test     # Run data quality tests
   dbt docs generate  # Generate documentation
   ```

## Models

- **summarize_model.sql**: Main transformation that processes raw data and adds description length metrics
- **schema.yml**: Defines data quality tests including not_null and unique constraints

## Tests

The project includes several data quality tests:
- `not_null` tests for critical fields
- `unique` tests for ID columns
- Custom tests can be added in the `tests/` directory

## Usage

This dbt project is designed to work with the monte-carlo-demo observability stack. The models are automatically tested and monitored by the observability layer.

### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
