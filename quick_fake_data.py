# Python one-liners for creating fake data during live demos

# Quick CSV creation during presentations
import csv
from datetime import datetime

# Create timestamp-based filename
timestamp = datetime.now().strftime("%H%M%S")

# Security incident
with open(f"demo/security_{timestamp}.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'description'])
    writer.writerow(['Security Breach', 'Unauthorized access detected in customer database. Investigation initiated.'])
    writer.writerow(['', 'Missing title field to test data quality validation'])

# Performance alert  
with open(f"demo/performance_{timestamp}.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'description'])
    writer.writerow(['Database Slow', 'Query response time increased 400% affecting user experience'])
    writer.writerow(['Critical Error', None])  # NULL value

# Success metrics
with open(f"demo/success_{timestamp}.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['title', 'description'])  
    writer.writerow(['Revenue Target', 'Exceeded quarterly revenue goal by 23% with strong customer retention'])
    writer.writerow(['System Uptime', '99.97% uptime achieved this month with zero critical incidents'])

print(f"✅ Created 3 demo files with timestamp {timestamp}")
