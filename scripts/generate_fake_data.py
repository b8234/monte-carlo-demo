#!/usr/bin/env python3
"""
Fake Data Generator for Monte Carlo Demo
Creates realistic business data with various quality issues for demonstration purposes.
"""

import csv
import random
import datetime
from pathlib import Path

class FakeDataGenerator:
    def __init__(self):
        # Business scenarios with quality issues
        self.good_scenarios = [
            ("Quarterly Revenue Report", "Q3 revenue increased by 23% year-over-year, reaching $4.2M with strong performance in enterprise sales and customer retention rates of 94%."),
            ("Product Launch Success", "New mobile application launched with 50,000+ downloads in first week, achieving 4.7-star rating and 85% user retention after 30 days."),
            ("Security Audit Complete", "Annual penetration testing completed with no critical vulnerabilities found. All systems updated and security protocols enhanced."),
            ("Infrastructure Upgrade", "Migration to cloud infrastructure completed successfully with 99.97% uptime maintained and 35% cost reduction achieved."),
            ("Customer Satisfaction", "NPS score improved to 78 (up from 65), with customers highlighting faster support response times and improved product reliability."),
            ("Team Performance", "Development team exceeded sprint goals by 15%, delivering all planned features ahead of schedule with zero production bugs."),
            ("Process Automation", "Automated deployment pipeline reduced release time from 4 hours to 12 minutes while eliminating manual errors."),
            ("Cost Optimization", "Database query optimization reduced average response time from 1.2s to 180ms, improving user experience significantly."),
        ]
        
        self.problematic_scenarios = [
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
        
        self.realistic_issues = [
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
            scenarios = self.good_scenarios * (num_records // len(self.good_scenarios) + 1)
        elif scenario_type == "problematic":
            scenarios = self.problematic_scenarios * (num_records // len(self.problematic_scenarios) + 1)
        elif scenario_type == "realistic":
            scenarios = self.realistic_issues * (num_records // len(self.realistic_issues) + 1)
        else:  # mixed
            scenarios = (self.good_scenarios + self.problematic_scenarios + self.realistic_issues)
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
    """Generate various types of fake data files."""
    
    generator = FakeDataGenerator()
    
    print("🎭 Fake Data Generator for Monte Carlo Demo")
    print("=" * 50)
    
    # Generate different types of data
    generator.generate_csv_file("fake_good_quality.csv", 15, "good")
    generator.generate_csv_file("fake_with_issues.csv", 20, "problematic") 
    generator.generate_csv_file("fake_realistic_alerts.csv", 12, "realistic")
    generator.generate_csv_file("fake_mixed_data.csv", 25, "mixed")
    generator.generate_time_series_data("fake_time_series.csv", 5)
    
    print("\n🎯 Fake data files created in demo/ folder!")
    print("📝 You can now use these for live demonstrations:")
    print("   - Copy files to demo/ folder during presentations")
    print("   - Edit files to create custom scenarios")
    print("   - Use different files to show various quality patterns")
    
    print("\n🚀 To use in live demo:")
    print("   cp demo/fake_mixed_data.csv demo/live_demo_$(date +%s).csv")

if __name__ == "__main__":
    main()
