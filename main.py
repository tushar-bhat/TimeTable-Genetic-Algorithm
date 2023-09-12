from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from deap import base, creator, tools
import random
from collections import defaultdict
import time
import numpy as np
from multiprocessing import Pool

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

class MetricsTable(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Population", "Generations", "Fitness Score", "Execution Time", "Convergence Generations", "Diversity Score"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.deleteRowButton = QPushButton("Delete Selected Row", self)
        self.deleteRowButton.clicked.connect(self.deleteRow)
        self.layout.addWidget(self.deleteRowButton)

    def addRow(self, data):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        for i, item in enumerate(data):
            self.table.setItem(rowPosition, i, QTableWidgetItem(str(item)))

    def getData(self):
        data = []
        for row in range(self.table.rowCount()):
            rowData = []
            for col in range(self.table.columnCount()):
                rowData.append(self.table.item(row, col).text())
            data.append(rowData)
        return data

    def setData(self, data):
        self.table.setRowCount(0)
        for rowData in data:
            self.addRow(rowData)

    def deleteRow(self):
        currentRow = self.table.currentRow()
        self.table.removeRow(currentRow)

class SchedulerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.timetableWindow = TimetableWindow(self)
        self.metricsTable = MetricsTable()
        self.settings = QSettings("SchedulerApp", "SchedulerUI")
        self.teacher_slot_classes = defaultdict(int)
        self.subject_section_classes = defaultdict(int)
        self.subject_hours = defaultdict(int)
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.basicSettingsTab = QWidget()
        basicLayout = QVBoxLayout()
        self.sectionsLabel = QLabel("Sections:")
        self.sectionsInput = QLineEdit(self.settings.value("sections", ""))
        self.workingDaysLabel = QLabel("Working Days:")
        self.workingDaysInput = QListWidget()
        self.workingDaysInput.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.workingDaysInput.setSelectionMode(QListWidget.MultiSelection)
        self.classDurationLabel = QLabel("Class Duration (minutes):")
        self.classDurationInput = QSpinBox()
        self.classDurationInput.setRange(1, 180)
        self.classDurationInput.setValue(int(self.settings.value("classDuration", 0)))

        basicLayout.addWidget(self.sectionsLabel)
        basicLayout.addWidget(self.sectionsInput)
        basicLayout.addWidget(self.workingDaysLabel)
        basicLayout.addWidget(self.workingDaysInput)
        basicLayout.addWidget(self.classDurationLabel)
        basicLayout.addWidget(self.classDurationInput)
        self.basicSettingsTab.setLayout(basicLayout)

        self.teachersTab = QWidget()
        teachersLayout = QVBoxLayout()
        self.teachersLabel = QLabel("Teachers, their Subjects, their constraints and subject hours per week (comma separated):")
        self.teachersInput = QListWidget()
        self.teachersInput.addItems(self.settings.value("teachers", []))
        self.addTeacherButton = QPushButton("Add Teacher", self)
        self.addTeacherButton.clicked.connect(self.addTeacher)
        self.removeTeacherButton = QPushButton("Remove Teacher", self)
        self.removeTeacherButton.clicked.connect(self.removeTeacher)

        teachersLayout.addWidget(self.teachersLabel)
        teachersLayout.addWidget(self.teachersInput)
        teachersLayout.addWidget(self.addTeacherButton)
        teachersLayout.addWidget(self.removeTeacherButton)
        self.teachersTab.setLayout(teachersLayout)

        self.timeSlotsTab = QWidget()
        timeSlotsLayout = QVBoxLayout()
        self.timeSlotsLabel = QLabel("Time Slots (comma separated):")
        self.timeSlotsInput = QLineEdit(self.settings.value("timeSlots", ""))
        self.lunchBreakLabel = QLabel("Lunch Breaks (Start-End, comma separated):")
        self.lunchBreakInput = QListWidget()
        self.lunchBreakInput.addItems(self.settings.value("lunchBreaks", []))
        self.addLunchBreakButton = QPushButton("Add Lunch Break", self)
        self.addLunchBreakButton.clicked.connect(self.addLunchBreak)
        self.removeLunchBreakButton = QPushButton("Remove Lunch Break",self)
        self.removeLunchBreakButton.clicked.connect(self.removeLunchBreak)

        timeSlotsLayout.addWidget(self.timeSlotsLabel)
        timeSlotsLayout.addWidget(self.timeSlotsInput)
        timeSlotsLayout.addWidget(self.lunchBreakLabel)
        timeSlotsLayout.addWidget(self.lunchBreakInput)
        timeSlotsLayout.addWidget(self.addLunchBreakButton)
        timeSlotsLayout.addWidget(self.removeLunchBreakButton)
        self.timeSlotsTab.setLayout(timeSlotsLayout)

        self.tabs.addTab(self.basicSettingsTab, "Basic Settings")
        self.tabs.addTab(self.teachersTab, "Teachers")
        self.tabs.addTab(self.timeSlotsTab, "Time Slots and Breaks")

        mainLayout.addWidget(self.tabs)

        self.submitButton = QPushButton("Submit", self)
        self.submitButton.clicked.connect(self.submitForm)
        mainLayout.addWidget(self.submitButton)

        self.saveButton = QPushButton("Save Settings", self)
        self.saveButton.clicked.connect(self.saveSettings)
        mainLayout.addWidget(self.saveButton)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setVisible(False)
        mainLayout.addWidget(self.progressBar)

        mainLayout.addWidget(self.metricsTable)

        self.setLayout(mainLayout)

    def addTeacher(self):
        teacher, ok = QInputDialog.getText(self, "Add Teacher", "Enter teacher's name, their subjects, subject hours per week, max classes per week and max consecutive classes (comma separated):\nFormat: TeacherName,Subject1,SubjectHours1,Subject2,SubjectHours2,...,MaxClassesPerWeek,MaxConsecutiveClasses")
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

    def saveSettings(self):
        self.settings.setValue("sections", self.sectionsInput.text())
        self.settings.setValue("classDuration", self.classDurationInput.value())
        self.settings.setValue("teachers", [self.teachersInput.item(i).text() for i in range(self.teachersInput.count())])
        self.settings.setValue("timeSlots", self.timeSlotsInput.text())
        self.settings.setValue("lunchBreaks", [self.lunchBreakInput.item(i).text() for i in range(self.lunchBreakInput.count())])
        self.settings.setValue("metricsData", self.metricsTable.getData())

    def submitForm(self):
        sections = self.sectionsInput.text().split(',')
        teachers = [self.teachersInput.item(i).text().split(",") for i in range(self.teachersInput.count())]
        timeSlots = self.timeSlotsInput.text().split(',')
        lunchBreaks = [self.lunchBreakInput.item(i).text().split('-') for i in range(self.lunchBreakInput.count())]
        workingDays = [self.workingDaysInput.item(i).text() for i in range(self.workingDaysInput.count()) if self.workingDaysInput.item(i).isSelected()]
        classDuration = self.classDurationInput.value()

        self.progressBar.setVisible(True)
        metrics = self.runGeneticAlgorithm(sections, teachers, timeSlots, workingDays, lunchBreaks, classDuration)
        self.metricsTable.addRow(metrics)
        self.progressBar.setValue(100)
        QMessageBox.information(self, "Success", "Timetable successfully generated!")
        self.progressBar.setVisible(False)
        self.timetableWindow.show()

    def generate_class(self, sections, teachers, time_slots, working_days):
        while True:
            section = random.choice(sections)
            teacher = random.choice(teachers)
            subject_index = random.choice(range(len(teacher[1:-2:2])))
            subject = teacher[1 + subject_index * 2]
            hours = int(teacher[2 + subject_index * 2])
            time_slot = random.choice(time_slots)
            working_day = random.choice(working_days)
            if self.teacher_slot_classes[(teacher[0], time_slot)] < int(teacher[-2]) and self.subject_section_classes[(subject, time_slot, working_day)] == 0 and self.subject_hours[(subject, section)] < hours:
                return (teacher[0], subject, time_slot, working_day, section)

    def mutate(self, individual):
        index1 = random.randrange(len(individual))
        index2 = random.randrange(len(individual))
        individual[index1], individual[index2] = individual[index2], individual[index1]

    def repair(self, individual, sections, teachers, time_slots, working_days):
        timetable_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        for class_info in individual:
            teacher, subject, slot, day, section = class_info
            timetable_dict[section][day][slot] = f"{subject} ({teacher})"
        for section in sections:
            for day in working_days:
                for slot in time_slots:
                    if timetable_dict[section][day][slot] == "":
                        individual.append(self.generate_class(sections, teachers, time_slots, working_days))

    def runGeneticAlgorithm(self, sections, teachers, timeSlots, workingDays, lunchBreaks, classDuration):
        def fitness(individual, lunchBreaks, teachers):
            penalty = 0

            for class_info in individual:
                teacher, subject, slot, day, section = class_info
                for lunchBreak in lunchBreaks:
                    start, end = lunchBreak
                    if start <= slot <= end:
                        penalty += 100

            teacher_classes = defaultdict(int)
            for class_info in individual:
                teacher, subject, slot, day, section = class_info
                teacher_classes[teacher] += 1
            for teacher in teachers:
                if teacher_classes[teacher[0]] > int(teacher[-2]):
                    penalty += 1

            teacher_consecutive_classes = defaultdict(int)
            for class_info in sorted(individual, key=lambda x: (x[0], x[3], x[2])):
                teacher, subject, slot, day, section = class_info
                if teacher_consecutive_classes[teacher] > 0 and teacher_consecutive_classes[teacher] != day:
                    teacher_consecutive_classes[teacher] = 0
                teacher_consecutive_classes[teacher] += 1
                max_consecutive_classes = next(int(val[-1]) for val in teachers if val[0] == teacher)
                if teacher_consecutive_classes[teacher] > max_consecutive_classes:
                    penalty += 1

            teacher_sections = defaultdict(lambda: defaultdict(set))
            for class_info in individual:
                teacher, subject, slot, day, section = class_info
                teacher_sections[teacher][day, slot].add(section)
            for teacher, sections in teacher_sections.items():
                for _, section_set in sections.items():
                    if len(section_set) > 1:
                        penalty += 100

            timetable_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
            for class_info in individual:
                teacher, subject, slot, day, section = class_info
                timetable_dict[section][day][slot] = f"{subject} ({teacher})"
            for section in sections:
                for day in workingDays:
                    for slot in timeSlots:
                        if timetable_dict[section][day][slot] == "":
                            penalty += 100

            day_classes = defaultdict(int)
            for class_info in individual:
                teacher, subject, slot, day, section = class_info
                day_classes[day] += 1
            average_classes = sum(day_classes.values()) / len(workingDays)
            for day in workingDays:
                if day_classes[day] > average_classes:
                    penalty += 1

            teacher_count_per_subject_section = defaultdict(lambda: defaultdict(int))
            for class_info in individual:
                teacher, subject, slot, day, section = class_info
                teacher_count_per_subject_section[section][subject] += 1

            for section, subjects in teacher_count_per_subject_section.items():
                for subject, count in subjects.items():
                    if count > 1:
                        penalty += 100

            return penalty,

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("attr_class", self.generate_class, sections=sections, teachers=teachers, time_slots=timeSlots, working_days=workingDays)        
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_class, n=len(timeSlots)*len(workingDays)*len(sections))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", fitness, lunchBreaks=lunchBreaks, teachers=teachers)
        toolbox.register("mate", tools.cxUniform, indpb=0.5)
        toolbox.register("mutate", self.mutate)
        toolbox.register("select", tools.selTournament, tournsize=3)

        pop = toolbox.population(n=100)
        fitnesses = list(map(toolbox.evaluate, pop))

        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
            self.repair(ind, sections, teachers, timeSlots, workingDays)

        start_time = time.time()
        fitness_scores = []
        diversity_scores = []

        mutation_rate = 0.01
        crossover_rate = 0.9

        for g in range(100):
            fitness_values = [ind.fitness.values[0] for ind in pop]
            fitness_variance = np.var(fitness_values)
            fitness_mean = np.mean(fitness_values)
            mutation_rate = min(1, max(0.01, mutation_rate + (fitness_variance / (fitness_mean ** 2))))
            crossover_rate = min(1, max(0.01, crossover_rate + (fitness_mean / (fitness_variance ** 2))))

            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < crossover_rate:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
                    self.repair(child1, sections, teachers, timeSlots, workingDays)
                    self.repair(child2, sections, teachers, timeSlots, workingDays)

            for mutant in offspring:
                if random.random() < mutation_rate:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
                    self.repair(mutant, sections, teachers, timeSlots, workingDays)

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            elite = tools.selBest(pop, 1)
            offspring = tools.selBest(offspring, len(offspring) - 1)
            offspring.append(elite[0])

            for ind in offspring:
                self.repair(ind, sections, teachers, timeSlots, workingDays)

            pop[:] = offspring

            fitness_scores.append(min(ind.fitness.values[0] for ind in pop))
            diversity_scores.append(np.var([ind.fitness.values[0] for ind in pop]))

        execution_time = time.time() - start_time

        best_ind = tools.selBest(pop, 1)[0]

        timetable_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        for class_info in best_ind:
            teacher, subject, slot, day, section = class_info
            timetable_dict[section][day][slot] = f"{subject} ({teacher})"

        for lunchBreak in lunchBreaks:
            start, end = lunchBreak
            for day in workingDays:
                for slot in timeSlots:
                    if start <= slot <= end:
                        timetable_dict[section][day][slot] = "Lunch Break"

        for section in sections:
            self.timetableWindow.updateTable(section, workingDays, timeSlots, timetable_dict[section])

        convergence_gen = next((i for i, score in enumerate(fitness_scores) if score == fitness_scores[-1]), 100)
        return [100, 100, fitness_scores[-1], execution_time, convergence_gen, diversity_scores[-1]]

def main():
        app = QApplication([])
        ui = SchedulerUI()
        ui.metricsTable.setData(ui.settings.value("metricsData", []))
        ui.show()
        app.exec_()

if __name__ == "__main__":
    main()
