"""
Quality Test Data Generator for Monte Carlo Data Observability Platform
Generates enterprise-grade test datasets with various quality patterns for platform validation.
Creates realistic sample data for testing observability features and quality monitoring.
"""

import pandas as pd
import random
import string
from datetime import datetime, timedelta
import uuid

# Enterprise data templates
BUSINESS_TITLES = [
    "System Performance Alert",
    "Customer Feedback Summary", 
    "Security Patch Deployment",
    "Feature Release Notes",
    "Database Optimization",
    "User Engagement Metrics",
    "Revenue Analysis Report",
    "Infrastructure Monitoring",
    "API Performance Review",
    "Data Quality Assessment",
    "Product Roadmap Update",
    "Team Meeting Notes",
    "Compliance Review",
    "Marketing Campaign Results",
    "Technical Documentation"
]

HIGH_QUALITY_DESCRIPTIONS = [
    "Quarterly performance metrics show steady improvement across all key indicators. Customer satisfaction up 15% year-over-year.",
    "Successfully implemented new caching layer resulting in 40% reduction in page load times and improved user experience.",
    "Completed security audit with zero critical vulnerabilities found. All recommended patches applied successfully.",
    "New feature rollout exceeded expectations with 85% user adoption rate within first week of launch.",
    "Database optimization project completed ahead of schedule. Query performance improved by 60% on average.",
    "Mobile app update includes enhanced accessibility features and improved battery efficiency.",
    "Integration with third-party payment processor completed. Transaction success rate improved to 99.7%.",
    "Cloud infrastructure migration finished with zero downtime. Monthly costs reduced by 30%.",
    "AI recommendation engine shows 25% improvement in click-through rates during A/B testing phase.",
    "Customer onboarding flow redesigned based on user research. Completion rate increased from 68% to 89%."
]

QUALITY_VIOLATION_DESCRIPTIONS = [
    "",  # Empty description
    "OK",  # Too short
    "N/A",  # Generic
    "See attached file",  # Vague reference
    "Same as last time",  # Uninformative
    "TBD",  # Placeholder text
    "Lorem ipsum dolor sit amet",  # Placeholder text
    "Contact John for details",  # Missing context
    "Error occurred",  # Too vague
    "Update needed"  # Unclear
]

EDGE_CASE_DESCRIPTIONS = [
    "This description contains special characters: àáâãäåæçèéêë ñòóôõö ùúûüý €£¥ @#$%^&*()",
    "Description with\nnewlines\nand\ttabs\tfor testing",
    "Very long description " + "that keeps going " * 50 + "and never seems to end.",
    'Description with "quotes" and \'apostrophes\' for testing',
    "Description with emojis 🚀 📊 ✅ ❌ 🔧 to test unicode handling",
    "Numbers: 123456789 and decimals: 3.14159 and percentages: 95.7%",
    "URLs like https://example.com and emails like test@example.com",
    "SQL injection attempt: '; DROP TABLE users; --",
    "HTML tags: <script>alert('test')</script> <b>bold</b> <i>italic</i>",
    "Unicode test: 测试 тест テスト اختبار परीक्षा"
]

def generate_enterprise_operational_data(num_records=100, include_quality_issues=True):
    """Generate sample data with various quality characteristics."""
    
    data = []
    start_id = 2000  # Start from 2000 to avoid conflicts
    
    for i in range(num_records):
        record_id = start_id + i
        
        # Choose title
        if random.random() < 0.05 and include_quality_issues:  # 5% chance of problematic title
            title = random.choice(["", "TBD", "Update", "Fix"])
        else:
            title = random.choice(BUSINESS_TITLES)
            
        # Add variation to titles
        if random.random() < 0.3:
            title += f" - {random.choice(['Q1', 'Q2', 'Q3', 'Q4', '2025', 'v2.1', 'Phase 1'])}"
        
        # Choose description based on probability
        description_type = random.choices(
            ['good', 'problematic', 'edge_case', 'null'],
            weights=[70, 15, 10, 5],  # 70% good, 15% problematic, 10% edge cases, 5% null
            k=1
        )[0]
        
        if description_type == 'good':
            description = random.choice(HIGH_QUALITY_DESCRIPTIONS)
            # Add some variation
            if random.random() < 0.3:
                description += f" Ticket ID: {random.randint(1000, 9999)}"
        elif description_type == 'problematic':
            description = random.choice(QUALITY_VIOLATION_DESCRIPTIONS)
        elif description_type == 'edge_case':
            description = random.choice(EDGE_CASE_DESCRIPTIONS)
        else:  # null
            description = None
            
        data.append({
            'id': record_id,
            'title': title,
            'description': description
        })
    
    return pd.DataFrame(data)

def generate_system_monitoring_events(num_records=50):
    """Generate data with timestamps to simulate real-time data flow."""
    
    data = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(num_records):
        # Generate timestamp
        timestamp = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Simulate different event types
        event_types = ['alert', 'info', 'warning', 'error', 'success']
        event_type = random.choice(event_types)
        
        # Generate severity based on event type
        severity_map = {
            'error': random.choice(['high', 'critical']),
            'warning': random.choice(['medium', 'high']),
            'alert': random.choice(['medium', 'high', 'critical']),
            'info': 'low',
            'success': 'low'
        }
        
        data.append({
            'id': 3000 + i,
            'title': f"{event_type.title()} Event {i+1}",
            'description': f"Automated {event_type} generated at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            'event_type': event_type,
            'severity': severity_map[event_type],
            'timestamp': timestamp.isoformat(),
            'source_system': random.choice(['api', 'database', 'frontend', 'mobile', 'etl'])
        })
    
    return pd.DataFrame(data)

def main():
    """Generate enterprise quality test datasets for Monte Carlo platform validation."""
    
    print("� Generating Enterprise Quality Test Data for Monte Carlo Platform...")
    
    # Generate baseline operational data
    operational_df = generate_enterprise_operational_data(100, include_quality_issues=True)
    operational_df.to_csv("data/user_behavior_analytics_2025.csv", index=False)
    print(f"✅ Generated user_behavior_analytics_2025.csv with {len(operational_df)} records")
    
    # Generate system monitoring events
    monitoring_df = generate_system_monitoring_events(50)
    monitoring_df.to_csv("data/system_monitoring_events_2025.csv", index=False)
    print(f"✅ Generated system_monitoring_events_2025.csv with {len(monitoring_df)} records")
    
    # Generate quality violation dataset
    quality_violations = []
    for i in range(20):
        quality_violations.append({
            'id': 4000 + i,
            'title': random.choice(["", "TBD", "Fix", "Update", "NULL", "n/a"]) if i < 10 else f"Valid Title {i}",
            'description': random.choice(QUALITY_VIOLATION_DESCRIPTIONS + [None, "", " "]) if i < 15 else f"Valid description {i}"
        })
    
    violations_df = pd.DataFrame(quality_violations)
    violations_df.to_csv("data/data_quality_violations_2025.csv", index=False)
    print(f"✅ Generated data_quality_violations_2025.csv with {len(violations_df)} records")
    
    # Show enterprise summary
    print(f"\n📊 Enterprise Dataset Generation Summary:")
    print(f"   Total records across all datasets: {len(operational_df) + len(monitoring_df) + len(violations_df)}")
    print(f"   Enterprise datasets created: 3")
    print(f"   Quality patterns included: Empty fields, validation failures, encoding issues, edge cases")
    
    print(f"\n💡 Use these datasets for Monte Carlo platform testing:")
    print(f"   - Quality monitoring validation with user behavior analytics")
    print(f"   - Real-time alerting testing with system monitoring events") 
    print(f"   - Anomaly detection validation with quality violations")
    print(f"   - End-to-end pipeline monitoring with time-series data")

if __name__ == "__main__":
    main()
