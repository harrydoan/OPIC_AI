"""
Database Manager for OPIC Learning App
Handles SQLite database operations for user progress, questions, and game sessions
"""

import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager

class DatabaseManager:
    """Manages SQLite database operations for the OPIC Learning App"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to database file. If None, uses default path.
        """
        if db_path is None:
            app_dir = Path.home() / ".opic_learning"
            app_dir.mkdir(exist_ok=True)
            self.db_path = str(app_dir / "opic_app.db")
        else:
            self.db_path = db_path
        
        logging.info(f"Database path: {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Initialize database with all required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create user_progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    current_level TEXT DEFAULT 'IM1',
                    unlocked_levels TEXT DEFAULT '["IM1"]',
                    total_score INTEGER DEFAULT 0,
                    current_streak INTEGER DEFAULT 0,
                    best_streak INTEGER DEFAULT 0,
                    total_questions INTEGER DEFAULT 0,
                    correct_answers INTEGER DEFAULT 0,
                    last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create topic_progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topic_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    best_score INTEGER DEFAULT 0,
                    attempts INTEGER DEFAULT 0,
                    total_questions INTEGER DEFAULT 0,
                    correct_answers INTEGER DEFAULT 0,
                    last_attempt TIMESTAMP,
                    is_completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(level, topic)
                )
            """)
            
            # Create questions_cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    question_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    UNIQUE(level, topic)
                )
            """)
            
            # Create game_sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    accuracy REAL NOT NULL,
                    duration INTEGER,
                    streak INTEGER DEFAULT 0,
                    questions_data TEXT,
                    answers_data TEXT,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_key TEXT UNIQUE NOT NULL,
                    setting_value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert default user progress if not exists
            cursor.execute("""
                INSERT OR IGNORE INTO user_progress (id) 
                VALUES (1)
            """)
            
            # Insert default settings
            default_settings = [
                ('api_key', ''),
                ('sound_enabled', 'true'),
                ('auto_advance', 'false'),
                ('theme', 'default'),
                ('language', 'vi')
            ]
            
            for key, value in default_settings:
                cursor.execute("""
                    INSERT OR IGNORE INTO app_settings (setting_key, setting_value) 
                    VALUES (?, ?)
                """, (key, value))
            
            conn.commit()
            logging.info("Database initialized successfully")
    
    # User Progress Methods
    def get_user_progress(self) -> Dict[str, Any]:
        """Get current user progress data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_progress WHERE id = 1")
            row = cursor.fetchone()
            
            if row:
                return {
                    'current_level': row['current_level'],
                    'unlocked_levels': json.loads(row['unlocked_levels']),
                    'total_score': row['total_score'],
                    'current_streak': row['current_streak'],
                    'best_streak': row['best_streak'],
                    'total_questions': row['total_questions'],
                    'correct_answers': row['correct_answers'],
                    'last_played': row['last_played'],
                    'accuracy': (row['correct_answers'] / row['total_questions'] * 100) if row['total_questions'] > 0 else 0
                }
            
            return self._get_default_progress()
    
    def update_user_progress(self, progress: Dict[str, Any]):
        """Update user progress data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user_progress 
                SET current_level = ?, 
                    unlocked_levels = ?, 
                    total_score = ?, 
                    current_streak = ?,
                    best_streak = ?,
                    total_questions = ?,
                    correct_answers = ?,
                    last_played = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (
                progress['current_level'],
                json.dumps(progress['unlocked_levels']),
                progress['total_score'],
                progress['current_streak'],
                progress['best_streak'],
                progress['total_questions'],
                progress['correct_answers']
            ))
            conn.commit()
            logging.debug("User progress updated")
    
    def _get_default_progress(self) -> Dict[str, Any]:
        """Get default user progress"""
        return {
            'current_level': 'IM1',
            'unlocked_levels': ['IM1'],
            'total_score': 0,
            'current_streak': 0,
            'best_streak': 0,
            'total_questions': 0,
            'correct_answers': 0,
            'last_played': None,
            'accuracy': 0
        }
    
    # Topic Progress Methods
    def get_topic_progress(self, level: str, topic: str) -> Dict[str, Any]:
        """Get progress for specific topic"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM topic_progress 
                WHERE level = ? AND topic = ?
            """, (level, topic))
            row = cursor.fetchone()
            
            if row:
                return {
                    'best_score': row['best_score'],
                    'attempts': row['attempts'],
                    'total_questions': row['total_questions'],
                    'correct_answers': row['correct_answers'],
                    'last_attempt': row['last_attempt'],
                    'is_completed': bool(row['is_completed']),
                    'accuracy': (row['correct_answers'] / row['total_questions'] * 100) if row['total_questions'] > 0 else 0
                }
            
            return {
                'best_score': 0,
                'attempts': 0,
                'total_questions': 0,
                'correct_answers': 0,
                'last_attempt': None,
                'is_completed': False,
                'accuracy': 0
            }
    
    def update_topic_progress(self, level: str, topic: str, score: int, total_questions: int, correct_answers: int):
        """Update progress for specific topic"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get current progress
            current = self.get_topic_progress(level, topic)
            
            # Calculate new values
            new_best_score = max(current['best_score'], score)
            new_attempts = current['attempts'] + 1
            new_total_questions = current['total_questions'] + total_questions
            new_correct_answers = current['correct_answers'] + correct_answers
            is_completed = new_best_score >= 80
            
            cursor.execute("""
                INSERT OR REPLACE INTO topic_progress 
                (level, topic, best_score, attempts, total_questions, correct_answers, 
                 last_attempt, is_completed)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
            """, (level, topic, new_best_score, new_attempts, new_total_questions, 
                  new_correct_answers, is_completed))
            
            conn.commit()
            logging.debug(f"Topic progress updated: {level} - {topic}")
    
    def get_all_topic_progress(self, level: str) -> Dict[str, Dict[str, Any]]:
        """Get progress for all topics in a level"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM topic_progress 
                WHERE level = ?
            """, (level,))
            rows = cursor.fetchall()
            
            progress = {}
            for row in rows:
                progress[row['topic']] = {
                    'best_score': row['best_score'],
                    'attempts': row['attempts'],
                    'total_questions': row['total_questions'],
                    'correct_answers': row['correct_answers'],
                    'last_attempt': row['last_attempt'],
                    'is_completed': bool(row['is_completed']),
                    'accuracy': (row['correct_answers'] / row['total_questions'] * 100) if row['total_questions'] > 0 else 0
                }
            
            return progress
    
    # Questions Cache Methods
    def cache_questions(self, level: str, topic: str, questions: List[Dict], expires_hours: int = 24):
        """Cache generated questions"""
        from datetime import datetime, timedelta
        
        expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO questions_cache 
                (level, topic, question_data, expires_at)
                VALUES (?, ?, ?, ?)
            """, (level, topic, json.dumps(questions), expires_at.isoformat()))
            conn.commit()
            logging.debug(f"Questions cached: {level} - {topic}")
    
    def get_cached_questions(self, level: str, topic: str) -> Optional[List[Dict]]:
        """Get cached questions if not expired"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT question_data, expires_at FROM questions_cache 
                WHERE level = ? AND topic = ?
            """, (level, topic))
            row = cursor.fetchone()
            
            if row:
                expires_at = datetime.fromisoformat(row['expires_at'])
                if datetime.now() < expires_at:
                    return json.loads(row['question_data'])
                else:
                    # Remove expired cache
                    cursor.execute("""
                        DELETE FROM questions_cache 
                        WHERE level = ? AND topic = ?
                    """, (level, topic))
                    conn.commit()
            
            return None
    
    def clear_expired_cache(self):
        """Clear all expired cached questions"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM questions_cache 
                WHERE expires_at < CURRENT_TIMESTAMP
            """)
            deleted = cursor.rowcount
            conn.commit()
            logging.info(f"Cleared {deleted} expired cache entries")
    
    # Game Sessions Methods
    def save_game_session(self, session_data: Dict[str, Any]):
        """Save completed game session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO game_sessions 
                (level, topic, score, total_questions, accuracy, duration, streak, 
                 questions_data, answers_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_data['level'],
                session_data['topic'],
                session_data['score'],
                session_data['total_questions'],
                session_data['accuracy'],
                session_data.get('duration'),
                session_data.get('streak', 0),
                json.dumps(session_data.get('questions', [])),
                json.dumps(session_data.get('answers', []))
            ))
            conn.commit()
            logging.debug(f"Game session saved: {session_data['level']} - {session_data['topic']}")
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent game sessions"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT level, topic, score, total_questions, accuracy, 
                       duration, streak, completed_at
                FROM game_sessions 
                ORDER BY completed_at DESC 
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
    
    def get_session_statistics(self, level: Optional[str] = None, 
                             topic: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics for sessions"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            where_clause = ""
            params = []
            
            if level:
                where_clause += " WHERE level = ?"
                params.append(level)
                
                if topic:
                    where_clause += " AND topic = ?"
                    params.append(topic)
            elif topic:
                where_clause += " WHERE topic = ?"
                params.append(topic)
            
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as total_sessions,
                    AVG(accuracy) as avg_accuracy,
                    AVG(score) as avg_score,
                    MAX(score) as best_score,
                    AVG(duration) as avg_duration,
                    MAX(streak) as best_streak
                FROM game_sessions
                {where_clause}
            """, params)
            
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    # Settings Methods
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get application setting"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT setting_value FROM app_settings 
                WHERE setting_key = ?
            """, (key,))
            row = cursor.fetchone()
            
            if row:
                value = row['setting_value']
                # Try to parse as JSON for complex types
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            
            return default
    
    def set_setting(self, key: str, value: Any):
        """Set application setting"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Convert to JSON if needed
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value)
            else:
                value_str = str(value)
            
            cursor.execute("""
                INSERT OR REPLACE INTO app_settings 
                (setting_key, setting_value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, value_str))
            conn.commit()
            logging.debug(f"Setting updated: {key}")
    
    # Utility Methods
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get table counts
            tables = ['user_progress', 'topic_progress', 'questions_cache', 
                     'game_sessions', 'app_settings']
            stats = {}
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                stats[f"{table}_count"] = cursor.fetchone()['count']
            
            # Get database size
            cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
            stats['database_size_bytes'] = cursor.fetchone()['size']
            
            return stats
    
    def backup_database(self, backup_path: str):
        """Create database backup"""
        import shutil
        try:
            shutil.copy2(self.db_path, backup_path)
            logging.info(f"Database backed up to: {backup_path}")
            return True
        except Exception as e:
            logging.error(f"Database backup failed: {e}")
            return False
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Clean old game sessions
            cursor.execute("""
                DELETE FROM game_sessions 
                WHERE completed_at < datetime('now', '-{} days')
            """.format(days))
            deleted_sessions = cursor.rowcount
            
            # Clean expired cache
            cursor.execute("""
                DELETE FROM questions_cache 
                WHERE expires_at < CURRENT_TIMESTAMP
            """)
            deleted_cache = cursor.rowcount
            
            conn.commit()
            logging.info(f"Cleaned up {deleted_sessions} old sessions and {deleted_cache} expired cache entries")
