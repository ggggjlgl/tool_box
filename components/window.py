from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QScrollArea, QStyle
from PySide6.QtCore import QRect

from components.common import Tool, ToolButton, GridLayout
from tools.tool_batch_rename import WidgetBatchRename


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # setup_ui
        self.setWindowTitle('常用工具箱')
        self.resize(1200, 800)
        self.central_widget = QWidget(self)
        self.vertical_layout_2 = QVBoxLayout(self.central_widget)
        self.vertical_layout = QVBoxLayout()
        self.horizontal_layout = QHBoxLayout()
        self.tab = QTabWidget(self.central_widget)

        self.tool_list = QWidget()

        self.vertical_layout_4 = QVBoxLayout(self.tool_list)

        self.vertical_layout_3 = QVBoxLayout()

        self.horizontal_layout_2 = QHBoxLayout()

        self.scroll_main = QScrollArea(self.tool_list)

        self.scroll_main.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()

        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 1148, 685))
        self.grid_layout = GridLayout(4, self.scroll_area_widget_contents)
        self.scroll_main.setWidget(self.scroll_area_widget_contents)

        self.horizontal_layout_2.addWidget(self.scroll_main)

        self.vertical_layout_3.addLayout(self.horizontal_layout_2)

        self.vertical_layout_4.addLayout(self.vertical_layout_3)

        self.tab.addTab(self.tool_list, '工具列表')

        self.horizontal_layout.addWidget(self.tab)

        self.vertical_layout.addLayout(self.horizontal_layout)

        self.vertical_layout_2.addLayout(self.vertical_layout)

        self.setCentralWidget(self.central_widget)

        self.tab.setCurrentIndex(0)

        # 注册工具
        self.register_tools()

        self.bind()

    def register_tools(self):
        tool_batch_rename = Tool('批量重命名', self.style().standardIcon(QStyle.StandardPixmap.SP_FileLinkIcon),
                                 '将符合条件的文件或目录名中指定部分替换为指定字符串', WidgetBatchRename)

        tools = [tool_batch_rename, ] * 20

        for i in tools:
            tool_btn = ToolButton(*i.get_properties())
            tool_btn.clicked.connect(lambda: self.handle_click(i.widget, i.name))
            self.grid_layout.add_widget(tool_btn)

    def handle_click(self, widget, name: str):
        self.tab.addTab(widget, name)
        self.tab.setCurrentIndex(self.tab.count() - 1)

    def bind(self):
        ...

    def closeEvent(self, event):
        event.accept()