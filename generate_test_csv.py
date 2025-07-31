#!/usr/bin/env python3
"""
CSV Generator for Monte Carlo Dashboard Live Import Testing
==========================================================

This script generates CSV files compatible with the Monte Carlo dashboard's
live import feature. Files are automatically detected and ingested when
dropped into the sample_data/ folder.

Usage:
    python generate_test_csv.py                    # Generate basic test file
    python generate_test_csv.py --quality-issues   # Generate file with quality issues
    python generate_test_csv.py --large            # Generate larger dataset
    python generate_test_csv.py --custom           # Interactive custom generation
"""

import os
import csv
import random
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


class CSVGenerator:
    """Generates CSV files for testing Monte Carlo dashboard live import"""
    
    def __init__(self):
        self.sample_data_dir = Path("sample_data")
        self.sample_data_dir.mkdir(exist_ok=True)
        
        # Sample titles and descriptions for generating realistic test data
        self.sample_titles = [
            "System Performance Alert",
            "Data Quality Incident",
            "User Authentication Issue", 
            "Database Connection Timeout",
            "API Rate Limit Exceeded",
            "Cache Invalidation Error",
            "Memory Usage Warning",
            "Disk Space Alert",
            "Network Latency Spike",
            "Service Degradation Notice",
            "Security Scan Results",
            "Backup Operation Status",
            "Load Balancer Health Check",
            "Container Restart Event",
            "Pipeline Execution Summary"
        ]
        
        self.sample_descriptions = [
            "System monitoring detected unusual patterns in the application performance metrics during peak usage hours.",
            "Data validation rules identified inconsistencies in the customer demographics table requiring immediate attention.",
            "Multiple failed authentication attempts detected from suspicious IP addresses in the last 30 minutes.",
            "Database connection pool exhausted, causing application timeouts. Investigating connection leak issues.",
            "API rate limits exceeded for premium tier customers. Consider implementing better throttling mechanisms.",
            "Cache invalidation process failed for user session data, potentially affecting user experience.",
            "Memory utilization reached 90% on production servers. Scaling operations initiated automatically.",
            "Available disk space dropped below 15% on database servers. Archive and cleanup procedures started.",
            "Network latency between regions increased significantly, affecting cross-region data replication.",
            "Service response times degraded due to unexpected traffic surge. Auto-scaling policies activated.",
            "Weekly security vulnerability scan completed. Several medium-priority issues identified for remediation.",
            "Automated backup process completed successfully for all critical databases and configuration files.",
            "Load balancer health checks detected one unhealthy instance. Traffic automatically rerouted to healthy nodes.",
            "Container orchestration system restarted failed pods. Root cause analysis scheduled for investigation.",
            "ETL pipeline execution summary: 1.2M records processed, 3 data quality warnings, 0 critical errors."
        ]
        
        self.quality_issue_descriptions = [
            "",  # Empty description (NULL quality issue)
            "Short",  # Very short description (length quality issue)
            "N/A",  # Minimal content
            "TBD",  # Placeholder content
            None,  # Actual NULL value
        ]
    
    def generate_basic_test_file(self) -> str:
        """Generate a basic test file with good quality data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_test_{timestamp}.csv"
        filepath = self.sample_data_dir / filename
        
        records = []
        for i in range(5):
            title = random.choice(self.sample_titles)
            description = random.choice(self.sample_descriptions)
            records.append((title, description))
        
        self._write_csv(filepath, records)
        return str(filepath)
    
    def generate_quality_issues_file(self) -> str:
        """Generate a file with intentional data quality issues"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_quality_issues_{timestamp}.csv"
        filepath = self.sample_data_dir / filename
        
        records = []
        
        # Mix of good and problematic records
        for i in range(8):
            if i < 3:
                # Good quality records
                title = random.choice(self.sample_titles)
                description = random.choice(self.sample_descriptions)
            else:
                # Quality issue records
                title = random.choice(self.sample_titles)
                description = random.choice(self.quality_issue_descriptions)
                if description is None:
                    description = ""  # Convert None to empty string for CSV
            
            records.append((title, description))
        
        self._write_csv(filepath, records)
        return str(filepath)
    
    def generate_large_dataset(self) -> str:
        """Generate a larger dataset for performance testing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_large_dataset_{timestamp}.csv"
        filepath = self.sample_data_dir / filename
        
        records = []
        for i in range(50):
            title = f"{random.choice(self.sample_titles)} #{i+1}"
            
            # Vary description quality
            if i % 10 == 0:
                description = random.choice(self.quality_issue_descriptions) or ""
            else:
                description = random.choice(self.sample_descriptions)
                # Add some variation
                if i % 3 == 0:
                    description += f" Record ID: {i+1}. Timestamp: {datetime.now().isoformat()}"
            
            records.append((title, description))
        
        self._write_csv(filepath, records)
        return str(filepath)
    
    def generate_custom_file(self, num_records: int, include_issues: bool = False) -> str:
        """Generate a custom file with specified parameters"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_custom_{timestamp}.csv"
        filepath = self.sample_data_dir / filename
        
        records = []
        for i in range(num_records):
            title = f"{random.choice(self.sample_titles)} #{i+1}"
            
            if include_issues and i % 5 == 0:
                # Inject quality issues
                description = random.choice(self.quality_issue_descriptions) or ""
            else:
                description = random.choice(self.sample_descriptions)
                if i % 2 == 0:
                    description += f" Custom record {i+1} generated at {datetime.now().strftime('%H:%M:%S')}"
            
            records.append((title, description))
        
        self._write_csv(filepath, records)
        return str(filepath)
    
    def _write_csv(self, filepath: Path, records: List[Tuple[str, str]]):
        """Write records to CSV file"""
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header (dashboard expects title,description - no id column)
            writer.writerow(['title', 'description'])
            
            # Write records
            for title, description in records:
                writer.writerow([title, description])
        
        print(f"✅ Generated CSV file: {filepath}")
        print(f"📊 Records: {len(records)}")
        return filepath


def main():
    """Main function with command-line interface"""
    import sys
    
    generator = CSVGenerator()
    
    print("🚀 Monte Carlo Dashboard CSV Generator")
    print("=" * 45)
    
    if len(sys.argv) == 1:
        # Default: generate basic test file
        filepath = generator.generate_basic_test_file()
        print(f"\n💡 Basic test file created: {filepath}")
        
    elif "--quality-issues" in sys.argv:
        filepath = generator.generate_quality_issues_file()
        print(f"\n⚠️  Quality issues file created: {filepath}")
        print("   This file contains intentional data quality problems for testing")
        
    elif "--large" in sys.argv:
        filepath = generator.generate_large_dataset()
        print(f"\n📈 Large dataset created: {filepath}")
        print("   Use this to test dashboard performance with more records")
        
    elif "--custom" in sys.argv:
        print("\n⚙️  Custom File Generation")
        try:
            num_records = int(input("Number of records (1-100): "))
            if not 1 <= num_records <= 100:
                num_records = 10
                print(f"Using default: {num_records} records")
            
            include_issues = input("Include quality issues? (y/n): ").lower().startswith('y')
            
            filepath = generator.generate_custom_file(num_records, include_issues)
            print(f"\n🎯 Custom file created: {filepath}")
            
        except (ValueError, KeyboardInterrupt):
            print("Cancelled or invalid input. Generating default file...")
            filepath = generator.generate_basic_test_file()
    
    else:
        print("Unknown option. Generating basic test file...")
        filepath = generator.generate_basic_test_file()
    
    print(f"\n📂 To test live import:")
    print(f"   1. Start the dashboard: streamlit run src/monte_carlo_dashboard.py")
    print(f"   2. Go to 'Live Monitor' tab")
    print(f"   3. Click '🎬 Start Monitor'")
    print(f"   4. The CSV file will be automatically detected and imported!")
    print(f"   5. Watch the metrics update in real-time")
    
    print(f"\n🎉 Ready for live CSV import testing!")


if __name__ == "__main__":
    main()
