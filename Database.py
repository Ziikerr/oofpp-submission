import sqlite3, datetime

def adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()

def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()

sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)

def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())

def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(val.decode())

sqlite3.register_converter("date", convert_date)
sqlite3.register_converter("datetime", convert_datetime)

def connectDB(name:str):
    db = sqlite3.connect(name+".db")
    return db

def createTables(db:sqlite3.Connection):
    cursor = db.cursor()
    req = """CREATE TABLE IF NOT EXISTS habits (id TEXT, name VARCHAR(200), frequency INT, 
    creationDate DATE, isCompleted BOOLEAN, lastCompleted DATETIME, currentStreak INT, maxStreak INT, PRIMARY KEY("id"))"""
    cursor.execute(req)
    req = """CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY,name VARCHAR(200),
    isCompleted BOOLEAN,lastCompleted DATETIME,habit TEXT, FOREIGN KEY("habit") REFERENCES habits("id"));"""
    cursor.execute(req)
    db.commit()
    cursor.close()

def populateTables(db:sqlite3.Connection):
    """Populates database tables with test entries

    Args:
        db (sqlite3.Connection): Database connection to use
    """
    
    def addTasks(dateVar,taskNames,habitName,completionStatus,timeDelta,cursor):
        reqTask = "INSERT INTO tasks (id, name, isCompleted, lastCompleted, habit) VALUES (?, ?, ?, ?, ?);"
        for name in taskNames:
            if timeDelta >0:
                valuesTask = [name+"--"+habitName,name,completionStatus,dateVar-datetime.timedelta(seconds=timeDelta*60), habitName]
                timeDelta +=5
            elif timeDelta == 0:
                valuesTask = [name+"--"+habitName,name,completionStatus,dateVar, habitName]
            else:
                valuesTask = [name+"--"+habitName,name,completionStatus,datetime.datetime(1,1,1,1,1,1), habitName]
            cursor.execute(reqTask,valuesTask)
    
    cursor = db.cursor()
    req = "INSERT INTO habits (id, name, frequency, creationDate, isCompleted, lastCompleted, currentStreak, maxStreak) VALUES (?, ?, ?, ?, ?, ?, ?,?);"
    
    #1st Habit| Clean room | weekly | Clean table | Clean floor | Clean dust | 4 weeks ago
    dateVar = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(seconds=120)
    values = ["Clean room","Clean room", 1, datetime.date.today()-datetime.timedelta(days=28), True, dateVar,1,2]
    cursor.execute(req,values)
    addTasks(dateVar,["Clean desk","Clean floor","Clean dust"],"Clean room",True,15,cursor)
    #2nd Habit| Take pills | daily | Morning | Evening | Today
    dateVar = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(seconds=30*60)
    values = ["Take medicine","Take medicine", 0, datetime.date.today(), False, datetime.datetime(1,1,1,1,1,1),0,0]
    cursor.execute(req,values)
    addTasks(dateVar,["Morning","Evening"],"Take medicine",False,-1,cursor)
    #3rd Habit| Excercise | daily | Stretches | Sit-ups | 3 weeks ago
    dateVar = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(seconds=10*60)
    values = ["Excercise","Excercise", 0, datetime.date.today()-datetime.timedelta(days=21), True, dateVar,5,12]
    cursor.execute(req,values)
    addTasks(dateVar,["Stretches","Sit-ups"],"Excercise",True,15,cursor)
    #4th Habit| Learn language | daily | Learn words | Excercises | 2 weeks ago
    dateVar = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(seconds=300*60)
    values = ["Learn language","Learn language", 0, datetime.date.today()-datetime.timedelta(days=14), True, dateVar,1,12]
    cursor.execute(req,values)
    addTasks(dateVar,["Learn words"],"Learn language",True,1,cursor)
    #5th Habit| Chess | daily | Play games | Learn openings | 1 week ago
    dateVar = datetime.datetime.now().replace(microsecond=0)
    values = ["Chess","Chess", 0, datetime.date.today()-datetime.timedelta(days=7), True, dateVar,3,3]
    cursor.execute(req,values)
    addTasks(dateVar,["Learn openings","Play games"],"Chess",True,0,cursor)
    
    db.commit()
    cursor.close()

def destroyDB(db:sqlite3.Connection):
    cursor = db.cursor()
    req ="DROP TABLE tasks"
    cursor.execute(req)
    req ="DROP TABLE habits"
    cursor.execute(req)
    db.commit()
    cursor.close()

def requestDB(query:str,db:sqlite3.Connection, values:list= None):
    """Sends a query to the database

    Args:
        query (str): Query to be sent
        db (sqlite3.Connection): Database to use
        values (list, optional): Used if values are needed for the query. Defaults to None.

    Returns:
        list: Database response
    """
    cursor = db.cursor()
    if values != None:
        cursor.execute(query,values)
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data