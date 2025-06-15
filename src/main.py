import sys
import os
import time
import json
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
    QFileDialog,  # Add this import
    QMessageBox,  # Add this import
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from SummaryWindow import SummaryWindow 
from Database import Database
from ExtractCV import ExtractCV
from Search.Search import Search
from RegEx import extract_all_details

class CVAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gurt:Yo CV Analyzer")
        self.setGeometry(100, 100, 1000, 700)
        self.db = None
        self.config_path = "config/database.json"  # Default config path
        self.search_engine = Search()  # Create search engine once

        # Set application-wide stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            #contentContainer {
                background-color: #f5f6fa;
            }
            #cardContainer {
                background-color: #f5f6fa;
            }
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton {
                background-color: #4834d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #686de0;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #dcdde1;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4834d4;
            }
            QLabel {
                color: #2d3436;
                font-size: 14px;
            }
            QLabel#statusLabel {
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QLabel#statusLabel[status="success"] {
                background-color: #27ae60;
                color: white;
            }
            QLabel#statusLabel[status="error"] {
                background-color: #e74c3c;
                color: white;
            }
            QLabel#statusLabel[status="none"] {
                background-color: #95a5a6;
                color: white;
            }
            QLabel#pathLabel {
                color: #636e72;
                font-size: 12px;
                padding: 5px 10px;
                background-color: #f1f2f6;
                border-radius: 3px;
            }
            QMessageBox {
                background-color: white;
            }
            QRadioButton {
                font-size: 14px;
                spacing: 8px;
                color: #2d3436;
            }
            QSpinBox {
                padding: 8px;
                border: 2px solid #dcdde1;
                border-radius: 5px;
            }
            QScrollArea {
                border: none;
                background-color: #f5f6fa;
            }
        """)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        # scroll_area.setStyleSheet()
        self.setCentralWidget(scroll_area)

        # Main widget and layout
        main_widget = QWidget()
        main_widget.setObjectName("contentContainer")
        scroll_area.setWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        ### Top Bar with Database Controls ###
        top_bar_frame = QFrame()
        top_bar_layout = QHBoxLayout(top_bar_frame)
        top_bar_layout.setContentsMargins(20, 10, 20, 10)
        
        # Left side - Status and Path
        left_layout = QVBoxLayout()
        
        # Status Label
        self.status_label = QLabel("No Database Loaded")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setProperty("status", "none")
        left_layout.addWidget(self.status_label)
        
        # Config Path Label
        self.path_label = QLabel(f"Config: {self.config_path}")
        self.path_label.setObjectName("pathLabel")
        left_layout.addWidget(self.path_label)
        
        # Database Controls
        db_controls_layout = QHBoxLayout()
        db_controls_layout.setSpacing(10)
        
        top_bar_layout.addLayout(left_layout)
        top_bar_layout.addStretch()
        
        self.config_button = QPushButton("Set Database Path")
        self.config_button.setFixedWidth(150)
        self.config_button.clicked.connect(self.set_database_path)
        self.load_database_button = QPushButton("Load Database")
        self.load_database_button.setFixedWidth(150)
        self.load_database_button.clicked.connect(self.load_database)
        
        top_bar_layout.addWidget(self.config_button)
        top_bar_layout.addWidget(self.load_database_button)
        
        main_layout.addWidget(top_bar_frame)

        ### Search Panel ###
        search_panel = QFrame()
        search_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        search_layout = QFormLayout(search_panel)
        search_layout.setSpacing(15)
        search_layout.setContentsMargins(20, 20, 20, 20)

        # Title for search panel
        search_title = QLabel("Search CVs")
        search_title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 10px;
        """)
        search_layout.addRow(search_title)

        # Keywords input
        self.keywords_input = QLineEdit()
        self.keywords_input.setStyleSheet("color: #2d3436;")
        self.keywords_input.setPlaceholderText("e.g., React, Express, HTML")
        search_layout.addRow(QLabel("Keywords:"), self.keywords_input)

        # Search Algorithm selection
        algorithm_layout = QHBoxLayout()
        self.kmp_radio = QRadioButton("KMP")
        self.kmp_radio.setStyleSheet("color: #2d3436;")
        self.bm_radio = QRadioButton("BM")
        self.bm_radio.setStyleSheet("color: #2d3436;")
        self.kmp_radio.setChecked(True)
        algorithm_layout.addWidget(self.kmp_radio)
        algorithm_layout.addWidget(self.bm_radio)
        search_layout.addRow(QLabel("Search Algorithm:"), algorithm_layout)

        # Top Matches selector
        self.top_matches_spinbox = QSpinBox()
        self.top_matches_spinbox.setMinimum(1)
        self.top_matches_spinbox.setValue(5)
        search_layout.addRow(QLabel("Top Matches:"), self.top_matches_spinbox)

        # Search Button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.search_button = QPushButton("Search CVs")
        self.search_button.setEnabled(False)
        self.search_button.setFixedWidth(200)
        button_layout.addWidget(self.search_button)
        search_layout.addRow(button_layout)

        main_layout.addWidget(search_panel)

        ### Results Section ###
        results_frame = QFrame()
        results_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        results_frame.setMinimumHeight(400)
        main_layout.addWidget(results_frame)
        results_layout = QVBoxLayout(results_frame)
        results_layout.setContentsMargins(20, 20, 20, 20)
        results_layout.setSpacing(0)

        # Results title
        results_title = QLabel("Search Results")
        results_title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 5px;
        """)
        results_layout.addWidget(results_title)

        # Summary of search performance
        self.results_summary_label = QLabel("Search results will appear here.")
        self.results_summary_label.setAlignment(Qt.AlignCenter)
        self.results_summary_label.setStyleSheet("""
            color: #636e72;
            font-size: 16px;
            padding: 5px;
        """)
        results_layout.addWidget(self.results_summary_label)

        # Area for CV cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f6fa;
            }
        """)
        results_layout.addWidget(scroll_area)

        self.results_container = QWidget()
        self.results_container.setObjectName("cardContainer")
        self.results_grid_layout = QVBoxLayout(self.results_container)
        self.results_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.results_grid_layout.setSpacing(1)
        scroll_area.setWidget(self.results_container)
        self.summary_window = None

        # Connect buttons to their handlers (only once)
        self.search_button.clicked.connect(self.perform_search)

    def set_database_path(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Database Configuration File",
                "",
                "JSON Files (*.json)"
            )
            if file_path:                # Update the config path
                self.config_path = file_path
                # Test if the config file is valid by trying to load it
                with open(file_path, 'r') as f:
                    json.load(f)  # This will raise an error if JSON is invalid
                
                # Update the path display
                self.path_label.setText(f"Config: {file_path}")
                self.status_label.setText("Database Path Updated")
                self.status_label.setProperty("status", "success")
                self.status_label.style().unpolish(self.status_label)
                self.status_label.style().polish(self.status_label)
                QMessageBox.information(self, "Success", "Database configuration path updated successfully!")
        except json.JSONDecodeError:
            self.status_label.setText("Invalid Config File")
            self.status_label.setProperty("status", "error")
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)
            QMessageBox.critical(self, "Error", "The selected file is not a valid JSON configuration file.")
        except Exception as e:
            self.status_label.setText("Failed to Set Path")
            self.status_label.setProperty("status", "error")
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)
            QMessageBox.critical(self, "Error", f"Failed to update database path: {str(e)}")

    def load_database(self):
        try:
            # Create new database instance with current config path
            self.db = Database(self.config_path)
            
            # Try to establish connection
            if self.db.create_connection():
                self.status_label.setText("Database Connected")
                self.status_label.setProperty("status", "success")
                self.status_label.style().unpolish(self.status_label)
                self.status_label.style().polish(self.status_label)
                self.search_button.setEnabled(True)
                QMessageBox.information(self, "Success", "Database loaded and connected successfully!")
            else:
                raise Exception("Failed to establish database connection")
        except Exception as e:
            self.status_label.setText("Failed to Load")
            self.status_label.setProperty("status", "error")
            self.status_label.style().unpolish(self.status_label)
            self.status_label.style().polish(self.status_label)
            self.search_button.setEnabled(False)
            QMessageBox.critical(self, "Error", f"Failed to load database: {str(e)}")

    def perform_search(self):
        ## Clear Cards ##
        for i in reversed(range(self.results_grid_layout.count())):
            widget = self.results_grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        keywords_text = self.keywords_input.text()
        if not keywords_text:
            self.results_summary_label.setText("Please enter at least one keyword.")
            return
        keywords = [kw.strip().lower() for kw in keywords_text.replace(",", " ").split() if kw.strip()]
        algorithm = "kmp" if self.kmp_radio.isChecked() else "bm"
        top_n = self.top_matches_spinbox.value()

        if not self.db:
            self.results_summary_label.setText("Please load the database first.")
            return
        
        self.results_summary_label.setText(f"Searching {algorithm.upper()} for '{keywords}'...")
        QApplication.processEvents() # Allow GUI to update

        start_time = time.time()
        all_applications = self.db.get_all_cv_data()
        results = []
        
        for app_data in all_applications:
            cv_path = app_data['cv_path']
            cv_extractor = ExtractCV(cv_path) 
            
            matched_keywords = {}
            for keyword in keywords:
                count = self.search_engine._search(algorithm, cv_extractor, keyword)
                if count > 0:
                    matched_keywords[keyword] = count
            
            if matched_keywords:
                result_entry = {
                    "detail_id": app_data['detail_id'],
                    "applicant_id": app_data['applicant_id'],
                    "name": f"{app_data['first_name']} {app_data['last_name']}",
                    "application_role": app_data['application_role'],
                    "cv_path": cv_path,
                    "matched_keywords": matched_keywords
                }
                results.append(result_entry)
        
        runtime_ms = (time.time() - start_time) * 1000

        # Sort results and get top N
        results.sort(key=lambda x: sum(x['matched_keywords'].values()), reverse=True)
        final_results = results[:top_n]
        
        self.results_summary_label.setText(
            f"Exact Match: Scanned {len(all_applications)} CVs in {runtime_ms:.2f} ms. Found {len(results)} relevant CV(s)."
        )

        # Clear previous results
        for i in reversed(range(self.results_grid_layout.count())):
            widget = self.results_grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        if not final_results:
            self.results_summary_label.setText("No matches found.")
            return

        for result in final_results:
            card = self.create_cv_card(
                result["detail_id"],
                result["applicant_id"],
                result["name"],
                result["application_role"],
                result["cv_path"],
                result["matched_keywords"]
            )
            self.results_grid_layout.addWidget(card)

    def create_cv_card(self, detail_id, applicant_id, name, application_role, cv_path, matched_keywords_data):
        card = QFrame()
        card.setFrameShape(QFrame.Box)
        card.setLineWidth(1)
        card_layout = QVBoxLayout(card)

        name_label = QLabel(f"<b>{name}</b>")
        role_label = QLabel(f"{application_role}")
        match_count_label = QLabel(f"{len(matched_keywords_data)} keywords matched")

        details_text = []
        i = 1
        for keyword, count in matched_keywords_data.items():
            occurrence_str = "occurrence" if count == 1 else "occurrences"
            details_text.append(f"{i}. {keyword}: {count} {occurrence_str}")
            i += 1
        keywords_label = QLabel("\n".join(details_text))
        keywords_label.setAlignment(Qt.AlignLeft)

        card_layout.addWidget(name_label)
        card_layout.addWidget(role_label)
        card_layout.addWidget(match_count_label)
        card_layout.addWidget(keywords_label)

        button_layout = QHBoxLayout()
        summary_button = QPushButton("Summary")
        view_cv_button = QPushButton("View CV")

        summary_button.clicked.connect(lambda: self.show_summary(detail_id))
        view_cv_button.clicked.connect(lambda: self.view_cv(name, cv_path))

        button_layout.addWidget(summary_button)
        button_layout.addWidget(view_cv_button)
        card_layout.addLayout(button_layout)

        return card

    def show_summary(self, detail_id): 
        if not self.db:
            self.results_summary_label.setText("Please load the database first.")
            return
            
        details = self.db.get_summary_details_by_id(detail_id)

        if details:
            cv_path = details.get('cv_path', '')
            if cv_path:
                extractor = ExtractCV(cv_path)
                extractor.extract()
                full_text = extractor.get_raw_text() # Use the raw extracted text for Regex
                regex_details = extract_all_details(full_text)
                print(f"Extracted details: {regex_details}") # DEBUG
                details.update(regex_details)

            self.summary_window = SummaryWindow(details)
            self.summary_window.show()
        else:
            print(f"No details found for application with Detail ID {detail_id}.")

    def view_cv(self, name, cv_path):
        if not os.path.exists(cv_path):
            self.results_summary_label.setText(f"CV file not found: {cv_path}")
            return

        # Open the CV file using the default application
        try:
            absolute_path = os.path.abspath(cv_path)
            os.startfile(absolute_path)  # For Windows
        except Exception as e:
            self.results_summary_label.setText(f"Error opening CV: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CVAnalyzerApp()
    window.show()
    sys.exit(app.exec())