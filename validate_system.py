#!/usr/bin/env python3
"""
Advanced System Validation
Tests the system across multiple domains and scenarios
"""

import json
import time
from typing import Dict, List, Any
from main import analyze_query_structure, calculate_multi_factor_score
from sentence_transformers import SentenceTransformer

def load_test_cases() -> List[Dict[str, Any]]:
    """Load comprehensive test cases."""
    return [
        {
            "name": "Food Contractor - Buffet Menu",
            "persona": "Food Contractor",
            "job": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items.",
            "expected_entities": ["menu", "dinner", "buffet", "gathering"],
            "expected_constraints": ["vegetarian", "gluten-free", "corporate"],
            "expected_priority": "mains"
        },
        {
            "name": "PhD Researcher - Literature Review",
            "persona": "PhD Researcher in Computational Biology",
            "job": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks",
            "expected_entities": ["literature", "review", "methodologies", "datasets", "benchmarks"],
            "expected_constraints": ["comprehensive", "detailed", "thorough"],
            "expected_priority": "methodology"
        },
        {
            "name": "Investment Analyst - Financial Analysis",
            "persona": "Investment Analyst",
            "job": "Analyze revenue trends, R&D investments, and market positioning strategies",
            "expected_entities": ["revenue", "trends", "investments", "strategies"],
            "expected_constraints": ["detailed", "comprehensive", "analytical"],
            "expected_priority": "financial"
        },
        {
            "name": "Chemistry Student - Exam Preparation",
            "persona": "Undergraduate Chemistry Student",
            "job": "Identify key concepts and mechanisms for exam preparation on reaction kinetics",
            "expected_entities": ["concepts", "mechanisms", "kinetics", "preparation"],
            "expected_constraints": ["key", "important", "essential"],
            "expected_priority": "key_concepts"
        }
    ]

def validate_query_understanding(test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate query understanding capabilities."""
    results = {
        "total_tests": len(test_cases),
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for test_case in test_cases:
        try:
            # Analyze query structure
            analysis = analyze_query_structure(test_case["persona"], test_case["job"])
            
            # Check entity extraction
            entities_found = len(set(analysis["core_entities"]) & set(test_case["expected_entities"]))
            entity_score = entities_found / len(test_case["expected_entities"])
            
            # Check constraint extraction
            constraints_found = len(set(analysis["constraints"]["positive"]) & set(test_case["expected_constraints"]))
            constraint_score = constraints_found / len(test_case["expected_constraints"])
            
            # Overall score
            overall_score = (entity_score + constraint_score) / 2
            
            test_result = {
                "name": test_case["name"],
                "entity_score": entity_score,
                "constraint_score": constraint_score,
                "overall_score": overall_score,
                "passed": overall_score >= 0.7
            }
            
            results["details"].append(test_result)
            
            if test_result["passed"]:
                results["passed"] += 1
            else:
                results["failed"] += 1
                
        except Exception as e:
            results["details"].append({
                "name": test_case["name"],
                "error": str(e),
                "passed": False
            })
            results["failed"] += 1
    
    return results

def validate_performance() -> Dict[str, Any]:
    """Validate system performance."""
    results = {
        "model_loading": 0,
        "embedding_generation": 0,
        "query_analysis": 0,
        "scoring": 0
    }
    
    try:
        # Test model loading time
        start_time = time.time()
        model = SentenceTransformer('all-MiniLM-L6-v2')
        results["model_loading"] = time.time() - start_time
        
        # Test embedding generation
        start_time = time.time()
        test_texts = ["This is a test document", "Another test document", "Third test document"]
        embeddings = model.encode(test_texts, convert_to_tensor=False)
        results["embedding_generation"] = time.time() - start_time
        
        # Test query analysis
        start_time = time.time()
        analysis = analyze_query_structure("Test Persona", "Test job to be done")
        results["query_analysis"] = time.time() - start_time
        
        # Test scoring
        start_time = time.time()
        test_section = {
            "section_title": "Test Section",
            "text": "This is a test section content",
            "document": "test.pdf"
        }
        query_embedding = model.encode("test query", convert_to_tensor=False)
        score = calculate_multi_factor_score(test_section, analysis, query_embedding, model)
        results["scoring"] = time.time() - start_time
        
    except Exception as e:
        results["error"] = str(e)
    
    return results

def run_comprehensive_validation():
    """Run comprehensive system validation."""
    print("🚀 Starting Comprehensive System Validation...")
    print("=" * 60)
    
    # Load test cases
    test_cases = load_test_cases()
    
    # Validate query understanding
    print("\n📊 Testing Query Understanding...")
    understanding_results = validate_query_understanding(test_cases)
    
    print(f"✅ Passed: {understanding_results['passed']}/{understanding_results['total_tests']}")
    print(f"❌ Failed: {understanding_results['failed']}/{understanding_results['total_tests']}")
    
    for detail in understanding_results["details"]:
        status = "✅" if detail["passed"] else "❌"
        print(f"  {status} {detail['name']}: {detail.get('overall_score', 0):.2f}")
    
    # Validate performance
    print("\n⚡ Testing Performance...")
    performance_results = validate_performance()
    
    if "error" not in performance_results:
        print(f"✅ Model Loading: {performance_results['model_loading']:.3f}s")
        print(f"✅ Embedding Generation: {performance_results['embedding_generation']:.3f}s")
        print(f"✅ Query Analysis: {performance_results['query_analysis']:.3f}s")
        print(f"✅ Scoring: {performance_results['scoring']:.3f}s")
    else:
        print(f"❌ Performance Test Error: {performance_results['error']}")
    
    # Overall assessment
    print("\n🎯 Overall Assessment:")
    if understanding_results["passed"] == understanding_results["total_tests"]:
        print("✅ System is ready for hackathon submission!")
    else:
        print("⚠️  Some tests failed. Review and fix issues.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_comprehensive_validation() 