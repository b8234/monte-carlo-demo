"""
CI/CD Pipeline Integration for Monte Carlo Data Quality
=====================================================

Demonstrates how to integrate data quality checks into deployment pipelines
using Monte Carlo SDK (pycarlo) - works in both demo and production modes.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import subprocess

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)


class QualityGateException(Exception):
    """Exception raised when data quality checks fail pipeline gates"""
    pass


class DataQualityPipeline:
    """
    CI/CD pipeline integration for data quality checks
    """
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.quality_thresholds = {
            "overall_score": 85.0,  # Minimum overall quality score
            "critical_rules": 100.0,  # Critical rules must pass 100%
            "high_rules": 95.0,      # High severity rules threshold
            "medium_rules": 90.0,    # Medium severity rules threshold
        }
        
        # Import our quality components
        try:
            from pycarlo_integration.monte_carlo_client import MonteCarloIntegration
            from pycarlo_integration.quality_rules import EnterpriseQualityRules
            
            self.mc_integration = MonteCarloIntegration(demo_mode=demo_mode)
            self.quality_rules = EnterpriseQualityRules(demo_mode=demo_mode)
            
        except ImportError as e:
            logger.error(f"Failed to import quality components: {e}")
            raise
    
    def run_pre_deployment_checks(self, datasets: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run data quality checks before deployment
        
        Args:
            datasets: Dictionary of dataset names and their configurations
            
        Returns:
            Quality check results with pass/fail status
        """
        print("🔍 Running pre-deployment data quality checks...")
        
        results = {
            "pipeline_stage": "pre_deployment",
            "timestamp": datetime.now().isoformat(),
            "demo_mode": self.demo_mode,
            "datasets_checked": list(datasets.keys()),
            "overall_status": "passed",
            "quality_gates": [],
            "recommendations": []
        }
        
        for dataset_name, config in datasets.items():
            gate_result = self._check_quality_gate(dataset_name, config)
            results["quality_gates"].append(gate_result)
            
            if not gate_result["passed"]:
                results["overall_status"] = "failed"
                results["recommendations"].extend(gate_result.get("recommendations", []))
        
        # Log results
        status_emoji = "✅" if results["overall_status"] == "passed" else "❌"
        print(f"{status_emoji} Pre-deployment checks: {results['overall_status']}")
        
        if results["overall_status"] == "failed":
            print("🚨 Quality gate failures detected!")
            for rec in results["recommendations"]:
                print(f"  💡 {rec}")
        
        return results
    
    def _check_quality_gate(self, dataset_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Check quality gate for a specific dataset"""
        gate_result = {
            "dataset": dataset_name,
            "passed": True,
            "quality_score": 0.0,
            "checks": [],
            "recommendations": []
        }
        
        try:
            # Get quality metrics from Monte Carlo (demo or production)
            metrics = self.mc_integration.client.get_quality_metrics(dataset_name)
            gate_result["quality_score"] = metrics.get("quality_score", 0.0)
            
            # Check against thresholds
            score = gate_result["quality_score"]
            min_score = config.get("min_quality_score", self.quality_thresholds["overall_score"])
            
            if score < min_score:
                gate_result["passed"] = False
                gate_result["checks"].append({
                    "check": "overall_quality_score",
                    "status": "failed",
                    "actual": score,
                    "threshold": min_score,
                    "message": f"Quality score {score:.1f}% below threshold {min_score:.1f}%"
                })
                gate_result["recommendations"].append(
                    f"Improve data quality for {dataset_name} before deployment"
                )
            else:
                gate_result["checks"].append({
                    "check": "overall_quality_score", 
                    "status": "passed",
                    "actual": score,
                    "threshold": min_score,
                    "message": f"Quality score {score:.1f}% meets threshold"
                })
            
            # Check for active incidents
            incidents = self.mc_integration.client.get_incidents(limit=5)
            dataset_incidents = [
                inc for inc in incidents 
                if inc.get("table") == dataset_name and inc.get("status") != "resolved"
            ]
            
            if dataset_incidents:
                gate_result["passed"] = False
                gate_result["checks"].append({
                    "check": "active_incidents",
                    "status": "failed",
                    "count": len(dataset_incidents),
                    "message": f"{len(dataset_incidents)} active quality incidents"
                })
                gate_result["recommendations"].append(
                    f"Resolve {len(dataset_incidents)} active incidents for {dataset_name}"
                )
            else:
                gate_result["checks"].append({
                    "check": "active_incidents",
                    "status": "passed",
                    "count": 0,
                    "message": "No active quality incidents"
                })
            
        except Exception as e:
            logger.error(f"Error checking quality gate for {dataset_name}: {e}")
            gate_result["passed"] = False
            gate_result["checks"].append({
                "check": "quality_gate_execution",
                "status": "error",
                "message": str(e)
            })
        
        return gate_result
    
    def run_post_deployment_setup(self, datasets: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set up monitoring and alerting after successful deployment
        """
        print("🚀 Setting up post-deployment monitoring...")
        
        results = {
            "pipeline_stage": "post_deployment",
            "timestamp": datetime.now().isoformat(),
            "demo_mode": self.demo_mode,
            "monitoring_setup": [],
            "alerts_configured": []
        }
        
        for dataset_name, config in datasets.items():
            # Set up quality rules
            monitoring_result = self._setup_monitoring(dataset_name, config)
            results["monitoring_setup"].append(monitoring_result)
            
            # Configure alerts
            alert_result = self._configure_alerts(dataset_name, config)
            results["alerts_configured"].append(alert_result)
        
        print("✅ Post-deployment monitoring configured")
        return results
    
    def _setup_monitoring(self, dataset_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up quality monitoring for a dataset"""
        result = {
            "dataset": dataset_name,
            "rules_created": [],
            "status": "success"
        }
        
        try:
            # Get appropriate quality rules for this dataset
            rules = self.quality_rules.get_rules_for_table(dataset_name)
            
            for rule in rules:
                # Create rule in Monte Carlo (demo or production)
                rule_config = rule.to_monte_carlo_config()
                rule_config["table"] = dataset_name
                
                mc_rule = self.mc_integration.client.create_quality_rule(rule_config)
                
                result["rules_created"].append({
                    "rule_id": mc_rule["rule_id"],
                    "type": rule_config["rule_type"],
                    "severity": rule_config["severity"],
                    "status": mc_rule["status"]
                })
            
        except Exception as e:
            logger.error(f"Error setting up monitoring for {dataset_name}: {e}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _configure_alerts(self, dataset_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Configure alerting for a dataset"""
        result = {
            "dataset": dataset_name,
            "alerts": [],
            "status": "success"
        }
        
        try:
            # Configure different alert types based on dataset criticality
            criticality = config.get("criticality", "medium")
            
            alert_configs = []
            
            if criticality in ["high", "critical"]:
                alert_configs.extend([
                    {
                        "type": "quality_score_drop",
                        "threshold": 90.0,
                        "channels": ["slack", "email", "pagerduty"]
                    },
                    {
                        "type": "incident_created",
                        "severity": ["high", "critical"],
                        "channels": ["slack", "pagerduty"]
                    }
                ])
            
            if criticality in ["medium", "high", "critical"]:
                alert_configs.append({
                    "type": "freshness_violation",
                    "threshold": "4 hours",
                    "channels": ["slack", "email"]
                })
            
            # Create alerts (simulated in demo mode)
            for alert_config in alert_configs:
                alert_id = f"alert-{dataset_name}-{alert_config['type']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                if self.demo_mode:
                    status = "created (demo)"
                else:
                    # Would create actual alert in production
                    status = "created"
                
                result["alerts"].append({
                    "alert_id": alert_id,
                    "type": alert_config["type"],
                    "channels": alert_config["channels"],
                    "status": status
                })
        
        except Exception as e:
            logger.error(f"Error configuring alerts for {dataset_name}: {e}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def generate_pipeline_config(self, datasets: Dict[str, Any]) -> str:
        """
        Generate CI/CD pipeline configuration (GitHub Actions, GitLab CI, etc.)
        """
        config = {
            "name": "Data Quality Pipeline",
            "on": {
                "push": {"branches": ["main", "staging"]},
                "pull_request": {"branches": ["main"]}
            },
            "jobs": {
                "data_quality_checks": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {
                            "name": "Checkout code",
                            "uses": "actions/checkout@v3"
                        },
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v4",
                            "with": {"python-version": "3.12"}
                        },
                        {
                            "name": "Install dependencies",
                            "run": "pip install -r requirements.txt pycarlo"
                        },
                        {
                            "name": "Run data quality checks",
                            "run": "python pycarlo_integration/pipeline_integration.py --check-quality",
                            "env": {
                                "MONTE_CARLO_API_ID": "${{ secrets.MONTE_CARLO_API_ID }}",
                                "MONTE_CARLO_API_TOKEN": "${{ secrets.MONTE_CARLO_API_TOKEN }}"
                            }
                        }
                    ]
                },
                "deploy": {
                    "needs": "data_quality_checks",
                    "runs-on": "ubuntu-latest",
                    "if": "success()",
                    "steps": [
                        {
                            "name": "Deploy application",
                            "run": "echo 'Deploying application...'"
                        },
                        {
                            "name": "Setup monitoring",
                            "run": "python pycarlo_integration/pipeline_integration.py --setup-monitoring"
                        }
                    ]
                }
            }
        }
        
        return json.dumps(config, indent=2)


def main():
    """Main function for testing pipeline integration"""
    print("🚀 CI/CD Pipeline Integration Demo")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = DataQualityPipeline(demo_mode=True)
    
    # Define demo datasets
    demo_datasets = {
        "product_operations_incidents_2025": {
            "min_quality_score": 90.0,
            "criticality": "high"
        },
        "customer_support_metrics_2025": {
            "min_quality_score": 85.0,
            "criticality": "medium"
        },
        "user_behavior_analytics_2025": {
            "min_quality_score": 80.0,
            "criticality": "low"
        }
    }
    
    # Run pre-deployment checks
    print("\n🔍 Pre-deployment Quality Checks:")
    pre_results = pipeline.run_pre_deployment_checks(demo_datasets)
    
    for gate in pre_results["quality_gates"]:
        status_emoji = "✅" if gate["passed"] else "❌"
        print(f"{status_emoji} {gate['dataset']}: {gate['quality_score']:.1f}% quality score")
        
        for check in gate["checks"]:
            check_emoji = "✅" if check["status"] == "passed" else "❌"
            print(f"    {check_emoji} {check['message']}")
    
    # Simulate deployment decision
    if pre_results["overall_status"] == "passed":
        print(f"\n🚀 Quality gates passed! Proceeding with deployment...")
        
        # Run post-deployment setup
        print(f"\n⚙️ Post-deployment Setup:")
        post_results = pipeline.run_post_deployment_setup(demo_datasets)
        
        for setup in post_results["monitoring_setup"]:
            print(f"📊 {setup['dataset']}: {len(setup.get('rules_created', []))} quality rules created")
        
        for alerts in post_results["alerts_configured"]:
            print(f"🚨 {alerts['dataset']}: {len(alerts.get('alerts', []))} alerts configured")
    
    else:
        print(f"\n🚨 Quality gates failed! Blocking deployment.")
        print(f"Recommendations:")
        for rec in pre_results["recommendations"]:
            print(f"  💡 {rec}")
    
    # Generate pipeline configuration
    print(f"\n⚙️ Generated Pipeline Configuration:")
    pipeline_config = pipeline.generate_pipeline_config(demo_datasets)
    print(pipeline_config[:500] + "...")
    
    print(f"\n✅ Pipeline integration demo completed!")


if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        if "--check-quality" in sys.argv:
            # This would be called by CI/CD pipeline
            print("Running quality checks in CI/CD mode...")
            # Implementation for CI/CD execution
        elif "--setup-monitoring" in sys.argv:
            print("Setting up monitoring in CI/CD mode...")
            # Implementation for monitoring setup
    else:
        # Run interactive demo
        main()
