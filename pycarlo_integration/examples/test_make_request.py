#!/usr/bin/env python3
"""
Test the make_request functionality in our Monte Carlo integration.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from pycarlo_integration.monte_carlo_client import MonteCarloIntegration

def test_make_request_functionality():
    """Test that our integration supports make_request with different scopes."""
    
    print("🧪 Testing make_request functionality")
    print("=" * 40)
    
    # Test cases for different scopes and endpoints
    test_cases = [
        {
            'scope': 'AirflowCallbacks',
            'path': '/airflow/callbacks',
            'method': 'POST',
            'body': {
                'dag_id': 'test_dag',
                'task_id': 'test_task',
                'status': 'success'
            }
        },
        {
            'scope': 'DataCollectors',
            'path': '/collectors/health',
            'method': 'GET'
        },
        {
            'scope': 'MetricIngestion',
            'path': '/custom-metrics',
            'method': 'POST',
            'body': {
                'metrics': [
                    {
                        'table_id': 'test.table',
                        'metric_type': 'completeness',
                        'value': 98.5
                    }
                ]
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['scope']} scope")
        
        # Create integration with specific scope
        integration = MonteCarloIntegration(demo_mode=True, scope=test_case['scope'])
        
        # Test if client has make_request method
        if hasattr(integration.client, 'make_request'):
            print(f"✅ make_request method available")
            
            # Test the make_request call
            try:
                response = integration.client.make_request(
                    path=test_case['path'],
                    method=test_case['method'],
                    body=test_case.get('body'),
                    timeout_in_seconds=10
                )
                
                print(f"✅ Request successful: {test_case['method']} {test_case['path']}")
                print(f"📄 Response: {response}")
                
            except Exception as e:
                print(f"❌ Request failed: {e}")
        else:
            print(f"❌ make_request method not available")
    
    print(f"\n🎉 make_request testing complete!")

if __name__ == "__main__":
    test_make_request_functionality()
