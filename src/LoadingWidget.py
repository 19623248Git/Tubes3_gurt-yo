from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt, QTimer

class LoadingWidget(QWidget):
    """Custom loading widget with animation and progress."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_animation()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignCenter)
        self.animation_label.setFixedSize(80, 80)
        self.animation_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)
        layout.addWidget(self.animation_label, 0, Qt.AlignCenter)
        
        self.status_label = QLabel("Initializing search...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #4834d4;
            margin: 10px;
        """)
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #dcdde1;
                border-radius: 10px;
                background-color: #f1f2f6;
                text-align: center;
                font-weight: bold;
                color: #2d3436;
            }
            QProgressBar::chunk {
                background-color: #8e7cc3;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("0 / 0 CVs processed")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("""
            font-size: 14px;
            color: #95a5a6;
            margin: 5px;
            font-weight: bold;
        """)
        layout.addWidget(self.progress_label)
        
        self.current_cv_label = QLabel("")
        self.current_cv_label.setAlignment(Qt.AlignCenter)
        self.current_cv_label.setStyleSheet("""
            font-size: 12px;
            color: #95a5a6;
            font-style: italic;
        """)
        layout.addWidget(self.current_cv_label)
        
        self.cancel_button = QPushButton("Cancel Search")
        self.cancel_button.setFixedWidth(150)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(self.cancel_button, 0, Qt.AlignCenter)
    
    def setup_animation(self):
        """Setup spinning animation using QTimer."""
        self.rotation_angle = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)
        
        self.update_animation()
    
    def update_animation(self):
        """Update the loading animation."""
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        char_index = (self.rotation_angle // 5) % len(chars)
        
        self.animation_label.setText(chars[char_index])
        self.animation_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                font-size: 32px;
                color: #4834d4;
                font-weight: bold;
            }
        """)
        self.rotation_angle += 1
    
    def update_progress(self, current, total, current_cv):
        """Update progress information."""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.progress_label.setText(f"{current} / {total} CVs processed")
        
        if current_cv:
            self.current_cv_label.setText(f"Processing: {current_cv}")
        
        if current == 0:
            self.status_label.setText("Starting search...")
        elif current == total:
            self.status_label.setText("Finalizing results...")
        else:
            percentage = (current / total) * 100
            self.status_label.setText(f"Searching... ({percentage:.1f}%)")
    
    def stop_animation(self):
        """Stop the loading animation."""
        if hasattr(self, 'animation_timer'):
            self.animation_timer.stop()