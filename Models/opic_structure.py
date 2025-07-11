"""
OPIC Level Structure and Content Organization
Contains comprehensive OPIC level definitions, topics, and grammar focus areas
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class OpicLevel:
    """Data class representing an OPIC level"""
    code: str
    name: str
    description: str
    passing_score: int
    color: str
    topics: List[str]
    grammar_focus: List[str]
    vocabulary_themes: List[str]
    cultural_contexts: List[str]
    speaking_tasks: List[str]
    difficulty_indicators: List[str]

class OpicStructure:
    """Complete OPIC structure with all levels, topics, and requirements"""
    
    # OPIC Level definitions
    LEVELS = {
        'IM1': OpicLevel(
            code='IM1',
            name='Intermediate Mid 1',
            description='Basic daily conversations and routine situations',
            passing_score=80,
            color='#4CAF50',
            topics=[
                'Daily Routines', 'Family & Friends', 'Food & Dining', 'Shopping',
                'Transportation', 'Weather', 'Hobbies', 'Work/School Basic',
                'Health & Body', 'Home & Living', 'Past Events', 'Future Plans'
            ],
            grammar_focus=[
                'Present Simple vs Present Continuous',
                'Past Simple vs Present Perfect',
                'Basic Future forms (will/going to)',
                'Comparative and Superlative',
                'Modal verbs (can/could/should)',
                'Prepositions of time and place',
                'Question formation (WH-questions)',
                'Frequency adverbs',
                'There is/are constructions',
                'Basic conjunctions (and, but, or)',
                'Simple conditional (if + present)',
                'Possessive adjectives and pronouns'
            ],
            vocabulary_themes=[
                'Personal information', 'Family relationships', 'Daily activities',
                'Food and meals', 'Shopping items', 'Transportation modes',
                'Weather conditions', 'Hobbies and interests', 'Body parts',
                'Health problems', 'Home and furniture', 'Time expressions'
            ],
            cultural_contexts=[
                'Greetings and introductions', 'Family customs', 'Meal times',
                'Shopping etiquette', 'Public transportation', 'Weather talk',
                'Leisure activities', 'Work schedules', 'Healthcare visits',
                'Housing arrangements'
            ],
            speaking_tasks=[
                'Describe daily routine', 'Talk about family', 'Order food',
                'Ask for directions', 'Make appointments', 'Express preferences',
                'Give personal information', 'Talk about past experiences',
                'Make simple plans', 'Describe living situation'
            ],
            difficulty_indicators=[
                'Simple sentence structures', 'Present tense dominant',
                'Concrete vocabulary', 'Familiar topics', 'Basic time concepts',
                'Simple descriptions', 'Personal experiences',
