#!/usr/bin/env python3
"""
Quick demo script to show live data ingestion during presentations.
Copies sample files to the demo folder with delays for dramatic effect.
"""

import time
import shutil
import os
from pathlib import Path

def run_live_demo():
    """Execute a live demo sequence."""
    
    demo_folder = Path("demo")
    
    print("🎬 Starting live demo sequence...")
    print("📋 Make sure your dashboard is open at http://localhost:8501")
    print("👀 Make sure live monitor is running: python live_demo_monitor.py")
    print()
    
    input("Press Enter when ready to start the demo... ")
    
    print("\n🎯 Demo Step 1: Adding mixed quality data...")
    shutil.copy("demo/sample_mixed_quality.csv", "demo/live_demo_1.csv")
    print("✅ File added! Check your dashboard...")
    time.sleep(5)
    
    print("\n🎯 Demo Step 2: Adding critical issues...")
    shutil.copy("demo/sample_critical_issues.csv", "demo/live_demo_2.csv") 
    print("✅ File added! Check your dashboard...")
    time.sleep(5)
    
    print("\n🎯 Demo Step 3: Adding good quality data...")
    shutil.copy("demo/sample_good_quality.csv", "demo/live_demo_3.csv")
    print("✅ File added! Check your dashboard...")
    
    print("\n🎉 Demo complete!")
    print("🔬 Now run: python ai_layer/summarize.py")
    print("📊 Watch the complete AI quality analysis!")

if __name__ == "__main__":
    run_live_demo()
