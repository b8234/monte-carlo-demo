# Pycarlo SDK Usage Guide

This guide shows how to use the official Monte Carlo Python SDK (`pycarlo`) with proper API patterns.

## Installation & Configuration

```bash
# Install the official Monte Carlo Python SDK
pip install pycarlo

# Configure credentials (creates ~/.mcd/profiles.ini)
montecarlo configure

# Or use environment variables
export MONTE_CARLO_API_ID="your_api_id"
export MONTE_CARLO_API_TOKEN="your_api_token"
```

## Core API Patterns

### 1. Basic Client Setup

```python
from pycarlo.core import Client, Query, Mutation, Session

# Method 1: Use default profile from ~/.mcd/profiles.ini
# (created automatically via `montecarlo configure` CLI)
client = Client()

# Method 2: Use environment variables with basic Session
session = Session(
    mcd_id=os.getenv("MONTE_CARLO_API_ID"),
    mcd_token=os.getenv("MONTE_CARLO_API_TOKEN")
)
client = Client(session=session)

# Method 3: Use Session with specialized scope
session = Session(
    mcd_id=os.getenv("MONTE_CARLO_API_ID"),
    mcd_token=os.getenv("MONTE_CARLO_API_TOKEN"),
    scope='AirflowCallbacks'  # For Airflow integration
)
client = Client(session=session)
```

### 1.1. Available Scopes

Different scopes enable access to specialized Monte Carlo APIs:

- **`AirflowCallbacks`**: For Airflow DAG/task status integration
- **`DataCollectors`**: For data collector management and health monitoring  
- **`MetricIngestion`**: For custom metric and KPI ingestion
- **`IncidentManagement`**: For automated incident workflow management

### 2. Query Examples

#### Get User Information
```python
query = Query()
query.get_user.__fields__('email', 'first_name', 'last_name')
response = client(query)
print(f"User: {response.get_user.first_name} {response.get_user.last_name}")
print(f"Email: {response.get_user.email}")
```

#### Test Connection
```python
query = Query()
query.test_telnet_connection(host='montecarlodata.com', port=443)
response = client(query)
print(response)
```

#### Get Tables (with structured fields)
```python
query = Query()
query.get_tables(first=10).__fields__(
    edges=query.get_tables.edges.__fields__(
        node=query.get_tables.edges.node.__fields__(
            'full_table_id', 'database', 'schema', 'table_name', 'row_count'
        )
    )
)
response = client(query)

for edge in response.get_tables.edges:
    table = edge.node
    print(f"Table: {table.full_table_id} (rows: {table.row_count})")
```

#### Raw Query Execution
```python
get_table_query = """
query getTables{
  getTables(first: 10) {
    edges {
      node {
        fullTableId
        database
        schema
        tableName
        rowCount
      }
    }
  }
}
"""
response = client(get_table_query)

# Access with dot notation (snake_case)
for edge in response.get_tables.edges:
    print(edge.node.full_table_id)

# Or access as dictionary
print(response['get_tables']['edges'][0]['node']['full_table_id'])
```

#### Get Incidents
```python
query = Query()
query.get_incidents(first=20).__fields__(
    edges=query.get_incidents.edges.__fields__(
        node=query.get_incidents.edges.node.__fields__(
            'id', 'status', 'incident_type', 'severity', 
            'description', 'created_time', 'full_table_id'
        )
    )
)
response = client(query)

for edge in response.get_incidents.edges:
    incident = edge.node
    print(f"Incident: {incident.incident_type} ({incident.severity})")
    print(f"  Table: {incident.full_table_id}")
    print(f"  Status: {incident.status}")
```

### 3. Mutation Examples

#### Generate Collector Template
```python
mutation = Mutation()
mutation.generate_collector_template().dc.template_launch_url()
response = client(mutation)
print(f"Template URL: {response}")
```

#### Error Handling
```python
from pycarlo.common.errors import GqlError

try:
    mutation = Mutation()
    mutation.generate_collector_template(region='invalid_region')
    response = client(mutation)
except GqlError as e:
    print(f"GraphQL Error: {e}")
    # Handle specific Monte Carlo API errors
```

### 3.1. Direct API Calls with make_request

For specialized endpoints beyond GraphQL, use `make_request()`:

#### Airflow Callbacks
```python
# Setup with AirflowCallbacks scope
session = Session(
    mcd_id=api_id, 
    mcd_token=api_token, 
    scope='AirflowCallbacks'
)
client = Client(session=session)

# Send Airflow task status
response = client.make_request(
    path='/airflow/callbacks',
    method='POST',
    body={
        'dag_id': 'data_quality_pipeline',
        'task_id': 'validate_tables',
        'status': 'success',
        'timestamp': '2025-07-30T14:30:00Z'
    },
    timeout_in_seconds=20
)
```

#### Data Collector Management
```python
# Setup with DataCollectors scope
session = Session(mcd_id=api_id, mcd_token=api_token, scope='DataCollectors')
client = Client(session=session)

# Check collector health
health = client.make_request(path='/collectors/health', method='GET')

# Deploy new collector
deployment = client.make_request(
    path='/collectors',
    method='POST',
    body={
        'collector_type': 'dbt',
        'config': {'project_path': '/opt/dbt/project'}
    }
)
```

#### Custom Metrics Ingestion
```python
# Setup with MetricIngestion scope
session = Session(mcd_id=api_id, mcd_token=api_token, scope='MetricIngestion')
client = Client(session=session)

# Send custom quality metrics
response = client.make_request(
    path='/custom-metrics',
    method='POST',
    body={
        'metrics': [
            {
                'table_id': 'warehouse.analytics.events',
                'metric_type': 'data_freshness',
                'value': 0.5,  # 30 minutes
                'timestamp': '2025-07-30T14:30:00Z'
            }
        ]
    }
)
```

### 4. Query Generation

You can generate and inspect queries before execution:

```python
query = Query()
query.test_telnet_connection(host='montecarlodata.com', port=443)

# Print the generated GraphQL query
print(query)
# Output:
# query {
#   testTelnetConnection(host: "montecarlodata.com", port: 443) {
#     success
#     validations {
#       type
#       message
#     }
#     warnings {
#       type
#       message
#     }
#   }
# }
```

## Integration with Our Demo

Our Monte Carlo integration demonstrates these patterns in:

1. **Production Mode** (`ProductionMonteCarloClient`):
   - Uses real pycarlo.core Client, Query, Mutation
   - Handles authentication and credentials
   - Executes actual GraphQL queries
   - Proper error handling with GqlError

2. **Demo Mode** (`MockMonteCarloClient`):
   - Simulates the same API patterns
   - No credentials required
   - Shows expected data structures
   - Educational for learning pycarlo patterns

## Key Differences from Generic GraphQL

1. **Snake Case Conversion**: GraphQL camelCase → Python snake_case
2. **Dot Notation Access**: Use `response.get_user.email` instead of `response['getUser']['email']`
3. **Field Selection**: Use `.__fields__()` method for structured queries
4. **Profile Management**: Built-in credential management via `montecarlo configure`
5. **Error Types**: Specific `GqlError` for Monte Carlo API issues

## Production Checklist

- [ ] Install pycarlo: `pip install pycarlo`
- [ ] Configure credentials: `montecarlo configure` or set environment variables
- [ ] Test connection with basic query
- [ ] Handle `GqlError` exceptions appropriately
- [ ] Use proper field selection for complex queries
- [ ] Consider rate limiting and pagination for large datasets

## Demo to Production Migration

Switch from demo mode to production mode by:

1. Installing pycarlo: `pip install pycarlo>=0.5.0`
2. Setting up credentials via CLI or environment variables
3. Changing client initialization to use `ProductionMonteCarloClient`
4. All existing code patterns remain the same!

This seamless transition is a key benefit of our integration design.
