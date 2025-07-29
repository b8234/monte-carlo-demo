#!/usr/bin/env python3
"""
Live Demo Monitor: Watches for new CSV files and automatically ingests them into the database.
Perfect for live demonstrations where you want to show real-time data quality monitoring.
"""

import os
import time
import pandas as pd
import duckdb
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CSVFileHandler(FileSystemEventHandler):
    """Handle new CSV files added to the demo folder."""
    
    def __init__(self, db_path):
        self.db_path = db_path
        
    def on_created(self, event):
        """Called when a new file is created."""
        if not event.is_directory and event.src_path.endswith('.csv'):
            print(f"\n🔥 NEW CSV DETECTED: {event.src_path}")
            time.sleep(1)  # Give file time to finish writing
            self.process_csv_file(event.src_path)
    
    def process_csv_file(self, csv_path):
        """Process a new CSV file and add it to the database."""
        try:
            print(f"📊 Processing: {os.path.basename(csv_path)}")
            
            # Read the CSV file
            df = pd.read_csv(csv_path)
            print(f"   📋 Found {len(df)} rows, {len(df.columns)} columns")
            
            # Validate required columns
            required_columns = ['title', 'description']
            missing_cols = [col for col in required_columns if col not in df.columns]
            
            if missing_cols:
                print(f"   ❌ Missing required columns: {missing_cols}")
                print(f"   📋 Available columns: {list(df.columns)}")
                return
            
            # Connect to database
            con = duckdb.connect(self.db_path)
            
            # Get current max ID
            max_id = con.execute("SELECT COALESCE(MAX(id), 0) FROM summarize_model").fetchone()[0]
            
            # Process each row
            new_records = 0
            for idx, row in df.iterrows():
                try:
                    new_id = max_id + idx + 1
                    title = str(row['title']) if pd.notna(row['title']) else f"Record {new_id}"
                    description = str(row['description']) if pd.notna(row['description']) else None
                    desc_length = len(description) if description else 0
                    
                    # Insert record
                    con.execute("""
                        INSERT INTO summarize_model (id, title, description, description_length)
                        VALUES (?, ?, ?, ?)
                    """, (new_id, title, description, desc_length))
                    
                    new_records += 1
                    quality_flag = "🚨" if not description or len(description) < 10 else "✅"
                    print(f"   {quality_flag} Added ID {new_id}: {title[:40]}...")
                    
                except Exception as e:
                    print(f"   ❌ Error processing row {idx}: {e}")
            
            con.close()
            
            # Move processed file to avoid reprocessing
            processed_dir = Path(csv_path).parent / "processed"
            processed_dir.mkdir(exist_ok=True)
            processed_path = processed_dir / f"processed_{int(time.time())}_{os.path.basename(csv_path)}"
            os.rename(csv_path, processed_path)
            
            print(f"✅ Successfully added {new_records} records to database!")
            print(f"📁 File moved to: {processed_path}")
            print(f"🎯 Ready for AI analysis! Run: python ai_layer/summarize.py")
            print("-" * 60)
            
        except Exception as e:
            logging.error(f"Error processing CSV file {csv_path}: {e}")
            print(f"❌ Error: {e}")

def start_live_monitor(watch_folder="demo"):
    """Start monitoring the demo folder for new CSV files."""
    
    # Create demo folder if it doesn't exist
    demo_path = Path(watch_folder)
    demo_path.mkdir(exist_ok=True)
    
    print(f"🎬 LIVE DEMO MONITOR STARTED")
    print(f"👀 Watching folder: {demo_path.absolute()}")
    print(f"📝 Drop CSV files with 'title' and 'description' columns")
    print(f"⚡ Files will be processed automatically and results updated live!")
    print(f"🛑 Press Ctrl+C to stop monitoring")
    print("-" * 60)
    
    # Setup file watcher
    event_handler = CSVFileHandler(config.duckdb_path)
    observer = Observer()
    observer.schedule(event_handler, str(demo_path), recursive=False)
    
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping live monitor...")
        observer.stop()
    
    observer.join()
    print(f"✅ Live monitor stopped")

if __name__ == "__main__":
    start_live_monitor()
