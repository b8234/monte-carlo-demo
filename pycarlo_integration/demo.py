#!/usr/bin/env python3
"""
Monte Carlo SDK Integration Demo
===============================

Quick demonstration of pycarlo integration capabilities.
This script shows the key features without requiring Monte Carlo credentials.
"""

from monte_carlo_client import MonteCarloIntegration


def main():
    """Run Monte Carlo SDK demo"""
    print("🚀 Monte Carlo SDK Integration Demo")
    print("=" * 50)
    
    # Initialize in demo mode (no credentials required)
    print("🔧 Initializing Monte Carlo client...")
    integration = MonteCarloIntegration(demo_mode=True)
    
    # 1. Test connection
    print("\n📡 Testing connection...")
    status = integration.get_integration_status()
    print(f"   Mode: {status['mode']}")
    print(f"   Status: {status['connection']['status']}")
    print(f"   Message: {status['connection']['message']}")
    
    # 2. Get quality metrics
    print("\n📊 Fetching quality metrics...")
    metrics = integration.client.get_quality_metrics()
    print(f"   Overall Score: {metrics['overall_score']}%")
    print(f"   Tables Monitored: {metrics['tables_monitored']}")
    print(f"   Active Incidents: {metrics['active_incidents']}")
    print(f"   Quality Trend: {metrics['quality_trends']['improvement']}")
    
    # 3. Show recent incidents
    print("\n🚨 Recent incidents...")
    incidents = integration.client.get_incidents(limit=3)
    for incident in incidents:
        severity = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(incident['severity'], "⚪")
        print(f"   {severity} {incident['type'].title()} - {incident['table']} ({incident['status']})")
    
    # 4. Create a quality rule
    print("\n⚙️ Creating quality rule...")
    rule = integration.client.create_quality_rule({
        "type": "completeness",
        "table": "demo_analytics_table",
        "threshold": 0.95
    })
    print(f"   Rule ID: {rule['rule_id']}")
    print(f"   Status: {rule['status']}")
    
    # 5. Test direct API call (Session + make_request pattern)
    print("\n🔌 Testing direct API call...")
    api_response = integration.client.make_request("/test/endpoint", "GET")
    print(f"   Response: {api_response['status']}")
    print(f"   Message: {api_response['message']}")
    
    # 6. Show next steps
    print("\n🎯 Next Steps:")
    for i, step in enumerate(status['next_steps'][:3], 1):
        print(f"   {i}. {step}")
    
    print("\n✅ Demo completed successfully!")
    print("\n💡 Key Takeaways:")
    print("   • Monte Carlo SDK integration works in demo mode")
    print("   • All major pycarlo patterns are demonstrated")
    print("   • Ready for production deployment with real credentials")
    print("   • Seamlessly integrates with existing dashboard")


if __name__ == "__main__":
    main()
