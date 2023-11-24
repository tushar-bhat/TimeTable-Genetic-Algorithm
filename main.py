from PyQt5.QtWidgets import QApplication
from scheduler_ui import SchedulerUI

if __name__ == '__main__':
    app = QApplication([])
    window = SchedulerUI()
    window.show()
    app.exec_()
