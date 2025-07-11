"""
Main Window for OPIC Learning App
Handles window management and screen coordination
"""

import sys
import logging
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStackedWidget, 
    QMenuBar, QMenu, QAction, QStatusBar, QMessageBox,
    QDialog, QLabel, QProgressBar, QApplication
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeySequence

from gui.home_screen import HomeScreen
from gui.topic_screen import TopicScreen  
from gui.game_screen import GameScreen
from gui.settings_dialog import SettingsDialog
from gui.progress_dialog import ProgressDialog
from gui.about_dialog import AboutDialog

from models.database import DatabaseManager
from services.ai_service import ai_service
from config.settings import app_settings
from utils.helpers import resource_path, play_sound

class APITestThread(QThread):
    """Thread for testing API connection"""
    finished = pyqtSignal(bool, str)
    
    def run(self):
        try:
            result = ai_service.test_api_connection()
            self.finished.emit(result['success'], result['message'])
        except Exception as e:
            self.finished.emit(False, str(e))

class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signals
    level_changed = pyqtSignal(str)
    topic_selected = pyqtSignal(str, str)  # level, topic
    game_started = pyqtSignal()
    game_finished = pyqtSignal(dict)  # session data
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.db_manager = DatabaseManager()
        self.current_level = 'IM1'
        self.current_topic = ''
        
        # Screen references
        self.home_screen = None
        self.topic_screen = None
        self.game_screen = None
        self.stacked_widget = None
        
        # Status and progress
        self.status_label = None
        self.progress_bar = None
        
        # Threads
        self.api_test_thread = None
        
        # Setup UI
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.setup_connections()
        self.load_settings()
        
        # Initialize with home screen
        self.show_home_screen()
        
        logging.info("Main window initialized")
    
    def setup_ui(self):
        """Setup main UI components"""
        # Set window properties
        self.setWindowTitle("OPIC Master - Luyện thi OPIC chuẩn quốc tế")
        self.setMinimumSize(800, 600)
        
        # Load and set icon
        icon_path = resource_path("resources/icons/app_icon.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Create central widget with stacked layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Create screens
        self.home_screen = HomeScreen()
        self.topic_screen = TopicScreen()
        self.game_screen = GameScreen()
        
        # Add screens to stack
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.topic_screen)
        self.stacked_widget.addWidget(self.game_screen)
    
    def setup_menu_bar(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu('&Tệp')
        
        # New Game action
        new_game_action = QAction('&Bài thi mới', self)
        new_game_action.setShortcut(QKeySequence.New)
        new_game_action.setStatusTip('Bắt đầu bài thi mới')
        new_game_action.triggered.connect(self.show_topic_screen)
        file_menu.addAction(new_game_action)
        
        file_menu.addSeparator()
        
        # Import/Export actions
        import_action = QAction('&Nhập dữ liệu...', self)
        import_action.setStatusTip('Nhập dữ liệu từ file')
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        export_action = QAction('&Xuất dữ liệu...', self)
        export_action.setStatusTip('Xuất dữ liệu ra file')
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('T&hoát', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.setStatusTip('Thoát ứng dụng')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View Menu
        view_menu = menubar.addMenu('&Hiển thị')
        
        # Home action
        home_action = QAction('&Trang chủ', self)
        home_action.setShortcut('Ctrl+H')
        home_action.setStatusTip('Về trang chủ')
        home_action.triggered.connect(self.show_home_screen)
        view_menu.addAction(home_action)
        
        # Progress action
        progress_action = QAction('&Tiến độ', self)
        progress_action.setShortcut('Ctrl+P')
        progress_action.setStatusTip('Xem tiến độ học tập')
        progress_action.triggered.connect(self.show_progress_dialog)
        view_menu.addAction(progress_action)
        
        view_menu.addSeparator()
        
        # Fullscreen action
        fullscreen_action = QAction('&Toàn màn hình', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.setCheckable(True)
        fullscreen_action.setStatusTip('Chuyển đổi chế độ toàn màn hình')
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu('&Công cụ')
        
        # Settings action
        settings_action = QAction('&Cài đặt...', self)
        settings_action.setShortcut('Ctrl+,')
        settings_action.setStatusTip('Mở cài đặt ứng dụng')
        settings_action.triggered.connect(self.show_settings_dialog)
        tools_menu.addAction(settings_action)
        
        # API Test action
        api_test_action = QAction('&Kiểm tra API...', self)
        api_test_action.setStatusTip('Kiểm tra kết nối API')
        api_test_action.triggered.connect(self.test_api_connection)
        tools_menu.addAction(api_test_action)
        
        tools_menu.addSeparator()
        
        # Clear cache action
        clear_cache_action = QAction('&Xóa cache', self)
        clear_cache_action.setStatusTip('Xóa cache câu hỏi')
        clear_cache_action.triggered.connect(self.clear_cache)
        tools_menu.addAction(clear_cache_action)
        
        # Help Menu
        help_menu = menubar.addMenu('&Trợ giúp')
        
        # User Guide action
        guide_action = QAction('&Hướng dẫn sử dụng', self)
        guide_action.setShortcut('F1')
        guide_action.setStatusTip('Mở hướng dẫn sử dụng')
        guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(guide_action)
        
        # OPIC Info action
        opic_info_action = QAction('&Thông tin OPIC', self)
        opic_info_action.setStatusTip('Thông tin về kỳ thi OPIC')
        opic_info_action.triggered.connect(self.show_opic_info)
        help_menu.addAction(opic_info_action)
        
        help_menu.addSeparator()
        
        # About action
        about_action = QAction('&Giới thiệu...', self)
        about_action.setStatusTip('Thông tin về ứng dụng')
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Setup status bar"""
        status_bar = self.statusBar()
        
        # Status label
        self.status_label = QLabel("Sẵn sàng")
        status_bar.addWidget(self.status_label)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        status_bar.addPermanentWidget(self.progress_bar)
        
        # API status
        api_status = QLabel("API: Chưa kiểm tra")
        status_bar.addPermanentWidget(api_status)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Home screen connections
        self.home_screen.start_learning.connect(self.show_topic_screen)
        self.home_screen.level_changed.connect(self.on_level_changed)
        self.home_screen.show_progress.connect(self.show_progress_dialog)
        self.home_screen.show_settings.connect(self.show_settings_dialog)
        
        # Topic screen connections
        self.topic_screen.back_to_home.connect(self.show_home_screen)
        self.topic_screen.topic_selected.connect(self.on_topic_selected)
        self.topic_screen.level_changed.connect(self.on_level_changed)
        
        # Game screen connections
        self.game_screen.back_to_topics.connect(self.show_topic_screen)
        self.game_screen.back_to_home.connect(self.show_home_screen)
        self.game_screen.game_completed.connect(self.on_game_completed)
        self.game_screen.progress_updated.connect(self.on_progress_updated)
    
    def load_settings(self):
        """Load and apply settings"""
        try:
            # Load window geometry
            geometry = app_settings.get_window_geometry()
            self.resize(geometry['width'], geometry['height'])
            if geometry['maximized']:
                self.showMaximized()
            
            # Load current level
            user_progress = self.db_manager.get_user_progress()
            self.current_level = user_progress['current_level']
            
            # Apply font settings
            font = QFont(app_settings.ui_config.font_family, app_settings.get_font_size())
            self.setFont(font)
            
            logging.info("Settings loaded and applied")
            
        except Exception as e:
            logging.error(f"Failed to load settings: {e}")
    
    def save_settings(self):
        """Save current settings"""
        try:
            # Save window geometry
            if not self.isMaximized():
                app_settings.set_window_geometry(
                    self.width(), 
                    self.height(), 
                    self.isMaximized()
                )
            
            logging.info("Settings saved")
            
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")
    
    # Screen Navigation Methods
    def show_home_screen(self):
        """Show home screen"""
        self.stacked_widget.setCurrentWidget(self.home_screen)
        self.home_screen.refresh_data()
        self.status_label.setText("Trang chủ")
        
        if app_settings.is_sound_enabled():
            play_sound("navigate")
    
    def show_topic_screen(self):
        """Show topic selection screen"""
        self.topic_screen.set_level(self.current_level)
        self.stacked_widget.setCurrentWidget(self.topic_screen)
        self.status_label.setText(f"Chọn chủ đề - {self.current_level}")
        
        if app_settings.is_sound_enabled():
            play_sound("navigate")
    
    def show_game_screen(self, level: str, topic: str):
        """Show game screen"""
        self.current_level = level
        self.current_topic = topic
        
        self.game_screen.start_game(level, topic)
        self.stacked_widget.setCurrentWidget(self.game_screen)
        self.status_label.setText(f"Đang luyện tập - {level}: {topic}")
        
        if app_settings.is_sound_enabled():
            play_sound("game_start")
    
    # Event Handlers
    @pyqtSlot(str)
    def on_level_changed(self, level: str):
        """Handle level change"""
        self.current_level = level
        self.level_changed.emit(level)
        logging.info(f"Level changed to: {level}")
    
    @pyqtSlot(str, str)
    def on_topic_selected(self, level: str, topic: str):
        """Handle topic selection"""
        self.show_game_screen(level, topic)
        self.topic_selected.emit(level, topic)
        logging.info(f"Topic selected: {level} - {topic}")
    
    @pyqtSlot(dict)
    def on_game_completed(self, session_data: dict):
        """Handle game completion"""
        try:
            # Save session data
            self.db_manager.save_game_session(session_data)
            
            # Update progress
            accuracy = session_data['accuracy']
            if accuracy >= 80:
                if app_settings.is_sound_enabled():
                    play_sound("success")
            else:
                if app_settings.is_sound_enabled():
                    play_sound("try_again")
            
            self.game_finished.emit(session_data)
            logging.info(f"Game completed: {accuracy}% accuracy")
            
        except Exception as e:
            logging.error(f"Failed to handle game completion: {e}")
    
    @pyqtSlot(str, str, int, int)
    def on_progress_updated(self, level: str, topic: str, score: int, total: int):
        """Handle progress update"""
        try:
            accuracy = (score / total) * 100 if total > 0 else 0
            self.db_manager.update_topic_progress(level, topic, int(accuracy), total, score)
            logging.info(f"Progress updated: {level} - {topic}: {accuracy}%")
            
        except Exception as e:
            logging.error(f"Failed to update progress: {e}")
    
    # Dialog Methods
    def show_settings_dialog(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Reload settings
            self.load_settings()
            # Refresh screens
            self.home_screen.refresh_data()
    
    def show_progress_dialog(self):
        """Show progress dialog"""
        dialog = ProgressDialog(self)
        dialog.exec_()
    
    def show_about_dialog(self):
        """Show about dialog"""
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def show_user_guide(self):
        """Show user guide"""
        QMessageBox.information(
            self,
            "Hướng dẫn sử dụng",
            """
            <h3>Hướng dẫn sử dụng OPIC Master</h3>
            <p><b>1. Chọn Level:</b> Bắt đầu từ IM1 và tiến lên các level cao hơn</p>
            <p><b>2. Chọn chủ đề:</b> Mỗi level có 12 chủ đề khác nhau</p>
            <p><b>3. Luyện tập:</b> Trả lời 10 câu hỏi điền vào chỗ trống</p>
            <p><b>4. Đạt 80%:</b> Cần đạt ≥80% để hoàn thành chủ đề</p>
            <p><b>5. Lên level:</b> Hoàn thành 80% chủ đề để mở level mới</p>
            <p><b>6. Giải thích:</b> Đọc giải thích chi tiết sau mỗi câu</p>
            
            <p><b>Phím tắt:</b></p>
            <p>• Ctrl+H: Trang chủ</p>
            <p>• Ctrl+P: Xem tiến độ</p>
            <p>• F11: Toàn màn hình</p>
            <p>• F1: Hướng dẫn này</p>
            """
        )
    
    def show_opic_info(self):
        """Show OPIC information"""
        QMessageBox.information(
            self,
            "Thông tin về OPIC",
            """
            <h3>OPIC (Oral Proficiency Interview-Computer)</h3>
            <p>OPIC là kỳ thi đánh giá khả năng giao tiếp tiếng Anh được công nhận quốc tế.</p>
            
            <h4>Các level OPIC:</h4>
            <p><b>IM1-IM3:</b> Intermediate Mid (Trung cấp)</p>
            <p><b>IH:</b> Intermediate High (Trung cấp cao)</p>
            <p><b>AL:</b> Advanced Low (Nâng cao thấp)</p>
            <p><b>AM:</b> Advanced Mid (Nâng cao trung)</p>
            <p><b>AH:</b> Advanced High (Nâng cao cao)</p>
            
            <h4>Cấu trúc bài thi:</h4>
            <p>• Thời gian: 40 phút</p>
            <p>• Dạng câu hỏi: Nói về các chủ đề quen thuộc</p>
            <p>• Đánh giá: Khả năng giao tiếp thực tế</p>
            
            <p><b>Ứng dụng này giúp:</b> Luyện tập ngữ pháp và từ vựng theo chuẩn OPIC</p>
            """
        )
    
    # Utility Methods
    def test_api_connection(self):
        """Test API connection"""
        if not app_settings.get_api_key():
            QMessageBox.warning(
                self,
                "Thiếu API Key",
                "Vui lòng cài đặt API key trong menu Công cụ > Cài đặt"
            )
            return
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText("Đang kiểm tra API...")
        
        # Start test in thread
        self.api_test_thread = APITestThread()
        self.api_test_thread.finished.connect(self.on_api_test_finished)
        self.api_test_thread.start()
    
    @pyqtSlot(bool, str)
    def on_api_test_finished(self, success: bool, message: str):
        """Handle API test completion"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("Sẵn sàng")
        
        if success:
            QMessageBox.information(
                self,
                "Kết nối thành công",
                f"API hoạt động bình thường!\n\n{message}"
            )
            # Update status bar
            status_bar = self.statusBar()
            api_label = status_bar.children()[-1]  # Last widget
            if isinstance(api_label, QLabel):
                api_label.setText("API: Hoạt động")
        else:
            QMessageBox.warning(
                self,
                "Kết nối thất bại",
                f"Không thể kết nối API:\n{message}\n\nVui lòng kiểm tra:\n• API key đúng\n• Kết nối internet\n• Cài đặt proxy"
            )
    
    def clear_cache(self):
        """Clear question cache"""
        reply = QMessageBox.question(
            self,
            "Xóa cache",
            "Bạn có chắc muốn xóa tất cả cache câu hỏi?\nCache sẽ được tạo lại khi luyện tập.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.db_manager.clear_expired_cache()
                # Clear all cache by setting expiry to past
                with self.db_manager.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE questions_cache SET expires_at = '2000-01-01'")
                    conn.commit()
                
                QMessageBox.information(self, "Hoàn thành", "Cache đã được xóa thành công!")
                logging.info("Cache cleared manually")
                
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa cache:\n{str(e)}")
                logging.error(f"Failed to clear cache: {e}")
    
    def import_data(self):
        """Import user data"""
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Nhập dữ liệu",
            "",
            "JSON files (*.json);;All files (*.*)"
        )
        
        if file_path:
            try:
                success = app_settings.import_settings(file_path)
                if success:
                    QMessageBox.information(self, "Thành công", "Dữ liệu đã được nhập thành công!")
                    self.load_settings()
                    self.home_screen.refresh_data()
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể nhập dữ liệu từ file này.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi nhập dữ liệu:\n{str(e)}")
    
    def export_data(self):
        """Export user data"""
        from PyQt5.QtWidgets import QFileDialog
        from datetime import datetime
        
        default_filename = f"opic_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Xuất dữ liệu",
            default_filename,
            "JSON files (*.json);;All files (*.*)"
        )
        
        if file_path:
            try:
                success = app_settings.export_settings(file_path)
                if success:
                    QMessageBox.information(self, "Thành công", f"Dữ liệu đã được xuất ra:\n{file_path}")
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể xuất dữ liệu.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xuất dữ liệu:\n{str(e)}")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    # Window Events
    def closeEvent(self, event):
        """Handle window close event"""
        # Save current settings
        self.save_settings()
        
        # Close AI service
        ai_service.close()
        
        # Cleanup threads
        if self.api_test_thread and self.api_test_thread.isRunning():
            self.api_test_thread.quit()
            self.api_test_thread.wait(3000)  # Wait up to 3 seconds
        
        # Accept close
        event.accept()
        logging.info("Main window closed")
    
    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        # Auto-save geometry after resize
        QTimer.singleShot(1000, self.save_settings)  # Delay to avoid too frequent saves
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        # Global shortcuts
        if event.key() == Qt.Key_Escape:
            # Escape key behavior depends on current screen
            current_widget = self.stacked_widget.currentWidget()
            if current_widget == self.game_screen:
                self.show_topic_screen()
            elif current_widget == self.topic_screen:
                self.show_home_screen()
            event.accept()
        else:
            super().keyPressEvent(event)
    
    # Status Updates
    def update_status(self, message: str, timeout: int = 0):
        """Update status bar message"""
        self.status_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.status_label.setText("Sẵn sàng"))
    
    def show_progress(self, show: bool = True):
        """Show/hide progress bar"""
        self.progress_bar.setVisible(show)
        if not show:
            self.progress_bar.setRange(0, 1)
            self.progress_bar.setValue(0)
    
    def set_progress(self, value: int, maximum: int = 100):
        """Set progress bar value"""
        self.progress_bar.setRange(0, maximum)
        self.progress_bar.setValue(value)
        self.progress_bar.setVisible(True)
    
    # Public Methods for Screen Communication
    def get_current_level(self) -> str:
        """Get current selected level"""
        return self.current_level
    
    def get_current_topic(self) -> str:
        """Get current selected topic"""
        return self.current_topic
    
    def refresh_all_screens(self):
        """Refresh all screens with updated data"""
        self.home_screen.refresh_data()
        if hasattr(self.topic_screen, 'refresh_data'):
            self.topic_screen.refresh_data()
    
    def get_database_manager(self) -> DatabaseManager:
        """Get database manager instance"""
        return self.db_manager
