from PySide6.QtWidgets import QGridLayout, QWidget
from PySide6.QtWidgets import QToolButton, QSizePolicy
from PySide6.QtCore import QSize, Qt


class Tool:
    def __init__(self, name, icon, desc='', widget=None):
        self.name = name
        self.icon = icon
        self.desc = desc
        self.widget = widget() if widget else QWidget()

    def get_properties(self):
        return self.name, self.icon, self.desc


class GridLayout(QGridLayout):
    def __init__(self, max_col=4, parent=None):
        super().__init__(parent)
        self.max_col = max_col

    def add_widget(self, widget):
        next_w_row, next_w_col = divmod(self.count(), self.max_col)
        self.addWidget(widget, next_w_row, next_w_col, 1, 1)


class ToolButton(QToolButton):
    def __init__(self, name, icon, desc='', parent=None):
        super().__init__(parent)
        self.setText(name)
        self.setIcon(icon)
        self.setToolTip(desc)
        self.setIconSize(QSize(160, 160))
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QSize(200, 200))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

