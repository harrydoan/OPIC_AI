"""
Utility functions and helpers for OPIC Learning App
"""

import os
import sys
import json
import logging
import random
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
import importlib.util

def setup_logging(log_level: int = logging.INFO, log_file: Optional[str] = None):
    """Setup application logging"""
    # Create logs directory
    if log_file is None:
        logs_dir = Path.home() / ".opic_learning" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / f"opic_app_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Setup logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logging.info(f"Logging setup complete - Log file: {log_file}")

def resource_path(relative_path: str) -> Path:
    """Get absolute path to resource file"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return Path(base_path) / relative_path

def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load JSON file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"JSON file not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in file {file_path}: {e}")
        return {}
    except Exception as e:
        logging.error(f"Error loading JSON file {file_path}: {e}")
        return {}

def save_json_file(data: Dict[str, Any], file_path: Union[str, Path]) -> bool:
    """Save data to JSON file safely"""
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logging.error(f"Error saving JSON file {file_path}: {e}")
        return False

def check_dependencies() -> bool:
    """Check if all required dependencies are installed"""
    required_packages = [
        'PyQt5',
        'requests',
        'sqlite3'  # Built-in, but check anyway
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
            else:
                importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logging.error(f"Missing required packages: {missing_packages}")
        return False
    
    return True

def shuffle_list(items: List[Any]) -> List[Any]:
    """Shuffle list items using Fisher-Yates algorithm"""
    shuffled = items.copy()
    for i in range(len(shuffled) - 1, 0, -1):
        j = random.randint(0, i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled

def calculate_accuracy(correct: int, total: int) -> float:
    """Calculate accuracy percentage"""
    if total == 0:
        return 0.0
    return (correct / total) * 100

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable string"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s" if secs > 0 else f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def format_file_size(bytes_size: int) -> str:
    """Format file size in bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def generate_hash(text: str) -> str:
    """Generate SHA256 hash of text"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def get_app_version() -> str:
    """Get application version"""
    try:
        version_file = resource_path("version.txt")
        if version_file.exists():
            return version_file.read_text().strip()
        else:
            return "1.0.0"
    except:
        return "1.0.0"

def play_sound(sound_name: str) -> bool:
    """Play sound effect"""
    try:
        # Check if sound is enabled
        from config.settings import app_settings
        if not app_settings.is_sound_enabled():
            return False
        
        # Try to import and play sound
        try:
            from playsound import playsound
        except ImportError:
            logging.warning("playsound not available, skipping sound")
            return False
        
        sound_file = resource_path(f"resources/sounds/{sound_name}.wav")
        if sound_file.exists():
            playsound(str(sound_file), block=False)
            return True
        else:
            logging.warning(f"Sound file not found: {sound_file}")
            return False
            
    except Exception as e:
        logging.error(f"Error playing sound {sound_name}: {e}")
        return False

def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    if not api_key:
        return False
    
    # OpenRouter API key format: sk-or-v1-...
    if api_key.startswith('sk-or-v1-') and len(api_key) > 20:
        return True
    
    # OpenAI API key format: sk-...
    if api_key.startswith('sk-') and len(api_key) > 20:
        return True
    
    return False

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_blank_from_sentence(sentence: str) -> tuple:
    """Extract the blank position and surrounding context from sentence"""
    blank_marker = "_____"
    if blank_marker not in sentence:
        return None, sentence
    
    parts = sentence.split(blank_marker)
    if len(parts) != 2:
        return None, sentence
    
    before = parts[0].strip()
    after = parts[1].strip()
    
    return (before, after), sentence

def validate_question_structure(question: Dict[str, Any]) -> List[str]:
    """Validate question data structure"""
    errors = []
    
    required_fields = ['sentence', 'correctAnswer', 'explanation', 'wrongAnswers']
    for field in required_fields:
        if field not in question:
            errors.append(f"Missing required field: {field}")
    
    if 'sentence' in question:
        if '_____' not in question['sentence']:
            errors.append("Sentence must contain blank marker '_____'")
        
        if len(question['sentence'].strip()) < 10:
            errors.append("Sentence too short")
    
    if 'correctAnswer' in question:
        if not question['correctAnswer'] or not question['correctAnswer'].strip():
            errors.append("Correct answer cannot be empty")
    
    if 'wrongAnswers' in question:
        if not isinstance(question['wrongAnswers'], list):
            errors.append("Wrong answers must be a list")
        elif len(question['wrongAnswers']) < 3:
            errors.append("Must have at least 3 wrong answers")
        elif len(question['wrongAnswers']) > 5:
            errors.append("Too many wrong answers (max 5)")
    
    if 'explanation' in question:
        if len(question['explanation'].strip()) < 20:
            errors.append("Explanation too short")
    
    return errors

def calculate_level_progress(topic_scores: Dict[str, float], passing_score: int = 80) -> Dict[str, Any]:
    """Calculate level progress statistics"""
    if not topic_scores:
        return {
            'completion_rate': 0.0,
            'average_score': 0.0,
            'completed_topics': 0,
            'total_topics': 0,
            'passed_topics': 0
        }
    
    total_topics = len(topic_scores)
    completed_topics = sum(1 for score in topic_scores.values() if score > 0)
    passed_topics = sum(1 for score in topic_scores.values() if score >= passing_score)
    
    # Calculate average only for attempted topics
    attempted_scores = [score for score in topic_scores.values() if score > 0]
    average_score = sum(attempted_scores) / len(attempted_scores) if attempted_scores else 0.0
    
    completion_rate = (passed_topics / total_topics) * 100
    
    return {
        'completion_rate': completion_rate,
        'average_score': average_score,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
        'passed_topics': passed_topics
    }

def get_difficulty_color(score: float) -> str:
    """Get color code based on difficulty/score"""
    if score >= 90:
        return "#4CAF50"  # Green - Excellent
    elif score >= 80:
        return "#8BC34A"  # Light Green - Good
    elif score >= 70:
        return "#FFC107"  # Yellow - Average
    elif score >= 60:
        return "#FF9800"  # Orange - Below Average
    else:
        return "#F44336"  # Red - Poor

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format percentage with specified decimal places"""
    return f"{value:.{decimals}f}%"

def get_performance_message(accuracy: float) -> str:
    """Get performance message based on accuracy"""
    if accuracy >= 95:
        return "🌟 Xuất sắc! Bạn đã thành thạo hoàn toàn!"
    elif accuracy >= 90:
        return "🎉 Tuyệt vời! Bạn làm rất tốt!"
    elif accuracy >= 80:
        return "✅ Tốt! Bạn đã đạt yêu cầu!"
    elif accuracy >= 70:
        return "👍 Khá tốt! Cần cải thiện một chút!"
    elif accuracy >= 60:
        return "📚 Cần luyện tập thêm!"
    else:
        return "💪 Hãy cố gắng hơn nữa!"

def create_backup_filename(prefix: str = "backup") -> str:
    """Create backup filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.json"

def is_recent_date(date_str: str, days: int = 7) -> bool:
    """Check if date string is within recent days"""
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        cutoff_date = datetime.now() - timedelta(days=days)
        return date_obj >= cutoff_date
    except:
        return False

def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def safe_division(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Perform safe division with default value"""
    if denominator == 0:
        return default
    return numerator / denominator

class ProgressTracker:
    """Utility class for tracking progress across multiple operations"""
    
    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0
        self.step_messages = {}
    
    def next_step(self, message: str = ""):
        """Move to next step"""
        self.current_step += 1
        if message:
            self.step_messages[self.current_step] = message
    
    def get_progress(self) -> float:
        """Get current progress percentage"""
        return (self.current_step / self.total_steps) * 100
    
    def get_current_message(self) -> str:
        """Get current step message"""
        return self.step_messages.get(self.current_step, "")
    
    def is_complete(self) -> bool:
        """Check if all steps are complete"""
        return self.current_step >= self.total_steps

class TextProcessor:
    """Utility class for text processing operations"""
    
    @staticmethod
    def normalize_answer(answer: str) -> str:
        """Normalize answer for comparison"""
        return answer.strip().lower()
    
    @staticmethod
    def highlight_blank(sentence: str, answer: str) -> str:
        """Replace blank with highlighted answer"""
        return sentence.replace("_____", f"[{answer}]")
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """Extract keywords from text"""
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) >= min_length]
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

class DataValidator:
    """Utility class for data validation"""
    
    @staticmethod
    def validate_level_code(level: str) -> bool:
        """Validate OPIC level code"""
        valid_levels = ['IM1', 'IM2', 'IM3', 'IH', 'AL', 'AM', 'AH']
        return level in valid_levels
    
    @staticmethod
    def validate_score(score: int, min_score: int = 0, max_score: int = 100) -> bool:
        """Validate score within range"""
        return min_score <= score <= max_score
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

def debug_log_function_call(func):
    """Decorator to log function calls in debug mode"""
    def wrapper(*args, **kwargs):
        logging.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logging.error(f"{func.__name__} raised exception: {e}")
            raise
    return wrapper

# Configuration helpers
def get_system_info() -> Dict[str, str]:
    """Get system information"""
    import platform
    return {
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'system': platform.system(),
        'release': platform.release()
    }

def check_disk_space(path: str, required_mb: int = 100) -> bool:
    """Check if sufficient disk space is available"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(path)
        free_mb = free // (1024 * 1024)
        return free_mb >= required_mb
    except:
        return True  # Assume OK if can't check

def create_sample_data() -> Dict[str, Any]:
    """Create sample data for testing"""
    return {
        'questions': [
            {
                'sentence': 'I _____ breakfast every morning.',
                'correctAnswer': 'have',
                'explanation': 'Giải thích: "Have breakfast" là cách diễn đạt chuẩn trong tiếng Anh.',
                'wrongAnswers': ['take', 'make', 'eat', 'do']
            }
        ],
        'progress': {
            'current_level': 'IM1',
            'unlocked_levels': ['IM1'],
            'total_score': 0,
            'current_streak': 0
        }
    }

# Export commonly used functions
__all__ = [
    'setup_logging',
    'resource_path', 
    'load_json_file',
    'save_json_file',
    'check_dependencies',
    'shuffle_list',
    'calculate_accuracy',
    'format_duration',
    'format_file_size',
    'play_sound',
    'validate_api_key',
    'clean_text',
    'validate_question_structure',
    'calculate_level_progress',
    'get_difficulty_color',
    'format_percentage',
    'get_performance_message',
    'ProgressTracker',
    'TextProcessor',
    'DataValidator',
    'get_system_info'
]
            '
