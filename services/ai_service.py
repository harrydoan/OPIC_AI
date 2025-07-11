"""
AI Service for OPIC Question Generation
Handles OpenAI/OpenRouter API integration for dynamic question creation
"""

import json
import logging
import requests
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

from models.opic_structure import opic_structure
from config.settings import AppSettings

@dataclass
class GenerationRequest:
    """Request data for question generation"""
    level: str
    topic: str
    count: int = 10
    difficulty_progression: bool = True
    cultural_context: bool = True
    grammar_focus: Optional[List[str]] = None

@dataclass
class GenerationResult:
    """Result of question generation"""
    success: bool
    questions: List[Dict[str, Any]]
    error_message: Optional[str] = None
    generation_time: Optional[float] = None
    api_usage: Optional[Dict[str, Any]] = None

class AIService:
    """Service for AI-powered question generation"""
    
    def __init__(self):
        self.settings = AppSettings()
        self.api_key = self.settings.get_api_key()
        self.api_url = self.settings.get_api_url()
        self.model = self.settings.get_model()
        self.timeout = self.settings.get_timeout()
        
        # Request session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://opic-learning-app.com",
            "X-Title": "OPIC Learning Desktop App"
        })
        
        logging.info(f"AI Service initialized with model: {self.model}")
    
    def generate_questions(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate OPIC questions using AI
        
        Args:
            request: Generation request parameters
            
        Returns:
            GenerationResult with questions or error information
        """
        start_time = datetime.now()
        
        try:
            # Validate request
            if not self._validate_request(request):
                return GenerationResult(
                    success=False,
                    questions=[],
                    error_message="Invalid request parameters"
                )
            
            # Get level information
            level_info = opic_structure.get_level(request.level)
            if not level_info:
                return GenerationResult(
                    success=False,
                    questions=[],
                    error_message=f"Invalid level: {request.level}"
                )
            
            # Create prompt
            prompt = self._create_comprehensive_prompt(request, level_info)
            
            # Make API call
            api_response = self._call_api(prompt)
            
            if not api_response['success']:
                return GenerationResult(
                    success=False,
                    questions=[],
                    error_message=api_response['error']
                )
            
            # Parse and validate questions
            questions = self._parse_and_validate_questions(
                api_response['content'], 
                request
            )
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            return GenerationResult(
                success=True,
                questions=questions,
                generation_time=generation_time,
                api_usage=api_response.get('usage')
            )
            
        except Exception as e:
            logging.error(f"Question generation failed: {e}")
            return GenerationResult(
                success=False,
                questions=[],
                error_message=str(e)
            )
    
    def _validate_request(self, request: GenerationRequest) -> bool:
        """Validate generation request"""
        if not request.level or not request.topic:
            return False
        
        if not opic_structure.is_valid_level(request.level):
            return False
        
        if request.topic not in opic_structure.get_level_topics(request.level):
            return False
        
        if request.count < 1 or request.count > 20:
            return False
        
        return True
    
    def _create_comprehensive_prompt(self, request: GenerationRequest, level_info) -> str:
        """Create comprehensive prompt for AI question generation"""
        
        # Get grammar focus (custom or default)
        grammar_focus = request.grammar_focus or level_info.grammar_focus
        
        # Select grammar points for this generation (rotate for variety)
        selected_grammar = grammar_focus[:min(8, len(grammar_focus))]
        
        prompt = f"""Generate {request.count} comprehensive OPIC {request.level} ({level_info.name}) English fill-in-the-blank questions for the topic: "{request.topic}".

CRITICAL OPIC {request.level} REQUIREMENTS:
1. Questions must reflect ACTUAL OPIC {request.level} difficulty and assessment criteria
2. Cover key grammar patterns: {', '.join(selected_grammar)}
3. Use vocabulary and sentence structures appropriate for: {level_info.description}
4. Each question should test different specific grammar points from the focus list
5. {"Progressive difficulty (questions 1-3 easier, 4-7 medium, 8-10 harder)" if request.difficulty_progression else "Consistent difficulty appropriate for " + request.level}
6. Include realistic OPIC speaking test contexts and scenarios
7. {"Test cultural knowledge and situational appropriateness" if request.cultural_context else "Focus on grammatical accuracy"}

TOPIC FOCUS: "{request.topic}" - All questions must relate to this topic area
LEVEL DESCRIPTION: {level_info.description}
GRAMMAR PATTERNS TO TEST: {', '.join(selected_grammar)}
CULTURAL CONTEXTS: {', '.join(level_info.cultural_contexts[:5])}
SPEAKING TASKS: {', '.join(level_info.speaking_tasks[:5])}

QUALITY STANDARDS FOR OPIC {request.level}:
- Sentences must sound natural in real OPIC interview contexts
- Grammar complexity appropriate for {request.level} proficiency level
- Wrong answers should represent common {request.level} student errors
- Cultural contexts should be appropriate for international test-takers
- Vocabulary level should match OPIC {request.level} expectations
- Test both grammatical accuracy and pragmatic appropriateness

DIFFICULTY INDICATORS FOR {request.level}:
{chr(10).join('- ' + indicator for indicator in level_info.difficulty_indicators)}

For each question provide:
- sentence: Natural, conversational sentence with ONE blank (use _____ for blank)
- correctAnswer: Grammatically correct answer (single word or short phrase)
- explanation: Detailed Vietnamese explanation including:
  * Specific grammar rule being tested and why
  * Why this answer demonstrates OPIC {request.level} proficiency
  * Common mistakes students make at this level
  * How this grammar point appears in OPIC speaking contexts
  * Cultural or pragmatic information if relevant
  * Connection to {request.topic} topic area
- wrongAnswers: Exactly 4 plausible incorrect options that represent:
  * Common grammar mistakes at {request.level} level
  * Vocabulary confusion typical for {request.level} students
  * False friends or similar structures from other levels
  * Overgeneralization errors from simpler grammar rules

CONTEXT REQUIREMENTS:
- Use realistic {request.topic} scenarios that could appear in OPIC interviews
- Include appropriate register and formality for the situation
- Ensure cultural sensitivity and international relevance
- Connect to typical OPIC speaking tasks: {', '.join(level_info.speaking_tasks[:3])}

Generate exactly {request.count} questions as a valid JSON array. Ensure variety in grammar points tested and {"clear progression in difficulty" if request.difficulty_progression else "consistent appropriate difficulty"}.

EXAMPLE FORMAT (adapt complexity for {request.level}):
{{
  "sentence": "When discussing {request.topic.lower()} in an OPIC interview, this approach _____ the most effective results.",
  "correctAnswer": "produces",
  "explanation": "Giải thích OPIC {request.level}: Câu hỏi này kiểm tra khả năng sử dụng động từ 'produce' trong ngữ cảnh chuyên môn về {request.topic}. Ở mức OPIC {request.level}, thí sinh cần thành thạo việc diễn đạt kết quả và hiệu quả. 'Produce results' là collocation quan trọng trong tiếng Anh chuyên nghiệp. Sai lầm phổ biến ở level này là dùng 'make' hoặc 'create' thay vì 'produce'.",
  "wrongAnswers": ["makes", "creates", "gives", "brings"]
}}"""
        
        return prompt
    
    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """Make API call to generate questions"""
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert OPIC test creator with deep knowledge of English grammar and OPIC assessment standards. Create high-quality, authentic OPIC-style questions with accurate Vietnamese explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 4000,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
            
            response = self.session.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'choices' not in data or not data['choices']:
                return {
                    'success': False,
                    'error': 'No choices in API response'
                }
            
            content = data['choices'][0]['message']['content']
            
            return {
                'success': True,
                'content': content,
                'usage': data.get('usage', {})
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'API request timed out'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'API request failed: {str(e)}'
            }
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': 'Invalid JSON response from API'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _parse_and_validate_questions(self, content: str, request: GenerationRequest) -> List[Dict[str, Any]]:
        """Parse and validate generated questions"""
        try:
            # Try to extract JSON from content
            content = content.strip()
            
            # Handle cases where content might have extra text
            if not content.startswith('['):
                # Find JSON array in content
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                if start_idx != -1 and end_idx != 0:
                    content = content[start_idx:end_idx]
                else:
                    raise ValueError("No JSON array found in response")
            
            questions = json.loads(content)
            
            if not isinstance(questions, list):
                raise ValueError("Response is not a list")
            
            validated_questions = []
            
            for i, question in enumerate(questions):
                # Validate required fields
                required_fields = ['sentence', 'correctAnswer', 'explanation', 'wrongAnswers']
                if not all(field in question for field in required_fields):
                    logging.warning(f"Question {i+1} missing required fields")
                    continue
                
                # Validate sentence has blank
                if '_____' not in question['sentence']:
                    logging.warning(f"Question {i+1} missing blank in sentence")
                    continue
                
                # Validate wrong answers
                if not isinstance(question['wrongAnswers'], list) or len(question['wrongAnswers']) < 4:
                    logging.warning(f"Question {i+1} insufficient wrong answers")
                    continue
                
                # Clean and validate data
                validated_question = {
                    'sentence': question['sentence'].strip(),
                    'correctAnswer': question['correctAnswer'].strip(),
                    'explanation': question['explanation'].strip(),
                    'wrongAnswers': [ans.strip() for ans in question['wrongAnswers'][:4]],
                    'level': request.level,
                    'topic': request.topic,
                    'generated_at': datetime.now().isoformat()
                }
                
                validated_questions.append(validated_question)
                
                # Stop if we have enough questions
                if len(validated_questions) >= request.count:
                    break
            
            if not validated_questions:
                raise ValueError("No valid questions found in response")
            
            return validated_questions
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed: {e}")
            raise ValueError(f"Invalid JSON in API response: {str(e)}")
        except Exception as e:
            logging.error(f"Question validation failed: {e}")
            raise ValueError(f"Question validation failed: {str(e)}")
    
    def test_api_connection(self) -> Dict[str, Any]:
        """Test API connection and credentials"""
        try:
            test_prompt = "Generate a simple test question: 'I _____ happy.' with correctAnswer 'am' and explanation 'Test question' and wrongAnswers ['is', 'are', 'was', 'were']"
            
            result = self._call_api(test_prompt)
            
            if result['success']:
                return {
                    'success': True,
                    'message': 'API connection successful',
                    'model': self.model
                }
            else:
                return {
                    'success': False,
                    'message': f"API test failed: {result['error']}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f"Connection test failed: {str(e)}"
            }
    
    def get_api_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics (if available)"""
        # This would depend on the specific API provider
        # For now, return placeholder
        return {
            'requests_today': 0,
            'tokens_used': 0,
            'quota_remaining': 'Unknown'
        }
    
    def set_api_key(self, api_key: str):
        """Update API key"""
        self.api_key = api_key
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })
        logging.info("API key updated")
    
    def close(self):
        """Close the session"""
        if hasattr(self, 'session'):
            self.session.close()
            logging.info("AI Service session closed")

# Global AI service instance
ai_service = AIService()
