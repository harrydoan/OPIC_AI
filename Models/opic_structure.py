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
                'Simple descriptions', 'Personal experiences'
            ]
        ),
        
        'IM2': OpicLevel(
            code='IM2',
            name='Intermediate Mid 2',
            description='Most routine social exchanges with some complications',
            passing_score=80,
            color='#2196F3',
            topics=[
                'Travel & Vacations', 'Entertainment & Media', 'Technology Use',
                'Education & Learning', 'Work Situations', 'Problem Solving',
                'Opinions & Preferences', 'Cultural Events', 'Health Issues',
                'Money & Banking', 'Relationships', 'Current Events Basic'
            ],
            grammar_focus=[
                'Present Perfect vs Past Simple',
                'Present Perfect Continuous',
                'Past Continuous vs Past Simple',
                'Used to vs Would',
                'First Conditional',
                'Reported Speech basics',
                'Passive Voice present/past',
                'Relative Clauses (who/which/that)',
                'Modal verbs of possibility',
                'Gerunds vs Infinitives basics',
                'Linking words (because, although)',
                'Future plans and intentions'
            ],
            vocabulary_themes=[
                'Travel and tourism', 'Entertainment industry', 'Technology devices',
                'Educational systems', 'Workplace terminology', 'Problem descriptions',
                'Opinion expressions', 'Cultural activities', 'Medical conditions',
                'Financial services', 'Relationship types', 'News and media'
            ],
            cultural_contexts=[
                'Travel customs', 'Entertainment preferences', 'Technology adoption',
                'Education systems', 'Work environments', 'Problem-solving approaches',
                'Opinion sharing', 'Cultural celebrations', 'Healthcare systems',
                'Banking practices', 'Social relationships', 'Media consumption'
            ],
            speaking_tasks=[
                'Plan a trip', 'Discuss entertainment', 'Explain technology use',
                'Talk about education', 'Describe work experience', 'Solve problems',
                'Express opinions', 'Discuss cultural events', 'Describe health issues',
                'Handle banking', 'Talk about relationships', 'Discuss current events'
            ],
            difficulty_indicators=[
                'More complex sentence structures', 'Past tense narratives',
                'Abstract concepts introduction', 'Opinion expression',
                'Problem-solution patterns', 'Cause-effect relationships'
            ]
        ),
        
        'IM3': OpicLevel(
            code='IM3',
            name='Intermediate Mid 3',
            description='Complex social and work situations',
            passing_score=80,
            color='#FF9800',
            topics=[
                'Career Development', 'Social Issues', 'Environmental Topics',
                'Cultural Differences', 'Decision Making', 'Problem Analysis',
                'Future Predictions', 'Personal Goals', 'Lifestyle Changes',
                'Technology Impact', 'Education Systems', 'Workplace Challenges'
            ],
            grammar_focus=[
                'Second Conditional',
                'Present Perfect Continuous',
                'Future Perfect',
                'Passive Voice all tenses',
                'Advanced Relative Clauses',
                'Reported Speech advanced',
                'Gerunds vs Infinitives',
                'Modal verbs of deduction',
                'Complex conjunctions',
                'Cause and effect expressions',
                'Comparison structures',
                'Hypothetical situations'
            ],
            vocabulary_themes=[
                'Career terminology', 'Social problems', 'Environmental issues',
                'Cultural concepts', 'Decision processes', 'Analysis vocabulary',
                'Future trends', 'Goal setting', 'Lifestyle choices',
                'Technology impact', 'Educational methods', 'Workplace dynamics'
            ],
            cultural_contexts=[
                'Career progression', 'Social awareness', 'Environmental consciousness',
                'Cross-cultural understanding', 'Decision-making styles',
                'Analytical thinking', 'Future planning', 'Personal development',
                'Lifestyle trends', 'Technology integration', 'Learning approaches',
                'Professional challenges'
            ],
            speaking_tasks=[
                'Discuss career plans', 'Analyze social issues', 'Debate environmental topics',
                'Compare cultures', 'Explain decisions', 'Analyze problems',
                'Make predictions', 'Set goals', 'Discuss lifestyle changes',
                'Evaluate technology', 'Compare education systems', 'Handle workplace issues'
            ],
            difficulty_indicators=[
                'Complex sentence structures', 'Abstract reasoning',
                'Multiple perspectives', 'Analytical thinking',
                'Future speculation', 'Comparative analysis'
            ]
        ),
        
        'IH': OpicLevel(
            code='IH',
            name='Intermediate High',
            description='Unexpected complications and abstract topics',
            passing_score=80,
            color='#9C27B0',
            topics=[
                'Abstract Concepts', 'Hypothetical Situations', 'Complex Problem Solving',
                'Professional Communication', 'Academic Topics', 'Research & Analysis',
                'Innovation & Change', 'Global Issues', 'Ethics & Values',
                'Leadership & Management', 'Conflict Resolution', 'Future Scenarios'
            ],
            grammar_focus=[
                'Third Conditional',
                'Mixed Conditionals',
                'Advanced Modal verbs',
                'Inversion structures',
                'Subjunctive mood',
                'Cleft sentences',
                'Advanced Passive constructions',
                'Complex sentence structures',
                'Advanced reported speech',
                'Discourse markers',
                'Emphatic structures',
                'Advanced conjunctions'
            ],
            vocabulary_themes=[
                'Abstract concepts', 'Hypothetical language', 'Problem-solving vocabulary',
                'Professional terminology', 'Academic language', 'Research methods',
                'Innovation concepts', 'Global terminology', 'Ethical vocabulary',
                'Leadership language', 'Conflict resolution', 'Future scenarios'
            ],
            cultural_contexts=[
                'Abstract thinking', 'Hypothetical reasoning', 'Complex problem solving',
                'Professional environments', 'Academic settings', 'Research culture',
                'Innovation mindset', 'Global perspective', 'Ethical considerations',
                'Leadership styles', 'Conflict management', 'Future planning'
            ],
            speaking_tasks=[
                'Discuss abstract ideas', 'Handle hypothetical situations', 'Solve complex problems',
                'Communicate professionally', 'Present academic topics', 'Analyze research',
                'Discuss innovation', 'Address global issues', 'Explore ethics',
                'Demonstrate leadership', 'Resolve conflicts', 'Plan future scenarios'
            ],
            difficulty_indicators=[
                'Abstract conceptualization', 'Hypothetical reasoning',
                'Complex argumentation', 'Professional discourse',
                'Academic language use', 'Sophisticated analysis'
            ]
        ),
        
        'AL': OpicLevel(
            code='AL',
            name='Advanced Low',
            description='Most situations with confidence and nuanced expressions',
            passing_score=80,
            color='#795548',
            topics=[
                'Academic Research', 'Professional Presentations', 'Complex Negotiations',
                'Policy Analysis', 'Scientific Concepts', 'Philosophical Ideas',
                'Historical Analysis', 'Economic Theories', 'Social Psychology',
                'Cross-cultural Communication', 'Advanced Technology', 'Innovation Management'
            ],
            grammar_focus=[
                'Advanced Conditionals',
                'Sophisticated Modal usage',
                'Complex Inversion',
                'Advanced Subjunctive',
                'Nominalization',
                'Advanced Passive structures',
                'Discourse markers',
                'Academic writing structures',
                'Complex clause combinations',
                'Advanced cohesion devices',
                'Sophisticated conjunctions',
                'Register variation'
            ],
            vocabulary_themes=[
                'Academic terminology', 'Professional presentations', 'Negotiation language',
                'Policy vocabulary', 'Scientific terminology', 'Philosophical concepts',
                'Historical analysis', 'Economic language', 'Psychology terms',
                'Cross-cultural concepts', 'Advanced technology', 'Innovation management'
            ],
            cultural_contexts=[
                'Academic environments', 'Professional presentations', 'Business negotiations',
                'Policy making', 'Scientific research', 'Philosophical discourse',
                'Historical interpretation', 'Economic analysis', 'Psychological understanding',
                'Cultural sensitivity', 'Technology adoption', 'Innovation culture'
            ],
            speaking_tasks=[
                'Present research', 'Deliver presentations', 'Negotiate agreements',
                'Analyze policies', 'Explain scientific concepts', 'Discuss philosophy',
                'Interpret history', 'Analyze economics', 'Explore psychology',
                'Navigate cultures', 'Evaluate technology', 'Manage innovation'
            ],
            difficulty_indicators=[
                'Academic discourse', 'Professional fluency',
                'Sophisticated argumentation', 'Nuanced expression',
                'Complex analysis', 'Specialized terminology'
            ]
        ),
        
        'AM': OpicLevel(
            code='AM',
            name='Advanced Mid',
            description='All routine and most non-routine situations',
            passing_score=80,
            color='#607D8B',
            topics=[
                'Specialized Professional Fields', 'Advanced Academic Discourse',
                'Complex Problem Analysis', 'Strategic Planning', 'Research Methodology',
                'Advanced Cultural Analysis', 'Sophisticated Argumentation',
                'Expert-level Communication', 'Advanced Technical Topics',
                'High-level Negotiations', 'Complex Project Management', 'Advanced Leadership'
            ],
            grammar_focus=[
                'Near-native grammar structures',
                'Sophisticated register variation',
                'Advanced cohesion devices',
                'Complex clause structures',
                'Advanced hedging language',
                'Sophisticated emphasis structures',
                'Advanced reported speech',
                'Complex temporal relationships',
                'Advanced modal combinations',
                'Sophisticated discourse management',
                'Complex nominalization',
                'Advanced stylistic devices'
            ],
            vocabulary_themes=[
                'Specialized professions', 'Advanced academics', 'Complex analysis',
                'Strategic terminology', 'Research vocabulary', 'Cultural analysis',
                'Sophisticated argumentation', 'Expert communication', 'Technical language',
                'High-level negotiations', 'Project management', 'Advanced leadership'
            ],
            cultural_contexts=[
                'Professional specialization', 'Academic excellence', 'Complex problem solving',
                'Strategic thinking', 'Research methodology', 'Cultural sophistication',
                'Advanced argumentation', 'Expert communication', 'Technical proficiency',
                'High-level negotiations', 'Project leadership', 'Advanced management'
            ],
            speaking_tasks=[
                'Expert professional communication', 'Advanced academic discourse',
                'Complex problem analysis', 'Strategic planning', 'Research presentation',
                'Cultural analysis', 'Sophisticated argumentation', 'Expert consultation',
                'Technical explanation', 'High-level negotiation', 'Project leadership',
                'Advanced management communication'
            ],
            difficulty_indicators=[
                'Professional expertise', 'Academic sophistication',
                'Complex analytical thinking', 'Strategic communication',
                'Research proficiency', 'Cultural expertise'
            ]
        ),
        
        'AH': OpicLevel(
            code='AH',
            name='Advanced High',
            description='Near-native proficiency with cultural mastery',
            passing_score=80,
            color='#E91E63',
            topics=[
                'Expert Professional Communication', 'Advanced Academic Research',
                'Complex Cultural Analysis', 'Sophisticated Argumentation',
                'High-level Strategic Thinking', 'Advanced Problem Solving',
                'Expert Presentations', 'Complex Negotiations',
                'Advanced Leadership Communication', 'Sophisticated Analysis',
                'Expert-level Discussions', 'Near-native Interactions'
            ],
            grammar_focus=[
                'Native-like structures',
                'Advanced stylistic variation',
                'Sophisticated discourse management',
                'Complex pragmatic awareness',
                'Advanced register control',
                'Sophisticated emphasis and focus',
                'Complex grammatical metaphor',
                'Advanced textual organization',
                'Native-like fluency markers',
                'Sophisticated hedging',
                'Complex modal meanings',
                'Advanced pragmatic competence'
            ],
            vocabulary_themes=[
                'Expert professional language', 'Advanced research terminology',
                'Complex cultural concepts', 'Sophisticated argumentation',
                'Strategic thinking vocabulary', 'Advanced problem solving',
                'Expert presentation language', 'Complex negotiation terms',
                'Advanced leadership concepts', 'Sophisticated analysis',
                'Expert discussion language', 'Near-native expressions'
            ],
            cultural_contexts=[
                'Expert professional culture', 'Advanced academic culture',
                'Complex cultural understanding', 'Sophisticated discourse',
                'Strategic thinking culture', 'Advanced problem-solving mindset',
                'Expert presentation culture', 'Complex negotiation environment',
                'Advanced leadership culture', 'Sophisticated analytical thinking',
                'Expert discussion culture', 'Near-native cultural competence'
            ],
            speaking_tasks=[
                'Expert professional discourse', 'Advanced academic research presentation',
                'Complex cultural analysis', 'Sophisticated debate and argumentation',
                'High-level strategic communication', 'Advanced problem-solving discussion',
                'Expert-level presentations', 'Complex high-stakes negotiations',
                'Advanced leadership communication', 'Sophisticated analytical discourse',
                'Expert-level academic and professional discussions', 'Near-native social interactions'
            ],
            difficulty_indicators=[
                'Near-native fluency', 'Expert-level discourse',
                'Sophisticated cultural competence', 'Advanced pragmatic skills',
                'Complex analytical ability', 'Native-like communication patterns'
            ]
        )
    }
    
    # Level progression order
    LEVEL_ORDER = ['IM1', 'IM2', 'IM3', 'IH', 'AL', 'AM', 'AH']
    
    @classmethod
    def get_level(cls, level_code: str) -> OpicLevel:
        """Get OPIC level by code"""
        return cls.LEVELS.get(level_code)
    
    @classmethod
    def get_all_levels(cls) -> Dict[str, OpicLevel]:
        """Get all OPIC levels"""
        return cls.LEVELS
    
    @classmethod
    def get_level_topics(cls, level_code: str) -> List[str]:
        """Get topics for a specific level"""
        level = cls.get_level(level_code)
        return level.topics if level else []
    
    @classmethod
    def get_level_grammar_focus(cls, level_code: str) -> List[str]:
        """Get grammar focus for a specific level"""
        level = cls.get_level(level_code)
        return level.grammar_focus if level else []
    
    @classmethod
    def get_next_level(cls, current_level: str) -> str:
        """Get next level in progression"""
        try:
            current_index = cls.LEVEL_ORDER.index(current_level)
            if current_index < len(cls.LEVEL_ORDER) - 1:
                return cls.LEVEL_ORDER[current_index + 1]
        except ValueError:
            pass
        return None
    
    @classmethod
    def get_previous_level(cls, current_level: str) -> str:
        """Get previous level in progression"""
        try:
            current_index = cls.LEVEL_ORDER.index(current_level)
            if current_index > 0:
                return cls.LEVEL_ORDER[current_index - 1]
        except ValueError:
            pass
        return None
    
    @classmethod
    def is_valid_level(cls, level_code: str) -> bool:
        """Check if level code is valid"""
        return level_code in cls.LEVELS
    
    @classmethod
    def get_level_statistics(cls) -> Dict[str, Any]:
        """Get statistics about OPIC structure"""
        total_topics = sum(len(level.topics) for level in cls.LEVELS.values())
        total_grammar_points = sum(len(level.grammar_focus) for level in cls.LEVELS.values())
        
        return {
            'total_levels': len(cls.LEVELS),
            'total_topics': total_topics,
            'total_grammar_points': total_grammar_points,
            'topics_per_level': total_topics // len(cls.LEVELS),
            'grammar_points_per_level': total_grammar_points // len(cls.LEVELS)
        }
    
    @classmethod
    def get_topic_level_mapping(cls) -> Dict[str, str]:
        """Get mapping of topics to their levels"""
        mapping = {}
        for level_code, level in cls.LEVELS.items():
            for topic in level.topics:
                mapping[topic] = level_code
        return mapping
    
    @classmethod
    def search_topics(cls, search_term: str) -> List[tuple]:
        """Search for topics containing the search term"""
        results = []
        search_term = search_term.lower()
        
        for level_code, level in cls.LEVELS.items():
            for topic in level.topics:
                if search_term in topic.lower():
                    results.append((level_code, topic))
        
        return results
    
    @classmethod
    def get_difficulty_progression(cls) -> List[Dict[str, Any]]:
        """Get difficulty progression information"""
        progression = []
        
        for level_code in cls.LEVEL_ORDER:
            level = cls.LEVELS[level_code]
            progression.append({
                'level_code': level_code,
                'level_name': level.name,
                'description': level.description,
                'difficulty_indicators': level.difficulty_indicators,
                'topic_count': len(level.topics),
                'grammar_count': len(level.grammar_focus)
            })
        
        return progression

# Create global instance
opic_structure = OpicStructure()
