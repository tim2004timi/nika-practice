"""
Цветовая палитра и стили для приложения Николь Бьюти
"""

def hsl_to_rgb(h, s, l):
    """Конвертирует HSL в RGB (0-255)"""
    import colorsys
    rgb = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return tuple(int(c * 255) for c in rgb)

def hsl_to_hex(h, s, l):
    """Конвертирует HSL в hex строку"""
    rgb = hsl_to_rgb(h, s, l)
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

# Основные цвета
BACKGROUND = hsl_to_hex(28, 25, 8)  # hsl(28, 25%, 8%)
FOREGROUND = hsl_to_hex(35, 25, 88)  # hsl(35, 25%, 88%)

# Карточки и поверхности
CARD = hsl_to_hex(28, 22, 12)  # hsl(28, 22%, 12%)
CARD_FOREGROUND = hsl_to_hex(35, 25, 88)
POPOVER = hsl_to_hex(28, 25, 10)  # hsl(28, 25%, 10%)

# Primary
PRIMARY = hsl_to_hex(35, 45, 70)  # hsl(35, 45%, 70%)
PRIMARY_FOREGROUND = hsl_to_hex(28, 30, 10)  # hsl(28, 30%, 10%)

# Secondary
SECONDARY = hsl_to_hex(30, 20, 20)  # hsl(30, 20%, 20%)
SECONDARY_FOREGROUND = hsl_to_hex(35, 25, 88)

# Muted
MUTED = hsl_to_hex(28, 15, 18)  # hsl(28, 15%, 18%)
MUTED_FOREGROUND = hsl_to_hex(35, 15, 60)  # hsl(35, 15%, 60%)

# Accent
ACCENT = hsl_to_hex(32, 40, 50)  # hsl(32, 40%, 50%)
ACCENT_FOREGROUND = hsl_to_hex(35, 25, 95)  # hsl(35, 25%, 95%)

# Destructive
DESTRUCTIVE = hsl_to_hex(0, 65, 50)  # hsl(0, 65%, 50%)
DESTRUCTIVE_FOREGROUND = hsl_to_hex(35, 25, 95)

# Границы и ввод
BORDER = hsl_to_hex(28, 20, 22)  # hsl(28, 20%, 22%)
INPUT = hsl_to_hex(28, 20, 18)  # hsl(28, 20%, 18%)
RING = PRIMARY  # hsl(35, 45%, 70%)

# Кастомные цвета
BEIGE_LIGHT = hsl_to_hex(35, 50, 75)
BEIGE = PRIMARY
BEIGE_DARK = hsl_to_hex(35, 40, 60)
BROWN_DARK = hsl_to_hex(28, 30, 15)
BROWN_MEDIUM = hsl_to_hex(30, 25, 25)
COFFEE = hsl_to_hex(25, 20, 20)
CARAMEL = ACCENT

# Радиус скругления
RADIUS = 12  # 0.75rem = 12px

def get_stylesheet():
    """Возвращает глобальную таблицу стилей"""
    return f"""
    QMainWindow {{
        background-color: {BACKGROUND};
        color: {FOREGROUND};
    }}
    
    QWidget {{
        background-color: {BACKGROUND};
        color: {FOREGROUND};
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        font-size: 13px;
    }}
    
    QPushButton {{
        background-color: {PRIMARY};
        color: {PRIMARY_FOREGROUND};
        border: none;
        border-radius: 8px;
        padding: 6px 12px;
        font-weight: 500;
        font-size: 13px;
        min-height: 28px;
    }}
    
    QPushButton:hover {{
        background-color: {BEIGE_LIGHT};
    }}
    
    QPushButton:pressed {{
        background-color: {BEIGE_DARK};
    }}
    
    QPushButton:disabled {{
        background-color: {MUTED};
        color: {MUTED_FOREGROUND};
        opacity: 0.5;
    }}
    
    QPushButton[buttonStyle="default"] {{
        background-color: {PRIMARY};
        color: {PRIMARY_FOREGROUND};
        border: none;
        border-radius: 8px;
        padding: 6px 12px;
        font-weight: 500;
        font-size: 13px;
        min-height: 28px;
    }}
    
    QPushButton[buttonStyle="default"]:hover {{
        background-color: {BEIGE_LIGHT};
    }}
    
    QPushButton[buttonStyle="default"]:pressed {{
        background-color: {BEIGE_DARK};
    }}
    
    QPushButton[buttonStyle="outline"] {{
        background-color: transparent;
        color: {FOREGROUND};
        border: 1px solid {BORDER};
    }}
    
    QPushButton[buttonStyle="outline"]:hover {{
        background-color: {ACCENT};
        color: {ACCENT_FOREGROUND};
        border-color: {ACCENT};
    }}
    
    QPushButton[buttonStyle="ghost"] {{
        background-color: transparent;
        color: {FOREGROUND};
        border: none;
    }}
    
    QPushButton[buttonStyle="ghost"]:hover {{
        background-color: {ACCENT};
        color: {ACCENT_FOREGROUND};
    }}
    
    QPushButton[buttonStyle="destructive"] {{
        background-color: {DESTRUCTIVE};
        color: {DESTRUCTIVE_FOREGROUND};
    }}
    
    QPushButton[buttonStyle="destructive"]:hover {{
        background-color: {hsl_to_hex(0, 65, 45)};
    }}
    
    QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        background-color: {CARD};
        color: {FOREGROUND};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 13px;
        min-height: 28px;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 2px solid {RING};
    }}
    
    QSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        width: 16px;
        border: none;
        background-color: {MUTED};
        border-radius: 4px;
    }}
    
    QSpinBox::up-button:hover, QSpinBox::down-button:hover, QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
        background-color: {PRIMARY};
    }}
    
    QSpinBox::up-arrow, QSpinBox::down-arrow, QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {{
        width: 0;
        height: 0;
        border: none;
    }}
    
    QSpinBox::up-arrow {{
        border-left: 3px solid transparent;
        border-right: 3px solid transparent;
        border-bottom: 4px solid {FOREGROUND};
        margin: 2px;
    }}
    
    QSpinBox::down-arrow {{
        border-left: 3px solid transparent;
        border-right: 3px solid transparent;
        border-top: 4px solid {FOREGROUND};
        margin: 2px;
    }}
    
    QDoubleSpinBox::up-arrow {{
        border-left: 3px solid transparent;
        border-right: 3px solid transparent;
        border-bottom: 4px solid {FOREGROUND};
        margin: 2px;
    }}
    
    QDoubleSpinBox::down-arrow {{
        border-left: 3px solid transparent;
        border-right: 3px solid transparent;
        border-top: 4px solid {FOREGROUND};
        margin: 2px;
    }}
    
    QLineEdit::placeholder {{
        color: {MUTED_FOREGROUND};
    }}
    
    QLabel {{
        color: {FOREGROUND};
    }}
    
    QLabel[labelStyle="h1"] {{
        font-size: 36px;
        font-weight: 700;
    }}
    
    QLabel[labelStyle="h2"] {{
        font-size: 24px;
        font-weight: 700;
    }}
    
    QLabel[labelStyle="h3"] {{
        font-size: 20px;
        font-weight: 600;
    }}
    
    QLabel[labelStyle="muted"] {{
        color: {MUTED_FOREGROUND};
    }}
    
    QLabel[labelStyle="primary"] {{
        color: {PRIMARY};
    }}
    
    QScrollArea {{
        border: none;
        background-color: {BACKGROUND};
    }}
    
    QScrollBar:vertical {{
        background-color: {CARD};
        width: 12px;
        border: none;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {BORDER};
        border-radius: 6px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {PRIMARY};
    }}
    
    QListWidget {{
        background-color: {BACKGROUND};
        border: none;
        color: {FOREGROUND};
    }}
    
    QListWidget::item {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 6px;
        margin: 2px;
    }}
    
    QListWidget::item:hover {{
        border-color: {PRIMARY};
    }}
    
    QListWidget::item:selected {{
        border-color: {PRIMARY};
        background-color: {BROWN_DARK};
    }}
    
    QTableWidget {{
        background-color: {BACKGROUND};
        border: none;
        gridline-color: {BORDER};
        color: {FOREGROUND};
    }}
    
    QTableWidget::item {{
        background-color: {CARD};
        border: none;
        padding: 4px;
        font-size: 12px;
    }}
    
    QTableWidget::item:selected {{
        background-color: {BROWN_DARK};
    }}
    
    QHeaderView::section {{
        background-color: {CARD};
        color: {FOREGROUND};
        border: none;
        padding: 4px;
        font-weight: 600;
        font-size: 12px;
    }}
    
    QMenuBar {{
        background-color: {CARD};
        color: {FOREGROUND};
        border-bottom: 1px solid {BORDER};
    }}
    
    QMenuBar::item {{
        padding: 8px 16px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {ACCENT};
        color: {ACCENT_FOREGROUND};
    }}
    
    QMenu {{
        background-color: {CARD};
        color: {FOREGROUND};
        border: 1px solid {BORDER};
        border-radius: {RADIUS}px;
    }}
    
    QMenu::item {{
        padding: 8px 24px;
    }}
    
    QMenu::item:selected {{
        background-color: {ACCENT};
        color: {ACCENT_FOREGROUND};
    }}
    """

