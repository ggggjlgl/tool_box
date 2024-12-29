from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QComboBox, QCheckBox, QWidget, QLineEdit, QListWidget, QListWidgetItem, QGridLayout, \
    QToolButton, QSizePolicy, QSpacerItem

from components.interface import WidgetWithComboCheckBox

H_SPACER = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)


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


class ComboCheckBox(QComboBox):
    def __init__(self, items: list, parent: WidgetWithComboCheckBox):
        super().__init__(parent)
        self.p = parent
        self.items = items
        self.text = QLineEdit()
        self.text.setReadOnly(True)
        self.setLineEdit(self.text)
        self.cb_s = list()
        self.li = QListWidget()
        self.setModel(self.li.model())
        self.setView(self.li)
        self.rebuild_items()

    def showPopup(self):
        if extensions := self.p.get_cbb_items():
            self.refresh_items(extensions)
        super().showPopup()

    def clear(self):
        self.items.clear()
        self.rebuild_items()

    def refresh_items(self, items: list):
        self.items = items
        self.rebuild_items()

    def rebuild_items(self):
        self.li.clear()
        self.cb_s.clear()
        for text in self.items:
            cb = QCheckBox(text)
            cb.setChecked(True)
            cb.stateChanged.connect(self.refresh_text)
            self.cb_s.append(cb)
            item = QListWidgetItem(self.li)
            self.li.setItemWidget(item, cb)

        self.refresh_text()

    @property
    def selected(self):
        return [cb.text() for cb in self.cb_s if cb.isChecked()]

    def refresh_text(self):
        self.text.setText(', '.join(self.selected))
