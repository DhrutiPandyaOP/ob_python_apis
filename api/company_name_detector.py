
# ===========================
# File: api/company_name_detector.py
# ===========================
from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer, util
from difflib import SequenceMatcher
import numpy as np
import re
from logger_config import Logger

# Create blueprint
bp = Blueprint('company_name_detector', __name__)
logger = Logger.get_logger()

# Load model once (global)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Enhanced placeholder patterns
PLACEHOLDER_PATTERNS = [
    "YOUR COMPANY", "YOUR BRAND", "COMPANY NAME", "INDUSTRY NAME", "SOCCER CLUB", "BRAND NAME", "SCHOOL NAME", "SALON NAME","THE CHURCH NAME","Catering Service",
    "CHURCH NAME", "COLLEGE NAME", "ENTERPRISE NAME", "BOOK STORE", "SHOP NAME","HVAC SERVICE","CAFE NAME",
    "STORE FOUNDATION", "ANY ASSOCIATION", "ORGANISER NAME", "FARM NAME",
    "FOOD STALL", "PUBLICATION NAME", "WRITE COMPANY NAME", "UNIVERSITY NAME",
    "ORGANIZATION NAME", "FIRM NAME", "AGENCY NAME", "STUDIO NAME", "CLINIC NAME",
    "HOSPITAL NAME", "RESTAURANT NAME", "HOTEL NAME", "BANK NAME", "INSURANCE NAME","CLEANING SERVICE",
    "COMPANY TITLE", "BRAND TITLE", "ORGANIZATION TITLE", "CLUB NAME", "YOUR CLUB NAME","CLEANING CLASSES", "CLEANING CLASS",
    "BUSINESS NAME", "CORPORATION NAME", "ENTERPRISE TITLE", "ESTABLISHMENT NAME",
    "INSTITUTION NAME", "VENUE NAME", "SERVICE NAME", "CENTER NAME", "GROUP NAME",
    "ASSOCIATION NAME", "FOUNDATION NAME", "SOCIETY NAME", "UNION NAME", "LEAGUE NAME",
    "COOPERATIVE NAME", "PARTNERSHIP NAME", "LLC NAME", "INC NAME", "CORP NAME",
    "INSERT COMPANY NAME", "ADD COMPANY NAME", "ENTER COMPANY NAME",
    "COMPANY NAME HERE", "YOUR BUSINESS NAME", "BUSINESS NAME HERE",
    "ORGANIZATION NAME HERE", "BRAND NAME HERE", "NAME OF COMPANY",
    "NAME OF ORGANIZATION", "NAME OF BUSINESS", "COMPANY/ORGANIZATION NAME"
]

# Regex patterns
REGEX_PATTERNS = [
    r'\[.*?(?:company|business|organization|brand|name).*?\]',
    r'\{.*?(?:company|business|organization|brand|name).*?\}',
    r'\(.*?(?:company|business|organization|brand|name).*?\)',
    r'<.*?(?:company|business|organization|brand|name).*?>',
    r'___+\s*(?:company|business|organization|brand|name).*?___+',
    r'\.\.\.+\s*(?:company|business|organization|brand|name)',
    r'(?:company|business|organization|brand|name)\s*\.\.\.+',
    r'_+(?:company|business|organization|brand|name)_+',
    r'\*+(?:company|business|organization|brand|name)\*+',
]

class AdvancedPlaceholderDetector:
    def __init__(self):
        self.model = model
        self.placeholder_patterns = PLACEHOLDER_PATTERNS
        self.regex_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in REGEX_PATTERNS]
        
        self.normalized_placeholders = [self.normalize_text(p) for p in self.placeholder_patterns]
        self.placeholder_embeddings = self.model.encode(self.normalized_placeholders, convert_to_tensor=True)
        
        self.sentence_indicators = [
            'the', 'a', 'an', 'this', 'that', 'these', 'those', 'our', 'their', 'his', 'her',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'will', 'would', 'could', 'should', 'must', 'can', 'may', 'might',
            'in', 'on', 'at', 'by', 'for', 'with', 'to', 'from', 'of', 'about'
        ]

    def normalize_text(self, text):
        if not text:
            return ""
        normalized = re.sub(r'\s+', ' ', text.strip().lower())
        normalized = re.sub(r'[^\w\s\[\](){}><_.*-]', '', normalized)
        return normalized

    def is_standalone_text(self, text, context_texts=None):
        normalized = self.normalize_text(text)
        words = normalized.split()
        
        if len(words) > 6:
            return False
        
        for word in words:
            if word in self.sentence_indicators:
                return False
        
        sentence_patterns = [
            r'\b(?:the|a|an)\s+\w+',
            r'\w+\s+(?:is|are|was|were|will|would)\s+',
            r'\w+\s+(?:has|have|had)\s+',
            r'(?:in|on|at|by|for|with|to|from)\s+\w+',
        ]
        
        for pattern in sentence_patterns:
            if re.search(pattern, normalized):
                return False
        
        if text.strip().endswith(('.', '!', '?', ';')):
            return False
        
        verb_patterns = [
            r'\b(?:provide|offer|deliver|create|make|build|develop|design|sell|buy)\b',
            r'\b(?:specializes?|focuses?|operates?|manages?|handles?)\b'
        ]
        
        for pattern in verb_patterns:
            if re.search(pattern, normalized):
                return False
        
        return True

    def exact_pattern_match(self, text):
        normalized = self.normalize_text(text)
        
        for pattern in self.normalized_placeholders:
            if normalized == pattern:
                return True, 1.0
        
        for regex_pattern in self.regex_patterns:
            if regex_pattern.search(text):
                return True, 0.95
        
        return False, 0.0

    def format_analysis(self, text):
        score = 0.0
        
        if text.isupper():
            score += 0.3
        
        if re.search(r'[\[\](){}><]', text):
            score += 0.4
        
        if re.search(r'[_.]{2,}', text):
            score += 0.3
        
        placeholder_words = ['company', 'business', 'organization', 'brand', 'name', 'your', 'insert', 'add', 'enter', 'classes', 'salon', 'service']
        text_lower = text.lower()
        for word in placeholder_words:
            if word in text_lower:
                score += 0.2
                break
        
        return min(score, 1.0)

    def semantic_similarity(self, texts):
        normalized_texts = [self.normalize_text(t) for t in texts]
        
        if not any(normalized_texts):
            return [0.0] * len(texts)
        
        text_embeddings = self.model.encode(normalized_texts, convert_to_tensor=True)
        cosine_scores = util.cos_sim(text_embeddings, self.placeholder_embeddings)
        max_scores = cosine_scores.max(dim=1).values.cpu().numpy()
        
        return max_scores.tolist()

    def fuzzy_matching(self, text):
        normalized = self.normalize_text(text)
        
        if not normalized:
            return 0.0
        
        scores = []
        
        for pattern in self.normalized_placeholders:
            scores.append(SequenceMatcher(None, normalized, pattern).ratio())
        
        text_words = set(normalized.split())
        for pattern in self.normalized_placeholders:
            pattern_words = set(pattern.split())
            if text_words and pattern_words:
                jaccard = len(text_words.intersection(pattern_words)) / len(text_words.union(pattern_words))
                scores.append(jaccard)
        
        return max(scores) if scores else 0.0

    def detect_placeholder(self, text_json, semantic_weight=0.4, fuzzy_weight=0.3, format_weight=0.3, threshold=0.75):
        if not text_json:
            return None
        
        texts = [item.get("text", "").strip() for item in text_json]
        indices = [item.get("index", i) for i, item in enumerate(text_json)]
        
        results = []
        
        for i, text in enumerate(texts):
            if not text:
                continue
            
            if not self.is_standalone_text(text):
                continue
            
            is_exact_match, exact_score = self.exact_pattern_match(text)
            if is_exact_match:
                return {
                    "status_code": 200,
                    "data": {
                        "company_name": text,
                        "index": indices[i],
                        "similarity": exact_score,
                        "confidence": "VERY_HIGH",
                        "detection_method": "EXACT_PATTERN_MATCH"
                    }
                }
            
            semantic_score = self.semantic_similarity([text])[0]
            fuzzy_score = self.fuzzy_matching(text)
            format_score = self.format_analysis(text)
            
            combined_score = (
                semantic_weight * semantic_score +
                fuzzy_weight * fuzzy_score +
                format_weight * format_score
            )
            
            results.append({
                "text": text,
                "index": indices[i],
                "semantic_score": semantic_score,
                "fuzzy_score": fuzzy_score,
                "format_score": format_score,
                "combined_score": combined_score
            })
        
        if not results:
            return None
        
        best_result = max(results, key=lambda x: x["combined_score"])
        
        if best_result["combined_score"] < threshold:
            return None
        
        score = best_result["combined_score"]
        if score >= 0.9:
            confidence = "VERY_HIGH"
        elif score >= 0.8:
            confidence = "HIGH"
        elif score >= 0.75:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        return {
            "status_code": 200,
            "data": {
                "company_name": best_result["text"],
                "index": best_result["index"],
                "similarity": round(best_result["combined_score"], 4),
                "confidence": confidence,
                "detection_method": "MULTI_FACTOR_ANALYSIS",
                "score_breakdown": {
                    "semantic": round(best_result["semantic_score"], 4),
                    "fuzzy": round(best_result["fuzzy_score"], 4),
                    "format": round(best_result["format_score"], 4)
                }
            }
        }

# Initialize detector
detector = AdvancedPlaceholderDetector()

@bp.route('/detect-company-name', methods=['POST'])
def detect_placeholder():
    try:
        content = request.get_json()
        
        if not content:
            logger.error("No JSON data provided")
            return jsonify({"status_code": 400, "error": "No JSON data provided"}), 400
        
        text_json = content.get("text_json", [])
        
        if not isinstance(text_json, list):
            logger.error("text_json must be a list")
            return jsonify({"status_code": 400, "error": "text_json must be a list"}), 400
        
        threshold = content.get("threshold", 0.75)
        semantic_weight = content.get("semantic_weight", 0.4)
        fuzzy_weight = content.get("fuzzy_weight", 0.3)
        format_weight = content.get("format_weight", 0.3)
        
        result = detector.detect_placeholder(
            text_json,
            semantic_weight=semantic_weight,
            fuzzy_weight=fuzzy_weight,
            format_weight=format_weight,
            threshold=threshold
        )
        
        if result:
            return jsonify(result), 200
        else:
            logger.info("No placeholder match found")
            return jsonify({
                "status_code": 201,
                "error": "No strong placeholder match found",
                "message": "No standalone company name placeholders detected above threshold"
            }), 200
    
    except Exception as e:
        logger.error(f"Company name detection error: {str(e)}")
        return jsonify({
            "status_code": 500,
            "error": f"Internal server error: {str(e)}"
        }), 500
