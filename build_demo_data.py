#!/usr/bin/env python3
"""
Interactive Fake Data Builder
Quick command-line tool to create custom CSV files for demos.
"""

import csv
from pathlib import Path
from datetime import datetime

def create_custom_data():
    """Interactive tool to create custom demo data."""
    
    print("🎭 Interactive Fake Data Builder")
    print("=" * 40)
    
    filename = input("📁 Enter filename (e.g., 'my_demo.csv'): ").strip()
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    records = []
    
    print("\n📝 Enter your data (press Enter with empty title to finish):")
    
    while True:
        print(f"\n--- Record {len(records) + 1} ---")
        title = input("Title: ").strip()
        
        if not title:
            break
            
        description = input("Description: ").strip()
        
        # Special options
        if description.lower() == 'null':
            description = None
        elif description.lower() == 'empty':
            description = ''
        
        records.append({
            'title': title,
            'description': description
        })
        
        print(f"✅ Added: {title}")
    
    if not records:
        print("❌ No records added. Exiting.")
        return
    
    # Write file
    filepath = Path("demo") / filename
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for record in records:
            writer.writerow(record)
    
    print(f"\n✅ Created {filepath} with {len(records)} records!")
    print(f"🚀 Ready for live demo!")

def quick_templates():
    """Generate quick template files."""
    
    templates = {
        'security_alerts': [
            ("Failed Login Attempts", "Multiple failed login attempts detected from IP 192.168.1.100. Account locked for security."),
            ("Malware Detection", "Suspicious file detected in user uploads. File quarantined and scanning initiated."),
            ("Unusual Access Pattern", "User accessing sensitive data outside normal hours. Additional verification required."),
        ],
        'system_issues': [
            ("Database Slow", "Database queries taking 5x longer than normal. Performance investigation started."),
            ("", "Missing title in system log entry - data quality issue detected."),
            ("Memory Alert", "Application server memory usage at 95%. Restart scheduled."),
        ],
        'business_updates': [
            ("Sales Milestone", "Reached $1M in quarterly sales - 15% ahead of target with strong customer satisfaction."),
            ("Product Launch", "New feature released to 100% of users with positive initial feedback and adoption rates."),
            ("Team Achievement", "Development team completed all sprint goals early with zero production incidents."),
        ]
    }
    
    print("🎯 Quick Template Generator")
    print("Available templates:")
    for i, template_name in enumerate(templates.keys(), 1):
        print(f"  {i}. {template_name}")
    
    choice = input("\nSelect template (1-3): ").strip()
    
    template_map = {
        '1': 'security_alerts',
        '2': 'system_issues', 
        '3': 'business_updates'
    }
    
    if choice in template_map:
        template_name = template_map[choice]
        records = templates[template_name]
        
        filename = f"template_{template_name}.csv"
        filepath = Path("demo") / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for title, description in records:
                writer.writerow({'title': title, 'description': description})
        
        print(f"✅ Created {filepath} with {len(records)} records!")
    else:
        print("❌ Invalid choice")

def main():
    print("🎭 Fake Data Creation Tools")
    print("1. Interactive Data Builder")
    print("2. Quick Templates")
    print("3. Exit")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == '1':
        create_custom_data()
    elif choice == '2':
        quick_templates()
    elif choice == '3':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
