#!/usr/bin/env python3
"""
OPIC Learning App - Main Entry Point
A comprehensive OPIC (Oral Proficiency Interview-Computer) learning application
Author: OPIC Learning Team
Version: 1.0.0
"""

import sys
import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import application modules
try:
    from gui.main_window import MainWindow
    from models.database import DatabaseManager
    from config.settings import AppSettings
    from utils.helpers import setup_logging, check_dependencies
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required modules are installed.")
    sys.exit(1)

class OpicApplication:
    """Main application class"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.splash = None
        
    def setup_application(self):
        """Initialize the QApplication with proper settings"""
        # Enable high DPI support
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Create application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("OPIC Master")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("OPIC Learning")
        self.app.setOrganizationDomain("opic-learning.com")
        
        # Set application icon
        icon_path = project_root / "resources" / "icons" / "app_icon.png"
        if icon_path.exists():
            self.app.setWindowIcon(QPixmap(str(icon_path)))
    
    def show_splash_screen(self):
        """Show splash screen during startup"""
        splash_path = project_root / "resources" / "icons" / "splash.png"
        
        if splash_path.exists():
            pixmap = QPixmap(str(splash_path))
        else:
            # Create a simple splash screen if image not found
            pixmap = QPixmap(400, 300)
            pixmap.fill(Qt.blue)
        
        self.splash = QSplashScreen(pixmap)
        self.splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        self.splash.show()
        
        # Add loading text
        self.splash.showMessage(
            "Đang khởi tạo OPIC Master...", 
            Qt.AlignHCenter | Qt.AlignBottom, 
            Qt.white
        )
        
        # Process events to show splash
        self.app.processEvents()
    
    def load_stylesheet(self):
        """Load and apply application stylesheet"""
        style_path = project_root / "resources" / "styles.qss"
        
        if style_path.exists():
            try:
                with open(style_path, "r", encoding="utf-8") as f:
                    stylesheet = f.read()
                self.app.setStyleSheet(stylesheet)
                logging.info("Stylesheet loaded successfully")
            except Exception as e:
                logging.warning(f"Failed to load stylesheet: {e}")
        else:
            logging.warning("Stylesheet file not found, using default styles")
    
    def initialize_database(self):
        """Initialize application database"""
        try:
            self.splash.showMessage(
                "Đang khởi tạo cơ sở dữ liệu...", 
                Qt.AlignHCenter | Qt.AlignBottom, 
                Qt.white
            )
            self.app.processEvents()
            
            db_manager = DatabaseManager()
            db_manager.init_database()
            logging.info("Database initialized successfully")
            return True
            
        except Exception as e:
            logging.error(f"Database initialization failed: {e}")
            QMessageBox.critical(
                None, 
                "Lỗi Cơ sở dữ liệu", 
                f"Không thể khởi tạo cơ sở dữ liệu:\n{str(e)}\n\nỨng dụng sẽ thoát."
            )
            return False
    
    def create_main_window(self):
        """Create and setup main window"""
        try:
            self.splash.showMessage(
                "Đang tạo giao diện chính...", 
                Qt.AlignHCenter | Qt.AlignBottom, 
                Qt.white
            )
            self.app.processEvents()
            
            self.main_window = MainWindow()
            logging.info("Main window created successfully")
            return True
            
        except Exception as e:
            logging.error(f"Main window creation failed: {e}")
            QMessageBox.critical(
                None, 
                "Lỗi Giao diện", 
                f"Không thể tạo giao diện chính:\n{str(e)}\n\nỨng dụng sẽ thoát."
            )
            return False
    
    def finalize_startup(self):
        """Finalize application startup"""
        # Hide splash screen and show main window
        QTimer.singleShot(1000, self.hide_splash_and_show_main)
    
    def hide_splash_and_show_main(self):
        """Hide splash screen and show main window"""
        if self.splash:
            self.splash.close()
        
        if self.main_window:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
    
    def setup_exception_handler(self):
        """Setup global exception handler"""
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            logging.critical(
                "Uncaught exception", 
                exc_info=(exc_type, exc_value, exc_traceback)
            )
            
            QMessageBox.critical(
                None,
                "Lỗi Nghiêm trọng",
                f"Đã xảy ra lỗi không mong muốn:\n{str(exc_value)}\n\nVui lòng khởi động lại ứng dụng."
            )
        
        sys.excepthook = handle_exception
    
    def run(self):
        """Run the application"""
        try:
            # Setup logging
            setup_logging()
            logging.info("Starting OPIC Learning Application")
            
            # Check dependencies
            if not check_dependencies():
                QMessageBox.critical(
                    None,
                    "Thiếu Dependencies",
                    "Một số thư viện cần thiết chưa được cài đặt.\nVui lòng chạy: pip install -r requirements.txt"
                )
                return 1
            
            # Setup exception handler
            self.setup_exception_handler()
            
            # Initialize application
            self.setup_application()
            logging.info("QApplication initialized")
            
            # Show splash screen
            self.show_splash_screen()
            
            # Load stylesheet
            self.load_stylesheet()
            
            # Initialize database
            if not self.initialize_database():
                return 1
            
            # Create main window
            if not self.create_main_window():
                return 1
            
            # Finalize startup
            self.finalize_startup()
            
            # Run application
            logging.info("Application startup completed")
            return self.app.exec_()
            
        except Exception as e:
            logging.critical(f"Fatal error during startup: {e}")
            if hasattr(self, 'app') and self.app:
                QMessageBox.critical(
                    None,
                    "Lỗi Khởi động",
                    f"Không thể khởi động ứng dụng:\n{str(e)}"
                )
            return 1
        
        finally:
            logging.info("Application shutdown")

def main():
    """Main entry point"""
    app = OpicApplication()
    return app.run()

if __name__ == "__main__":
    sys.exit(main())
