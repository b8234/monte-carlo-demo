#!/usr/bin/env python3
"""
Pycarlo Advanced Integration Examples
Shows specialized scopes and make_request patterns for different use cases.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

def demo_session_scopes():
    """
    Demonstrate different Monte Carlo session scopes and their use cases.
    """
    print("🔧 Monte Carlo Session Scopes & Direct API Examples")
    print("=" * 60)
    
    # Available scopes in Monte Carlo
    scopes = {
        'AirflowCallbacks': {
            'description': 'For Airflow integration callbacks',
            'endpoints': ['/airflow/callbacks'],
            'use_cases': ['DAG status updates', 'Task completion notifications']
        },
        'DataCollectors': {
            'description': 'For data collector management',
            'endpoints': ['/collectors', '/collectors/health'],
            'use_cases': ['Collector deployment', 'Health monitoring']
        },
        'MetricIngestion': {
            'description': 'For custom metric ingestion',
            'endpoints': ['/metrics', '/custom-metrics'],
            'use_cases': ['Custom quality metrics', 'Business KPIs']
        },
        'IncidentManagement': {
            'description': 'For incident workflow automation',
            'endpoints': ['/incidents', '/notifications'],
            'use_cases': ['Auto-resolution', 'Custom alerting']
        }
    }
    
    print("📋 Available Monte Carlo Scopes:")
    for scope_name, scope_info in scopes.items():
        print(f"\n🎯 {scope_name}")
        print(f"   Description: {scope_info['description']}")
        print(f"   Endpoints: {', '.join(scope_info['endpoints'])}")
        print(f"   Use Cases: {', '.join(scope_info['use_cases'])}")
    
    return scopes

def demo_production_session_patterns():
    """
    Show the proper production patterns using Session with scopes.
    """
    print("\n🚀 Production Session Patterns")
    print("=" * 40)
    
    try:
        # This would be the real implementation
        from pycarlo.core import Client, Session
        
        api_id = os.getenv("MONTE_CARLO_API_ID", "demo_id")
        api_token = os.getenv("MONTE_CARLO_API_TOKEN", "demo_token")
        
        examples = [
            {
                'name': 'Basic Session',
                'code': f'''
# Basic Session without scope
session = Session(mcd_id='{api_id}', mcd_token='{api_token}')
client = Client(session=session)
''',
                'use_case': 'General GraphQL queries and mutations'
            },
            {
                'name': 'Airflow Callbacks',
                'code': f'''
# Session with AirflowCallbacks scope
session = Session(
    mcd_id='{api_id}', 
    mcd_token='{api_token}', 
    scope='AirflowCallbacks'
)
client = Client(session=session)

# Direct API call for Airflow callback
response = client.make_request(
    path='/airflow/callbacks',
    method='POST',
    body={{
        'dag_id': 'data_quality_check',
        'task_id': 'validate_tables',
        'status': 'success',
        'timestamp': '2025-07-30T14:30:00Z'
    }},
    timeout_in_seconds=20
)
''',
                'use_case': 'Notify Monte Carlo about Airflow DAG/task status'
            },
            {
                'name': 'Data Collector Management',
                'code': f'''
# Session with DataCollectors scope
session = Session(
    mcd_id='{api_id}', 
    mcd_token='{api_token}', 
    scope='DataCollectors'
)
client = Client(session=session)

# Check collector health
health_response = client.make_request(
    path='/collectors/health',
    method='GET',
    timeout_in_seconds=15
)

# Deploy new collector
deploy_response = client.make_request(
    path='/collectors',
    method='POST',
    body={{
        'collector_type': 'dbt',
        'config': {{
            'project_path': '/opt/dbt/project',
            'profiles_dir': '/opt/dbt/profiles'
        }}
    }}
)
''',
                'use_case': 'Manage and monitor data collectors'
            },
            {
                'name': 'Custom Metrics Ingestion',
                'code': f'''
# Session with MetricIngestion scope
session = Session(
    mcd_id='{api_id}', 
    mcd_token='{api_token}', 
    scope='MetricIngestion'
)
client = Client(session=session)

# Send custom quality metrics
metrics_response = client.make_request(
    path='/custom-metrics',
    method='POST',
    body={{
        'metrics': [
            {{
                'table_id': 'warehouse.analytics.user_events',
                'metric_type': 'custom_completeness',
                'value': 98.5,
                'timestamp': '2025-07-30T14:30:00Z'
            }},
            {{
                'table_id': 'warehouse.analytics.user_events',
                'metric_type': 'business_kpi',
                'value': 1250000,  # Daily active users
                'timestamp': '2025-07-30T14:30:00Z'
            }}
        ]
    }},
    timeout_in_seconds=30
)
''',
                'use_case': 'Send custom business and quality metrics'
            }
        ]
        
        for example in examples:
            print(f"\n📝 {example['name']}")
            print(f"Use Case: {example['use_case']}")
            print("Code:")
            print(example['code'])
        
        return True
        
    except ImportError:
        print("❌ pycarlo not installed - showing mock examples")
        return False

def demo_mock_session_patterns():
    """
    Demo the session patterns without requiring pycarlo installation.
    """
    print("\n🎭 Mock Session Patterns (Demo Mode)")
    print("=" * 45)
    
    class MockSession:
        def __init__(self, mcd_id: str, mcd_token: str, scope: Optional[str] = None):
            self.mcd_id = mcd_id
            self.mcd_token = mcd_token
            self.scope = scope
            print(f"📋 Created Session with scope: {scope or 'default'}")
    
    class MockClient:
        def __init__(self, session: MockSession):
            self.session = session
            print(f"🔗 Client initialized with {session.scope or 'default'} scope")
        
        def make_request(self, path: str, method: str = 'GET', 
                        body: Optional[Dict] = None, timeout_in_seconds: int = 30) -> Dict[str, Any]:
            print(f"📡 {method} {path}")
            if body:
                print(f"📄 Body: {json.dumps(body, indent=2)}")
            
            # Mock responses based on path
            if '/airflow/callbacks' in path:
                return {'status': 'received', 'callback_id': 'cb_12345'}
            elif '/collectors/health' in path:
                return {'status': 'healthy', 'collectors': ['dbt-prod', 'snowflake-prod']}
            elif '/collectors' in path and method == 'POST':
                return {'status': 'deployed', 'collector_id': 'col_67890'}
            elif '/custom-metrics' in path:
                return {'status': 'ingested', 'metrics_count': len(body.get('metrics', []))}
            else:
                return {'status': 'success', 'data': 'mock_response'}
    
    # Demo examples
    examples = [
        {
            'name': 'Airflow Integration',
            'scope': 'AirflowCallbacks',
            'demo': lambda client: client.make_request(
                path='/airflow/callbacks',
                method='POST',
                body={
                    'dag_id': 'data_quality_pipeline',
                    'task_id': 'validate_customer_data',
                    'status': 'success',
                    'execution_date': '2025-07-30T14:30:00Z'
                }
            )
        },
        {
            'name': 'Collector Health Check',
            'scope': 'DataCollectors',
            'demo': lambda client: client.make_request(
                path='/collectors/health',
                method='GET'
            )
        },
        {
            'name': 'Custom Metrics',
            'scope': 'MetricIngestion',
            'demo': lambda client: client.make_request(
                path='/custom-metrics',
                method='POST',
                body={
                    'metrics': [
                        {
                            'table_id': 'analytics.user_behavior',
                            'metric_type': 'data_freshness',
                            'value': 0.5,  # 30 minutes
                            'unit': 'hours'
                        }
                    ]
                }
            )
        }
    ]
    
    for example in examples:
        print(f"\n🎯 {example['name']}")
        session = MockSession('demo_id', 'demo_token', example['scope'])
        client = MockClient(session)
        response = example['demo'](client)
        print(f"✅ Response: {response}")
    
    return True

def demo_integration_with_scopes():
    """
    Show how to use our Monte Carlo integration with different scopes.
    """
    print("\n🔧 Integration with Scopes")
    print("=" * 30)
    
    try:
        # Import our integration
        from pycarlo_integration.monte_carlo_client import MonteCarloIntegration
        
        # Different scope examples
        integrations = [
            {'scope': None, 'description': 'General purpose integration'},
            {'scope': 'AirflowCallbacks', 'description': 'Airflow workflow integration'},
            {'scope': 'DataCollectors', 'description': 'Collector management'},
            {'scope': 'MetricIngestion', 'description': 'Custom metrics pipeline'}
        ]
        
        for config in integrations:
            print(f"\n📌 {config['description']}")
            # In demo mode, scope doesn't affect functionality but shows the pattern
            integration = MonteCarloIntegration(demo_mode=True, scope=config['scope'])
            status = integration.get_integration_status()
            print(f"   Mode: {status['mode']}")
            print(f"   Scope: {config['scope'] or 'default'}")
            print(f"   Connection: {status['connection']['status']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Integration import failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Monte Carlo Advanced Integration Demo")
    print("========================================")
    
    # 1. Show available scopes
    scopes = demo_session_scopes()
    
    # 2. Try production patterns (will fall back to mock if pycarlo not installed)
    if not demo_production_session_patterns():
        demo_mock_session_patterns()
    
    # 3. Show integration usage
    demo_integration_with_scopes()
    
    print("\n" + "=" * 60)
    print("🎉 Advanced Integration Demo Complete!")
    print("\n💡 Key Takeaways:")
    print("   • Use Session with scopes for specialized integrations")
    print("   • make_request() for direct API calls beyond GraphQL")
    print("   • Different scopes enable different endpoint access")
    print("   • Our integration supports both patterns seamlessly")
    print("\n🚀 Production Setup:")
    print("   1. pip install pycarlo==0.10.51")
    print("   2. montecarlo configure")
    print("   3. Set appropriate scope for your use case")
    print("   4. Use make_request() for specialized endpoints")
