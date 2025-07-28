#!/usr/bin/env python3
"""
Show Results Script
Displays the output in a readable format
"""

import json
import sys

def show_results():
    """Display the results from the output file."""
    try:
        # Load the output file
        with open('output_dir/output_food_contractor.json', 'r') as f:
            data = json.load(f)
        
        print("🎉 HACKATHON RESULTS 🎉")
        print("=" * 50)
        
        # Show metadata
        print(f"👤 Persona: {data['metadata']['persona']}")
        print(f"📝 Task: {data['metadata']['job_to_be_done']}")
        print(f"📊 Total Sections Found: {len(data['extracted_sections'])}")
        print()
        
        # Show top 10 results
        print("🏆 TOP 10 RECOMMENDED MENU ITEMS:")
        print("-" * 40)
        for i, item in enumerate(data['extracted_sections'][:10], 1):
            print(f"{i:2d}. {item['section_title']}")
            print(f"    📄 From: {item['document']}")
            print()
        
        # Show sub-section analysis
        print("🔍 DETAILED ANALYSIS (Top 5):")
        print("-" * 40)
        for i, item in enumerate(data['sub-section_analysis'][:5], 1):
            print(f"{i}. {item['document']}")
            print(f"   💡 Key Points: {item['refined_text']}")
            print()
            
        print("✅ Analysis Complete!")
        
    except FileNotFoundError:
        print("❌ Error: output_food_contractor.json not found!")
        print("Run 'python process_input.py' first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    show_results() 