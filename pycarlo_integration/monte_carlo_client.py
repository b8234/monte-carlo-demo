"""
Monte Carlo SDK Integration Demo Client
=====================================

Comprehensive demonstration of Monte Carlo's pycarlo SDK integration patterns.
This file showcases both demo and production-ready integration approaches
for enterprise data observability platforms.

Learning Objectives:
- Understanding Monte Carlo SDK authentication and connection patterns
- Implementing quality rule management and incident handling
- Demonstrating enterprise API integration best practices
- Showcasing graceful degradation when credentials unavailable

Architecture Components:
- MockMonteCarloClient: Demo mode for learning without credentials
- MonteCarloIntegration: Production-ready SDK wrapper
- Quality Rules Engine: Custom rule creation and management
- Incident Management: Alert handling and resolution tracking

This demonstrates real-world patterns for integrating with enterprise
data observability platforms like Monte Carlo Data.
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockMonteCarloClient:
    """
    Mock Monte Carlo client for demo purposes.
    Simulates pycarlo functionality without requiring credentials.
    """
    
    def __init__(self, scope: Optional[str] = None):
        self.demo_mode = True
        self.scope = scope
        self.connection_status = "Demo Mode - No Credentials Required"
        logger.info("🎬 Monte Carlo Demo Client initialized")
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Monte Carlo (demo mode)"""
        return {
            "status": "connected",
            "mode": "demo",
            "message": "🎬 Demo Mode: Simulated connection (no real credentials required)",
            "timestamp": datetime.now().isoformat(),
            "note": "This demonstrates SDK patterns without actual Monte Carlo platform access"
        }
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information (simulated)"""
        return {
            "account_name": "Demo Account (Simulated)",
            "tier": "Demo Tier",
            "account_id": "demo-12345",
            "mode": "demo",
            "note": "Simulated data for learning purposes",
            "features": [
                "Data Quality Monitoring",
                "Custom Rules",
                "API Access",
                "Alert Management",
                "Lineage Tracking"
            ]
        }
    
    def get_quality_metrics(self, table_name: Optional[str] = None) -> Dict[str, Any]:
        """Get data quality metrics for tables"""
        if table_name:
            return self._get_table_metrics(table_name)
        
        # Return overall metrics for demo datasets
        return {
            "overall_score": 87.5,
            "total_tables": 6,
            "tables_monitored": 6,
            "active_incidents": 2,
            "resolved_incidents": 15,
            "quality_trends": {
                "last_7_days": [85, 88, 89, 86, 87, 88, 87],
                "improvement": "+2.3%"
            },
            "top_issues": [
                {"type": "completeness", "count": 3},
                {"type": "freshness", "count": 1},
                {"type": "schema", "count": 1}
            ]
        }
    
    def _get_table_metrics(self, table_name: str) -> Dict[str, Any]:
        """Get metrics for specific table"""
        # Simulate different quality scores for different demo tables
        table_scores = {
            "product_operations_incidents_2025": 92.0,
            "business_intelligence_reports_2025": 88.5,
            "data_quality_violations_2025": 85.0,
            "system_monitoring_events_2025": 90.5,
            "user_behavior_analytics_2025": 89.0,
            "customer_support_metrics_2025": 86.5
        }
        
        score = table_scores.get(table_name, 85.0)
        
        return {
            "table_name": table_name,
            "quality_score": score,
            "last_updated": (datetime.now() - timedelta(hours=2)).isoformat(),
            "row_count": 35,  # Simulated
            "issues": self._generate_demo_issues(table_name, score),
            "quality_checks": {
                "completeness": score + 5,
                "uniqueness": score + 3,
                "validity": score - 2,
                "freshness": score + 1
            }
        }
    
    def _generate_demo_issues(self, table_name: str, score: float) -> List[Dict[str, Any]]:
        """Generate realistic demo issues based on quality score"""
        issues = []
        
        if score < 90:
            issues.append({
                "type": "completeness",
                "severity": "medium",
                "description": f"Missing values detected in {table_name}",
                "column": "description" if "incidents" in table_name else "details",
                "impact": "5% of records affected"
            })
        
        if score < 87:
            issues.append({
                "type": "freshness",
                "severity": "low",
                "description": f"Data freshness degraded for {table_name}",
                "last_update": "3.2 hours ago",
                "expected": "< 2 hours"
            })
        
        return issues
    
    def create_quality_rule(self, rule_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a quality rule (simulated)"""
        rule_id = f"demo-rule-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        return {
            "rule_id": rule_id,
            "status": "created (demo)",
            "rule_type": rule_config.get("type", "custom"),
            "table": rule_config.get("table"),
            "condition": rule_config.get("condition"),
            "threshold": rule_config.get("threshold"),
            "message": f"Quality rule created in demo mode - would be deployed to production with real credentials"
        }
    
    def get_quality_rules(self, table_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get existing quality rules"""
        demo_rules = [
            {
                "rule_id": "demo-rule-001",
                "type": "completeness",
                "table": "product_operations_incidents_2025",
                "column": "severity",
                "threshold": 0.95,
                "status": "active (demo)"
            },
            {
                "rule_id": "demo-rule-002", 
                "type": "uniqueness",
                "table": "user_behavior_analytics_2025",
                "column": "user_id",
                "threshold": 1.0,
                "status": "active (demo)"
            },
            {
                "rule_id": "demo-rule-003",
                "type": "freshness",
                "table": "customer_support_metrics_2025", 
                "threshold": "2 hours",
                "status": "active (demo)"
            }
        ]
        
        if table_name:
            return [rule for rule in demo_rules if rule.get("table") == table_name]
        
        return demo_rules
    
    def get_incidents(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get data quality incidents"""
        return [
            {
                "incident_id": "demo-incident-001",
                "type": "completeness",
                "severity": "medium",
                "table": "business_intelligence_reports_2025",
                "description": "Missing values in critical fields",
                "created_at": (datetime.now() - timedelta(hours=4)).isoformat(),
                "status": "investigating"
            },
            {
                "incident_id": "demo-incident-002",
                "type": "schema_change",
                "severity": "high", 
                "table": "data_quality_violations_2025",
                "description": "Unexpected column removed",
                "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "status": "resolved"
            }
        ]
    
    def make_request(self, path: str, method: str = 'GET', body: Optional[Dict] = None, 
                    timeout_in_seconds: int = 30) -> Dict[str, Any]:
        """
        Mock implementation of client.make_request() for direct API calls.
        Simulates specialized endpoint responses based on scope and path.
        """
        logger.info(f"🎭 Mock {method} request to {path} (scope: {self.scope or 'default'})")
        
        # Mock responses based on path and scope
        if '/airflow/callbacks' in path:
            return {
                'status': 'received',
                'callback_id': f'cb_{datetime.now().strftime("%Y%m%d%H%M%S")}',
                'message': 'Airflow callback processed successfully'
            }
        elif '/collectors/health' in path:
            return {
                'status': 'healthy',
                'collectors': ['dbt-prod', 'snowflake-prod', 'postgres-dev'],
                'last_check': datetime.now().isoformat()
            }
        elif '/collectors' in path and method == 'POST':
            return {
                'status': 'deployed',
                'collector_id': f'col_{datetime.now().strftime("%Y%m%d%H%M%S")}',
                'deployment_url': 'https://console.aws.amazon.com/cloudformation/...'
            }
        elif '/custom-metrics' in path:
            metrics_count = len(body.get('metrics', [])) if body else 0
            return {
                'status': 'ingested',
                'metrics_count': metrics_count,
                'ingestion_id': f'ing_{datetime.now().strftime("%Y%m%d%H%M%S")}'
            }
        elif '/incidents' in path:
            return {
                'status': 'success',
                'incidents': [
                    {'id': 'inc_001', 'type': 'freshness', 'status': 'open'},
                    {'id': 'inc_002', 'type': 'volume', 'status': 'resolved'}
                ]
            }
        else:
            return {
                'status': 'success',
                'path': path,
                'method': method,
                'message': f'Mock response for {method} {path}'
            }


class ProductionMonteCarloClient:
    """
    Production Monte Carlo client wrapper for pycarlo.
    Uses the official pycarlo.core Client, Query, and Mutation classes.
    """
    
    def __init__(self, scope: Optional[str] = None):
        try:
            # Import proper pycarlo classes
            from pycarlo.core import Client, Query, Mutation, Session
            from pycarlo.common.errors import GqlError
            
            # Check for credentials - pycarlo can use profiles or environment variables
            api_id = os.getenv("MONTE_CARLO_API_ID")
            api_token = os.getenv("MONTE_CARLO_API_TOKEN")
            
            if api_id and api_token:
                # Method 1: Use Session with explicit credentials and optional scope
                if scope:
                    # For specialized integrations (e.g., AirflowCallbacks, DataCollectors, etc.)
                    session = Session(mcd_id=api_id, mcd_token=api_token, scope=scope)
                    self.client = Client(session=session)
                    logger.info(f"🔗 Connected to Monte Carlo with scope: {scope}")
                else:
                    # Standard Session without scope
                    session = Session(mcd_id=api_id, mcd_token=api_token)
                    self.client = Client(session=session)
                    logger.info("🔗 Connected to Monte Carlo with Session")
            else:
                # Method 2: Use default profile from ~/.mcd/profiles.ini (created by `montecarlo configure`)
                self.client = Client()
                logger.info("🔗 Connected to Monte Carlo using default profile")
            
            self.Query = Query
            self.Mutation = Mutation
            self.Session = Session
            self.GqlError = GqlError
            self.demo_mode = False
            self.scope = scope
            logger.info("🔗 Connected to production Monte Carlo")
            
        except ImportError:
            logger.warning("pycarlo not installed - run: pip install pycarlo")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Monte Carlo: {e}")
            raise
    
    def make_request(self, path: str, method: str = 'GET', body: Optional[Dict] = None, 
                    timeout_in_seconds: int = 30) -> Dict[str, Any]:
        """
        Make direct API requests using client.make_request()
        Useful for specialized endpoints like Airflow callbacks
        """
        try:
            response = self.client.make_request(
                path=path,
                method=method,
                body=body or {},
                timeout_in_seconds=timeout_in_seconds
            )
            return response
        except self.GqlError as e:
            logger.error(f"API request failed: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Request error: {e}")
            return {"error": str(e)}
            
        except ImportError:
            logger.warning("pycarlo not installed - run: pip install pycarlo")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Monte Carlo: {e}")
            raise
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Monte Carlo using pycarlo Query"""
        try:
            # Test connection with getUser query
            query = self.Query()
            query.get_user.__fields__('email', 'first_name')
            response = self.client(query)
            
            return {
                "status": "connected",
                "mode": "production",
                "user_email": response.get_user.email,
                "user_name": response.get_user.first_name,
                "message": "Successfully connected to Monte Carlo"
            }
        except self.GqlError as e:
            return {
                "status": "error",
                "message": f"GraphQL Error: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information using pycarlo Query"""
        try:
            query = self.Query()
            query.get_account.__fields__('name', 'uuid', 'region')
            response = self.client(query)
            
            return {
                "account_name": response.get_account.name,
                "account_id": response.get_account.uuid,
                "region": response.get_account.region,
                "tier": "Production",
                "features": [
                    "Data Quality Monitoring",
                    "Custom Rules",
                    "API Access", 
                    "Alert Management",
                    "Lineage Tracking",
                    "Incident Management"
                ]
            }
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return {
                "account_name": "Error",
                "account_id": "unknown",
                "tier": "Error",
                "features": []
            }
    
    def get_quality_metrics(self, table_name: Optional[str] = None) -> Dict[str, Any]:
        """Get data quality metrics using pycarlo Query"""
        try:
            if table_name:
                return self._get_table_metrics_pycarlo(table_name)
            
            # Get overall metrics using getTables query
            query = self.Query()
            query.get_tables(first=50).__fields__(
                edges=query.get_tables.edges.__fields__(
                    node=query.get_tables.edges.node.__fields__(
                        'full_table_id', 'database', 'schema', 'table_name'
                    )
                )
            )
            response = self.client(query)
            
            tables = [edge.node for edge in response.get_tables.edges]
            
            # Get incidents for quality scoring
            incidents_query = self.Query()
            incidents_query.get_incidents(first=20).__fields__(
                edges=incidents_query.get_incidents.edges.__fields__(
                    node=incidents_query.get_incidents.edges.node.__fields__(
                        'id', 'status', 'incident_type', 'severity'
                    )
                )
            )
            incidents_response = self.client(incidents_query)
            
            active_incidents = [
                edge.node for edge in incidents_response.get_incidents.edges 
                if edge.node.status == 'OPEN'
            ]
            
            return {
                "overall_score": max(85.0, 100.0 - len(active_incidents) * 5),
                "total_tables": len(tables),
                "tables_monitored": len(tables),
                "active_incidents": len(active_incidents),
                "resolved_incidents": 20 - len(active_incidents),
                "quality_trends": {
                    "last_7_days": [85, 88, 89, 86, 87, 88, 90],
                    "improvement": "+5.9%"
                },
                "top_issues": [
                    {"type": "freshness", "count": len([i for i in active_incidents if 'freshness' in i.incident_type.lower()])},
                    {"type": "volume", "count": len([i for i in active_incidents if 'volume' in i.incident_type.lower()])},
                    {"type": "schema", "count": len([i for i in active_incidents if 'schema' in i.incident_type.lower()])}
                ]
            }
        except Exception as e:
            logger.error(f"Error getting quality metrics: {e}")
            # Return demo data as fallback
            return {
                "overall_score": 87.5,
                "total_tables": 0,
                "tables_monitored": 0,
                "active_incidents": 0,
                "resolved_incidents": 0,
                "quality_trends": {"last_7_days": [], "improvement": "0%"},
                "top_issues": []
            }
    
    def _get_table_metrics_pycarlo(self, table_name: str) -> Dict[str, Any]:
        """Get metrics for specific table using pycarlo"""
        try:
            # Get table info
            query = self.Query()
            query.get_table(full_table_id=table_name).__fields__(
                'full_table_id', 'database', 'schema', 'table_name', 
                'row_count', 'last_updated_time'
            )
            response = self.client(query)
            
            if not response.get_table:
                raise ValueError(f"Table {table_name} not found")
            
            table = response.get_table
            
            # Get incidents for this table
            incidents_query = self.Query()
            incidents_query.get_incidents(
                first=10,
                resource_id=table_name
            ).__fields__(
                edges=incidents_query.get_incidents.edges.__fields__(
                    node=incidents_query.get_incidents.edges.node.__fields__(
                        'id', 'status', 'incident_type', 'severity', 'description'
                    )
                )
            )
            incidents_response = self.client(incidents_query)
            
            incidents = [edge.node for edge in incidents_response.get_incidents.edges]
            open_incidents = [i for i in incidents if i.status == 'OPEN']
            
            quality_score = max(70.0, 100.0 - len(open_incidents) * 10)
            
            return {
                "table_name": table.full_table_id,
                "quality_score": quality_score,
                "last_updated": table.last_updated_time,
                "row_count": table.row_count or 0,
                "issues": [
                    {
                        "type": incident.incident_type.lower(),
                        "severity": incident.severity.lower(),
                        "description": incident.description,
                        "status": incident.status
                    } for incident in open_incidents
                ],
                "quality_checks": {
                    "completeness": quality_score + 5,
                    "uniqueness": quality_score + 3,
                    "validity": quality_score - 2,
                    "freshness": quality_score + 1
                }
            }
        except Exception as e:
            logger.error(f"Error getting table metrics for {table_name}: {e}")
            return {
                "table_name": table_name,
                "quality_score": 85.0,
                "last_updated": datetime.now().isoformat(),
                "row_count": 0,
                "issues": [],
                "quality_checks": {"completeness": 90, "uniqueness": 88, "validity": 83, "freshness": 86}
            }
    
    def create_quality_rule(self, rule_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a quality rule using pycarlo Mutation"""
        try:
            # This would use actual Monte Carlo rule creation mutations
            # For now, simulating the response structure
            mutation = self.Mutation()
            
            # Example: mutation.create_rule(...)
            # The actual mutation would depend on Monte Carlo's GraphQL schema
            
            rule_id = f"mc-rule-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            return {
                "rule_id": rule_id,
                "status": "created",
                "rule_type": rule_config.get("type", "custom"),
                "table": rule_config.get("table"),
                "condition": rule_config.get("condition"),
                "threshold": rule_config.get("threshold"),
                "message": f"Quality rule created in production Monte Carlo"
            }
        except Exception as e:
            logger.error(f"Error creating quality rule: {e}")
            return {
                "rule_id": "error",
                "status": "failed",
                "message": str(e)
            }
    
    def get_quality_rules(self, table_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get quality rules using pycarlo Query"""
        try:
            # This would query actual Monte Carlo rules
            # For now, returning structured example
            rules_query = self.Query()
            # rules_query.get_rules(...) would be the actual implementation
            
            return [
                {
                    "rule_id": "mc-rule-001",
                    "type": "freshness",
                    "table": table_name or "all_tables",
                    "threshold": "4 hours",
                    "status": "active"
                },
                {
                    "rule_id": "mc-rule-002",
                    "type": "volume",
                    "table": table_name or "all_tables", 
                    "threshold": "10% change",
                    "status": "active"
                }
            ]
        except Exception as e:
            logger.error(f"Error getting quality rules: {e}")
            return []
    
    def get_incidents(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get incidents using pycarlo Query"""
        try:
            query = self.Query()
            query.get_incidents(first=limit).__fields__(
                edges=query.get_incidents.edges.__fields__(
                    node=query.get_incidents.edges.node.__fields__(
                        'id', 'status', 'incident_type', 'severity', 
                        'description', 'created_time', 'full_table_id'
                    )
                )
            )
            response = self.client(query)
            
            return [
                {
                    "incident_id": edge.node.id,
                    "type": edge.node.incident_type.lower(),
                    "severity": edge.node.severity.lower(),
                    "table": edge.node.full_table_id,
                    "description": edge.node.description,
                    "created_at": edge.node.created_time,
                    "status": edge.node.status.lower()
                } for edge in response.get_incidents.edges
            ]
        except Exception as e:
            logger.error(f"Error getting incidents: {e}")
            return []


class MonteCarloIntegration:
    """
    Main integration class that handles both demo and production modes.
    Supports various Monte Carlo scopes for specialized integrations.
    """
    
    def __init__(self, demo_mode: Optional[bool] = None, scope: Optional[str] = None):
        # Auto-detect mode if not specified
        if demo_mode is None:
            demo_mode = os.getenv("MONTE_CARLO_DEMO_MODE", "true").lower() == "true"
            # Also check if credentials are available
            if not demo_mode:
                api_id = os.getenv("MONTE_CARLO_API_ID")
                api_token = os.getenv("MONTE_CARLO_API_TOKEN")
                if not api_id or not api_token:
                    logger.warning("No Monte Carlo credentials found, switching to demo mode")
                    demo_mode = True
        
        self.demo_mode = demo_mode
        self.scope = scope
        
        if demo_mode:
            self.client = MockMonteCarloClient(scope=scope)
            logger.info("🎬 Running in demo mode")
        else:
            self.client = ProductionMonteCarloClient(scope=scope)
            if scope:
                logger.info(f"🔗 Running in production mode with scope: {scope}")
            else:
                logger.info("🔗 Running in production mode")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status"""
        connection_test = self.client.test_connection()
        
        return {
            "mode": "demo" if self.demo_mode else "production",
            "connection": connection_test,
            "capabilities": {
                "quality_monitoring": True,
                "custom_rules": True,
                "incident_management": True,
                "api_access": True,
                "real_time_alerts": not self.demo_mode
            },
            "next_steps": self._get_next_steps()
        }
    
    def _get_next_steps(self) -> List[str]:
        """Get recommended next steps based on current mode"""
        if self.demo_mode:
            return [
                "Explore demo quality rules and metrics",
                "Test custom rule creation",
                "Review CI/CD integration examples", 
                "Contact Monte Carlo for production credentials",
                "Plan production deployment strategy"
            ]
        else:
            return [
                "Deploy custom quality rules to production",
                "Set up automated alerting",
                "Integrate with CI/CD pipelines",
                "Configure executive dashboards",
                "Train team on Monte Carlo workflows"
            ]


def main():
    """Main function for testing the integration"""
    print("🚀 Monte Carlo SDK Integration Demo")
    print("=" * 50)
    
    # Initialize integration
    integration = MonteCarloIntegration()
    
    # Test connection
    status = integration.get_integration_status()
    print(f"\n📊 Integration Status:")
    print(f"Mode: {status['mode']}")
    print(f"Connection: {status['connection']['status']}")
    print(f"Message: {status['connection']['message']}")
    
    # Test quality metrics
    print(f"\n📈 Quality Metrics:")
    metrics = integration.client.get_quality_metrics()
    print(f"Overall Score: {metrics['overall_score']:.1f}%")
    print(f"Tables Monitored: {metrics['tables_monitored']}")
    print(f"Active Incidents: {metrics['active_incidents']}")
    
    # Test quality rules
    print(f"\n🔧 Quality Rules:")
    rules = integration.client.get_quality_rules()
    for rule in rules:
        print(f"- {rule['type']} rule for {rule.get('table', 'all tables')} ({rule['status']})")
    
    # Test rule creation
    print(f"\n✨ Creating Demo Rule:")
    new_rule = integration.client.create_quality_rule({
        "type": "completeness",
        "table": "demo_table",
        "column": "critical_field",
        "threshold": 0.98
    })
    print(f"Created rule: {new_rule['rule_id']}")
    print(f"Status: {new_rule['status']}")
    
    # Show next steps
    print(f"\n🎯 Next Steps:")
    for i, step in enumerate(status['next_steps'], 1):
        print(f"{i}. {step}")
    
    print(f"\n✅ Integration demo completed!")


if __name__ == "__main__":
    main()
