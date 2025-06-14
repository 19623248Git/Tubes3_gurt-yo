import sys
import os
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
from SummaryWindow import SummaryWindow 
from Database import create_connection, get_all_cv_data, get_all_cv_data, get_summary_details_by_id

class CVAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gurt:Yo CV Analyzer")
        self.setGeometry(100, 100, 800, 600)

        self.db_connection = None

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        ### Load Database Button ###
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()  # Add spacer to push the button to the right
        self.load_database_button = QPushButton("Load Database")
        self.load_database_button.setStyleSheet("padding: 1px;")
        top_bar_layout.addWidget(self.load_database_button)

        main_layout.addLayout(top_bar_layout)  # Add the top bar layout to the main layout

        ### Top Search Panel ###
        search_panel = QFrame()
        search_panel.setFrameShape(QFrame.StyledPanel)
        search_layout = QFormLayout(search_panel)
        search_layout.setSpacing(10)

        # Keywords input
        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("e.g., React, Express, HTML")
        search_layout.addRow(QLabel("Keywords:"), self.keywords_input)

        # Search Algorithm selection
        algorithm_layout = QHBoxLayout()
        self.kmp_radio = QRadioButton("KMP")
        self.bm_radio = QRadioButton("BM")
        self.kmp_radio.setChecked(True)  # Default selection
        algorithm_layout.addWidget(self.kmp_radio)
        algorithm_layout.addWidget(self.bm_radio)
        search_layout.addRow(QLabel("Search Algorithm:"), algorithm_layout)

        # Top Matches selector
        self.top_matches_spinbox = QSpinBox()
        self.top_matches_spinbox.setMinimum(1)
        self.top_matches_spinbox.setValue(5)
        search_layout.addRow(QLabel("Top Matches:"), self.top_matches_spinbox)

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.setEnabled(False) 
        self.search_button.setStyleSheet("padding: 10px;")
        search_layout.addRow(self.search_button)

        main_layout.addWidget(search_panel)

        ### Results Section ###
        results_frame = QFrame()
        main_layout.addWidget(results_frame)
        results_layout = QVBoxLayout(results_frame)

        # Summary of search performance
        self.results_summary_label = QLabel("Search results will appear here.")
        self.results_summary_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(self.results_summary_label)

        # Area for CV cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        results_layout.addWidget(scroll_area)

        self.results_container = QWidget()
        self.results_grid_layout = QVBoxLayout(self.results_container) # Using QVBoxLayout for vertical stacking
        scroll_area.setWidget(self.results_container)

        # Placeholder for summary window
        self.summary_window = None

        # Load database
        self.load_database_button.clicked.connect(self.load_database)
        self.search_button.clicked.connect(self.perform_search)

    def load_database(self):
        if self.db_connection is None:
            self.db_connection = create_connection()

        if self.db_connection and self.db_connection.is_connected():
            self.load_database_button.setEnabled(False) # Disable button after successful connection
            self.load_database_button.setText("Database Connected")
            self.search_button.setEnabled(True) # Enable search
            self.results_summary_label.setText("Database connected. Ready to search.")
        else:
            self.results_summary_label.setText("Database connection failed. Check credentials/server.")

    def perform_search(self):
        keywords = self.keywords_input.text()
        algorithm = "KMP" if self.kmp_radio.isChecked() else "BM"
        top_n = self.top_matches_spinbox.value()

        if not self.db_connection:
            self.results_summary_label.setText("Please load the database first.")
            return
        
        all_cvs = get_all_cv_data(self.db_connection)
        print(f"Found {len(all_cvs)} CVs to search through.")

        print(f"Searching for '{keywords}' using {algorithm}, showing top {top_n} matches.")
        # Insert Backend Logic Here?
        # results = something that returns an array of dictionary. An example can be seen below:
        dummy_results = [
            {
                "detail_id": 1,
                "applicant_id": 1, 
                "name": "Group1 Applicant1", 
                "application_role": "Business Development",
                "cv_path": "../data/BUSINESS-DEVELOPMENT/81310245.pdf",
                "matched_keywords": {'sales': 4, 'marketing': 2}
            },
            {
                "detail_id": 9,
                "applicant_id": 7, 
                "name": "Group1 Applicant7",
                "application_role": "Business Development",
                "cv_path": "../data/BUSINESS-DEVELOPMENT/77576845.pdf",
                "matched_keywords": {'strategy': 3, 'sales': 2}
            }
        ]

        # Results label
        # self.results_summary_label.setText("Exact Match: {amtOfScannedExactCVs} CVs ({runtime}ms).\nFuzzy Match: {amtOfScannedFuzzyCVs} CVs ({runtime}ms)")
        # E.g.
        self.results_summary_label.setText("Exact Match: 3 CVs (150ms).\nFuzzy Match: 2 CVs (200ms)")

        # Clear previous results
        for i in reversed(range(self.results_grid_layout.count())):
            widget = self.results_grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for result in dummy_results:
            card = self.create_cv_card(
                result["detail_id"], # Pass the detail_id
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
        if not self.db_connection:
            self.results_summary_label.setText("Please load the database first.")
            return
            
        details = get_summary_details_by_id(self.db_connection, detail_id)

        if details:
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