#!/usr/bin/env python3
"""
Advanced Document Intelligence System
Implements three-tier architecture: Query Understanding, Multi-Factor Scoring, Pinpoint Extraction
"""

import json
import numpy as np
import nltk
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from functools import lru_cache
import hashlib

# Global embedding cache
_embedding_cache = {}

@lru_cache(maxsize=1000)
def get_cached_embedding(text: str, model: SentenceTransformer) -> np.ndarray:
    """Cache embeddings for better performance."""
    # Create a hash of the text for caching
    text_hash = hashlib.md5(text.encode()).hexdigest()
    
    if text_hash not in _embedding_cache:
        _embedding_cache[text_hash] = model.encode(text, convert_to_tensor=False)
    
    return _embedding_cache[text_hash]

def batch_encode_texts(texts: List[str], model: SentenceTransformer, batch_size: int = 32) -> List[np.ndarray]:
    """Batch encode texts for better performance."""
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(batch, convert_to_tensor=False, show_progress_bar=False)
        embeddings.extend(batch_embeddings)
    
    return embeddings

def download_nltk_resources():
    """Download required NLTK resources."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

def extract_core_entities(text: str) -> List[str]:
    """Extract core entities (nouns) from text using NLP."""
    download_nltk_resources()
    
    # Tokenize and tag parts of speech
    tokens = nltk.word_tokenize(text.lower())
    pos_tags = nltk.pos_tag(tokens)
    
    # Extract nouns and noun phrases
    entities = []
    for word, tag in pos_tags:
        if tag.startswith('NN') and len(word) > 2:  # Nouns with length > 2
            entities.append(word)
    
    # Extract noun phrases using chunking
    try:
        grammar = r"""
            NP: {<DT|PP\$>?<JJ.*>*<NN.*>+}   # Noun phrases
        """
        chunk_parser = nltk.RegexpParser(grammar)
        chunks = chunk_parser.parse(pos_tags)
        
        for subtree in chunks.subtrees(filter=lambda t: t.label() == 'NP'):
            phrase = ' '.join(word for word, tag in subtree.leaves())
            if len(phrase) > 3:
                entities.append(phrase)
    except:
        pass
    
    return list(set(entities))

def extract_constraints(text: str) -> Dict[str, List[str]]:
    """Extract positive and negative constraints from text."""
    text_lower = text.lower()
    
    # Positive constraint patterns
    positive_patterns = [
        r'\b(vegetarian|vegan|gluten.?free|dairy.?free|nut.?free)\b',
        r'\b(budget.?friendly|affordable|cheap|inexpensive)\b',
        r'\b(quick|fast|easy|simple|convenient)\b',
        r'\b(healthy|organic|natural|fresh)\b',
        r'\b(corporate|business|professional|formal)\b',
        r'\b(group|shared|collaborative|team)\b',
        r'\b(student|youth|young|college)\b',
        r'\b(luxury|premium|high.?end|exclusive)\b',
        r'\b(urgent|immediate|asap|quickly)\b',
        r'\b(comprehensive|detailed|thorough|complete)\b'
    ]
    
    # Negative constraint patterns (what to avoid)
    negative_patterns = [
        r'\b(meat|beef|pork|chicken|fish)\b',
        r'\b(expensive|luxury|premium|high.?end|exclusive)\b',
        r'\b(breakfast|lunch)\b',  # If job is about dinner
        r'\b(slow|complicated|difficult|complex)\b',
        r'\b(unhealthy|processed|artificial)\b',
        r'\b(casual|informal|relaxed)\b',
        r'\b(individual|personal|private)\b',
        r'\b(adult|senior|elderly)\b',
        r'\b(low.?priority|non.?urgent|whenever)\b',
        r'\b(brief|summary|overview|basic)\b'
    ]
    
    positive_constraints = []
    negative_constraints = []
    
    # Extract positive constraints
    for pattern in positive_patterns:
        matches = re.findall(pattern, text_lower)
        positive_constraints.extend(matches)
    
    # Extract negative constraints
    for pattern in negative_patterns:
        matches = re.findall(pattern, text_lower)
        negative_constraints.extend(matches)
    
    # Context-aware negative constraints
    if 'dinner' in text_lower or 'evening' in text_lower:
        negative_constraints.extend(['breakfast', 'lunch', 'morning', 'afternoon'])
    
    if 'budget' in text_lower or 'affordable' in text_lower:
        negative_constraints.extend(['luxury', 'premium', 'expensive', 'high-end'])
    
    if 'vegetarian' in text_lower or 'vegan' in text_lower:
        negative_constraints.extend(['meat', 'beef', 'pork', 'chicken', 'fish'])
    
    return {
        'positive': list(set(positive_constraints)),
        'negative': list(set(negative_constraints))
    }

def extract_semantic_roles(text: str) -> Dict[str, List[str]]:
    """Extract semantic roles for deeper understanding."""
    text_lower = text.lower()
    
    # Action verbs (what they want to do)
    action_patterns = [
        r'\b(prepare|create|plan|organize|arrange|develop)\b',
        r'\b(analyze|review|study|examine|investigate|research)\b',
        r'\b(summarize|summarise|extract|identify|find|locate)\b',
        r'\b(compare|evaluate|assess|measure|calculate)\b'
    ]
    
    # Object entities (what they're working with)
    object_patterns = [
        r'\b(menu|dishes|food|meals|recipes)\b',
        r'\b(documents|papers|reports|data|information)\b',
        r'\b(concepts|topics|subjects|materials|content)\b',
        r'\b(trends|metrics|figures|statistics|results)\b'
    ]
    
    # Modifier patterns (how they want it)
    modifier_patterns = [
        r'\b(vegetarian|vegan|gluten.?free|healthy|organic)\b',
        r'\b(budget|affordable|cost.?effective|inexpensive)\b',
        r'\b(quick|fast|urgent|immediate|asap)\b',
        r'\b(detailed|comprehensive|thorough|complete|extensive)\b',
        r'\b(simple|easy|basic|straightforward|clear)\b'
    ]
    
    actions = []
    objects = []
    modifiers = []
    
    for pattern in action_patterns:
        matches = re.findall(pattern, text_lower)
        actions.extend(matches)
    
    for pattern in object_patterns:
        matches = re.findall(pattern, text_lower)
        objects.extend(matches)
    
    for pattern in modifier_patterns:
        matches = re.findall(pattern, text_lower)
        modifiers.extend(matches)
    
    return {
        'actions': list(set(actions)),
        'objects': list(set(objects)),
        'modifiers': list(set(modifiers))
    }

def analyze_query_structure(persona: str, job_to_be_done: str) -> Dict[str, Any]:
    """
    Deconstruct user request into structured components.
    This is the foundation for universal understanding.
    """
    combined_text = f"{persona} {job_to_be_done}"
    
    # Extract core entities (nouns)
    core_entities = extract_core_entities(combined_text)
    
    # Extract constraints
    constraints = extract_constraints(combined_text)
    
    # Infer context
    context = {
        'group_size': None,
        'age_group': None,
        'urgency': 'normal',
        'complexity': 'medium',
        'domain': 'general'
    }
    
    # Store persona for domain-specific scoring
    persona_info = persona
    
    # Analyze group size
    if any(word in combined_text.lower() for word in ['corporate', 'business', 'team', 'group']):
        context['group_size'] = 'large'
    elif any(word in combined_text.lower() for word in ['individual', 'personal', 'single']):
        context['group_size'] = 'small'
    
    # Analyze age group
    if any(word in combined_text.lower() for word in ['student', 'youth', 'college', 'young']):
        context['age_group'] = 'young'
    elif any(word in combined_text.lower() for word in ['senior', 'elderly', 'adult']):
        context['age_group'] = 'adult'
    
    # Analyze urgency
    if any(word in combined_text.lower() for word in ['urgent', 'asap', 'immediate', 'quickly']):
        context['urgency'] = 'high'
    elif any(word in combined_text.lower() for word in ['whenever', 'no rush', 'take time']):
        context['urgency'] = 'low'
    
    # Analyze complexity
    if any(word in combined_text.lower() for word in ['comprehensive', 'detailed', 'thorough', 'complete']):
        context['complexity'] = 'high'
    elif any(word in combined_text.lower() for word in ['brief', 'summary', 'overview', 'basic']):
        context['complexity'] = 'low'
    
    return {
        'core_entities': core_entities,
        'constraints': constraints,
        'context': context,
        'persona': persona_info
    }

def calculate_dynamic_weights(query_analysis: Dict[str, Any]) -> Tuple[float, float, float, float]:
    """Calculate dynamic weights based on query characteristics."""
    core_entities = query_analysis['core_entities']
    constraints = query_analysis['constraints']
    context = query_analysis['context']
    
    # Base weights
    w1, w2, w3, w4 = 0.4, 0.3, 0.2, 0.1
    
    # Adjust based on query complexity
    if len(core_entities) > 5:
        # Complex query - favor semantic understanding
        w1 += 0.1
        w2 -= 0.05
        w3 -= 0.05
    elif len(core_entities) < 3:
        # Simple query - favor keyword matching
        w1 -= 0.1
        w2 += 0.1
    
    # Adjust based on constraint density
    total_constraints = len(constraints['positive']) + len(constraints['negative'])
    if total_constraints > 3:
        # High constraint query - favor constraint matching
        w2 += 0.1
        w4 += 0.05
        w1 -= 0.1
        w3 -= 0.05
    
    # Adjust based on urgency
    if context['urgency'] == 'high':
        # Urgent query - favor title matches for quick identification
        w3 += 0.1
        w1 -= 0.1
    
    # Normalize weights
    total = w1 + w2 + w3 + w4
    return w1/total, w2/total, w3/total, w4/total

def calculate_multi_factor_score(section: Dict[str, Any], 
                               query_analysis: Dict[str, Any],
                               query_embedding: np.ndarray,
                               model: SentenceTransformer) -> float:
    """
    Multi-factor relevance scoring with weighted components.
    This replaces single similarity scoring with intelligent analysis.
    """
    text = f"{section['section_title']} {section['text']}".lower()
    title = section['section_title'].lower()
    document = section['document'].lower()
    
    # Weights for different factors (tunable)
    w1, w2, w3, w4 = 0.4, 0.3, 0.2, 0.1  # Semantic, Keyword, Title, Penalty
    
    # 1. Semantic Score (w1) - Thematic relevance
    try:
        section_embedding = model.encode(section['text'], convert_to_tensor=False)
        semantic_score = np.dot(query_embedding, section_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(section_embedding)
        )
    except:
        semantic_score = 0.0
    
    # 2. Keyword Score (w2) - Direct term matching
    keyword_score = 0.0
    core_entities = query_analysis['core_entities']
    positive_constraints = query_analysis['constraints']['positive']
    
    # Count matches in text
    for entity in core_entities:
        if entity in text:
            keyword_score += 1.0
    
    for constraint in positive_constraints:
        if constraint in text:
            keyword_score += 1.5  # Higher weight for constraints
    
    # Normalize keyword score
    total_keywords = len(core_entities) + len(positive_constraints)
    if total_keywords > 0:
        keyword_score = keyword_score / total_keywords
    
    # 3. Title Score (w3) - Heavy bonus for title matches
    title_score = 0.0
    for entity in core_entities:
        if entity in title:
            title_score += 2.0  # Heavy bonus for title matches
    
    for constraint in positive_constraints:
        if constraint in title:
            title_score += 2.5  # Even higher bonus for constraint in title
    
    # Normalize title score
    if total_keywords > 0:
        title_score = title_score / total_keywords
    
    # 4. Penalty Score (w4) - Negative constraint violations
    penalty_score = 0.0
    negative_constraints = query_analysis['constraints']['negative']
    
    for constraint in negative_constraints:
        if constraint in text:
            penalty_score += 2.0  # Heavy penalty for negative constraints
    
    # 5. Document Type Priority Score (NEW) - Prioritize main courses
    document_priority_score = 0.0
    
    # Food contractor specific logic
    if 'food contractor' in query_analysis.get('persona', '').lower() or 'menu' in text:
        # Main courses get highest priority
        if 'mains' in document or 'main' in document:
            document_priority_score += 3.0  # Heavy bonus for main courses
        # Entrees and primary dishes
        elif any(keyword in document for keyword in ['entree', 'primary', 'featured']):
            document_priority_score += 2.5
        # Side dishes get lower priority
        elif 'sides' in document or 'side' in document:
            document_priority_score += 1.0  # Lower priority for sides
        # Appetizers and starters
        elif any(keyword in document for keyword in ['appetizer', 'starter', 'breakfast']):
            document_priority_score += 0.5  # Lowest priority for starters
    
    # Academic/Research specific logic
    elif any(keyword in text for keyword in ['research', 'study', 'analysis', 'literature']):
        if 'methodology' in document or 'methods' in document:
            document_priority_score += 2.0
        elif 'results' in document or 'findings' in document:
            document_priority_score += 1.5
        elif 'introduction' in document or 'background' in document:
            document_priority_score += 1.0
    
    # Business/Financial specific logic
    elif any(keyword in text for keyword in ['revenue', 'financial', 'business', 'investment']):
        if 'financial' in document or 'revenue' in document:
            document_priority_score += 2.0
        elif 'strategy' in document or 'analysis' in document:
            document_priority_score += 1.5
        elif 'overview' in document or 'summary' in document:
            document_priority_score += 1.0
    
    # Educational specific logic
    elif any(keyword in text for keyword in ['student', 'study', 'exam', 'preparation']):
        if 'key concepts' in document or 'important' in document:
            document_priority_score += 2.0
        elif 'examples' in document or 'practice' in document:
            document_priority_score += 1.5
        elif 'introduction' in document or 'background' in document:
            document_priority_score += 1.0
    
    # Context bonuses
    context = query_analysis['context']
    
    # Group size bonus
    if context['group_size'] == 'large':
        group_keywords = ['group', 'shared', 'multiple', 'team', 'collaborative', 'batch', 'corporate']
        if any(keyword in text for keyword in group_keywords):
            keyword_score += 0.5
    
    # Age group bonus
    if context['age_group'] == 'young':
        youth_keywords = ['student', 'youth', 'young', 'college', 'budget', 'affordable']
        if any(keyword in text for keyword in youth_keywords):
            keyword_score += 0.3
    
    # Calculate final weighted score with document priority
    final_score = (w1 * semantic_score) + (w2 * keyword_score) + (w3 * title_score) - (w4 * penalty_score) + document_priority_score
    
    return final_score

def intelligent_subsection_analysis(sections: List[Dict[str, Any]], 
                                  model: SentenceTransformer,
                                  query_embedding: np.ndarray,
                                  persona: str,
                                  job_to_be_done: str) -> List[Dict[str, Any]]:
    """
    Pinpoint answer extraction with sentence-level analysis.
    This provides concise, high-value answers instead of text snippets.
    """
    download_nltk_resources()
    
    # Analyze query structure for extraction
    query_analysis = analyze_query_structure(persona, job_to_be_done)
    
    subsection_results = []
    
    # Process top 5 sections for detailed analysis
    for section in sections[:5]:
        text = section['text']
        
        # Split into sentences
        sentences = nltk.sent_tokenize(text)
        
        # Score each sentence
        sentence_scores = []
        for sentence in sentences:
            sentence_score = 0.0
            
            # Score based on core entities
            for entity in query_analysis['core_entities']:
                if entity in sentence.lower():
                    sentence_score += 1.0
            
            # Score based on positive constraints
            for constraint in query_analysis['constraints']['positive']:
                if constraint in sentence.lower():
                    sentence_score += 1.5
            
            # Penalty for negative constraints
            for constraint in query_analysis['constraints']['negative']:
                if constraint in sentence.lower():
                    sentence_score -= 2.0
            
            # Semantic similarity bonus
            try:
                sentence_embedding = model.encode(sentence, convert_to_tensor=False)
                semantic_similarity = np.dot(query_embedding, sentence_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(sentence_embedding)
                )
                sentence_score += semantic_similarity
            except:
                pass
            
            sentence_scores.append((sentence, sentence_score))
        
        # Select top 2-3 highest-scoring sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = sentence_scores[:3]
        
        # Combine into refined text
        refined_text = '. '.join([sentence for sentence, score in top_sentences if score > 0])
        
        if refined_text:
            subsection_results.append({
                'document': section['document'],
                'page_number': section['page_number'],
                'refined_text': refined_text
            })
    
    return subsection_results

def load_json_files(input_json_dir: str) -> List[Dict[str, Any]]:
    """Load JSON files from the input directory."""
    json_dir = Path(input_json_dir)
    doc_structures = []
    
    for json_file in json_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                doc_structure = json.load(f)
                doc_structures.append(doc_structure)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return doc_structures

def extract_sections(doc_structure: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract sections from document structure."""
    sections = []
    
    for section in doc_structure.get('sections', []):
        section_data = {
            'document': doc_structure['filename'],
            'page_number': section.get('page_number', 1),
            'section_title': section.get('heading', 'Unknown'),
            'text': section.get('text', ''),
            'similarity_score': 0.0,
            'importance_rank': 0
        }
        sections.append(section_data)
    
    return sections

def analyze_sections(sections: List[Dict[str, Any]], 
                   model: SentenceTransformer,
                   query_embedding: np.ndarray,
                   persona: str,
                   job_to_be_done: str) -> List[Dict[str, Any]]:
    """
    Analyze and rank sections using advanced multi-factor scoring.
    """
    # Analyze query structure
    query_analysis = analyze_query_structure(persona, job_to_be_done)
    
    # Calculate multi-factor scores for each section
    for section in sections:
        section['similarity_score'] = calculate_multi_factor_score(
            section, query_analysis, query_embedding, model
        )
    
    # Sort sections by score
    ranked_sections = sorted(sections, key=lambda x: x['similarity_score'], reverse=True)
    
    # Add importance rank
    for i, section in enumerate(ranked_sections):
        section['importance_rank'] = i + 1
    
    return ranked_sections

def analyze_subsections(ranked_sections: List[Dict[str, Any]],
                       model: SentenceTransformer,
                       query_embedding: np.ndarray,
                       persona: str,
                       job_to_be_done: str) -> List[Dict[str, Any]]:
    """
    Perform intelligent sub-section analysis with pinpoint extraction.
    """
    return intelligent_subsection_analysis(
        ranked_sections, model, query_embedding, persona, job_to_be_done
    )

def calculate_confidence_score(section: Dict[str, Any], query_analysis: Dict[str, Any]) -> float:
    """Calculate confidence in the relevance of a section."""
    text = f"{section['section_title']} {section['text']}".lower()
    
    # Factors that increase confidence
    confidence_factors = 0.0
    
    # Title match confidence
    title = section['section_title'].lower()
    if any(entity in title for entity in query_analysis['core_entities']):
        confidence_factors += 0.3
    
    # Constraint match confidence
    positive_matches = sum(1 for constraint in query_analysis['constraints']['positive'] 
                          if constraint in text)
    negative_matches = sum(1 for constraint in query_analysis['constraints']['negative'] 
                          if constraint in text)
    
    confidence_factors += (positive_matches * 0.2) - (negative_matches * 0.3)
    
    # Document type confidence
    document = section['document'].lower()
    if 'mains' in document and 'food contractor' in query_analysis.get('persona', '').lower():
        confidence_factors += 0.2
    
    # Text length confidence (not too short, not too long)
    text_length = len(section['text'])
    if 100 <= text_length <= 1000:
        confidence_factors += 0.1
    
    return min(1.0, max(0.0, confidence_factors))

def generate_performance_metrics(ranked_sections: List[Dict[str, Any]], 
                               query_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate performance metrics for the ranking."""
    metrics = {
        'total_sections': len(ranked_sections),
        'avg_confidence': 0.0,
        'domain_coverage': 0.0,
        'constraint_satisfaction': 0.0
    }
    
    if ranked_sections:
        # Average confidence
        confidences = [calculate_confidence_score(section, query_analysis) 
                      for section in ranked_sections[:10]]
        metrics['avg_confidence'] = sum(confidences) / len(confidences)
        
        # Domain coverage (unique documents)
        unique_docs = len(set(section['document'] for section in ranked_sections[:10]))
        metrics['domain_coverage'] = unique_docs / min(10, len(ranked_sections))
        
        # Constraint satisfaction
        satisfied_constraints = 0
        total_constraints = len(query_analysis['constraints']['positive'])
        
        for section in ranked_sections[:5]:
            text = f"{section['section_title']} {section['text']}".lower()
            for constraint in query_analysis['constraints']['positive']:
                if constraint in text:
                    satisfied_constraints += 1
        
        if total_constraints > 0:
            metrics['constraint_satisfaction'] = satisfied_constraints / total_constraints
    
    return metrics

def main():
    """Main function for testing."""
    # This would be called by process_input.py
    pass

if __name__ == "__main__":
    main()