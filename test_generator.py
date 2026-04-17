#!/usr/bin/env python3
"""Test script for portfolio generation"""
import sys
import json
import os

# Add paths
sys.path.insert(0, os.path.dirname(__file__))

import importlib.util
spec = importlib.util.spec_from_file_location("generate", "/workspace/portfolio-automation/website-generator/generate.py")
generate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_module)
generate_portfolio = generate_module.generate_portfolio

# Sample data
data = {
    'full_name': 'Sarah Mitchell',
    'email': 'sarah.design@example.com',
    'niche': 'UI/UX Design',
    'services': 'UI Design, UX Research, Prototyping, Brand Identity',
    'target_clients': 'Tech Startups, E-commerce Brands, Mobile Apps',
    'work_samples': ['https://dribbble.com/project1', 'https://behance.net/project2'],
    'testimonials': [
        'Sarah transformed our app into a beautiful, user-friendly experience!',
        'Exceptional design skills and great communication throughout the project.'
    ],
    'brand_colors': '#FF6B6B,#4ECDC4',
    'preferred_style': 'modern',
    'cta': 'Let\'s Work Together'
}

# Generate portfolio
result = generate_portfolio(data)
print(json.dumps(result, indent=2))

if result['success']:
    print(f"\nPortfolio created at: {result['path']}")
    print(f"Files generated: {os.listdir(result['path'])}")
