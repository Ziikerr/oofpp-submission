from datetime import date,datetime
import sqlite3

class Task:

    def __init__(self, ID:str, name:str):
        self.ID = ID
        self.name = name
        self.isCompleted = False
        self.lastCompleted = datetime(1,1,1,1,1,1)
    
    def setCompleted(self, value:bool,db:sqlite3.Connection):
        """Changes the status of a task based on a value

        Args:
            value (bool): New completion status value
            db (sqlite3.Connection): Database connection to use
        """
        cursor = db.cursor()
        if value:
            self.lastCompleted = datetime.now().replace(microsecond=0)
            cursor.execute("UPDATE tasks SET lastCompleted = ? WHERE ID =?",(self.lastCompleted,self.ID))
        self.isCompleted = value
        cursor.execute("UPDATE tasks SET isCompleted = ? WHERE ID =?",(self.isCompleted,self.ID))
        db.commit()
        cursor.close()
        

class Habit:
    
    def __init__(self, ID:str, name:str, frequency:int):
        self.ID = ID
        self.name = name
        self.frequency = frequency
        self.creationDate = date.today()
        self.isCompleted = False
        self.lastCompleted = datetime(1,1,1,1,1,1)
        self.taskList: list[Task] = []
        self.currentStreak: int = 0
        self.maxStreak: int = 0
        
    
    def createTask(self, task:Task,db:sqlite3.Connection):
        """Creates a task.

        Args:
            task (Task): Task to be created
            db (sqlite3.Connection): Database connection to use

        Returns:
            bool: False if tasks already exists. True if successful

        """
        cursor = db.cursor()
        
        for exTask in self.taskList:
            if exTask.name == task.name:
                return False
        
        self.taskList.append(task)
        req = "INSERT INTO tasks (id, name, isCompleted, lastCompleted, habit) VALUES (?, ?, ?, ?, ?);"
        values = (task.ID,task.name,task.isCompleted,task.lastCompleted,self.ID)
        cursor.execute(req,values)
        db.commit()
        cursor.close()
        
        return True
    
    def checkTask(self, task:Task):
        """Checks completion status of a task

        Args:
            task (Task): Task to check
        """
        if task.isCompleted == True:
            print("\nTask: "+task.name+"\nCompletion status: Completed")
        else:
            print("\nTask: "+task.name+"\nCompletion status: Not completed")
        if task.lastCompleted == datetime(1,1,1,1,1,1):
            print("Has never been completed")
        else:
            print("Last completed: " + str(task.lastCompleted))
    
    def completeTask(self, task:Task,db:sqlite3.Connection):
        """Sets a task's status to complete and checks if all tasks are completed to update own completion status

        Args:
            task (Task): Task to be completed
            db (sqlite3.Connection): Database connection to use
        """
        task.setCompleted(True,db)
        #check if all tasks have been completed
        completionStatus = True
        for i in self.taskList:
            if i.isCompleted == False:
                completionStatus = False
        if completionStatus == True: 
            self.setCompleted(True,db)
    
    def deleteTask(self, task: Task,db:sqlite3.Connection):
        """Removes a task from a taskList and database

        Args:
            task (Task): Task to be removed
            db (sqlite3.Connection): Database connection to use
        """
        
        cursor = db.cursor()

        cursor.execute("DELETE FROM tasks WHERE habit =?",(self.ID,))
        db.commit()
        self.taskList.remove(task)
    
    def setCompleted(self, value:bool,db:sqlite3.Connection):
        """Changes the status of a habit based on a value

        Args:
            value (bool): New completion status value
            db (sqlite3.Connection): Database connection to use
        """
        
        cursor = db.cursor()
        if value == False:
            for i in self.taskList:
                i.setCompleted(False,db)
        else:
            self.lastCompleted = datetime.now().replace(microsecond=0)
            cursor.execute("UPDATE habits SET lastCompleted = ? WHERE ID =?",(self.lastCompleted,self.ID))
            db.commit()
            self.streakAdd(db)
        self.isCompleted = value
        cursor.execute("UPDATE habits SET isCompleted = ? WHERE ID =?",(self.isCompleted,self.ID))
        db.commit()
        cursor.close()
        
        
    def streakAdd(self,db:sqlite3.Connection):
        """Increments current streak and updates max streak if neccessary

        Args:
            db (sqlite3.Connection): Database connection to use
        """
        
        cursor = db.cursor()
        self.currentStreak += 1
        if self.currentStreak > self.maxStreak:
            self.maxStreak = self.currentStreak
        req = "UPDATE habits SET currentStreak = ?, maxStreak = ?  WHERE ID =?"
        cursor.execute(req,(self.currentStreak,self.maxStreak, self.ID))
        db.commit()
        cursor.close()
        
    def streakBreak(self,db:sqlite3.Connection):
        """Sets current streak to 0

        Args:
            db (sqlite3.Connection): Database connection to use
        """
        
        cursor = db.cursor()
        self.currentStreak = 0
        cursor.execute("UPDATE habits SET currentStreak = 0 WHERE ID =?",(self.ID,))
        db.commit()
        cursor.close()