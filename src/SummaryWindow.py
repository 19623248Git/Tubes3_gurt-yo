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
    def __init__(self, applicant_name):
        super().__init__()
        self.setWindowTitle("CV Summary")
        self.setGeometry(150, 150, 700, 500)

        main_layout = QVBoxLayout(self)

        ### Information ###
        # EVERYTHING HERE ARE ALL DUMMY DATAS
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_layout = QFormLayout(info_frame)

        self.name_label = QLabel(f"<b>{applicant_name}</b>")
        self.birthdate_label = QLabel("07-03-2005") # Dummy data
        self.address_label = QLabel("Labtek V") # Dummy data
        self.phone_label = QLabel("0812 3456 7890") # Dummy data

        info_layout.addRow(self.name_label)
        info_layout.addRow(QLabel("Birthdate:"), self.birthdate_label)
        info_layout.addRow(QLabel("Address:"), self.address_label)
        info_layout.addRow(QLabel("Phone:"), self.phone_label)

        main_layout.addWidget(info_frame)

        ### Summary ###
        summary_frame = QFrame()
        summary_frame.setFrameShape(QFrame.StyledPanel)
        summary_layout = QVBoxLayout(summary_frame)
        summary_label = QLabel("A highly motivated and skilled individual with a passion for technology and innovation.") # Dummy data
        summary_label.setWordWrap(True)
        summary_layout.addWidget(summary_label)
        main_layout.addWidget(summary_frame)

        ### Skills ###
        skills_frame = self.create_section("Skills", ["Python", "PySide6", "SQL"])
        main_layout.addWidget(skills_frame)

        ### Job History ###
        job_history_frame = self.create_section("Job History", ["<b>CTO</b> (2000-2004)<br>Leading the organization's technology strategies"])
        main_layout.addWidget(job_history_frame)

        ### Education History ###
        education_frame = self.create_section("Education", ["<b>Informatics Engineering</b> - Institut Teknologi Bandung (2022-2026)"])
        main_layout.addWidget(education_frame)


    def create_section(self, title, items):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)

        title_label = QLabel(f"<b>{title}</b>")
        font = QFont()
        font.setPointSize(12)
        font.setCapitalization(QFont.AllUppercase)
        title_label.setFont(font)
        layout.addWidget(title_label)

        for item_text in items:
            item_label = QLabel(item_text)
            item_label.setWordWrap(True)
            layout.addWidget(item_label)

        return frame