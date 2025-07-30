#!/usr/bin/env python3
"""
Enterprise Dataset Generator for Monte Carlo Data Observability Platform
Creates realistic business data with various quality patterns for demonstration purposes.
Generates datasets that mirror actual enterprise data scenarios.
"""

import csv
import random
import datetime
from pathlib import Path

class EnterpriseDatasetGenerator:
    def __init__(self):
        # Enterprise business scenarios with quality patterns
        self.high_quality_scenarios = [
            ("Quarterly Revenue Report", "Q3 revenue increased by 23% year-over-year, reaching $4.2M with strong performance in enterprise sales and customer retention rates of 94%."),
            ("Product Launch Success", "New mobile application launched with 50,000+ downloads in first week, achieving 4.7-star rating and 85% user retention after 30 days."),
            ("Security Audit Complete", "Annual penetration testing completed with no critical vulnerabilities found. All systems updated and security protocols enhanced."),
            ("Infrastructure Upgrade", "Migration to cloud infrastructure completed successfully with 99.97% uptime maintained and 35% cost reduction achieved."),
            ("Customer Satisfaction", "NPS score improved to 78 (up from 65), with customers highlighting faster support response times and improved product reliability."),
            ("Team Performance", "Development team exceeded sprint goals by 15%, delivering all planned features ahead of schedule with zero production bugs."),
            ("Process Automation", "Automated deployment pipeline reduced release time from 4 hours to 12 minutes while eliminating manual errors."),
            ("Cost Optimization", "Database query optimization reduced average response time from 1.2s to 180ms, improving user experience significantly."),
        ]
        
        self.quality_violation_scenarios = [
            ("", "This record has a missing title field which should trigger data quality alerts and validation errors."),
            ("Data Breach Alert", ""),  # Empty description
            ("System Failure", None),  # NULL description
            ("Corrupted Record", "���� encoding issues detected ���� special characters causing display problems ����"),
            ("Suspicious Activity", "'; DROP TABLE users; SELECT * FROM passwords; --"),
            ("Short", "Hi"),  # Very short content
            ("Performance Issue", "Database slow today might need to check"),  # Incomplete/vague
            ("Critical Error During Migration Process That Exceeded Maximum Title Length Limits", "Title too long - indicates potential data loading issues or schema problems."),
            ("JSON Error", '{"incomplete": "json object without closing brace"'),
            ("Repeated Pattern", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
            ("Special Chars", "Testing with émojis 🚨 and spëcial chäractërs ñoñó"),
            ("Injection Test", "<script>alert('XSS')</script> DROP DATABASE;"),
        ]
        
        self.business_critical_incidents = [
            ("API Outage", "Payment processing API experiencing intermittent 500 errors affecting 12% of transactions. Engineering team investigating connection pool exhaustion."),
            ("Data Quality Alert", "ETL pipeline detected 2,847 records with invalid email formats in customer data. Data validation rules being updated."),
            ("Security Incident", "Unusual login patterns detected from IP range 185.220.101.x. Account security measures activated and monitoring increased."),
            ("Performance Degradation", "Application response times increased 340% during peak hours. Database query optimization and load balancing in progress."),
            ("Compliance Issue", "GDPR audit revealed 15,000 customer records retained beyond policy limits. Automated deletion process initiated."),
            ("System Capacity", "Database storage approaching 85% capacity. Archival process scheduled and additional storage provisioning requested."),
            ("Integration Failure", "Third-party payment gateway timeout errors affecting checkout completion. Fallback payment options activated."),
            ("Monitoring Alert", "CPU utilization exceeded 90% threshold on production servers for 45 minutes. Auto-scaling policies triggered."),
        ]
    
    def generate_csv_file(self, filename, num_records=20, scenario_type="mixed"):
        """Generate a CSV file with fake data."""
        
        records = []
        
        if scenario_type == "good":
            scenarios = self.high_quality_scenarios * (num_records // len(self.high_quality_scenarios) + 1)
        elif scenario_type == "problematic":
            scenarios = self.quality_violation_scenarios * (num_records // len(self.quality_violation_scenarios) + 1)
        elif scenario_type == "realistic":
            scenarios = self.business_critical_incidents * (num_records // len(self.business_critical_incidents) + 1)
        else:  # mixed
            scenarios = (self.high_quality_scenarios + self.quality_violation_scenarios + self.business_critical_incidents)
            random.shuffle(scenarios)
        
        # Select records
        selected_scenarios = scenarios[:num_records]
        
        # Add some variation and timestamps
        for i, (title, description) in enumerate(selected_scenarios):
            # Add some variation to titles
            if title and random.random() < 0.3:
                prefixes = ["URGENT:", "UPDATE:", "RESOLVED:", "PENDING:", "CRITICAL:"]
                title = f"{random.choice(prefixes)} {title}"
            
            records.append({
                'title': title,
                'description': description
            })
        
        # Write CSV file
        filepath = Path("demo") / filename
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        
        print(f"✅ Created {filepath} with {len(records)} records")
        return filepath
    
    def generate_time_series_data(self, filename, days=7):
        """Generate time-series data simulating daily operational events."""
        
        records = []
        base_date = datetime.datetime.now() - datetime.timedelta(days=days)
        
        daily_events = [
            "Daily backup completed successfully",
            "System health check passed all tests", 
            "User activity peak detected during lunch hours",
            "Database maintenance window completed",
            "Security scan completed with no issues",
            "Performance monitoring reports normal operations",
            "API rate limits within acceptable range",
        ]
        
        issues = [
            "Backup process took longer than expected",
            "Minor memory leak detected in application server",
            "Unusual spike in database connections",
            "SSL certificate expires in 30 days",
            "Disk space usage increased by 5%",
        ]
        
        for day in range(days):
            current_date = base_date + datetime.timedelta(days=day)
            
            # Generate 3-5 events per day
            num_events = random.randint(3, 5)
            
            for event in range(num_events):
                if random.random() < 0.15:  # 15% chance of issues
                    title = f"Alert - {current_date.strftime('%Y-%m-%d')}"
                    description = random.choice(issues) + f" detected at {current_date.strftime('%H:%M')}"
                else:
                    title = f"Status - {current_date.strftime('%Y-%m-%d')}"
                    description = random.choice(daily_events) + f" at {current_date.strftime('%H:%M')}"
                
                records.append({
                    'title': title,
                    'description': description
                })
        
        # Write CSV file
        filepath = Path("demo") / filename
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        
        print(f"✅ Created {filepath} with {len(records)} time-series records")
        return filepath

def main():
    """Generate various types of enterprise datasets for Monte Carlo platform demonstration."""
    
    generator = EnterpriseDatasetGenerator()
    
    print("� Enterprise Dataset Generator for Monte Carlo Platform")
    print("=" * 60)
    
    # Generate different types of enterprise data
    generator.generate_csv_file("customer_engagement_metrics_baseline.csv", 15, "good")
    generator.generate_csv_file("data_quality_violations_detected.csv", 20, "problematic") 
    generator.generate_csv_file("business_critical_incidents.csv", 12, "realistic")
    generator.generate_csv_file("mixed_quality_operations_data.csv", 25, "mixed")
    generator.generate_time_series_data("system_monitoring_events_stream.csv", 5)
    
    print("\n🎯 Enterprise datasets created in demo/ folder!")
    print("📝 Use these datasets for Monte Carlo platform demonstrations:")
    print("   - Copy files to data/ folder to trigger quality monitoring")
    print("   - Edit files to create custom business scenarios")
    print("   - Use different files to demonstrate various quality patterns")
    
    print("\n🚀 To use in live monitoring:")
    print("   cp demo/mixed_quality_operations_data.csv data/live_operations_$(date +%s).csv")

if __name__ == "__main__":
    main()
