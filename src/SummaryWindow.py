import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QScrollArea,
    QFormLayout,
    QRadioButton,
    QSpinBox,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

class SummaryWindow(QWidget):
    def __init__(self, details):
        super().__init__()
        self.setWindowTitle("CV Summary")
        self.setGeometry(150, 150, 800, 700)  # Slightly larger window
        self.setObjectName("summaryWindow")

        # Set window-wide stylesheet
        self.setStyleSheet("""
            #summaryWindow {
                background-color: #f5f6fa;
            }
            QWidget {
                background-color: #f5f6fa;
            }
            QFrame {
                background-color: white;
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
            QLabel {
                background-color: transparent;
                color: #2d3436;
                font-size: 14px;
            }
        """)

        window_layout = QHBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_content_widget = QWidget()
        main_layout = QVBoxLayout(scroll_content_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        ### Header ###
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        
        full_name = f"{details.get('first_name', '')} {details.get('last_name', '')}"
        self.name_label = QLabel(full_name)
        self.name_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 10px;
        """)
        header_layout.addWidget(self.name_label)

        main_layout.addWidget(header_frame)

        ### Information ###
        info_frame = QFrame()
        info_layout = QFormLayout(info_frame)
        info_layout.setSpacing(12)
        
        info_title = QLabel("Personal Information")
        info_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 10px;
        """)
        info_layout.addRow(info_title)

        self.birthdate_label = QLabel(details.get('date_of_birth', 'N/A'))
        self.address_label = QLabel(details.get('address', 'N/A'))
        self.phone_label = QLabel(details.get('phone_number', 'N/A'))

        self.birthdate_label.setStyleSheet("color: #636e72;")
        self.address_label.setStyleSheet("color: #636e72;")
        self.phone_label.setStyleSheet("color: #636e72;")

        info_layout.addRow(QLabel("<b>Birthdate:</b>"), self.birthdate_label)
        info_layout.addRow(QLabel("<b>Address:</b>"), self.address_label)
        info_layout.addRow(QLabel("<b>Phone:</b>"), self.phone_label)

        main_layout.addWidget(info_frame)

        ### Summary ###
        summary_frame = QFrame()
        summary_layout = QVBoxLayout(summary_frame)
        
        summary_title = QLabel("Professional Summary")
        summary_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 10px;
        """)
        summary_layout.addWidget(summary_title)
        
        summary_text = "A highly motivated and skilled individual with a passion for technology and innovation."  # Dummy data
        summary_label = QLabel(summary_text)
        summary_label.setWordWrap(True)
        summary_label.setStyleSheet("color: #636e72; line-height: 1.5;")
        summary_layout.addWidget(summary_label)
        
        main_layout.addWidget(summary_frame)

        ### Skills ###
        skills_frame = self.create_section("Skills", ["Python", "PySide6", "SQL"])
        main_layout.addWidget(skills_frame)

        ### Job History ###
        job_history_frame = self.create_section(
            "Professional Experience",
            ["<b>Chief Technology Officer</b><br>Company Name (2000-2004)<br>• Leading the organization's technology strategies<br>• Managing tech teams and implementing innovative solutions"]
        )
        main_layout.addWidget(job_history_frame)

        ### Education History ###
        education_frame = self.create_section(
            "Education",
            ["<b>Bachelor of Informatics Engineering</b><br>Institut Teknologi Bandung (2022-2026)<br>• Notable coursework in Software Engineering, Data Structures, and Algorithms"]
        )
        main_layout.addWidget(education_frame)

        main_layout.addStretch()
        scroll_area.setWidget(scroll_content_widget)
        window_layout.addWidget(scroll_area)

    def create_section(self, title, items):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 10px;
        """)
        layout.addWidget(title_label)

        for item_text in items:
            item_label = QLabel(item_text)
            item_label.setWordWrap(True)
            item_label.setStyleSheet("""
                color: #636e72;
                line-height: 1.5;
                margin-bottom: 8px;
            """)
            layout.addWidget(item_label)

        return frame