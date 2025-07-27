#!/bin/bash
# Quick CSV creation commands for live demos

# Function to create a quick CSV
create_demo_csv() {
    local filename=$1
    local title1="$2"
    local desc1="$3"
    local title2="$4" 
    local desc2="$5"
    
    cat > "demo/$filename" << EOF
title,description
$title1,$desc1
$title2,$desc2
EOF
    echo "✅ Created demo/$filename"
}

# Examples of quick CSV creation
echo "🎭 Quick CSV Creation Examples"
echo "==============================="

# Create urgent alert
create_demo_csv "urgent_alert.csv" \
    "CRITICAL: System Down" \
    "Production database unavailable affecting all users. Emergency response team activated." \
    "Performance Alert" \
    "API response times exceeded 10 seconds. Load balancer investigation in progress."

# Create data quality issues
create_demo_csv "quality_issues.csv" \
    "" \
    "Missing title field demonstrating data validation errors" \
    "Encoding Problem" \
    "Text with ���� corrupted characters"

# Create success stories  
create_demo_csv "success_metrics.csv" \
    "Revenue Growth" \
    "Q4 revenue increased 28% with customer satisfaction at all-time high of 94%." \
    "Security Milestone" \
    "Zero security incidents for 180 consecutive days with enhanced monitoring active."

echo ""
echo "🚀 Ready for live demo! Files created in demo/ folder"
