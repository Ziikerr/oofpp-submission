import datetime
from Habit import Habit, Task
from Analytics import showHabits
import sqlite3

def addTask(habit:Habit,db:sqlite3.Connection):
    """Used to provide interface for adding a task(s) to a habit

    Args:
        habit (Habit): Habit to which task(s) will be added to
    """
    typoCheck = False
    while typoCheck == False:
        taskName = input("Enter task name: ")
        if taskName == "":
            print("Empty value entered\n")
        else:
            if habit.createTask(Task(taskName+"--"+habit.name,taskName),db) == False:
                print("Task with that name already exists\n")
            else:
                print("Task added\n")
                typoCheck = True

def createHabit(db:sqlite3.Connection, habitList:list[Habit]):
    """Creates a habit and prompts an option to add tasks

    Args:
        db (sqlite3.Connection): Database connection to use
        habitList (list[Habit]): List of habits to use
    """
    cursor = db.cursor()
    
    typoCheck = False
    while typoCheck == False:
        name = input("Enter habit name: ")
        dbReq = "SELECT name FROM habits WHERE name =? "
        cursor.execute(dbReq,(name,))
        data = cursor.fetchone()
        if data != None:
                    print("Habit with that name already exists")
                    continue
        if name == "":
                print("Empty value entered")
        else:
            typoCheck = True
    typoCheck = False
    while typoCheck == False:
        frequency = input("Enter habit frequency (daily/weekly): ")
        if frequency.lower() == "daily":
            freq = 0
            typoCheck = True
        elif frequency.lower() == "weekly":
            freq = 1
            typoCheck = True
        else:
            print("Invalid value entered")
    typoCheck = False
    habit = Habit(name,name,freq)
    habitList.append(habit)
    req = "INSERT INTO habits (id, name, frequency, creationDate, isCompleted, lastCompleted, currentStreak, maxStreak) VALUES (?, ?, ?, ?, ?, ?, ?,?);"
    values = (habit.ID,habit.name,habit.frequency,habit.creationDate,habit.isCompleted,habit.lastCompleted,habit.currentStreak,habit.maxStreak)
    cursor.execute(req,values)
    db.commit()
    print("Habit created\n")
    
    #Add a task to habit
    taskCheck = False
    habitCount = 0
    while taskCheck == False:
        if habitCount == 0:
            print("Add a task to the habit")
            addTask(habit,db)
            habitCount +=1
        else:
            addTaskInput = input("Would you like to add another task to the habit? (Yes/No) ")
            if addTaskInput.lower() == "yes":
                addTask(habit,db)
            elif addTaskInput.lower() == "no":
                taskCheck = True
            else:
                print("Incorrect value entered")
    cursor.close()
    

def editHabit(db, habitList:list[Habit]):
    """Allows to edit a habit via commands

    Args:
        db (sqlite3.Connection): Database connection to use
        habitList (list[Habit]): List of habits to use
    """
    
    def habitInfo(habit: Habit):
        """Displays info about the habit

        Args:
            habit (Habit): habit to display info about
        """
        print("\nHabit: "+habit.name)
        print("Creation date: "+str(habit.creationDate))
        if habit.maxStreak == 0:
            print("Has never been completed")
        else:
            if habit.isCompleted == True:
                print("Completion status: Completed")
            else:
                print("Completion status: Not completed")
            print("Completed at: "+str(habit.lastCompleted))
            print("Current streak: "+str(habit.currentStreak))
        if habit.frequency == 1:
            print("Frequency: Weekly\n")
        else:
            print("Frequency: Daily\n")
    
    def deleteHabit(habit:Habit, habitList: list[Habit], db:sqlite3.Connection):
        """Removes a habit and its tasks from the database and habitList

        Args:
            habit (Habit): Habit to be deleted
            db (sqlite3.Connection): Database connection to use
        """
        
        cursor = db.cursor()
        for task in habit.taskList:
            habit.deleteTask(task,db)
        cursor.execute("DELETE FROM habits WHERE id =?",(habit.ID,))
        habitList.remove(habit)
        db.commit()
    
    def changeName(habit:Habit,db:sqlite3.Connection):
        """Changes the name of a habit

        Args:
            habit (Habit): Habit which name will be changed
            db (sqlite3.Connection): Database connection to use
        """
        cursor = db.cursor()
        nameTaken = False
        while nameTaken == False:
            newName = input("Enter new habit name: ")
            cursor.execute("SELECT name FROM habits")
            data = cursor.fetchall()
            for name in data:
                if name[0] != newName: 
                    nameTaken = False
            if nameTaken == True:
                print("Habit with that name already exists")
            else:
                cursor.execute("UPDATE habits SET name = ? WHERE name =?",(newName,habit.name))
                db.commit()
                habit.name = newName
                nameTaken = True
                print("Habit name changed")
    
    def changeFreq(habit:Habit,db:sqlite3.Connection):
        """Changes the frequency of a habit

        Args:
            habit (Habit): Habit which frequency will be changed
            db (sqlite3.Connection): Database connection to use
        """
        cursor = db.cursor()
        if habit.frequency == 0:
            habit.frequency = 1
            cursor.execute("UPDATE habits SET frequency = 1 WHERE name =?",(habit.name,))
            db.commit()
            print("Frequency changed to weekly")
        else:
            habit.frequency = 0
            cursor.execute("UPDATE habits SET frequency = 0 WHERE name =?",(habit.name,))
            db.commit()
            print("Frequency changed to daily")
        cursor.close()
    
    name = input("Enter the name of a habit: ")
    selectedHabit = None
    
    for habit in habitList:
        if habit.name.lower() == name.lower():
            selectedHabit = habit
    if selectedHabit == None: return print("Habit does not exist")
    
    habitInfo(selectedHabit)
    
    typoCheck = False
    while typoCheck == False:
        typoCheck = True
        print("To edit the name enter \"name\"")
        print("To edit a frequency \"freq\"")
        print("To complete a task enter \"complete\"")
        print("To add a task enter \"add\"")
        print("To remove a task enter \"remove\"")
        print("To delete this habit enter \"delete\"")
        print("To go back enter \"back\"")
        
        command = input("\nWaiting for input: ")
        match command:
            case "complete":
                for task in selectedHabit.taskList:
                    selectedHabit.checkTask(task)
                taskExists = False
                while taskExists == False:
                    taskName = input("\nEnter the name of a task: ")
                    for task in selectedHabit.taskList:
                        if task.name.lower() == taskName.lower():
                            taskExists = True
                            if task.isCompleted == False:
                                selectedHabit.completeTask(task,db)
                                print("Task completed")
                    if taskExists == False: 
                        print("Task with that name doesnt exist")         
            case "name":
                changeName(selectedHabit,db)
            case "freq":
                changeFreq(selectedHabit,db)
            case "add":
                addTask(selectedHabit,db)
            case "remove":
                    taskName = input("Enter task name: ")
                    if taskName == "":
                        print("Empty value entered\n")
                    else:
                        for task in selectedHabit.taskList:
                            if task.name.lower() == taskName.lower():
                                selectedHabit.deleteTask(task,db)
            case "delete":
                deleteHabit(selectedHabit,habitList,db)
            case "back": pass
            case _:
                print("Invalid command entered\n")
                typoCheck = False       
    

def retrieveHabits(db:sqlite3.Connection, habitList:list[Habit]):
    """Populates habitList using data from the database and updates habit completion status based on date

    Args:
        db (sqlite3.Connection): Database connection to use
        habitList (list[Habit]): list of habits
    """
        
    cursor = db.cursor()
    for name in showHabits(-1,db):
        cursor.execute("SELECT * FROM habits WHERE name =?",(name,))
        data = cursor.fetchall()
        for habitData in data:
            habit = Habit(habitData[0],habitData[1],habitData[2])
            habit.creationDate = habitData[3]
            habit.isCompleted = habitData[4]
            habit.lastCompleted = habitData[5]
            habit.currentStreak = habitData[6]
            habit.maxStreak = habitData[7]
            cursor.execute("SELECT * FROM tasks WHERE habit =?",(habit.ID,))
            tData = cursor.fetchall()
            for taskData in tData:
                task = Task(taskData[0],taskData[1])
                task.isCompleted = taskData[2]
                task.lastCompleted = taskData[3]
                lastCompleted = datetime.datetime.strptime(task.lastCompleted, "%Y-%m-%dT%H:%M:%S")
                task.lastCompleted = lastCompleted
                habit.taskList.append(task)
            habitList.append(habit)
            lastCompleted = datetime.datetime.strptime(habit.lastCompleted, "%Y-%m-%dT%H:%M:%S")
            habit.lastCompleted = lastCompleted
            match habit.frequency:
                case 0: 
                    if lastCompleted.date() < datetime.date.today():
                        habit.setCompleted(False,db)
                        if lastCompleted.date() + datetime.timedelta(days=1) < datetime.date.today():
                            habit.streakBreak(db)   
                case 1: 
                    if lastCompleted.date()+datetime.timedelta(days=7) <= datetime.date.today():
                        habit.setCompleted(False,db)
                        if lastCompleted.date() + datetime.timedelta(days=14) < datetime.date.today():
                            habit.streakBreak(db)
    cursor.close()

