#!/usr/bin/env python3
"""
Hackathon Input Processor
Reads input.json file and processes documents automatically
"""

import json
import os
import sys
from pathlib import Path
from main import load_json_files, extract_sections, analyze_sections, analyze_subsections
from sentence_transformers import SentenceTransformer
from datetime import datetime
from pdf_parser import create_json_from_pdfs

def load_input_json(input_file: str) -> dict:
    """Load the input.json file provided by the hackathon."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)

def create_json_from_documents(documents_dir: str, input_data: dict) -> str:
    """Create JSON files from actual PDF documents using the PDF parser."""
    return create_json_from_pdfs(documents_dir, input_data)

def process_challenge(input_file: str = "input.json"):
    """Main function to process the hackathon challenge."""
    print("🚀 Processing Hackathon Challenge...")
    
    # Load input data
    input_data = load_input_json(input_file)
    
    # Extract challenge information
    challenge_info = input_data.get('challenge_info', {})
    persona = input_data.get('persona', {})
    job_to_be_done = input_data.get('job_to_be_done', {})
    
    print(f"📋 Challenge ID: {challenge_info.get('challenge_id', 'Unknown')}")
    print(f"🎯 Test Case: {challenge_info.get('test_case_name', 'Unknown')}")
    print(f"👤 Persona: {persona.get('role', 'Unknown')}")
    print(f"📝 Task: {job_to_be_done.get('task', 'Unknown')}")
    
    # Use existing JSON files (created by create_real_json.py)
    print("📄 Using existing document structure...")
    json_dir = "input_json_dir"
    
    # Prepare arguments for main processing
    persona_role = persona.get('role', 'Unknown')
    task = job_to_be_done.get('task', 'Unknown')
    
    # Create output directory
    output_dir = Path("output_dir")
    output_dir.mkdir(exist_ok=True)
    
    # Load model
    print("🤖 Loading AI model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Load document structures
    print("📚 Loading documents...")
    doc_structures = load_json_files(json_dir)
    
    # Extract sections from all documents
    all_sections = []
    for doc in doc_structures:
        all_sections.extend(extract_sections(doc))
    
    print(f"📊 Found {len(all_sections)} sections across {len(doc_structures)} documents")
    
    # Generate query embedding
    query_text = f"{persona_role} {task}"
    query_embedding = model.encode(query_text, convert_to_tensor=False)
    
    # Analyze sections with advanced ranking
    print("🧠 Analyzing sections with advanced NLP...")
    ranked_sections = analyze_sections(all_sections, model, query_embedding, persona_role, task)
    
    # Analyze subsections
    print("🔍 Performing intelligent sub-section analysis...")
    subsection_analysis = analyze_subsections(ranked_sections, model, query_embedding, persona_role, task)
    
    # Prepare output
    output = {
        "metadata": {
            "challenge_info": challenge_info,
            "input_documents": [doc['filename'] for doc in doc_structures],
            "persona": persona_role,
            "job_to_be_done": task,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [
            {
                "document": section['document'],
                "page_number": section['page_number'],
                "section_title": section['section_title'],
                "importance_rank": section['importance_rank']
            }
            for section in ranked_sections[:10]  # Top 10 sections
        ],
        "sub-section_analysis": subsection_analysis
    }
    
    # Create persona-specific filename
    persona_name = persona_role.replace(" ", "_").replace("-", "_").lower()
    output_filename = f"output_{persona_name}.json"
    
    # Save output
    output_path = output_dir / output_filename
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Output saved as: {output_filename}")
    print(f"📁 Location: {output_path.absolute()}")
    print("🎉 Challenge processing completed successfully!")

if __name__ == "__main__":
    # Check if input file is provided as argument
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.json"
    process_challenge(input_file) 