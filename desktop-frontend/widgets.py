"""
PyQt5 UI Widgets for the desktop application.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QFileDialog,
    QListWidget, QListWidgetItem, QMessageBox, QFrame, QSplitter,
    QGroupBox, QFormLayout, QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# Color scheme matching web frontend (purple/violet gradient theme)
COLORS = {
    'primary': '#667eea',          # Main purple
    'primary_dark': '#5a67d8',     # Darker purple
    'secondary': '#764ba2',        # Secondary violet
    'success': '#38ef7d',          # Vibrant green
    'warning': '#f2994a',          # Orange
    'error': '#eb3349',            # Red
    'bg': '#ffffff',
    'bg_alt': '#f5f7fa',           # Light gradient background
    'bg_gradient': '#e4e8f0',
    'border': '#e2e8f0',
    'text': '#1e293b',
    'text_light': '#64748b',
    # Gradient colors for stat cards  
    'gradient_ocean': '#2193b0',
    'gradient_ocean_end': '#6dd5ed',
    'gradient_success': '#11998e',
    'gradient_danger': '#eb3349'
}

CHART_COLORS = ['#667eea', '#764ba2', '#38ef7d', '#f2994a', '#eb3349', 
                '#2193b0', '#11998e', '#f093fb', '#5ee7df', '#43e97b']


def get_stylesheet():
    """Return the main application stylesheet."""
    return f"""
        QWidget {{
            background-color: {COLORS['bg']};
            font-family: 'Segoe UI', 'Inter', sans-serif;
            color: {COLORS['text']};
        }}
        
        QLabel {{
            color: {COLORS['text']};
        }}
        
        QPushButton {{
            background-color: {COLORS['primary']};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 500;
            font-size: 13px;
        }}
        
        QPushButton:hover {{
            background-color: {COLORS['primary_dark']};
        }}
        
        QPushButton:disabled {{
            background-color: #94a3b8;
        }}
        
        QPushButton.secondary {{
            background-color: {COLORS['bg_alt']};
            color: {COLORS['text']};
            border: 1px solid {COLORS['border']};
        }}
        
        QPushButton.secondary:hover {{
            background-color: {COLORS['border']};
        }}
        
        QPushButton.danger {{
            background-color: {COLORS['error']};
        }}
        
        QPushButton.danger:hover {{
            background-color: #dc2626;
        }}
        
        QLineEdit {{
            padding: 10px 14px;
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            font-size: 14px;
            background-color: white;
        }}
        
        QLineEdit:focus {{
            border-color: {COLORS['primary']};
        }}
        
        QTableWidget {{
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            gridline-color: {COLORS['border']};
        }}
        
        QTableWidget::item {{
            padding: 8px;
        }}
        
        QHeaderView::section {{
            background-color: {COLORS['bg_alt']};
            padding: 10px;
            border: none;
            border-bottom: 1px solid {COLORS['border']};
            font-weight: 600;
        }}
        
        QListWidget {{
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
        }}
        
        QListWidget::item {{
            padding: 12px;
            border-bottom: 1px solid {COLORS['border']};
        }}
        
        QListWidget::item:selected {{
            background-color: rgba(102, 126, 234, 0.1);
            border-left: 3px solid {COLORS['primary']};
        }}
        
        QGroupBox {{
            font-weight: 600;
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
        }}
    """


class LoginWidget(QWidget):
    """Login form widget."""
    
    login_success = pyqtSignal(dict)
    switch_to_register = pyqtSignal()
    
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(24)
        
        # Title - larger font
        title = QLabel("Chemical Equipment Visualizer")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Sign in to your account")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet(f"color: {COLORS['text_light']};")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Form container - wider
        form_widget = QWidget()
        form_widget.setFixedWidth(450)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(12)
        
        # Username - larger label and input
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 13))
        form_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(QFont("Segoe UI", 13))
        self.username_input.setMinimumHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        form_layout.addSpacing(8)
        
        # Password - larger label and input
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 13))
        form_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 13))
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """)
        form_layout.addWidget(self.password_input)
        
        form_layout.addSpacing(16)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setFont(QFont("Segoe UI", 12))
        self.error_label.setStyleSheet(f"color: {COLORS['error']};")
        self.error_label.hide()
        form_layout.addWidget(self.error_label)
        
        # Login button - larger
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.login_btn.setMinimumHeight(48)
        self.login_btn.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_btn)
        
        form_layout.addSpacing(12)
        
        # Register link - larger
        register_label = QLabel("<a href='#'>Don't have an account? Create one</a>")
        register_label.setFont(QFont("Segoe UI", 12))
        register_label.setAlignment(Qt.AlignCenter)
        register_label.linkActivated.connect(lambda: self.switch_to_register.emit())
        form_layout.addWidget(register_label)
        
        layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Please enter username and password")
            return
        
        try:
            data = self.api.login(username, password)
            self.login_success.emit(data)
        except Exception as e:
            # Try to get more specific error from the response
            error_msg = "Invalid credentials. Please try again."
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', error_msg)
                except:
                    pass
            self.show_error(error_msg)
    
    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()


class RegisterWidget(QWidget):
    """Registration form widget."""
    
    register_success = pyqtSignal(dict)
    switch_to_login = pyqtSignal()
    
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(24)
        
        title = QLabel("Create Account")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Get started with equipment analysis")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet(f"color: {COLORS['text_light']};")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        form_widget = QWidget()
        form_widget.setFixedWidth(450)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(10)
        
        # Input field stylesheet
        input_style = """
            QLineEdit {
                padding: 12px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """
        
        # Username
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 13))
        form_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setFont(QFont("Segoe UI", 13))
        self.username_input.setMinimumHeight(45)
        self.username_input.setStyleSheet(input_style)
        form_layout.addWidget(self.username_input)
        
        # Email
        email_label = QLabel("Email")
        email_label.setFont(QFont("Segoe UI", 13))
        form_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setFont(QFont("Segoe UI", 13))
        self.email_input.setMinimumHeight(45)
        self.email_input.setStyleSheet(input_style)
        form_layout.addWidget(self.email_input)
        
        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 13))
        form_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 13))
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(self.password_input)
        
        # Confirm Password
        confirm_label = QLabel("Confirm Password")
        confirm_label.setFont(QFont("Segoe UI", 13))
        form_layout.addWidget(confirm_label)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setFont(QFont("Segoe UI", 13))
        self.confirm_input.setMinimumHeight(45)
        self.confirm_input.setStyleSheet(input_style)
        form_layout.addWidget(self.confirm_input)
        
        form_layout.addSpacing(12)
        
        self.error_label = QLabel()
        self.error_label.setFont(QFont("Segoe UI", 12))
        self.error_label.setStyleSheet(f"color: {COLORS['error']};")
        self.error_label.hide()
        form_layout.addWidget(self.error_label)
        
        self.register_btn = QPushButton("Create Account")
        self.register_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.register_btn.setMinimumHeight(48)
        self.register_btn.clicked.connect(self.handle_register)
        form_layout.addWidget(self.register_btn)
        
        form_layout.addSpacing(12)
        
        login_label = QLabel("<a href='#'>Already have an account? Sign in</a>")
        login_label.setFont(QFont("Segoe UI", 12))
        login_label.setAlignment(Qt.AlignCenter)
        login_label.linkActivated.connect(lambda: self.switch_to_login.emit())
        form_layout.addWidget(login_label)
        
        layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        self.setLayout(layout)
    
    def handle_register(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not all([username, email, password, confirm]):
            self.show_error("Please fill in all fields")
            return
        
        if password != confirm:
            self.show_error("Passwords do not match")
            return
        
        if len(password) < 6:
            self.show_error("Password must be at least 6 characters")
            return
        
        try:
            data = self.api.register(username, email, password)
            self.register_success.emit(data)
        except Exception as e:
            self.show_error("Registration failed. Username may already exist.")
    
    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()


class DataTableWidget(QTableWidget):
    """Table widget for displaying equipment data."""
    
    def __init__(self):
        super().__init__()
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
    
    def load_data(self, equipment: list):
        self.setRowCount(len(equipment))
        for row, item in enumerate(equipment):
            self.setItem(row, 0, QTableWidgetItem(item['name']))
            self.setItem(row, 1, QTableWidgetItem(item['equipment_type']))
            self.setItem(row, 2, QTableWidgetItem(f"{item['flowrate']:.2f}"))
            self.setItem(row, 3, QTableWidgetItem(f"{item['pressure']:.2f}"))
            self.setItem(row, 4, QTableWidgetItem(f"{item['temperature']:.2f}"))


class ChartWidget(QWidget):
    """Widget for displaying Matplotlib charts."""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Modern chart styling
        plt.style.use('seaborn-v0_8-whitegrid')
        
        self.figure = Figure(figsize=(12, 6), facecolor='#f8fafc', dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
    
    def update_charts(self, summary: dict, equipment: list):
        self.figure.clear()
        self.figure.set_facecolor('#f8fafc')
        
        # Create 1x3 subplot grid for better horizontal layout
        ax1 = self.figure.add_subplot(1, 3, 1)
        ax2 = self.figure.add_subplot(1, 3, 2)
        ax3 = self.figure.add_subplot(1, 3, 3)
        
        for ax in [ax1, ax2, ax3]:
            ax.set_facecolor('white')
        
        # Pie chart - Equipment Type Distribution (with legend, not labels)
        type_dist = summary.get('type_distribution', {})
        if type_dist:
            labels = list(type_dist.keys())
            sizes = list(type_dist.values())
            colors = ['#667eea', '#764ba2', '#38ef7d', '#f2994a', '#eb3349', 
                     '#2193b0', '#11998e', '#f093fb', '#5ee7df', '#43e97b'][:len(labels)]
            
            wedges, texts, autotexts = ax1.pie(
                sizes, colors=colors, autopct='%1.0f%%',
                startangle=90, pctdistance=0.75,
                wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2)
            )
            
            for autotext in autotexts:
                autotext.set_fontsize(8)
                autotext.set_fontweight('bold')
                autotext.set_color('white')
            
            # Add legend instead of labels
            ax1.legend(wedges, labels, loc='center left', bbox_to_anchor=(-0.1, 0.5),
                      fontsize=8, frameon=False)
            ax1.set_title('Type Distribution', fontsize=12, fontweight='bold', 
                         color='#1e293b', pad=15)
        
        # Bar chart - Average Values with gradient colors
        metrics = ['Flowrate', 'Pressure', 'Temp']
        values = [summary.get('avg_flowrate', 0), 
                 summary.get('avg_pressure', 0), 
                 summary.get('avg_temperature', 0)]
        bar_colors = ['#2193b0', '#38ef7d', '#eb3349']  # Ocean blue, green, red
        
        bars = ax2.bar(metrics, values, color=bar_colors, width=0.6, 
                      edgecolor='white', linewidth=1)
        ax2.set_title('Average Values', fontsize=12, fontweight='bold', 
                     color='#1e293b', pad=15)
        ax2.set_ylabel('Value', fontsize=10, color='#64748b')
        ax2.tick_params(axis='both', labelsize=9, colors='#64748b')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color('#e2e8f0')
        ax2.spines['bottom'].set_color('#e2e8f0')
        
        for bar, val in zip(bars, values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=9, 
                    fontweight='bold', color='#1e293b')
        
        # Min/Max comparison with grouped bars
        min_vals = summary.get('min_values', {})
        max_vals = summary.get('max_values', {})
        
        x = range(len(metrics))
        width = 0.35
        
        min_data = [min_vals.get('flowrate', 0), min_vals.get('pressure', 0), min_vals.get('temperature', 0)]
        max_data = [max_vals.get('flowrate', 0), max_vals.get('pressure', 0), max_vals.get('temperature', 0)]
        
        bars1 = ax3.bar([i - width/2 for i in x], min_data, width, label='Min', 
                       color='#94a3b8', edgecolor='white', linewidth=1)
        bars2 = ax3.bar([i + width/2 for i in x], max_data, width, label='Max', 
                       color='#667eea', edgecolor='white', linewidth=1)  # Purple theme
        ax3.set_xticks(x)
        ax3.set_xticklabels(metrics)
        ax3.set_title('Min / Max Range', fontsize=12, fontweight='bold', 
                     color='#1e293b', pad=15)
        ax3.legend(frameon=False, fontsize=9)
        ax3.set_ylabel('Value', fontsize=10, color='#64748b')
        ax3.tick_params(axis='both', labelsize=9, colors='#64748b')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.spines['left'].set_color('#e2e8f0')
        ax3.spines['bottom'].set_color('#e2e8f0')
        
        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()
    
    def clear(self):
        self.figure.clear()
        self.canvas.draw()


class StatsWidget(QWidget):
    """Widget for displaying statistics cards."""
    
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setSpacing(16)
        
        self.stat_labels = {}
        # Each stat has a key, title, and accent color matching web app
        stats = [
            ('total', 'Total Equipment', COLORS['primary']),          # Purple
            ('flowrate', 'Avg Flowrate', COLORS['gradient_ocean']),   # Blue
            ('pressure', 'Avg Pressure', COLORS['success']),          # Green
            ('temperature', 'Avg Temperature', COLORS['error'])       # Red
        ]
        
        for key, title, color in stats:
            card = self._create_stat_card(key, title, color)
            layout.addWidget(card)
    
    def _create_stat_card(self, key: str, title: str, accent_color: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                border-top: 4px solid {accent_color};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel("0")
        value_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        value_label.setStyleSheet(f"color: {accent_color}; border: none;")
        value_label.setAlignment(Qt.AlignCenter)
        self.stat_labels[key] = value_label
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 12px; font-weight: 500; border: none;")
        title_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        return card
    
    def update_stats(self, summary: dict):
        self.stat_labels['total'].setText(str(summary.get('total_count', 0)))
        self.stat_labels['flowrate'].setText(f"{summary.get('avg_flowrate', 0):.1f}")
        self.stat_labels['pressure'].setText(f"{summary.get('avg_pressure', 0):.1f}")
        self.stat_labels['temperature'].setText(f"{summary.get('avg_temperature', 0):.1f}")
