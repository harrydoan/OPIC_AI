"""
Application Settings and Configuration
Manages app configuration, API settings, and user preferences
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class APIConfig:
    """API configuration settings"""
    provider: str = "openrouter"
    api_key: str = ""
    api_url: str = "https://openrouter.ai/api/v1/chat/completions"
    model: str = "openai/gpt-4o-mini"
    timeout: int = 30
    max_retries: int = 3
    temperature: float = 0.3
    max_tokens: int = 4000

@dataclass
class UIConfig:
    """UI configuration settings"""
    theme: str = "default"
    language: str = "vi"
    font_size: int = 12
    font_family: str = "Segoe UI"
    window_width: int = 1200
    window_height: int = 800
    window_maximized: bool = False
    sound_enabled: bool = True
    animations_enabled: bool = True

@dataclass
class GameConfig:
    """Game configuration settings"""
    auto_advance: bool = False
    show_hints: bool = True
    question_timer: bool = False
    timer_duration: int = 30
    shuffle_choices: bool = True
    immediate_feedback: bool = True
    explanation_auto_show: bool = False

@dataclass
class ProgressConfig:
    """Progress tracking configuration"""
    backup_enabled: bool = True
    backup_frequency: int = 7  # days
    data_retention: int = 365  # days
    sync_enabled: bool = False
    export_enabled: bool = True

class AppSettings:
    """Main application settings manager"""
    
    def __init__(self):
        self.app_name = "OPIC_Learning"
        self.version = "1.0.0"
        
        # Setup directories
        self.app_dir = Path.home() / f".{self.app_name.lower()}"
        self.app_dir.mkdir(exist_ok=True)
        
        self.config_file = self.app_dir / "config.json"
        self.cache_dir = self.app_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        self.logs_dir = self.app_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.backups_dir = self.app_dir / "backups"
        self.backups_dir.mkdir(exist_ok=True)
        
        # Initialize configurations
        self.api_config = APIConfig()
        self.ui_config = UIConfig()
        self.game_config = GameConfig()
        self.progress_config = ProgressConfig()
        
        # Load existing settings
        self.load_settings()
        
        logging.info(f"Settings initialized - App dir: {self.app_dir}")
    
    def load_settings(self):
        """Load settings from config file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Load API config
                if 'api' in config_data:
                    api_data = config_data['api']
                    for key, value in api_data.items():
                        if hasattr(self.api_config, key):
                            setattr(self.api_config, key, value)
                
                # Load UI config
                if 'ui' in config_data:
                    ui_data = config_data['ui']
                    for key, value in ui_data.items():
                        if hasattr(self.ui_config, key):
                            setattr(self.ui_config, key, value)
                
                # Load Game config
                if 'game' in config_data:
                    game_data = config_data['game']
                    for key, value in game_data.items():
                        if hasattr(self.game_config, key):
                            setattr(self.game_config, key, value)
                
                # Load Progress config
                if 'progress' in config_data:
                    progress_data = config_data['progress']
                    for key, value in progress_data.items():
                        if hasattr(self.progress_config, key):
                            setattr(self.progress_config, key, value)
                
                logging.info("Settings loaded successfully")
            else:
                logging.info("No config file found, using defaults")
                self.save_settings()  # Create default config file
                
        except Exception as e:
            logging.error(f"Failed to load settings: {e}")
            # Keep default settings if loading fails
    
    def save_settings(self):
        """Save current settings to config file"""
        try:
            config_data = {
                'version': self.version,
                'api': asdict(self.api_config),
                'ui': asdict(self.ui_config),
                'game': asdict(self.game_config),
                'progress': asdict(self.progress_config)
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            logging.info("Settings saved successfully")
            
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")
    
    # API Configuration Methods
    def get_api_key(self) -> str:
        """Get API key from config or environment"""
        api_key = self.api_config.api_key
        if not api_key:
            # Try environment variable
            api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')
            if api_key:
                self.api_config.api_key = api_key
                self.save_settings()
        return api_key or ""
    
    def set_api_key(self, api_key: str):
        """Set API key"""
        self.api_config.api_key = api_key
        self.save_settings()
        logging.info("API key updated")
    
    def get_api_url(self) -> str:
        """Get API URL"""
        return self.api_config.api_url
    
    def set_api_url(self, url: str):
        """Set API URL"""
        self.api_config.api_url = url
        self.save_settings()
    
    def get_model(self) -> str:
        """Get AI model"""
        return self.api_config.model
    
    def set_model(self, model: str):
        """Set AI model"""
        self.api_config.model = model
        self.save_settings()
    
    def get_timeout(self) -> int:
        """Get API timeout"""
        return self.api_config.timeout
    
    def get_api_config(self) -> APIConfig:
        """Get complete API configuration"""
        return self.api_config
    
    # UI Configuration Methods
    def get_theme(self) -> str:
        """Get UI theme"""
        return self.ui_config.theme
    
    def set_theme(self, theme: str):
        """Set UI theme"""
        self.ui_config.theme = theme
        self.save_settings()
    
    def get_language(self) -> str:
        """Get interface language"""
        return self.ui_config.language
    
    def set_language(self, language: str):
        """Set interface language"""
        self.ui_config.language = language
        self.save_settings()
    
    def get_font_size(self) -> int:
        """Get font size"""
        return self.ui_config.font_size
    
    def set_font_size(self, size: int):
        """Set font size"""
        self.ui_config.font_size = max(8, min(24, size))  # Clamp between 8-24
        self.save_settings()
    
    def get_window_geometry(self) -> Dict[str, int]:
        """Get window geometry settings"""
        return {
            'width': self.ui_config.window_width,
            'height': self.ui_config.window_height,
            'maximized': self.ui_config.window_maximized
        }
    
    def set_window_geometry(self, width: int, height: int, maximized: bool = False):
        """Set window geometry"""
        self.ui_config.window_width = max(800, width)
        self.ui_config.window_height = max(600, height)
        self.ui_config.window_maximized = maximized
        self.save_settings()
    
    def is_sound_enabled(self) -> bool:
        """Check if sound is enabled"""
        return self.ui_config.sound_enabled
    
    def set_sound_enabled(self, enabled: bool):
        """Enable/disable sound"""
        self.ui_config.sound_enabled = enabled
        self.save_settings()
    
    def are_animations_enabled(self) -> bool:
        """Check if animations are enabled"""
        return self.ui_config.animations_enabled
    
    def set_animations_enabled(self, enabled: bool):
        """Enable/disable animations"""
        self.ui_config.animations_enabled = enabled
        self.save_settings()
    
    def get_ui_config(self) -> UIConfig:
        """Get complete UI configuration"""
        return self.ui_config
    
    # Game Configuration Methods
    def is_auto_advance_enabled(self) -> bool:
        """Check if auto advance is enabled"""
        return self.game_config.auto_advance
    
    def set_auto_advance(self, enabled: bool):
        """Enable/disable auto advance"""
        self.game_config.auto_advance = enabled
        self.save_settings()
    
    def are_hints_enabled(self) -> bool:
        """Check if hints are enabled"""
        return self.game_config.show_hints
    
    def set_hints_enabled(self, enabled: bool):
        """Enable/disable hints"""
        self.game_config.show_hints = enabled
        self.save_settings()
    
    def is_timer_enabled(self) -> bool:
        """Check if question timer is enabled"""
        return self.game_config.question_timer
    
    def set_timer_enabled(self, enabled: bool):
        """Enable/disable question timer"""
        self.game_config.question_timer = enabled
        self.save_settings()
    
    def get_timer_duration(self) -> int:
        """Get timer duration in seconds"""
        return self.game_config.timer_duration
    
    def set_timer_duration(self, seconds: int):
        """Set timer duration"""
        self.game_config.timer_duration = max(10, min(300, seconds))  # 10s to 5min
        self.save_settings()
    
    def is_shuffle_enabled(self) -> bool:
        """Check if choice shuffling is enabled"""
        return self.game_config.shuffle_choices
    
    def set_shuffle_enabled(self, enabled: bool):
        """Enable/disable choice shuffling"""
        self.game_config.shuffle_choices = enabled
        self.save_settings()
    
    def is_immediate_feedback_enabled(self) -> bool:
        """Check if immediate feedback is enabled"""
        return self.game_config.immediate_feedback
    
    def set_immediate_feedback(self, enabled: bool):
        """Enable/disable immediate feedback"""
        self.game_config.immediate_feedback = enabled
        self.save_settings()
    
    def is_explanation_auto_show_enabled(self) -> bool:
        """Check if explanation auto-show is enabled"""
        return self.game_config.explanation_auto_show
    
    def set_explanation_auto_show(self, enabled: bool):
        """Enable/disable explanation auto-show"""
        self.game_config.explanation_auto_show = enabled
        self.save_settings()
    
    def get_game_config(self) -> GameConfig:
        """Get complete game configuration"""
        return self.game_config
    
    # Progress Configuration Methods
    def is_backup_enabled(self) -> bool:
        """Check if backup is enabled"""
        return self.progress_config.backup_enabled
    
    def set_backup_enabled(self, enabled: bool):
        """Enable/disable backup"""
        self.progress_config.backup_enabled = enabled
        self.save_settings()
    
    def get_backup_frequency(self) -> int:
        """Get backup frequency in days"""
        return self.progress_config.backup_frequency
    
    def set_backup_frequency(self, days: int):
        """Set backup frequency"""
        self.progress_config.backup_frequency = max(1, min(30, days))
        self.save_settings()
    
    def get_data_retention(self) -> int:
        """Get data retention period in days"""
        return self.progress_config.data_retention
    
    def set_data_retention(self, days: int):
        """Set data retention period"""
        self.progress_config.data_retention = max(30, min(1095, days))  # 30 days to 3 years
        self.save_settings()
    
    def get_progress_config(self) -> ProgressConfig:
        """Get complete progress configuration"""
        return self.progress_config
    
    # Directory and Path Methods
    def get_app_directory(self) -> Path:
        """Get application directory"""
        return self.app_dir
    
    def get_cache_directory(self) -> Path:
        """Get cache directory"""
        return self.cache_dir
    
    def get_logs_directory(self) -> Path:
        """Get logs directory"""
        return self.logs_dir
    
    def get_backups_directory(self) -> Path:
        """Get backups directory"""
        return self.backups_dir
    
    def get_database_path(self) -> str:
        """Get database file path"""
        return str(self.app_dir / "opic_app.db")
    
    # Utility Methods
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.api_config = APIConfig()
        self.ui_config = UIConfig()
        self.game_config = GameConfig()
        self.progress_config = ProgressConfig()
        self.save_settings()
        logging.info("Settings reset to defaults")
    
    def export_settings(self, file_path: str) -> bool:
        """Export settings to file"""
        try:
            config_data = {
                'version': self.version,
                'exported_at': str(datetime.now()),
                'api': asdict(self.api_config),
                'ui': asdict(self.ui_config),
                'game': asdict(self.game_config),
                'progress': asdict(self.progress_config)
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Settings exported to: {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to export settings: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Import settings from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate version compatibility
            imported_version = config_data.get('version', '0.0.0')
            if not self._is_version_compatible(imported_version):
                logging.warning(f"Version mismatch: {imported_version} vs {self.version}")
            
            # Import configurations
            if 'api' in config_data:
                api_data = config_data['api']
                for key, value in api_data.items():
                    if hasattr(self.api_config, key):
                        setattr(self.api_config, key, value)
            
            if 'ui' in config_data:
                ui_data = config_data['ui']
                for key, value in ui_data.items():
                    if hasattr(self.ui_config, key):
                        setattr(self.ui_config, key, value)
            
            if 'game' in config_data:
                game_data = config_data['game']
                for key, value in game_data.items():
                    if hasattr(self.game_config, key):
                        setattr(self.game_config, key, value)
            
            if 'progress' in config_data:
                progress_data = config_data['progress']
                for key, value in progress_data.items():
                    if hasattr(self.progress_config, key):
                        setattr(self.progress_config, key, value)
            
            self.save_settings()
            logging.info(f"Settings imported from: {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to import settings: {e}")
            return False
    
    def _is_version_compatible(self, version: str) -> bool:
        """Check if version is compatible"""
        try:
            current_parts = [int(x) for x in self.version.split('.')]
            import_parts = [int(x) for x in version.split('.')]
            
            # Major version must match
            return current_parts[0] == import_parts[0]
            
        except:
            return False
    
    def get_setting_summary(self) -> Dict[str, Any]:
        """Get summary of all settings"""
        return {
            'app_info': {
                'name': self.app_name,
                'version': self.version,
                'app_directory': str(self.app_dir)
            },
            'api': {
                'provider': self.api_config.provider,
                'model': self.api_config.model,
                'api_key_set': bool(self.api_config.api_key),
                'timeout': self.api_config.timeout
            },
            'ui': {
                'theme': self.ui_config.theme,
                'language': self.ui_config.language,
                'font_size': self.ui_config.font_size,
                'sound_enabled': self.ui_config.sound_enabled,
                'animations_enabled': self.ui_config.animations_enabled
            },
            'game': {
                'auto_advance': self.game_config.auto_advance,
                'show_hints': self.game_config.show_hints,
                'question_timer': self.game_config.question_timer,
                'shuffle_choices': self.game_config.shuffle_choices,
                'immediate_feedback': self.game_config.immediate_feedback
            },
            'progress': {
                'backup_enabled': self.progress_config.backup_enabled,
                'backup_frequency': self.progress_config.backup_frequency,
                'data_retention': self.progress_config.data_retention
            }
        }
    
    def validate_settings(self) -> List[str]:
        """Validate current settings and return list of issues"""
        issues = []
        
        # Validate API settings
        if not self.api_config.api_key:
            issues.append("API key not set")
        
        if not self.api_config.api_url:
            issues.append("API URL not set")
        
        if self.api_config.timeout < 5 or self.api_config.timeout > 300:
            issues.append("API timeout out of range (5-300 seconds)")
        
        # Validate UI settings
        if self.ui_config.font_size < 8 or self.ui_config.font_size > 24:
            issues.append("Font size out of range (8-24)")
        
        if self.ui_config.window_width < 800 or self.ui_config.window_height < 600:
            issues.append("Window size too small (minimum 800x600)")
        
        # Validate game settings
        if self.game_config.timer_duration < 10 or self.game_config.timer_duration > 300:
            issues.append("Timer duration out of range (10-300 seconds)")
        
        # Validate progress settings
        if self.progress_config.backup_frequency < 1 or self.progress_config.backup_frequency > 30:
            issues.append("Backup frequency out of range (1-30 days)")
        
        if self.progress_config.data_retention < 30:
            issues.append("Data retention too short (minimum 30 days)")
        
        return issues

# Global settings instance
app_settings = AppSettings()

# Environment-specific configurations
class DevelopmentConfig:
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    API_TIMEOUT = 60
    CACHE_ENABLED = False

class ProductionConfig:
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = logging.INFO
    API_TIMEOUT = 30
    CACHE_ENABLED = True

class TestingConfig:
    """Testing environment configuration"""
    DEBUG = True
    LOG_LEVEL = logging.WARNING
    API_TIMEOUT = 10
    CACHE_ENABLED = False
    DATABASE_PATH = ":memory:"

def get_config_class():
    """Get configuration class based on environment"""
    env = os.getenv('OPIC_ENV', 'production').lower()
    
    if env == 'development':
        return DevelopmentConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return ProductionConfig

# Current environment config
current_config = get_config_class()
