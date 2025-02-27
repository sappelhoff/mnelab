# © MNELAB developers
#
# License: BSD (3-clause)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mne.channels import make_standard_montage
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QListWidget,
    QVBoxLayout,
    QWidget,
)


class MontageDialog(QDialog):
    def __init__(self, parent, montages):
        super().__init__(parent)
        self.setWindowTitle("Set montage")
        self.resize(760, 500)

        vbox = QVBoxLayout()
        self.montages = QListWidget()
        self.montages.insertItems(0, montages)
        self.montages.setSelectionMode(QListWidget.SingleSelection)
        vbox.addWidget(self.montages)
        self.montages.itemSelectionChanged.connect(self.view_montage)
        self.match_case = QCheckBox("Match case-sensitive", self)
        self.match_alias = QCheckBox("Match aliases", self)
        self.ignore_missing = QCheckBox("Ignore missing", self)
        self.ignore_missing.setChecked(True)
        vbox.addWidget(self.match_case)
        vbox.addWidget(self.match_alias)
        vbox.addWidget(self.ignore_missing)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox, stretch=1)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas_container = QWidget(self)
        self.canvas_container.setMinimumWidth(240)
        self.canvas_container.setMinimumHeight(220)
        self.canvas_layout = QVBoxLayout(self.canvas_container)
        self.canvas_layout.setContentsMargins(0, 0, 0, 0)
        self.canvas_layout.setSpacing(0)
        self.canvas_layout.addWidget(self.canvas)
        self.canvas_container.setLayout(self.canvas_layout)
        hbox.addWidget(self.canvas_container, stretch=2)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        button_layout.addWidget(self.buttonbox, alignment=Qt.AlignLeft)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(hbox)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        if self.montages.count() > 0:
            self.montages.setCurrentRow(0)
            self.view_montage()

    def view_montage(self):
        name = self.montages.selectedItems()[0].data(0)
        montage = make_standard_montage(name)
        self.figure.clear()
        ax = self.figure.add_subplot()
        montage.plot(show_names=True, show=False, axes=ax)
        ax.set_aspect("equal")
        self.figure.tight_layout(pad=0.5)
        ax.margins(0)
        self.canvas.draw()
