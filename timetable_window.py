from PyQt5.QtWidgets import QMainWindow, QScrollArea, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget

class TimetableWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TimetableWindow, self).__init__(parent)
        self.setWindowTitle("Timetable")
        self.setGeometry(100, 100, 800, 600)
        self.scrollArea = QScrollArea(self)
        self.setCentralWidget(self.scrollArea)
        self.sectionWidgets = []

    def updateTable(self, section, workingDays, timeSlots, timetable_dict):
        tableWidget = QTableWidget()
        tableWidget.setRowCount(len(workingDays))
        tableWidget.setColumnCount(len(timeSlots))
        tableWidget.setHorizontalHeaderLabels(timeSlots)
        tableWidget.setVerticalHeaderLabels(workingDays)
        for i, day in enumerate(workingDays):
            for j, slot in enumerate(timeSlots):
                item = QTableWidgetItem(timetable_dict[day][slot])
                tableWidget.setItem(i, j, item)
        self.sectionWidgets.append((section, tableWidget))

    def show(self):
        widget = QWidget()
        layout = QVBoxLayout()
        for section, tableWidget in self.sectionWidgets:
            layout.addWidget(QLabel(f"Section: {section}"))
            layout.addWidget(tableWidget)
        widget.setLayout(layout)
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
        super().show()
        self.showMaximized()
