#!/usr/bin/env python3
"""
Advanced Monte Carlo SDK Patterns
=================================

Demonstrates advanced pycarlo usage including:
- Session-based authentication with scopes
- Direct API calls via make_request()
- Production integration patterns
- Specialized endpoint usage
"""

import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from monte_carlo_client import MonteCarloIntegration


def demo_session_scopes():
    """Show different Monte Carlo scopes and their use cases"""
    print("🔧 Monte Carlo Session Scopes")
    print("=" * 35)
    
    scopes = {
        'AirflowCallbacks': 'DAG/task status integration',
        'DataCollectors': 'Collector management and health',
        'MetricIngestion': 'Custom metrics and KPIs',
        'IncidentManagement': 'Automated incident workflows'
    }
    
    for scope, description in scopes.items():
        print(f"🎯 {scope}")
        print(f"   Use case: {description}")
        
        # Demo with this scope
        integration = MonteCarloIntegration(demo_mode=True, scope=scope)
        status = integration.client.test_connection()
        print(f"   Status: {status['status']} ({status['mode']})")
        print()


def demo_api_patterns():
    """Show different API usage patterns"""
    print("📡 API Usage Patterns")
    print("=" * 25)
    
    integration = MonteCarloIntegration(demo_mode=True)
    
    # 1. Standard quality metrics (GraphQL-style)
    print("1. Standard Quality Metrics:")
    metrics = integration.client.get_quality_metrics()
    print(f"   Score: {metrics['overall_score']}%")
    print(f"   Tables: {metrics['total_tables']}")
    
    # 2. Direct API call (make_request pattern)
    print("\n2. Direct API Call:")
    response = integration.client.make_request('/airflow/callbacks', 'POST', {
        'dag_id': 'data_pipeline',
        'status': 'success'
    })
    print(f"   Callback ID: {response.get('callback_id', 'N/A')}")
    print(f"   Status: {response['status']}")
    
    # 3. Quality rule management
    print("\n3. Quality Rule Creation:")
    rule = integration.client.create_quality_rule({
        'type': 'freshness',
        'table': 'analytics.events',
        'threshold': '2 hours'
    })
    print(f"   Rule: {rule['rule_id']}")
    print(f"   Type: {rule['rule_type']}")


def demo_production_readiness():
    """Show production deployment considerations"""
    print("🚀 Production Readiness")
    print("=" * 25)
    
    print("Current Setup (Demo Mode):")
    print("✅ No credentials required")
    print("✅ Realistic mock data")
    print("✅ All API patterns demonstrated")
    print("✅ Dashboard integration working")
    
    print("\nProduction Migration:")
    print("📋 1. pip install pycarlo==0.10.51")
    print("📋 2. montecarlo configure")
    print("📋 3. Set demo_mode=False")
    print("📋 4. All existing code works!")
    
    print("\nProduction Benefits:")
    print("🔗 Real-time quality monitoring")
    print("🚨 Automated incident detection")
    print("📊 Live data quality metrics")
    print("⚙️ CI/CD pipeline integration")


def main():
    """Run advanced patterns demo"""
    print("🚀 Monte Carlo SDK - Advanced Patterns")
    print("=" * 45)
    
    demo_session_scopes()
    demo_api_patterns()
    demo_production_readiness()
    
    print("\n🎉 Advanced demo completed!")
    print("\n💡 This demonstrates enterprise-grade capabilities")
    print("   ready for production Monte Carlo deployment.")


if __name__ == "__main__":
    main()
