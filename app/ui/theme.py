STYLE = """
* { font-family: "Microsoft YaHei"; }
QMainWindow, QWidget { background: #071426; color: #E8F1FF; }
QFrame#TopBar { background: #0A1B31; border-bottom: 1px solid #18395B; }
QFrame#Sidebar { background: #08172A; border-right: 1px solid #18395B; }
QFrame#Content { background: #071426; }
QLabel { color: #D8E7F7; }
QLabel#Brand { color: #FFFFFF; font-size: 24px; font-weight: 700; }
QLabel#Subtitle { color: #79A9D6; font-size: 12px; }
QLabel#PageTitle { color: #52D6FF; font-size: 22px; font-weight: 700; }
QLabel#PageDesc { color: #7F9AB5; font-size: 12px; }
QLabel#StepBadge { background: #55D7FF; color: #062033; border-radius: 13px; font-size: 13px; font-weight: 700; padding: 3px 7px; }
QLabel#MetricValue { color: #62F2D0; font-size: 24px; font-weight: 700; }
QLabel#MetricName { color: #7894AE; font-size: 11px; }
QLabel#StatusGood { background: #123D34; color: #55E6A5; border: 1px solid #1B735B; border-radius: 10px; padding: 4px 10px; }
QLabel#StatusWarn { background: #49351C; color: #FFC65A; border: 1px solid #9A6A21; border-radius: 10px; padding: 4px 10px; }
QLabel#StatusBad { background: #4A2228; color: #FF7885; border: 1px solid #A73C4B; border-radius: 10px; padding: 4px 10px; }
QPushButton#NavButton { background: transparent; color: #91A9C1; border: none; border-radius: 6px; text-align: left; padding: 10px 14px; font-size: 13px; }
QPushButton#NavButton:hover { background: #102B48; color: #FFFFFF; }
QPushButton#NavButton:checked { background: #123B61; color: #55D7FF; border-left: 3px solid #55D7FF; }
QPushButton#Primary { background: #1685F5; color: white; border: none; border-radius: 6px; padding: 9px 18px; font-weight: 600; }
QPushButton#Primary:hover { background: #2A9BFF; }
QPushButton#Secondary { background: #102B48; color: #B9D6EE; border: 1px solid #24557D; border-radius: 6px; padding: 9px 18px; }
QPushButton#Secondary:hover { background: #163C60; }
QPushButton#Danger { background: #5A252C; color: #FFB2BA; border: 1px solid #A33B49; border-radius: 6px; padding: 9px 18px; }
QLineEdit, QComboBox { background: #0B2038; color: #EAF5FF; border: 1px solid #244A6A; border-radius: 5px; padding: 8px; }
QLineEdit:focus, QComboBox:focus { border: 1px solid #55D7FF; }
QGroupBox { background: #0A1B31; border: 1px solid #193A5B; border-radius: 8px; margin-top: 12px; padding: 14px; font-weight: 600; color: #A8C6DF; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; color: #55D7FF; }
QTableWidget { background: #08182B; alternate-background-color: #0B2038; color: #DCEBFA; border: 1px solid #193A5B; gridline-color: #193A5B; }
QHeaderView::section { background: #102B48; color: #9FC2DE; border: none; padding: 8px; font-weight: 600; }
QProgressBar { background: #0B2038; border: 1px solid #214661; border-radius: 6px; text-align: center; color: #DDEFFF; }
QProgressBar::chunk { background: #27C9E8; border-radius: 5px; }
QScrollArea { border: none; }
"""
