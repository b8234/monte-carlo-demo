"""
Quality Rules Engine for Monte Carlo Integration
==============================================

Defines custom data quality rules that can be applied to your demo data
and eventually deployed to production Monte Carlo platform.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class QualityRule:
    """Base class for data quality rules"""
    
    def __init__(self, name: str, description: str, severity: str = "medium"):
        self.name = name
        self.description = description
        self.severity = severity  # low, medium, high, critical
        self.created_at = datetime.now()
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Override this method in subclasses"""
        raise NotImplementedError
    
    def to_monte_carlo_config(self) -> Dict[str, Any]:
        """Convert rule to Monte Carlo configuration format"""
        raise NotImplementedError


class CompletenessRule(QualityRule):
    """Check for missing/null values in specified columns"""
    
    def __init__(self, columns: List[str], threshold: float = 0.95, **kwargs):
        super().__init__(**kwargs)
        self.columns = columns
        self.threshold = threshold
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {
            "rule_name": self.name,
            "rule_type": "completeness",
            "passed": True,
            "details": []
        }
        
        for column in self.columns:
            if column not in data.columns:
                results["details"].append({
                    "column": column,
                    "status": "error",
                    "message": f"Column '{column}' not found in dataset"
                })
                results["passed"] = False
                continue
            
            completeness = data[column].notna().mean()
            passed = completeness >= self.threshold
            
            results["details"].append({
                "column": column,
                "completeness": round(completeness, 3),
                "threshold": self.threshold,
                "status": "passed" if passed else "failed",
                "message": f"Completeness: {completeness:.1%} (threshold: {self.threshold:.1%})"
            })
            
            if not passed:
                results["passed"] = False
        
        return results
    
    def to_monte_carlo_config(self) -> Dict[str, Any]:
        return {
            "rule_type": "completeness",
            "columns": self.columns,
            "threshold": self.threshold,
            "severity": self.severity,
            "description": self.description
        }


class UniquenessRule(QualityRule):
    """Check for duplicate values in specified columns"""
    
    def __init__(self, columns: List[str], threshold: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.columns = columns
        self.threshold = threshold
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {
            "rule_name": self.name,
            "rule_type": "uniqueness", 
            "passed": True,
            "details": []
        }
        
        for column in self.columns:
            if column not in data.columns:
                results["details"].append({
                    "column": column,
                    "status": "error",
                    "message": f"Column '{column}' not found in dataset"
                })
                results["passed"] = False
                continue
            
            total_count = len(data)
            unique_count = data[column].nunique()
            uniqueness = unique_count / total_count if total_count > 0 else 0
            passed = uniqueness >= self.threshold
            
            results["details"].append({
                "column": column,
                "uniqueness": round(uniqueness, 3),
                "threshold": self.threshold,
                "unique_count": unique_count,
                "total_count": total_count,
                "duplicates": total_count - unique_count,
                "status": "passed" if passed else "failed",
                "message": f"Uniqueness: {uniqueness:.1%} ({unique_count}/{total_count} unique)"
            })
            
            if not passed:
                results["passed"] = False
        
        return results
    
    def to_monte_carlo_config(self) -> Dict[str, Any]:
        return {
            "rule_type": "uniqueness",
            "columns": self.columns,
            "threshold": self.threshold,
            "severity": self.severity,
            "description": self.description
        }


class ValidityRule(QualityRule):
    """Check data validity against specified constraints"""
    
    def __init__(self, column: str, constraints: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.column = column
        self.constraints = constraints  # e.g., {"min": 0, "max": 100, "pattern": "^[A-Z]+$"}
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {
            "rule_name": self.name,
            "rule_type": "validity",
            "passed": True,
            "details": []
        }
        
        if self.column not in data.columns:
            results["details"].append({
                "column": self.column,
                "status": "error", 
                "message": f"Column '{self.column}' not found in dataset"
            })
            results["passed"] = False
            return results
        
        column_data = data[self.column].dropna()  # Skip null values
        total_valid = len(column_data)
        
        for constraint_type, constraint_value in self.constraints.items():
            if constraint_type == "min":
                valid_count = (column_data >= constraint_value).sum()
            elif constraint_type == "max":
                valid_count = (column_data <= constraint_value).sum()
            elif constraint_type == "pattern":
                import re
                valid_count = column_data.astype(str).str.match(constraint_value).sum()
            elif constraint_type == "values":
                valid_count = column_data.isin(constraint_value).sum()
            else:
                continue
            
            validity_rate = valid_count / total_valid if total_valid > 0 else 0
            passed = validity_rate >= 0.95  # Default threshold
            
            results["details"].append({
                "constraint": f"{constraint_type}: {constraint_value}",
                "validity_rate": round(validity_rate, 3),
                "valid_count": int(valid_count),
                "total_count": int(total_valid),
                "invalid_count": int(total_valid - valid_count),
                "status": "passed" if passed else "failed",
                "message": f"{constraint_type.title()} constraint: {validity_rate:.1%} valid"
            })
            
            if not passed:
                results["passed"] = False
        
        return results
    
    def to_monte_carlo_config(self) -> Dict[str, Any]:
        return {
            "rule_type": "validity",
            "column": self.column,
            "constraints": self.constraints,
            "severity": self.severity,
            "description": self.description
        }


class FreshnessRule(QualityRule):
    """Check data freshness based on timestamp columns"""
    
    def __init__(self, timestamp_column: str, max_age_hours: int = 24, **kwargs):
        super().__init__(**kwargs)
        self.timestamp_column = timestamp_column
        self.max_age_hours = max_age_hours
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {
            "rule_name": self.name,
            "rule_type": "freshness",
            "passed": True,
            "details": []
        }
        
        if self.timestamp_column not in data.columns:
            results["details"].append({
                "column": self.timestamp_column,
                "status": "error",
                "message": f"Timestamp column '{self.timestamp_column}' not found"
            })
            results["passed"] = False
            return results
        
        try:
            timestamps = pd.to_datetime(data[self.timestamp_column])
            latest_timestamp = timestamps.max()
            current_time = datetime.now()
            age_hours = (current_time - latest_timestamp).total_seconds() / 3600
            
            passed = age_hours <= self.max_age_hours
            
            results["details"].append({
                "latest_timestamp": latest_timestamp.isoformat(),
                "current_time": current_time.isoformat(),
                "age_hours": round(age_hours, 2),
                "max_age_hours": self.max_age_hours,
                "status": "passed" if passed else "failed",
                "message": f"Data age: {age_hours:.1f} hours (max: {self.max_age_hours} hours)"
            })
            
            if not passed:
                results["passed"] = False
                
        except Exception as e:
            results["details"].append({
                "status": "error",
                "message": f"Error parsing timestamps: {str(e)}"
            })
            results["passed"] = False
        
        return results
    
    def to_monte_carlo_config(self) -> Dict[str, Any]:
        return {
            "rule_type": "freshness",
            "timestamp_column": self.timestamp_column,
            "max_age_hours": self.max_age_hours,
            "severity": self.severity,
            "description": self.description
        }


class EnterpriseQualityRules:
    """
    Enterprise-specific quality rules for Monte Carlo demo datasets
    """
    
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.rules = {}
        self._initialize_enterprise_rules()
    
    def _initialize_enterprise_rules(self):
        """Initialize standard enterprise quality rules"""
        
        # Product Operations Rules
        self.rules["product_operations"] = [
            CompletenessRule(
                name="Product Incidents Completeness",
                description="Ensure critical incident fields are complete",
                columns=["id", "title", "severity"],
                threshold=0.98,
                severity="high"
            ),
            UniquenessRule(
                name="Incident ID Uniqueness", 
                description="Incident IDs must be unique",
                columns=["id"],
                threshold=1.0,
                severity="critical"
            ),
            ValidityRule(
                name="Severity Values",
                description="Severity must be valid enum",
                column="severity",
                constraints={"values": ["low", "medium", "high", "critical"]},
                severity="medium"
            )
        ]
        
        # Customer Support Rules
        self.rules["customer_support"] = [
            CompletenessRule(
                name="Support Metrics Completeness",
                description="Essential support metrics must be complete",
                columns=["customer_id", "ticket_id", "resolution_time"],
                threshold=0.95,
                severity="high"
            ),
            ValidityRule(
                name="Resolution Time Validity",
                description="Resolution time must be positive",
                column="resolution_time",
                constraints={"min": 0, "max": 7200},  # 0 to 2 hours in minutes
                severity="medium"
            )
        ]
        
        # Business Intelligence Rules
        self.rules["business_intelligence"] = [
            CompletenessRule(
                name="BI Report Completeness",
                description="BI reports must have complete metadata",
                columns=["report_id", "department", "metric_value"],
                threshold=0.99,
                severity="high"
            ),
            ValidityRule(
                name="Metric Value Range",
                description="Metric values must be within expected range",
                column="metric_value", 
                constraints={"min": 0, "max": 1000000},
                severity="medium"
            )
        ]
        
        # User Behavior Rules
        self.rules["user_behavior"] = [
            UniquenessRule(
                name="User Session Uniqueness",
                description="User sessions should be unique",
                columns=["session_id"],
                threshold=1.0,
                severity="high"
            ),
            ValidityRule(
                name="User ID Format",
                description="User IDs must follow standard format",
                column="user_id",
                constraints={"pattern": r"^user_\d+$"},
                severity="low"
            )
        ]
    
    def get_rules_for_table(self, table_name: str) -> List[QualityRule]:
        """Get quality rules for a specific table"""
        # Map table names to rule categories
        table_mapping = {
            "product_operations_incidents_2025": "product_operations",
            "customer_support_metrics_2025": "customer_support", 
            "business_intelligence_reports_2025": "business_intelligence",
            "user_behavior_analytics_2025": "user_behavior"
        }
        
        category = table_mapping.get(table_name, "default")
        return self.rules.get(category, [])
    
    def validate_table(self, table_name: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate a table against its quality rules"""
        rules = self.get_rules_for_table(table_name)
        
        if not rules:
            return {
                "table_name": table_name,
                "status": "no_rules",
                "message": f"No quality rules defined for {table_name}",
                "overall_score": 100.0
            }
        
        results = {
            "table_name": table_name,
            "validated_at": datetime.now().isoformat(),
            "total_rules": len(rules),
            "rule_results": [],
            "passed_rules": 0,
            "failed_rules": 0,
            "overall_score": 0.0,
            "status": "passed"
        }
        
        for rule in rules:
            try:
                rule_result = rule.validate(data)
                results["rule_results"].append(rule_result)
                
                if rule_result["passed"]:
                    results["passed_rules"] += 1
                else:
                    results["failed_rules"] += 1
                    
            except Exception as e:
                logger.error(f"Error validating rule {rule.name}: {e}")
                results["rule_results"].append({
                    "rule_name": rule.name,
                    "status": "error",
                    "message": str(e)
                })
                results["failed_rules"] += 1
        
        # Calculate overall score
        if results["total_rules"] > 0:
            results["overall_score"] = (results["passed_rules"] / results["total_rules"]) * 100
            
        if results["failed_rules"] > 0:
            results["status"] = "failed"
        
        return results
    
    def validate_all_tables(self, tables_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Validate all tables against their quality rules"""
        overall_results = {
            "validated_at": datetime.now().isoformat(),
            "total_tables": len(tables_data),
            "table_results": {},
            "summary": {
                "total_rules": 0,
                "passed_rules": 0,
                "failed_rules": 0,
                "average_score": 0.0
            }
        }
        
        for table_name, data in tables_data.items():
            table_result = self.validate_table(table_name, data)
            overall_results["table_results"][table_name] = table_result
            
            # Update summary
            overall_results["summary"]["total_rules"] += table_result.get("total_rules", 0)
            overall_results["summary"]["passed_rules"] += table_result.get("passed_rules", 0)
            overall_results["summary"]["failed_rules"] += table_result.get("failed_rules", 0)
        
        # Calculate average score
        if overall_results["summary"]["total_rules"] > 0:
            overall_results["summary"]["average_score"] = (
                overall_results["summary"]["passed_rules"] / 
                overall_results["summary"]["total_rules"]
            ) * 100
        
        return overall_results
    
    def export_monte_carlo_config(self) -> Dict[str, Any]:
        """Export all rules as Monte Carlo configuration"""
        config = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "demo_mode": self.demo_mode,
            "rules": {}
        }
        
        for category, rules in self.rules.items():
            config["rules"][category] = [
                rule.to_monte_carlo_config() for rule in rules
            ]
        
        return config


def main():
    """Demo the quality rules engine"""
    print("🔧 Quality Rules Engine Demo")
    print("=" * 40)
    
    # Initialize rules engine
    rules_engine = EnterpriseQualityRules(demo_mode=True)
    
    # Create sample data for testing
    sample_data = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "title": ["Issue A", "Issue B", None, "Issue D", "Issue E"],
        "severity": ["high", "medium", "low", "critical", "invalid"],
        "timestamp": ["2025-01-29 10:00:00"] * 5
    })
    
    print("\n📊 Sample Data:")
    print(sample_data)
    
    # Test validation
    print("\n🔍 Validation Results:")
    results = rules_engine.validate_table("product_operations_incidents_2025", sample_data)
    
    print(f"Table: {results['table_name']}")
    print(f"Overall Score: {results['overall_score']:.1f}%")
    print(f"Status: {results['status']}")
    print(f"Rules: {results['passed_rules']}/{results['total_rules']} passed")
    
    # Show rule details
    print(f"\n📋 Rule Details:")
    for rule_result in results["rule_results"]:
        print(f"\n{rule_result['rule_name']} ({rule_result['rule_type']}):")
        for detail in rule_result.get("details", []):
            print(f"  - {detail.get('message', detail)}")
    
    # Export configuration
    print(f"\n⚙️ Monte Carlo Configuration:")
    config = rules_engine.export_monte_carlo_config()
    print(json.dumps(config, indent=2)[:500] + "...")
    
    print(f"\n✅ Quality rules demo completed!")


if __name__ == "__main__":
    main()
