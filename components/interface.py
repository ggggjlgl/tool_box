from PySide6.QtWidgets import QWidget


class WidgetWithComboCheckBox(QWidget):

    def get_cbb_items(self) -> list:
        raise NotImplementedError
