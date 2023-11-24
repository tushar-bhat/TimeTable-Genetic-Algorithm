from collections import defaultdict
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QLineEdit, QListWidget, QSpinBox, QPushButton, QProgressBar, QMessageBox, QInputDialog, QFileDialog
from PyQt5.QtCore import QSettings
from timetable_window import TimetableWindow
from collections import defaultdict
import random
import time
import numpy as np
from deap import base, creator, tools

class SchedulerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.timetableWindow = TimetableWindow(self)
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

        self.importButton = QPushButton('Import Settings', self)
        self.importButton.clicked.connect(self.importSettings)
        basicLayout.addWidget(self.importButton)

        self.exportButton = QPushButton('Export Settings', self)
        self.exportButton.clicked.connect(self.exportSettings)
        basicLayout.addWidget(self.exportButton)

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

    def exportSettings(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Export Settings", "", "INI Files (*.ini);;All Files (*)", options=options)
        
        if filePath:
            settings = QSettings(filePath, QSettings.IniFormat)

            settings.setValue("sections", self.sectionsInput.text())
            
            workingDaysSelected = [self.workingDaysInput.item(i).text() for i in range(self.workingDaysInput.count()) if self.workingDaysInput.item(i).isSelected()]
            settings.setValue("workingDays", workingDaysSelected)
            
            settings.setValue("classDuration", self.classDurationInput.value())

            teachersList = [self.teachersInput.item(i).text() for i in range(self.teachersInput.count())]
            settings.setValue("teachers", teachersList)

            settings.setValue("timeSlots", self.timeSlotsInput.text())
            
            lunchBreaksList = [self.lunchBreakInput.item(i).text() for i in range(self.lunchBreakInput.count())]
            settings.setValue("lunchBreaks", lunchBreaksList)

            settings.sync()

    def importSettings(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Settings", "", "INI Files (*.ini);;All Files (*)", options=options)
        
        if filePath:
            settings = QSettings(filePath, QSettings.IniFormat)

            self.sectionsInput.setText(settings.value("sections", type=str))
            
            workingDays = settings.value("workingDays", [])
            for i in range(self.workingDaysInput.count()):
                item = self.workingDaysInput.item(i)
                if item.text() in workingDays:
                    item.setSelected(True)
                else:
                    item.setSelected(False)
                    
            classDuration = settings.value("classDuration", type=int)
            self.classDurationInput.setValue(classDuration)

            teachersList = settings.value("teachers", [])
            self.teachersInput.clear()
            self.teachersInput.addItems(teachersList)

            self.timeSlotsInput.setText(settings.value("timeSlots", type=str))
            
            lunchBreaksList = settings.value("lunchBreaks", [])
            self.lunchBreakInput.clear()
            self.lunchBreakInput.addItems(lunchBreaksList)


    def submitForm(self):
        sections = self.sectionsInput.text().split(',')
        teachers = [self.teachersInput.item(i).text().split(",") for i in range(self.teachersInput.count())]
        timeSlots = self.timeSlotsInput.text().split(',')
        lunchBreaks = [self.lunchBreakInput.item(i).text().split('-') for i in range(self.lunchBreakInput.count())]
        workingDays = [self.workingDaysInput.item(i).text() for i in range(self.workingDaysInput.count()) if self.workingDaysInput.item(i).isSelected()]
        classDuration = self.classDurationInput.value()
        self.progressBar.setVisible(True)
        self.runGeneticAlgorithm(sections, teachers, timeSlots, workingDays, lunchBreaks, classDuration)
        self.progressBar.setValue(100)
        QMessageBox.information(self, "Success", "Timetable successfully generated!")
        self.progressBar.setVisible(False)
        self.timetableWindow.show()
    
    
    def generate_class(self, sections, teachers, time_slots, working_days, subject_teacher_map):
        while True:
            section = random.choice(sections)
            teacher = random.choice(teachers)
            subject_index = random.choice(range(len(teacher[1:-2:2])))
            subject = teacher[1 + subject_index * 2]
            hours = int(teacher[2 + subject_index * 2])
            time_slot = random.choice(time_slots)
            working_day = random.choice(working_days)
            if subject in subject_teacher_map[section]:
                teacher = next((t for t in teachers if t[0] == subject_teacher_map[section][subject]), None)
            else:
                subject_teacher_map[section][subject] = teacher[0]
            if self.teacher_slot_classes[(teacher[0], time_slot)] < int(teacher[-2]) and self.subject_section_classes[(subject, time_slot, working_day)] == 0 and self.subject_hours[(subject, section)] < hours:
                return (teacher[0], subject, time_slot, working_day, section)

    def mutate(self, individual):
        index1 = random.randrange(len(individual))
        index2 = random.randrange(len(individual))
        individual[index1], individual[index2] = individual[index2], individual[index1]

    def repair_over_teaching(self, individual, sections, teachers, time_slots, working_days, subject_teacher_map):
        subject_hours_taught = defaultdict(lambda: defaultdict(int))
        for class_info in individual:
            teacher, subject, slot, day, section = class_info
            subject_hours_taught[section][subject] += 1
        for section in sections:
            for teacher in teachers:
                for i in range(1, len(teacher)-2, 2):
                    subject = teacher[i]
                    required_hours = int(teacher[i+1])
                    taught_hours = subject_hours_taught[section][subject]
                    if taught_hours > required_hours:
                        for j in range(1, len(teacher)-2, 2):
                            replacement_subject = teacher[j]
                            required_replacement_hours = int(teacher[j+1])
                            taught_replacement_hours = subject_hours_taught[section][replacement_subject]
                            if taught_replacement_hours < required_replacement_hours:
                                for k, class_info in enumerate(individual):
                                    t, s, slot, day, sec = class_info
                                    if s == subject and sec == section:
                                        individual[k] = (t, replacement_subject, slot, day, sec)
                                        taught_hours -= 1
                                        taught_replacement_hours += 1
                                        if taught_hours == required_hours:
                                            break
                                if taught_hours == required_hours:
                                    break

    def repair(self, individual, sections, teachers, time_slots, working_days, subject_teacher_map):
        timetable_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        for class_info in individual:
            teacher, subject, slot, day, section = class_info
            timetable_dict[section][day][slot] = f"{subject} ({teacher})"
        for section in sections:
            for day in working_days:
                for slot in time_slots:
                    if timetable_dict[section][day][slot] == "":
                        individual.append(self.generate_class(sections, teachers, time_slots, working_days, subject_teacher_map))
        self.repair_over_teaching(individual, sections, teachers, time_slots, working_days, subject_teacher_map)

    def runGeneticAlgorithm(self, sections, teachers, timeSlots, workingDays, lunchBreaks, classDuration):
        subject_teacher_map = defaultdict(dict)
       

        def fitness(individual, lunchBreaks, teachers):
            penalty = 0
            teacher_classes = defaultdict(int)
            subject_hours_taught = defaultdict(lambda: defaultdict(int))
            for class_info in individual:
                teacher, subject, slot, day, section = class_info
                teacher_classes[teacher] += 1
                subject_hours_taught[section][subject] += 1
            for teacher in teachers:
                if teacher_classes[teacher[0]] > int(teacher[-2]):
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
            teacher_consecutive_hours = defaultdict(lambda: defaultdict(int))
            for class_info in individual:
                teacher_name, subject, slot, day, section = class_info
                teacher_data = next((t for t in teachers if t[0] == teacher_name), None)
                if not teacher_data:
                    continue
                try:
                    current_slot_index = timeSlots.index(slot)
                    next_slot = timeSlots[current_slot_index + 1] if current_slot_index + 1 < len(timeSlots) else None
                except ValueError:
                    next_slot = None
                if next_slot and (teacher_name, subject, next_slot, day, section) in individual:
                    teacher_consecutive_hours[teacher_name][day] += 1
                else:
                    teacher_consecutive_hours[teacher_name][day] = 0
                max_consecutive = int(teacher_data[-2])
                if teacher_consecutive_hours[teacher_name][day] > max_consecutive:
                    penalty += 100
            subject_teacher_map = defaultdict(dict)
            for class_info in individual:
                teacher, subject, slot, day, section = class_info
                if subject in subject_teacher_map[(section)]:
                    if subject_teacher_map[(section)][subject] != teacher:
                        penalty += 100
                else:
                    subject_teacher_map[(section)][subject] = teacher
            
            return penalty,

        creator.create("FitnessMin", base.Fitness, weights=(-0.125,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        toolbox = base.Toolbox()
        toolbox.register("attr_class", self.generate_class, sections=sections, teachers=teachers, time_slots=timeSlots, working_days=workingDays, subject_teacher_map=subject_teacher_map)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_class, n=len(timeSlots)*len(workingDays)*len(sections))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", fitness, lunchBreaks=lunchBreaks, teachers=teachers)
        toolbox.register("mate", tools.cxUniform, indpb=0.25)
        toolbox.register("mutate", self.mutate)
        toolbox.register("select", tools.selTournament, tournsize=3)
        pop = toolbox.population(n=200)
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
            self.repair(ind, sections, teachers, timeSlots, workingDays, subject_teacher_map)
        start_time = time.time()
        fitness_scores = []
        diversity_scores = []
        mutation_rate = 0.01
        crossover_rate = 0.9
        for g in range(200):
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
                    self.repair(child1, sections, teachers, timeSlots, workingDays, subject_teacher_map)
                    self.repair(child2, sections, teachers, timeSlots, workingDays, subject_teacher_map)
            for mutant in offspring:
                if random.random() < mutation_rate:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
                    self.repair(mutant, sections, teachers, timeSlots, workingDays, subject_teacher_map)
            fitnesses = list(map(toolbox.evaluate, offspring))
            for ind, fit in zip(offspring, fitnesses):
                ind.fitness.values = fit
                self.repair(ind, sections, teachers, timeSlots, workingDays, subject_teacher_map)
            pop[:] = offspring
            fits = [ind.fitness.values[0] for ind in pop]
            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5
            if std == 0:
                break
        end_time = time.time()
        best_individual = tools.selBest(pop, 1)[0]
        self.updateTimetable(best_individual, sections, teachers, timeSlots, workingDays, lunchBreaks, classDuration)
        print(f"Execution Time: {end_time - start_time:.2f}s")

    def updateTimetable(self, individual, sections, teachers, timeSlots, workingDays, lunchBreaks, classDuration):
        timetable_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        for class_info in individual:
            teacher, subject, slot, day, section = class_info
            timetable_dict[section][day][slot] = f"{subject} ({teacher})"
        for section in sections:
            self.timetableWindow.updateTable(section, workingDays, timeSlots, timetable_dict[section])