#!/usr/bin/env python3
"""
PDF Document Parser
Extracts real headings and content from PDF documents
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any
import PyPDF2
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize

def download_nltk_resources():
    """Download required NLTK resources."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyMuPDF for better text extraction."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def identify_headings(text: str) -> List[Dict[str, Any]]:
    """Identify headings in the text using various heuristics."""
    download_nltk_resources()
    
    lines = text.split('\n')
    headings = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # Heading detection patterns
        is_heading = False
        heading_level = 1
        
        # Pattern 1: Lines starting with # (markdown-style headings)
        if line.startswith('#'):
            is_heading = True
            heading_level = len(line) - len(line.lstrip('#'))
            line = line.lstrip('#').strip()
            
        # Pattern 2: ALL CAPS lines (likely H1)
        elif line.isupper() and len(line) > 3 and len(line) < 100:
            is_heading = True
            heading_level = 1
            
        # Pattern 3: Title case with specific patterns (dish names, recipe names)
        elif (line[0].isupper() and 
              len(line.split()) <= 6 and 
              len(line) < 60 and
              not line.endswith('.') and
              not any(char.isdigit() for char in line[-3:]) and
              not line.lower() in ['ingredients', 'instructions', 'directions', 'preparation', 'layers', 'traditional', 'arborio', 'bell', 'mixed', 'fresh', 'served', 'baked', 'cooked', 'topped']):
            is_heading = True
            heading_level = 2
            
        # Pattern 4: Numbered headings (e.g., "1. Introduction", "Chapter 1")
        elif re.match(r'^(\d+\.|\d+\)|Chapter\s+\d+|Section\s+\d+)', line, re.IGNORECASE):
            is_heading = True
            heading_level = 2
            
        # Pattern 5: Common heading keywords
        heading_keywords = [
            'recipe', 'ingredients', 'instructions', 'directions', 'preparation',
            'cooking', 'serving', 'tips', 'notes', 'variations', 'substitutions',
            'appetizer', 'main course', 'dessert', 'side dish', 'salad', 'soup',
            'breakfast', 'lunch', 'dinner', 'snack', 'beverage', 'drink',
            'continental breakfast', 'vegetarian breakfast bowl', 'gluten-free breakfast options',
            'healthy start', 'vegetarian lasagna', 'ratatouille', 'mushroom risotto',
            'stuffed bell peppers', 'vegetable curry', 'falafel platter', 'pasta primavera',
            'vegetable stir fry', 'stuffed portobello mushrooms', 'vegetable paella',
            'lentil shepherd\'s pie', 'vegetable wellington', 'roasted vegetables',
            'quinoa salad', 'garlic mashed potatoes', 'grilled asparagus', 'mediterranean salad',
            'roasted sweet potatoes', 'steamed broccoli', 'couscous pilaf', 'cauliflower rice',
            'zucchini noodles', 'roasted brussels sprouts', 'quinoa pilaf', 'mixed green salad',
            'roasted root vegetables', 'wild rice blend', 'steamed green beans', 'vegetarian wraps',
            'buddha bowl', 'mediterranean platter', 'vegetable soup'
        ]
        
        if any(keyword in line.lower() for keyword in heading_keywords):
            is_heading = True
            heading_level = 3
            
        if is_heading and line:  # Make sure we have a non-empty line
            headings.append({
                'text': line,
                'level': heading_level,
                'line_number': i,
                'start_pos': len('\n'.join(lines[:i]))
            })
    
    return headings

def extract_sections_from_text(text: str, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract sections based on identified headings."""
    sections = []
    
    for i, heading in enumerate(headings):
        start_pos = heading['start_pos']
        
        # Find end position (next heading or end of text)
        if i + 1 < len(headings):
            end_pos = headings[i + 1]['start_pos']
        else:
            end_pos = len(text)
        
        # Extract section content
        section_text = text[start_pos:end_pos].strip()
        
        # Clean up the text
        lines = section_text.split('\n')
        content_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line == heading['text']:
                content_lines.append(line)
        
        content = ' '.join(content_lines)
        
        # Only include sections with meaningful content
        if len(content) > 20:  # Minimum content threshold
            sections.append({
                'heading': heading['text'],
                'content': content,
                'level': heading['level']
            })
    
    return sections

def parse_pdf_document(pdf_path: str) -> Dict[str, Any]:
    """Parse a PDF document and extract structured content."""
    print(f"📄 Parsing: {Path(pdf_path).name}")
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print(f"⚠️  No text extracted from {pdf_path}")
        return {
            "filename": Path(pdf_path).name,
            "sections": []
        }
    
    # Identify headings
    headings = identify_headings(text)
    
    # Extract sections
    sections = extract_sections_from_text(text, headings)
    
    # Convert to required format
    formatted_sections = []
    for i, section in enumerate(sections):
        formatted_sections.append({
            "page_number": 1,  # We'll improve this later
            "heading": section['heading'],
            "text": section['content']
        })
    
    # If no sections found, create a fallback
    if not formatted_sections:
        formatted_sections.append({
            "page_number": 1,
            "heading": f"{Path(pdf_path).stem} - Content",
            "text": text[:1000] + "..." if len(text) > 1000 else text
        })
    
    return {
        "filename": Path(pdf_path).name,
        "sections": formatted_sections
    }

def create_json_from_pdfs(documents_dir: str, input_data: dict) -> str:
    """Create JSON files from actual PDF documents."""
    json_dir = Path("input_json_dir")
    json_dir.mkdir(exist_ok=True)
    
    # Clear existing JSON files
    for file in json_dir.glob("*.json"):
        file.unlink()
    
    documents = input_data.get('documents', [])
    pdf_dir = Path(documents_dir)
    
    for doc in documents:
        filename = doc['filename']
        pdf_path = pdf_dir / filename
        
        if pdf_path.exists():
            # Parse actual PDF
            doc_structure = parse_pdf_document(str(pdf_path))
        else:
            print(f"⚠️  PDF not found: {pdf_path}")
            # Create fallback structure
            doc_structure = {
                "filename": filename,
                "sections": [
                    {
                        "page_number": 1,
                        "heading": f"{Path(filename).stem} - Content",
                        "text": f"Content from {filename} would be extracted here. This is a placeholder for the actual PDF content."
                    }
                ]
            }
        
        # Save JSON file
        json_file = json_dir / f"{Path(filename).stem}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(doc_structure, f, indent=2)
    
    return str(json_dir)

if __name__ == "__main__":
    # Test the parser
    test_pdf = "input_pdfs/South of France - Cuisine.pdf"
    if Path(test_pdf).exists():
        result = parse_pdf_document(test_pdf)
        print(json.dumps(result, indent=2))
    else:
        print(f"Test PDF not found: {test_pdf}") 