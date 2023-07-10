from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QComboBox, QTimeEdit, QSpinBox, QListWidget, QInputDialog, QErrorMessage, QGridLayout, QTableWidget, QTableWidgetItem, QMainWindow, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from deap import base, creator, tools
import random
from collections import defaultdict

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
        self.scrollArea.setWidgetResizable(True)  # Make the widget resizable
        super().show()
        self.showMaximized()  # Show the window maximized

class SchedulerUI(QWidget):
    def __init__(self):
        super().__init__()

        self.timetableWindow = TimetableWindow(self)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create labels and fields for user input
        self.sectionsLabel = QLabel("Sections:")
        self.sectionsInput = QLineEdit()
        self.teachersLabel = QLabel("Teachers, their Subjects and their constraints (comma separated):")
        self.teachersInput = QListWidget()
        self.timeSlotsLabel = QLabel("Time Slots (comma separated):")
        self.timeSlotsInput = QLineEdit()
        self.lunchBreakLabel = QLabel("Lunch Breaks (Start-End, comma separated):")
        self.lunchBreakInput = QListWidget()
        self.workingDaysLabel = QLabel("Working Days:")
        self.workingDaysInput = QListWidget()
        self.classDurationLabel = QLabel("Class Duration (minutes):")
        self.classDurationInput = QSpinBox()

        # Configure input widgets
        self.workingDaysInput.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.workingDaysInput.setSelectionMode(QListWidget.MultiSelection)
        self.classDurationInput.setRange(1, 180)  # Class duration between 1 and 180 minutes

        # Add labels and fields to layout
        layout.addWidget(self.sectionsLabel)
        layout.addWidget(self.sectionsInput)
        layout.addWidget(self.teachersLabel)
        layout.addWidget(self.teachersInput)
        layout.addWidget(self.timeSlotsLabel)
        layout.addWidget(self.timeSlotsInput)
        layout.addWidget(self.lunchBreakLabel)
        layout.addWidget(self.lunchBreakInput)
        layout.addWidget(self.workingDaysLabel)
        layout.addWidget(self.workingDaysInput)
        layout.addWidget(self.classDurationLabel)
        layout.addWidget(self.classDurationInput)

        # Create buttons for adding and removing teachers and lunch breaks
        self.addTeacherButton = QPushButton("Add Teacher", self)
        self.addTeacherButton.clicked.connect(self.addTeacher)
        self.removeTeacherButton = QPushButton("Remove Teacher", self)
        self.removeTeacherButton.clicked.connect(self.removeTeacher)
        self.addLunchBreakButton = QPushButton("Add Lunch Break", self)
        self.addLunchBreakButton.clicked.connect(self.addLunchBreak)
        self.removeLunchBreakButton = QPushButton("Remove Lunch Break",self)
        self.removeLunchBreakButton.clicked.connect(self.removeLunchBreak)

        # Add buttons to layout
        layout.addWidget(self.addTeacherButton)
        layout.addWidget(self.removeTeacherButton)
        layout.addWidget(self.addLunchBreakButton)
        layout.addWidget(self.removeLunchBreakButton)

        # Create a button for submitting the form
        self.submitButton = QPushButton("Submit", self)
        self.submitButton.clicked.connect(self.submitForm)

        # Add button to layout
        layout.addWidget(self.submitButton)

        # Set the layout for the widget
        self.setLayout(layout)

    def addTeacher(self):
        teacher, ok = QInputDialog.getText(self, "Add Teacher", "Enter teacher's name, their subjects, max classes per day and max consecutive classes (comma separated):\nFormat: TeacherName,Subject1,Subject2,...,MaxClassesPerDay,MaxConsecutiveClasses")
        if ok and teacher:
            self.teachersInput.addItem(teacher)

    def removeTeacher(self):
        for item in self.teachersInput.selectedItems():
            self.teachersInput.takeItem(self.teachersInput.row(item))

    def addLunchBreak(self):
        lunchBreak, ok = QInputDialog.getText(self, "Add Lunch Break", "Enter lunch break start and end time (comma separated):\nFormat: Start-End")
        if ok and lunchBreak:
            self.lunchBreakInput.addItem(lunchBreak)

    def removeLunchBreak(self):
        for item in self.lunchBreakInput.selectedItems():
            self.lunchBreakInput.takeItem(self.lunchBreakInput.row(item))

    def submitForm(self):
        # Get user input from form
        sections = self.sectionsInput.text().split(',')
        teachers = [self.teachersInput.item(i).text().split(",") for i in range(self.teachersInput.count())]
        timeSlots = self.timeSlotsInput.text().split(',')
        lunchBreaks = [self.lunchBreakInput.item(i).text().split('-') for i in range(self.lunchBreakInput.count())]
        workingDays = [self.workingDaysInput.item(i).text() for i in range(self.workingDaysInput.count()) if self.workingDaysInput.item(i).isSelected()]
        classDuration = self.classDurationInput.value()

        # Run the genetic algorithm for each section
        for section in sections:
            self.runGeneticAlgorithm(section, teachers, timeSlots, workingDays, lunchBreaks, classDuration)

        self.timetableWindow.show()

    def generate_class(self, teachers, time_slots, working_days):
        teacher = random.choice(teachers)
        subject = random.choice(teacher[1:-2])
        time_slot = random.choice(time_slots)
        working_day = random.choice(working_days)
        return (teacher[0], subject, time_slot, working_day)

    def mutate(self, individual, teachers, time_slots, working_days):
        index = random.randrange(len(individual))
        individual[index] = self.generate_class(teachers, time_slots, working_days)

    def runGeneticAlgorithm(self, section, teachers, timeSlots, workingDays, lunchBreaks, classDuration):
        # Define the fitness function
        def fitness(individual, lunchBreaks, teachers):
            penalty = 0
            teacher_day_classes = defaultdict(int)
            teacher_consecutive_classes = defaultdict(int)
            last_class_info = None
            for class_info in sorted(individual, key=lambda x: (x[3], x[2])):
                teacher, subject, slot, day = class_info
                # Conflict: same teacher at the same time
                if any(teacher == other_class[0] and slot == other_class[2] and day == other_class[3] for other_class in individual if other_class != class_info):
                    penalty += 1
                # Conflict: class during lunch break
                for lunchBreak in lunchBreaks:
                    if lunchBreak[0] <= slot < lunchBreak[1]:
                        penalty += 1
                # Conflict: more classes per day than a teacher can handle
                teacher_day_classes[(teacher, day)] += 1
                if teacher_day_classes[(teacher, day)] > int([t for t in teachers if t[0] == teacher][0][-2]):
                    penalty += 1
                # Conflict: more consecutive classes than a teacher can handle
                if last_class_info and last_class_info[0] == teacher and last_class_info[3] == day and timeSlots.index(last_class_info[2]) == timeSlots.index(slot) - 1:
                    teacher_consecutive_classes[teacher] += 1
                    if teacher_consecutive_classes[teacher] > int([t for t in teachers if t[0] == teacher][0][-1]):
                        penalty += 1
                else:
                    teacher_consecutive_classes[teacher] = 1
                last_class_info = class_info
            # Conflict: unbalanced number of classes across different days
            day_classes = defaultdict(int)
            for class_info in individual:
                day_classes[class_info[3]] += 1
            average_classes_per_day = sum(day_classes.values()) / len(workingDays)
            for day in workingDays:
                if abs(day_classes[day] - average_classes_per_day) > 1:
                    penalty += 1
            return penalty,

        # Define the individual and population
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("attr_class", self.generate_class, teachers=teachers, time_slots=timeSlots, working_days=workingDays)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_class, n=100)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        # Define the genetic operators
        toolbox.register("evaluate", fitness, lunchBreaks=lunchBreaks, teachers=teachers)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", self.mutate, teachers=teachers, time_slots=timeSlots, working_days=workingDays)
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Initialize the population and evolve it
        pop = toolbox.population(n=300)
        fitnesses = list(map(toolbox.evaluate, pop))

        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for g in range(100):
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.5:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < 0.2:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            pop[:] = offspring

        # Get the best individual in the population
        best_ind = tools.selBest(pop, 1)[0]

        # Create a dictionary to store the timetable
        timetable_dict = {}
        for day in workingDays:
            timetable_dict[day] = {}
            for slot in timeSlots:
                timetable_dict[day][slot] = ""

        # Fill the timetable with the best individual
        for class_info in best_ind:
            teacher, subject, slot, day = class_info
            timetable_dict[day][slot] = f"{subject} ({teacher})"

        # Add lunch breaks to the timetable
        for lunchBreak in lunchBreaks:
            start, end = lunchBreak
            for day in workingDays:
                for slot in timeSlots:
                    if start <= slot <= end:
                        timetable_dict[day][slot] = "Lunch Break"

        # Update the timetable widget
        self.timetableWindow.updateTable(section, workingDays, timeSlots, timetable_dict)

def main():
    app = QApplication([])
    ui = SchedulerUI()
    ui.show()
    app.exec_()

if __name__ == "__main__":
    main()
