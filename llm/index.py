"""
Skill Extractor — Hands-on practice for noon SDE-2 interview
Uses Claude API (Anthropic) to extract skills from resumes.

Setup:
1. pip install anthropic
2. Set your API key: export ANTHROPIC_API_KEY="sk-ant-..."
3. Run: python skill_extractor.py

What this demonstrates:
- System prompts and user messages
- Structured JSON output
- Error handling with retries
- Cost tracking
- Fallback strategy
"""

import os
import json
import time
import hashlib
from anthropic import Anthropic, APIError

# ============================================
# Setup
# ============================================

client = Anthropic(api_key="<API KEY>")

# Simple in-memory cache
cache = {}

# Cost tracking (Claude Sonnet 4 pricing)
total_cost = 0.0
PRICE_INPUT = 3.0 / 1_000_000   # $3 per 1M input tokens
PRICE_OUTPUT = 15.0 / 1_000_000  # $15 per 1M output tokens


# ============================================
# Core function with all production patterns
# ============================================

def extract_skills(resume_text: str, max_retries: int = 3) -> dict:
    """
    Extract skills from a resume using Claude.
    
    Production patterns used:
    - Caching (same resume → same result)
    - Retry with exponential backoff
    - Structured JSON output
    - Cost tracking
    - Fallback on failure
    """
    global total_cost
    
    # 1. Check cache first (save costs)
    cache_key = hashlib.md5(resume_text.encode()).hexdigest()
    if cache_key in cache:
        print("Cache HIT - no API call made")
        return cache[cache_key]
    
    # 2. Build the prompt
    system_prompt = """You are a resume parsing expert.
Extract technical skills from the given resume.

Rules:
- Only extract hard technical skills (languages, frameworks, tools, databases, cloud)
- Ignore soft skills like "teamwork", "communication", "leadership"
- Extract years of experience per skill ONLY if explicitly mentioned
- Return total years of professional experience if mentioned

Output format: valid JSON only, no explanations, no markdown."""
    
    user_prompt = f"""Extract skills from this resume:

{resume_text}

Return JSON with this exact structure:
{{
  "total_years_experience": <number or null>,
  "skills": [
    {{"name": "<skill>", "years": <number or null>}}
  ]
}}"""
    
    # 3. Try with retries and exponential backoff
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                temperature=0.0,  # Deterministic for extraction
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            # 4. Track cost
            input_cost = response.usage.input_tokens * PRICE_INPUT
            output_cost = response.usage.output_tokens * PRICE_OUTPUT
            cost = input_cost + output_cost
            total_cost += cost
            
            print(f"API call - tokens: {response.usage.input_tokens} in, "
                  f"{response.usage.output_tokens} out | cost: ${cost:.5f}")
            
            # 5. Parse JSON
            content = response.content[0].text.strip()
            
            # Strip markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            result = json.loads(content)
            
            # 6. Cache successful result
            cache[cache_key] = result
            return result
            
        except json.JSONDecodeError as e:
            print(f"Attempt {attempt + 1}: JSON parse error - {e}")
            if attempt == max_retries - 1:
                return fallback_extraction(resume_text)
                
        except APIError as e:
            wait = 2 ** attempt  # 1s, 2s, 4s
            print(f"Attempt {attempt + 1}: API error - {e}. Retrying in {wait}s")
            time.sleep(wait)
    
    # All retries failed - use fallback
    return fallback_extraction(resume_text)


def fallback_extraction(resume_text: str) -> dict:
    """
    Simple regex-based fallback when LLM fails.
    Not as good as LLM but ensures the service stays up.
    """
    import re
    
    print("Using fallback extraction (regex-based)")
    
    # Common technical keywords (extend this list in production)
    tech_keywords = [
        "python", "java", "javascript", "typescript", "go", "rust",
        "django", "flask", "fastapi", "spring", "react", "node",
        "postgresql", "mysql", "mongodb", "redis", "kafka",
        "aws", "gcp", "azure", "docker", "kubernetes",
        "openai", "claude", "llm", "mcp", "vertex ai"
    ]
    
    found = []
    text_lower = resume_text.lower()
    for keyword in tech_keywords:
        if keyword in text_lower:
            found.append({"name": keyword, "years": None})
    
    return {
        "total_years_experience": None,
        "skills": found,
        "_fallback": True  # flag so caller knows
    }


# ============================================
# Hallucination detector
# ============================================

def detect_hallucinations(resume_text: str, extracted: dict) -> list:
    """
    Check if extracted skills actually exist in the resume.
    This is an evaluation technique the JD mentions.
    """
    hallucinations = []
    text_lower = resume_text.lower()
    
    for skill in extracted.get("skills", []):
        skill_name = skill["name"].lower()
        if skill_name not in text_lower:
            hallucinations.append(skill["name"])
    
    return hallucinations


# ============================================
# Run it!
# ============================================

if __name__ == "__main__":
    
    # Test resume
    resume = """
    Deepak Raju
    Senior Software Engineer with 8 years of experience.
    
    Skills:
    - 6 years of Python (Django, Flask)
    - 3 years of Node.js
    - AWS deployment (EC2, S3, Lambda)
    - PostgreSQL and MongoDB
    - Recently built AI tools using OpenAI API and MCP protocol
    - Strong team player with excellent communication skills
    """
    
    print("=" * 60)
    print("First call (no cache)")
    print("=" * 60)
    result = extract_skills(resume)
    print("\nExtracted:")
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 60)
    print("Second call (should hit cache)")
    print("=" * 60)
    result2 = extract_skills(resume)
    
    print("\n" + "=" * 60)
    print("Hallucination check")
    print("=" * 60)
    halluc = detect_hallucinations(resume, result)
    if halluc:
        print(f"WARNING: These skills may be hallucinations: {halluc}")
    else:
        print("All extracted skills are present in the resume - no hallucinations!")
    
    print(f"\nTotal cost for this session: ${total_cost:.5f}")
    
    # Try a second resume to see it handle different inputs
    print("\n" + "=" * 60)
    print("Testing with a different resume")
    print("=" * 60)
    
    resume2 = """
    Jane Doe - Backend Engineer
    5 years experience building Java Spring Boot microservices.
    Worked with Kafka, Redis, and PostgreSQL.
    Deployed to Kubernetes on GCP.
    """
    
    result3 = extract_skills(resume2)
    print("\nExtracted:")
    print(json.dumps(result3, indent=2))
    print(f"\nTotal cost: ${total_cost:.5f}")