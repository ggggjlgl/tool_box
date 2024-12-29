import os.path
import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, \
    QPushButton, QComboBox, QCheckBox, QStyle, QFileDialog, QMessageBox, QApplication
from PySide6.QtCore import QSize, Qt

from components.common import H_SPACER
from util.io import get_files_by_dir, get_dirs_by_dir, get_new_target_path

run_type_handler = {'批量去除指定字符': 'remove_str', '批量去除指定前缀': 'remove_pre_by_str',
                    '批量去除指定后缀': 'remove_suf_by_str',
                    '批量新增指定前缀': 'add_pre_by_str', '批量新增指定后缀': 'add_suf_by_str',
                    '批量替换指定前缀': 'replace_pre_by_str', '批量替换指定后缀': 'replace_suf_by_str', }

run_type_validator = {'批量去除指定字符': lambda p, s: p.__contains__(s),
                      '批量去除指定前缀': lambda p, s: p.startswith(s),
                      '批量去除指定后缀': lambda p, s: p.endswith(s) or os.path.splitext(p)[0].endswith(s),
                      '批量新增指定前缀': lambda _p, _s: True, '批量新增指定后缀': lambda _p, _s: True,
                      '批量替换指定前缀': lambda p, s: p.startswith(s),
                      '批量替换指定后缀': lambda p, s: p.endswith(s) or os.path.splitext(p)[0].endswith(s), }


class WidgetBatchRename(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.origin = None
        self.old = ''
        self.new = ''
        self.success_file = 0
        self.success_dir = 0
        self.errs = list()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 20)
        self.origin_layout = QHBoxLayout()

        self.origin_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.lb_origin = QLabel('执行目录：', self)

        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.lb_origin.sizePolicy().hasHeightForWidth())
        self.lb_origin.setSizePolicy(size_policy)

        self.origin_layout.addWidget(self.lb_origin)

        self.le_origin = QLineEdit(self)

        self.le_origin.setMinimumSize(QSize(0, 25))

        self.origin_layout.addWidget(self.le_origin)

        self.btn_pick = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon), '选择目录', self)

        self.btn_pick.setMinimumSize(QSize(100, 25))

        self.origin_layout.addWidget(self.btn_pick)

        self.origin_layout.addItem(H_SPACER)

        self.origin_layout.setStretch(0, 1)
        self.origin_layout.setStretch(1, 1)
        self.origin_layout.setStretch(2, 4)
        self.origin_layout.setStretch(3, 1)
        self.origin_layout.setStretch(4, 1)

        self.main_layout.addLayout(self.origin_layout)

        self.mode_layout = QHBoxLayout()
        self.mode_layout.setSpacing(0)

        self.mode_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.lb_mode = QLabel('执行模式：', self)
        self.lb_mode.setSizePolicy(size_policy)

        self.mode_layout.addWidget(self.lb_mode)

        self.cbb_mode = QComboBox(self)
        self.cbb_mode.addItems(list(run_type_handler.keys()))

        self.cbb_mode.setMinimumSize(QSize(0, 25))

        self.mode_layout.addWidget(self.cbb_mode)

        self.mode_layout.addItem(H_SPACER)

        self.mode_layout.setStretch(0, 1)
        self.mode_layout.setStretch(1, 1)
        self.mode_layout.setStretch(2, 5)
        self.mode_layout.setStretch(3, 1)

        self.main_layout.addLayout(self.mode_layout)

        self.old_layout = QHBoxLayout()
        self.old_layout.setSpacing(0)
        self.old_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.lb_old = QLabel('原字符串：', self)
        self.lb_old.setSizePolicy(size_policy)

        self.old_layout.addWidget(self.lb_old)

        self.le_old = QLineEdit(self)

        self.le_old.setMinimumSize(QSize(0, 25))

        self.old_layout.addWidget(self.le_old)

        self.old_layout.addItem(H_SPACER)

        self.old_layout.setStretch(0, 1)
        self.old_layout.setStretch(1, 1)
        self.old_layout.setStretch(2, 5)
        self.old_layout.setStretch(3, 1)

        self.main_layout.addLayout(self.old_layout)

        self.new_layout = QHBoxLayout()
        self.new_layout.setSpacing(0)
        self.new_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.lb_new = QLabel('新字符串：', self)
        self.lb_new.setSizePolicy(size_policy)

        self.new_layout.addWidget(self.lb_new)

        self.le_new = QLineEdit(self)

        self.le_new.setMinimumSize(QSize(0, 25))

        self.new_layout.addWidget(self.le_new)

        self.new_layout.addItem(H_SPACER)

        self.new_layout.setStretch(0, 1)
        self.new_layout.setStretch(1, 1)
        self.new_layout.setStretch(2, 5)
        self.new_layout.setStretch(3, 1)

        self.main_layout.addLayout(self.new_layout)

        self.misc_layout = QHBoxLayout()

        self.misc_layout.addItem(H_SPACER)

        self.cb_recursion = QCheckBox('递归应用到子目录', self)
        self.cb_recursion.setSizePolicy(size_policy)
        self.cb_recursion.setChecked(True)

        self.misc_layout.addWidget(self.cb_recursion, 0, Qt.AlignmentFlag.AlignHCenter)

        self.misc_layout.addItem(H_SPACER)

        self.cb_dir_name = QCheckBox('应用到目录名', self)

        self.misc_layout.addWidget(self.cb_dir_name, 0, Qt.AlignmentFlag.AlignHCenter)

        self.misc_layout.addItem(H_SPACER)

        self.misc_layout.setStretch(0, 1)
        self.misc_layout.setStretch(1, 1)
        self.misc_layout.setStretch(2, 1)
        self.misc_layout.setStretch(3, 1)
        self.misc_layout.setStretch(4, 1)

        self.main_layout.addLayout(self.misc_layout)

        self.run_layout = QHBoxLayout()

        self.run_layout.addItem(H_SPACER)

        self.btn_reset = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton), '重置',
                                     self)

        self.btn_reset.setMinimumSize(QSize(200, 45))

        self.run_layout.addWidget(self.btn_reset)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.run_layout.addItem(self.vertical_spacer)

        self.run_layout.addItem(H_SPACER)

        self.vertical_spacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.run_layout.addItem(self.vertical_spacer_2)

        self.btn_run = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay), '执行', self)

        self.btn_run.setMinimumSize(QSize(200, 45))

        self.run_layout.addWidget(self.btn_run)

        self.run_layout.addItem(H_SPACER)

        self.run_layout.setStretch(0, 1)
        self.run_layout.setStretch(1, 1)
        self.run_layout.setStretch(3, 2)
        self.run_layout.setStretch(5, 1)
        self.run_layout.setStretch(6, 1)

        self.main_layout.addLayout(self.run_layout)

        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 1)
        self.main_layout.setStretch(2, 1)
        self.main_layout.setStretch(3, 1)
        self.main_layout.setStretch(4, 1)
        self.main_layout.setStretch(5, 1)
        self.bind()

    def remove_str(self, origin_path):
        return str(os.path.basename(origin_path).replace(self.old, ''))

    def remove_pre_by_str(self, origin_path):
        return str(os.path.basename(origin_path).replace(self.old, '', 1))

    def remove_suf_by_str(self, origin_path):
        if (file_name := os.path.basename(origin_path)).endswith(self.old):
            re_name = file_name[::-1]
            return re_name.replace(self.old[::-1], '', 1)[::-1]
        elif (pure_name := os.path.splitext(file_name)[0]).endswith(self.old):
            re_name = pure_name[::-1]
            return re_name.replace(self.old[::-1], '', 1)[::-1] + os.path.splitext(file_name)[-1]

    def add_pre_by_str(self, origin_path):
        return self.new + os.path.basename(origin_path)

    def add_suf_by_str(self, origin_path):
        file_name = os.path.basename(origin_path)
        pure_name, suffix = os.path.splitext(file_name)
        return pure_name + self.new + suffix

    def replace_pre_by_str(self, origin_path):
        return str(os.path.basename(origin_path).replace(self.old, self.new, 1))

    def replace_suf_by_str(self, origin_path):
        if (file_name := os.path.basename(origin_path)).endswith(self.old):
            re_name = file_name[::-1]
            return re_name.replace(self.old[::-1], self.new[::-1], 1)[::-1]
        elif (pure_name := os.path.splitext(file_name)[0]).endswith(self.old):
            re_name = pure_name[::-1]
            return re_name.replace(self.old[::-1], self.new[::-1], 1)[::-1] + os.path.splitext(file_name)[-1]

    def bind(self):
        self.btn_pick.clicked.connect(self.pick_dir)
        self.cbb_mode.currentTextChanged.connect(self.switch_mode)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_run.clicked.connect(self.run)

    def run(self):
        if self.validate():
            if to_modify := self.collect():
                self.modify(to_modify)
                if self.errs:
                    e = '\n'.join(self.errs)
                    QMessageBox.information(self, '异常', f'😢执行已经结束，{self.success_file}个文件名&{self.success_dir}个目录名已修改，但存在异常：{e}')
                else:
                    QMessageBox.information(self, '成功', f'😊执行成功结束，{self.success_file}个文件名&{self.success_dir}个目录名已修改。')

    def modify(self, to_modify: tuple):
        self.errs.clear()
        files, dirs = to_modify
        self.success_file = len(files)
        self.success_dir = len(dirs)
        self.modify_paths(files, self.success_file, os.path.isfile)
        self.modify_paths(dirs, self.success_dir, os.path.isdir)

    def modify_paths(self, paths, count, exist_func):
        handler = getattr(self, run_type_handler[self.cbb_mode.currentText()])
        for p in paths:
            want_target_path = get_new_target_path(p, os.path.normpath(os.path.join(os.path.dirname(p), handler(p))),
                                                   exist_func=exist_func)
            try:
                os.rename(p, want_target_path)
            except Exception as e:
                count -= 1
                self.errs.append(
                    f'原路径:{p}，目标路径:{want_target_path}，操作方式：{self.cbb_mode.currentText()}，错误信息:{e}，您可以在关闭对应路径的文件资源管理器窗口后再试。')

    def collect(self):
        if self.cb_recursion.isChecked():
            files = get_files_by_dir(self.origin)
            dirs = get_dirs_by_dir(self.origin) if self.cb_dir_name.isChecked() else list()
        else:
            files = [os.path.normpath(os.path.join(self.origin, file)) for file in os.listdir(self.origin) if
                     os.path.isfile(file)]
            dirs = [os.path.normpath(os.path.join(self.origin, dir_)) for dir_ in os.listdir(self.origin) if
                    os.path.isdir(dir_)] if self.cb_dir_name.isChecked() else list()
        files = [x for x in files if run_type_validator[self.cbb_mode.currentText()](os.path.basename(x), self.old)]
        dirs = [y for y in dirs if run_type_validator[self.cbb_mode.currentText()](os.path.basename(y), self.old)]
        return files, dirs

    def validate(self) -> bool:
        if (tmp_origin := self.le_origin.text().strip()) and os.path.isdir(origin := os.path.normpath(tmp_origin)):
            self.origin = origin
        else:
            QMessageBox.information(self, '参数错误', '请选择有效的操作目录')
            return False
        if s := self.le_old.text().strip():
            self.old = s
        elif '去除' in self.cbb_mode.currentText() or '替换' in self.cbb_mode.currentText():
            QMessageBox.information(self, '参数错误', '请输入有效的原字符串')
            return False
        if s := self.le_new.text().strip():
            self.new = s
        elif '替换' in self.cbb_mode.currentText() or '新增' in self.cbb_mode.currentText():
            QMessageBox.information(self, '参数错误', '请输入有效的新字符串')
            return False
        return True

    def reset(self):
        self.le_origin.clear()
        self.cbb_mode.setCurrentIndex(0)
        self.le_old.clear()
        self.le_new.clear()
        self.cb_recursion.setChecked(False)
        self.cb_dir_name.setChecked(False)

    def switch_mode(self, text):
        if '替换' in text:
            self.le_new.setEnabled(True)
            self.le_old.setEnabled(True)
        elif '新增' in text:
            self.le_old.setEnabled(False)
            self.le_new.setEnabled(True)
        else:
            self.le_old.setEnabled(True)
            self.le_new.setEnabled(False)

    def pick_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择目录', '')
        if dir_path:
            self.origin = os.path.normpath(dir_path)
            self.le_origin.setText(self.origin)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = WidgetBatchRename()
    w.show()
    sys.exit(app.exec())
