#!/usr/bin/env python3
"""
PycarloAPI Demo - Real-world examples using pycarlo.core API patterns
Demonstrates the proper way to use pycarlo Client, Query, and Mutation classes.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

def demo_with_credentials():
    """
    Example showing how to use pycarlo with real Monte Carlo credentials.
    This follows the exact patterns from the pycarlo documentation.
    """
    print("🔗 Production Monte Carlo with pycarlo.core")
    print("=" * 50)
    
    try:
        # Real pycarlo import
        from pycarlo.core import Client, Query, Mutation
        from pycarlo.common.errors import GqlError
        
        # Method 1: Use default profile from ~/.mcd/profiles.ini
        # (created automatically via `montecarlo configure` CLI)
        print("📋 Method 1: Using default profile")
        client = Client()
        
        # Method 2: Use environment variables
        # api_id = os.getenv("MONTE_CARLO_API_ID")
        # api_token = os.getenv("MONTE_CARLO_API_TOKEN")
        # client = Client(api_id=api_id, api_token=api_token)
        
        print("✅ Client created successfully")
        
        # Example 1: Get user information
        print("\n👤 Getting user information...")
        query = Query()
        query.get_user.__fields__('email', 'first_name', 'last_name')
        response = client(query)
        print(f"User: {response.get_user.first_name} {response.get_user.last_name}")
        print(f"Email: {response.get_user.email}")
        
        # Example 2: Test connection with parameters
        print("\n🔌 Testing connection...")
        query = Query()
        query.test_telnet_connection(host='montecarlodata.com', port=443)
        response = client(query)
        print(f"Connection test: {response}")
        
        # Example 3: Get tables (first 10)
        print("\n📊 Getting tables...")
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
        
        print(f"Found {len(response.get_tables.edges)} tables:")
        for edge in response.get_tables.edges:
            node = edge.node
            print(f"  - {node.full_table_id} (rows: {node.row_count or 'unknown'})")
        
        # Example 4: Get incidents
        print("\n🚨 Getting recent incidents...")
        incidents_query = Query()
        incidents_query.get_incidents(first=5).__fields__(
            edges=incidents_query.get_incidents.edges.__fields__(
                node=incidents_query.get_incidents.edges.node.__fields__(
                    'id', 'status', 'incident_type', 'severity', 'description'
                )
            )
        )
        response = client(incidents_query)
        
        print(f"Found {len(response.get_incidents.edges)} recent incidents:")
        for edge in response.get_incidents.edges:
            incident = edge.node
            print(f"  - {incident.incident_type} ({incident.severity}): {incident.description[:50]}...")
        
        # Example 5: Create collector template (mutation example)
        print("\n⚙️ Generating collector template...")
        try:
            mutation = Mutation()
            mutation.generate_collector_template().dc.template_launch_url()
            response = client(mutation)
            print(f"Collector template URL: {response}")
        except GqlError as e:
            print(f"Expected error for invalid region: {e}")
        
        print("\n✅ All pycarlo API examples completed successfully!")
        
    except ImportError:
        print("❌ pycarlo not installed. Install with: pip install pycarlo==0.10.51")
        print("💡 After installation, configure with: montecarlo configure")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have configured Monte Carlo credentials:")
        print("   1. Run: montecarlo configure")
        print("   2. Or set environment variables:")
        print("      export MONTE_CARLO_API_ID=your_api_id")
        print("      export MONTE_CARLO_API_TOKEN=your_api_token")
        return False
    
    return True


def demo_without_credentials():
    """
    Demo mode that shows what the API calls would look like without requiring credentials.
    This simulates the pycarlo API patterns for learning purposes.
    """
    print("🎭 Demo Mode - Simulating pycarlo.core API")
    print("=" * 50)
    
    # Simulate the pycarlo import structure
    class MockQuery:
        def __init__(self):
            self.get_user = MockUserQuery()
            self.get_tables = MockTablesQuery()
            self.get_incidents = MockIncidentsQuery()
            self.test_telnet_connection = MockTelnetQuery()
            
        def __str__(self):
            return """query {
  testTelnetConnection(host: "montecarlodata.com", port: 443) {
    success
    validations {
      type
      message
    }
    warnings {
      type
      message
    }
  }
}"""
    
    class MockUserQuery:
        def __fields__(self, *fields):
            print(f"📝 Query fields selected: {', '.join(fields)}")
            return self
    
    class MockTablesQuery:
        def __call__(self, first=10):
            return MockTablesQueryWithArgs(first)
            
        def __fields__(self, **kwargs):
            return self
    
    class MockTablesQueryWithArgs:
        def __init__(self, first):
            self.first = first
            
        def __fields__(self, **kwargs):
            return self
    
    class MockIncidentsQuery:
        def __call__(self, first=10, **kwargs):
            return MockIncidentsQueryWithArgs(first)
            
        def __fields__(self, **kwargs):
            return self
    
    class MockIncidentsQueryWithArgs:
        def __init__(self, first):
            self.first = first
            self.edges = MockIncidentsEdgesQuery()
            
        def __fields__(self, **kwargs):
            return self
    
    class MockIncidentsEdgesQuery:
        def __init__(self):
            self.node = MockIncidentsNodeQuery()
            
        def __fields__(self, **kwargs):
            return self
    
    class MockIncidentsNodeQuery:
        def __fields__(self, *fields):
            return self
    
    class MockTelnetQuery:
        def __call__(self, host, port):
            return MockTelnetResponse(host, port)
    
    class MockTelnetResponse:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.success = True
            
        def __str__(self):
            return f"{{success: true, host: '{self.host}', port: {self.port}}}"
    
    class MockMutation:
        def __init__(self):
            self.generate_collector_template = MockCollectorMutation()
    
    class MockCollectorMutation:
        def __call__(self, region=None):
            if region == 'artemis':
                raise MockGqlError("Region \"'artemis'\" not currently active.")
            return self
            
        def dc(self):
            return MockDcResponse()
    
    class MockDcResponse:
        def template_launch_url(self):
            return "https://aws.amazon.com/cloudformation/..."
    
    class MockGqlError(Exception):
        pass
    
    class MockResponse:
        def __init__(self):
            self.get_user = MockUser()
            self.get_tables = MockTablesResponse()
            self.get_incidents = MockIncidentsResponse()
    
    class MockUser:
        email = "demo@example.com"
        first_name = "Demo"
        last_name = "User"
    
    class MockTablesResponse:
        def __init__(self):
            self.edges = [
                MockEdge("demo_db.demo_schema.users", 1000),
                MockEdge("demo_db.demo_schema.orders", 2500),
                MockEdge("demo_db.demo_schema.products", 150)
            ]
    
    class MockIncidentsResponse:
        def __init__(self):
            self.edges = [
                MockIncidentEdge("INC001", "freshness", "medium", "Table data is 6 hours old"),
                MockIncidentEdge("INC002", "volume", "low", "Row count decreased by 15%")
            ]
    
    class MockEdge:
        def __init__(self, table_id, row_count):
            self.node = MockTableNode(table_id, row_count)
    
    class MockTableNode:
        def __init__(self, table_id, row_count):
            self.full_table_id = table_id
            self.row_count = row_count
            parts = table_id.split('.')
            self.database = parts[0] if len(parts) > 0 else "demo_db"
            self.schema = parts[1] if len(parts) > 1 else "demo_schema"
            self.table_name = parts[2] if len(parts) > 2 else "demo_table"
    
    class MockIncidentEdge:
        def __init__(self, incident_id, incident_type, severity, description):
            self.node = MockIncidentNode(incident_id, incident_type, severity, description)
    
    class MockIncidentNode:
        def __init__(self, incident_id, incident_type, severity, description):
            self.id = incident_id
            self.incident_type = incident_type.upper()
            self.severity = severity.upper()
            self.description = description
            self.status = "OPEN"
    
    class MockClient:
        def __call__(self, query_or_mutation):
            if isinstance(query_or_mutation, str):
                # Raw query execution
                print(f"📡 Executing raw query:\n{query_or_mutation[:100]}...")
                return MockResponse()
            elif isinstance(query_or_mutation, MockQuery):
                print("📡 Executing Query object...")
                return MockResponse()
            elif isinstance(query_or_mutation, MockMutation):
                print("📡 Executing Mutation object...")
                return "https://aws.amazon.com/cloudformation/template-url"
            else:
                return MockResponse()
    
    # Simulate the pycarlo workflow
    print("📋 Creating client (demo mode)...")
    client = MockClient()
    Query = MockQuery
    Mutation = MockMutation
    GqlError = MockGqlError
    
    print("✅ Mock client created successfully")
    
    # Example 1: Get user information
    print("\n👤 Getting user information...")
    query = Query()
    query.get_user.__fields__('email', 'first_name', 'last_name')
    response = client(query)
    print(f"User: {response.get_user.first_name} {response.get_user.last_name}")
    print(f"Email: {response.get_user.email}")
    
    # Example 2: Test connection
    print("\n🔌 Testing telnet connection...")
    query = Query()
    result = query.test_telnet_connection(host='montecarlodata.com', port=443)
    print(f"Connection test: {result}")
    
    # Example 3: Get tables with raw query
    print("\n📊 Getting tables with raw query...")
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
    
    print(f"Found {len(response.get_tables.edges)} tables:")
    for edge in response.get_tables.edges:
        node = edge.node
        print(f"  - {node.full_table_id} (rows: {node.row_count})")
    
    # Example 4: Get incidents with Query object
    print("\n🚨 Getting recent incidents...")
    incidents_query = Query()
    # In real pycarlo, this would be structured differently
    # but for demo purposes, we'll simulate the response
    response = client(incidents_query)
    
    print(f"Found {len(response.get_incidents.edges)} recent incidents:")
    for edge in response.get_incidents.edges:
        incident = edge.node
        print(f"  - {incident.incident_type} ({incident.severity}): {incident.description}")
    
    # Example 5: Generate query string
    print("\n📝 Generated query string:")
    query = Query()
    query.test_telnet_connection(host='montecarlodata.com', port=443)
    print(query)
    
    # Example 6: Mutation example
    print("\n⚙️ Generating collector template...")
    try:
        mutation = Mutation()
        result = mutation.generate_collector_template()
        template_url = result.dc().template_launch_url()
        print(f"Collector template URL: {template_url}")
    except MockGqlError as e:
        print(f"Demo error: {e}")
    
    print("\n✅ All demo API examples completed successfully!")
    print("\n💡 To use real pycarlo:")
    print("   1. Install: pip install pycarlo==0.10.51")
    print("   2. Configure: montecarlo configure")
    print("   3. Run: python pycarlo_api_demo.py --production")
    
    return True


if __name__ == "__main__":
    print("🚀 Pycarlo API Demo")
    print("==================")
    
    # Check if user wants production mode
    if "--production" in sys.argv or os.getenv("MONTE_CARLO_API_ID"):
        success = demo_with_credentials()
    else:
        success = demo_without_credentials()
    
    if success:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n❌ Demo failed - check credentials and configuration")
        sys.exit(1)
