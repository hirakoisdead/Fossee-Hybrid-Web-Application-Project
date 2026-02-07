"""
Chemical Equipment Parameter Visualizer - Desktop Application
Main entry point for the PyQt5 desktop frontend.
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFileDialog, QMessageBox,
    QListWidget, QListWidgetItem, QSplitter, QGroupBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from api_client import api_client
from widgets import (
    LoginWidget, RegisterWidget, DataTableWidget, ChartWidget,
    StatsWidget, get_stylesheet, COLORS
)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.datasets = []
        self.selected_dataset = None
        self.summary = None
        
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(get_stylesheet())
        
        self.init_ui()
    
    def init_ui(self):
        # Central widget with stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.stack = QStackedWidget()
        
        # Auth pages
        self.login_widget = LoginWidget(api_client)
        self.login_widget.login_success.connect(self.handle_login_success)
        self.login_widget.switch_to_register.connect(lambda: self.stack.setCurrentIndex(1))
        
        self.register_widget = RegisterWidget(api_client)
        self.register_widget.register_success.connect(self.handle_login_success)
        self.register_widget.switch_to_login.connect(lambda: self.stack.setCurrentIndex(0))
        
        # Dashboard page
        self.dashboard_widget = self.create_dashboard()
        
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.register_widget)
        self.stack.addWidget(self.dashboard_widget)
        
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)
    
    def create_dashboard(self) -> QWidget:
        """Create the main dashboard widget."""
        dashboard = QWidget()
        main_layout = QVBoxLayout(dashboard)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(24)
        
        # Sidebar
        sidebar = self.create_sidebar()
        content_layout.addWidget(sidebar, 1)
        
        # Main content
        main_area = self.create_main_area()
        content_layout.addWidget(main_area, 3)
        
        main_layout.addWidget(content, 1)
        
        return dashboard
    
    def create_header(self) -> QFrame:
        """Create the application header."""
        header = QFrame()
        # Use gradient from purple (#667eea) to violet (#764ba2) like web app
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                padding: 16px;
            }
            QLabel {
                color: white;
            }
        """)
        
        layout = QHBoxLayout(header)
        
        # Logo and title
        title = QLabel("Chemical Equipment Visualizer")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title)
        
        layout.addStretch()
        
        # User info
        self.user_label = QLabel()
        self.user_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        layout.addWidget(self.user_label)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.3);
            }}
        """)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return header
    
    def create_sidebar(self) -> QWidget:
        """Create the sidebar with upload and history."""
        sidebar = QWidget()
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Upload section
        upload_group = QGroupBox("Upload CSV File")
        upload_layout = QVBoxLayout(upload_group)
        
        upload_btn = QPushButton("Select CSV File")
        upload_btn.clicked.connect(self.handle_upload)
        upload_layout.addWidget(upload_btn)
        
        upload_hint = QLabel("Columns: Equipment Name, Type, Flowrate, Pressure, Temperature")
        upload_hint.setWordWrap(True)
        upload_hint.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px;")
        upload_layout.addWidget(upload_hint)
        
        layout.addWidget(upload_group)
        
        # History section
        history_group = QGroupBox("Upload History")
        history_layout = QVBoxLayout(history_group)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.handle_dataset_select)
        history_layout.addWidget(self.history_list)
        
        hint = QLabel("Last 5 datasets are stored")
        hint.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px;")
        hint.setAlignment(Qt.AlignCenter)
        history_layout.addWidget(hint)
        
        layout.addWidget(history_group)
        layout.addStretch()
        
        return sidebar
    
    def create_main_area(self) -> QWidget:
        """Create the main content area."""
        main = QWidget()
        layout = QVBoxLayout(main)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Title row with action buttons
        title_row = QWidget()
        title_layout = QHBoxLayout(title_row)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        self.dataset_title = QLabel("No Dataset Selected")
        self.dataset_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_layout.addWidget(self.dataset_title)
        
        title_layout.addStretch()
        
        # Action buttons in main area
        self.pdf_btn = QPushButton("Download PDF Report")
        self.pdf_btn.setEnabled(False)
        self.pdf_btn.clicked.connect(self.handle_download_pdf)
        title_layout.addWidget(self.pdf_btn)
        
        self.delete_btn = QPushButton("Delete Dataset")
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['error']};
            }}
            QPushButton:hover {{
                background: #dc2626;
            }}
        """)
        self.delete_btn.clicked.connect(self.handle_delete)
        title_layout.addWidget(self.delete_btn)
        
        layout.addWidget(title_row)
        
        # Stats
        self.stats_widget = StatsWidget()
        layout.addWidget(self.stats_widget)
        
        # Charts
        self.chart_widget = ChartWidget()
        layout.addWidget(self.chart_widget, 2)
        
        # Data table
        table_group = QGroupBox("Equipment Data")
        table_layout = QVBoxLayout(table_group)
        self.data_table = DataTableWidget()
        table_layout.addWidget(self.data_table)
        layout.addWidget(table_group, 1)
        
        return main
    
    def handle_login_success(self, data: dict):
        """Handle successful login/registration."""
        self.current_user = data.get('user', {})
        self.user_label.setText(f"Welcome, {self.current_user.get('username', 'User')}")
        self.stack.setCurrentIndex(2)
        self.load_datasets()
    
    def handle_logout(self):
        """Handle logout."""
        api_client.logout()
        self.current_user = None
        self.datasets = []
        self.selected_dataset = None
        self.history_list.clear()
        self.stack.setCurrentIndex(0)
    
    def load_datasets(self):
        """Load user's datasets."""
        try:
            self.datasets = api_client.list_datasets()
            self.history_list.clear()
            
            for ds in self.datasets:
                item = QListWidgetItem(f"{ds['filename']}\n{ds['total_count']} items")
                item.setData(Qt.UserRole, ds['id'])
                self.history_list.addItem(item)
            
            if self.datasets:
                self.history_list.setCurrentRow(0)
                self.load_dataset_details(self.datasets[0]['id'])
            else:
                self.clear_display()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load datasets: {e}")
    
    def load_dataset_details(self, dataset_id: int):
        """Load details for a specific dataset."""
        try:
            self.selected_dataset = api_client.get_dataset(dataset_id)
            self.summary = api_client.get_summary(dataset_id)
            
            self.dataset_title.setText(self.selected_dataset['filename'])
            self.stats_widget.update_stats(self.summary)
            self.chart_widget.update_charts(self.summary, self.selected_dataset['equipment_items'])
            self.data_table.load_data(self.selected_dataset['equipment_items'])
            
            self.pdf_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load dataset: {e}")
    
    def clear_display(self):
        """Clear the display when no dataset is selected."""
        self.dataset_title.setText("No Dataset Selected")
        self.data_table.setRowCount(0)
        self.chart_widget.clear()
        self.pdf_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
    
    def handle_dataset_select(self, item: QListWidgetItem):
        """Handle dataset selection from history."""
        dataset_id = item.data(Qt.UserRole)
        self.load_dataset_details(dataset_id)
    
    def handle_upload(self):
        """Handle CSV file upload."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                dataset = api_client.upload_csv(file_path)
                QMessageBox.information(self, "Success", "File uploaded successfully!")
                self.load_datasets()
            except Exception as e:
                QMessageBox.warning(self, "Upload Failed", str(e))
    
    def handle_download_pdf(self):
        """Handle PDF report download."""
        if not self.selected_dataset:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", 
            f"equipment_report_{self.selected_dataset['id']}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if save_path:
            try:
                api_client.download_report(self.selected_dataset['id'], save_path)
                QMessageBox.information(self, "Success", "PDF report saved!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to download report: {e}")
    
    def handle_delete(self):
        """Handle dataset deletion."""
        if not self.selected_dataset:
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this dataset?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                api_client.delete_dataset(self.selected_dataset['id'])
                self.load_datasets()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete: {e}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
