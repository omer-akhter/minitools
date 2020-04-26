#!/usr/bin/env python3
'''
format json
'''
from PySide2 import QtWidgets

from logic import format_json_str


class MainForm(object):

    def do_layout(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle('json formatter')

        self.box_sort_keys = QtWidgets.QCheckBox('sort keys', self.dialog)
        self.box_compact = QtWidgets.QRadioButton('compact', self.dialog)
        self.box_do_indent = QtWidgets.QRadioButton('indent', self.dialog)
        self.box_indent = QtWidgets.QSpinBox(self.dialog)
        self.box_json_in = QtWidgets.QPlainTextEdit('', self.dialog)
        self.box_json_out = QtWidgets.QPlainTextEdit('', self.dialog)

        self.box_indent.setMinimum(1)
        self.box_indent.setValue(2)
        self.box_json_in.setPlaceholderText('input json string here...')
        self.box_json_out.setPlaceholderText('output json string here...')
        self.box_json_out.setReadOnly(True)

        for box_edit in (self.box_json_in,
                         self.box_json_out,):
            doc = box_edit.document()
            font = doc.defaultFont()
            font.setFamilies([
                'lucida console'
                'courier new'
                'monaco',
                'courier',
                'monospace',
            ])
            # font = QFont()
            # font.setStyleHint(QFont.Monospace)
            doc.setDefaultFont(font)

        # Create layout and add widgets
        layout = QtWidgets.QVBoxLayout()

        layout_row = QtWidgets.QHBoxLayout()
        layout_row.addWidget(self.box_sort_keys)
        layout_row.addWidget(self.box_compact)
        layout_row.addWidget(self.box_do_indent)
        layout_row.addWidget(self.box_indent)
        layout.addLayout(layout_row)

        layout_row = QtWidgets.QHBoxLayout()
        layout_row.addWidget(self.box_json_in)
        layout_row.addWidget(self.box_json_out)
        layout.addLayout(layout_row)

        layout_row = QtWidgets.QHBoxLayout()
        btn = QtWidgets.QPushButton('from file', self.dialog)
        btn.clicked.connect(self.load_file)
        layout_row.addWidget(btn)
        btn = QtWidgets.QPushButton('to file', self.dialog)
        btn.clicked.connect(self.save_file)
        layout_row.addWidget(btn)
        layout.addLayout(layout_row)

        # Set dialog layout
        self.dialog.setLayout(layout)

        # Add signals
        self.box_do_indent.toggled.connect(
            lambda x: self.box_indent.setEnabled(x))
        self.box_do_indent.toggle()

        self.box_sort_keys.toggled.connect(self.do_format)
        self.box_compact.toggled.connect(self.do_format)
        self.box_indent.valueChanged.connect(self.do_format)
        self.box_json_in.textChanged.connect(self.do_format)

        return self

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.dialog, 'load file')
        with open(file_name) as f:
            self.box_json_in.setPlainText(f.read())

    def save_file(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.dialog, 'save file')
        with open(file_name, 'w') as f:
            f.write(self.box_json_out.toPlainText())

    def do_format(self):
        json_str = self.box_json_in.toPlainText().strip()
        if not json_str:
            return

        params = {
            'sort_keys': self.box_sort_keys.isChecked(),
            'compact': self.box_compact.isChecked(),
            'indent': self.box_indent.value()
        }

        _, output = format_json_str(json_str, **params)
        self.box_json_out.setPlainText(output)

    @classmethod
    def run_as_application(cls, args=None):
        app = QtWidgets.QApplication(args or [])
        form = cls().do_layout()
        form.dialog.show()
        exit(app.exec_())


if __name__ == '__main__':
    MainForm.run_as_application()
