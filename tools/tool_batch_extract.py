import os.path

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, \
    QPushButton, QCheckBox, QStyle, QFileDialog, QMessageBox
from PySide6.QtCore import QSize, Qt

from components.common import ComboCheckBox, H_SPACER
from components.interface import WidgetWithComboCheckBox
from util.common import global_config
from util.io import get_files_by_dir, get_new_target_path, get_target_path_with_dn


class WidgetBatchExtract(WidgetWithComboCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.origin = ''
        self.target = ''
        self.name_features = ''
        self.type_features = list()
        self.success = 0
        self.errs = list()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 20)

        self.origin_layout = QHBoxLayout()
        self.origin_layout.setSpacing(0)
        self.origin_layout.addItem(H_SPACER)
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
        self.btn_pick_origin = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon), '选择目录',
                                           self)
        self.btn_pick_origin.setMinimumSize(QSize(0, 30))
        self.origin_layout.addWidget(self.btn_pick_origin)
        self.origin_layout.addItem(H_SPACER)
        self.origin_layout.setStretch(0, 1)
        self.origin_layout.setStretch(1, 1)
        self.origin_layout.setStretch(2, 4)
        self.origin_layout.setStretch(3, 1)
        self.origin_layout.setStretch(4, 1)
        self.main_layout.addLayout(self.origin_layout)

        self.target_layout = QHBoxLayout()
        self.target_layout.setSpacing(0)
        self.target_layout.addItem(H_SPACER)
        self.lb_target = QLabel('目标目录：', self)
        self.lb_target.setSizePolicy(size_policy)
        self.target_layout.addWidget(self.lb_target)
        self.le_target = QLineEdit(self)
        self.le_target.setMinimumSize(QSize(0, 25))
        self.target_layout.addWidget(self.le_target)
        self.btn_pick_target = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon), '选择目录',
                                           self)
        self.btn_pick_target.setMinimumSize(QSize(0, 30))
        self.target_layout.addWidget(self.btn_pick_target)
        self.target_layout.addItem(H_SPACER)
        self.target_layout.setStretch(0, 1)
        self.target_layout.setStretch(1, 1)
        self.target_layout.setStretch(2, 4)
        self.target_layout.setStretch(3, 1)
        self.target_layout.setStretch(4, 1)
        self.main_layout.addLayout(self.target_layout)

        self.features_layout = QHBoxLayout()
        self.features_layout.setSpacing(0)
        self.features_layout.addItem(H_SPACER)
        self.lb_name_features = QLabel('名称特征：', self)
        self.lb_name_features.setSizePolicy(size_policy)
        self.features_layout.addWidget(self.lb_name_features)
        self.le_name_features = QLineEdit(self)
        self.le_name_features.setMinimumSize(QSize(0, 25))
        self.features_layout.addWidget(self.le_name_features)
        self.features_layout.addItem(H_SPACER)
        self.features_layout.setStretch(0, 1)
        self.features_layout.setStretch(1, 1)
        self.features_layout.setStretch(2, 5)
        self.features_layout.setStretch(3, 1)
        self.main_layout.addLayout(self.features_layout)

        self.type_layout = QHBoxLayout()
        self.type_layout.setSpacing(0)

        self.type_layout.addItem(H_SPACER)

        self.lb_type_features = QLabel('类型特征：', self)
        self.lb_type_features.setSizePolicy(size_policy)

        self.type_layout.addWidget(self.lb_type_features)

        self.cbb_type_features = ComboCheckBox(list(), self)
        self.cbb_type_features.setMinimumSize(QSize(0, 25))

        self.type_layout.addWidget(self.cbb_type_features)

        self.type_layout.addItem(H_SPACER)

        self.type_layout.setStretch(0, 1)
        self.type_layout.setStretch(1, 1)
        self.type_layout.setStretch(2, 5)
        self.type_layout.setStretch(3, 1)

        self.main_layout.addLayout(self.type_layout)

        self.misc_layout = QHBoxLayout()
        self.misc_layout.setSpacing(0)

        self.misc_layout.addItem(H_SPACER)

        self.cb_recursion = QCheckBox('递归应用到子目录', self)
        self.cb_recursion.setSizePolicy(size_policy)
        self.cb_recursion.setChecked(True)

        self.misc_layout.addWidget(self.cb_recursion, 0, Qt.AlignmentFlag.AlignHCenter)

        self.misc_layout.addItem(H_SPACER)

        self.cb_del_origin = QCheckBox('删除源文件', self)

        self.misc_layout.addWidget(self.cb_del_origin, 0, Qt.AlignmentFlag.AlignHCenter)

        self.misc_layout.addItem(H_SPACER)

        self.cb_with_dn = QCheckBox('附加原目录名', self)

        self.misc_layout.addWidget(self.cb_with_dn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.misc_layout.addItem(H_SPACER)

        self.misc_layout.setStretch(0, 1)
        self.misc_layout.setStretch(1, 1)
        self.misc_layout.setStretch(2, 1)
        self.misc_layout.setStretch(3, 1)
        self.misc_layout.setStretch(4, 1)
        self.misc_layout.setStretch(5, 1)
        self.misc_layout.setStretch(6, 1)

        self.main_layout.addLayout(self.misc_layout)

        self.run_layout = QHBoxLayout()
        self.run_layout.setSpacing(0)

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

    def bind(self):
        self.btn_pick_origin.clicked.connect(self.pick_dir)
        self.btn_pick_target.clicked.connect(self.pick_dir)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_run.clicked.connect(self.run)

    def run(self):
        if self.validate():
            if to_modify := self.collect():
                self.modify(to_modify)
                if self.errs:
                    e = '\n'.join(self.errs)
                    QMessageBox.information(self, '异常', f'😢执行已经结束，{self.success}个路径已修改，但存在异常：{e}')
                else:
                    QMessageBox.information(self, '成功', f'😊执行成功结束，{self.success}个路径已修改。')

    def modify(self, to_modify: list):
        self.errs.clear()
        self.success = len(to_modify)
        self.modify_paths(to_modify)

    def modify_paths(self, paths):
        for p in paths:
            if self.cb_with_dn.isChecked():
                want_target_path = get_new_target_path(p, get_target_path_with_dn(p, self.target),
                                                       exist_func=os.path.isfile)
            else:
                want_target_path = get_new_target_path(p,
                                                       os.path.normpath(os.path.join(self.target, os.path.basename(p))),
                                                       exist_func=os.path.isfile)
            if self.cb_del_origin.isChecked():
                try:
                    os.rename(p, want_target_path)
                except Exception as e:
                    self.success -= 1
                    self.errs.append(f'原路径:{p}，目标路径:{want_target_path}，错误信息:{e}')
            else:
                try:
                    os.system(f'{global_config.cp_order} "{p}" "{want_target_path}"')
                except Exception as e:
                    self.success -= 1
                    self.errs.append(f'原路径:{p}，目标路径:{want_target_path}，错误信息:{e}')

    def fit_features(self, file_name: str):
        fit_name_features = False
        fit_type_features = False
        if self.name_features in file_name:
            fit_name_features = True
        if self.type_features:
            for t in self.type_features:
                if file_name.endswith(t):
                    fit_type_features = True
        else:
            fit_type_features = True
        return fit_name_features and fit_type_features

    def get_cbb_items(self):
        extensions = list()
        if self.silent_validate():
            if to_modify := self.collect():
                extensions = list(set([os.path.splitext(file)[1] for file in to_modify]))
        return extensions

    def collect(self) -> list:
        if self.cb_recursion.isChecked():
            files = get_files_by_dir(self.origin)
        else:
            files = [os.path.normpath(os.path.join(self.origin, file)) for file in os.listdir(self.origin) if
                     os.path.isfile(file)]
        files = [x for x in files if self.fit_features(os.path.basename(x))]
        return files

    def silent_validate(self) -> bool:
        if (tmp_origin := self.le_origin.text().strip()) and os.path.isdir(origin := os.path.normpath(tmp_origin)):
            self.origin = origin
        else:
            return False
        if s := self.le_name_features.text().strip():
            self.name_features = s
        else:
            self.name_features = ''
        self.type_features = list()
        return True


    def validate(self) -> bool:
        if (tmp_origin := self.le_origin.text().strip()) and os.path.isdir(origin := os.path.normpath(tmp_origin)):
            self.origin = origin
        else:
            QMessageBox.information(self, '参数错误', '请选择有效的操作目录')
            return False
        if (tmp_target := self.le_target.text().strip()) and os.path.isdir(target := os.path.normpath(tmp_target)):
            self.target = target
        else:
            QMessageBox.information(self, '参数错误', '请选择有效的目标目录')
            return False
        if s := self.le_name_features.text().strip():
            self.name_features = s
            self.type_features = self.cbb_type_features.selected
        elif self.cbb_type_features.selected:
            self.name_features = ''
            self.type_features = self.cbb_type_features.selected
        else:
            QMessageBox.information(self, '参数错误',
                                    '请输入有效的名称（字符串）特征或选择有效的类型特征。\n（可能当前目录下无符合特征约束的文件）')
            return False

        if (not self.cb_with_dn.isChecked()) and self.cb_del_origin.isChecked():
            reply = QMessageBox.question(self, '执行确认',
                                         '您没有选择附加父目录名并且选择删除源文件，这样可能会造成丢失源目录树结构信息，确定继续吗？',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.No:
                return False
        return True

    def reset(self):
        self.le_origin.clear()
        self.le_name_features.clear()
        self.cbb_type_features.clear()
        self.cb_recursion.setChecked(True)
        self.cb_del_origin.setChecked(False)
        self.cb_with_dn.setChecked(False)

    def pick_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择目录', '')
        if dir_path:
            if self.sender() == self.btn_pick_origin:
                self.origin = os.path.normpath(dir_path)
                self.le_origin.setText(self.origin)
            elif self.sender() == self.btn_pick_target:
                self.target = os.path.normpath(dir_path)
                self.le_target.setText(self.target)
