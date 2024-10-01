from functools import partial
from Database import requestDB
import sqlite3

def dataMap(data:list, value:int):
    """Used to map data

    Args:
        data (list): List of data
        value (int): index
    """
    return(data[value])

def returnHabits(freq:int,db:sqlite3.Connection):
    """Returns habits based on frequency

    Args:
        freq (int): Frequency of a habit
        db (sqlite3.Connection): Database connection to use

    Returns:
        list: list of habit names
    """
    return list(map(partial(dataMap,value =1),requestDB("SELECT * FROM habits WHERE frequency = ?",db,(freq,))))

def showHabits(frequency:int,db:sqlite3.Connection):
    """Calls functions to return habits based of frequency

    Args:
        frequency (int): Frequency of a habit
        db (sqlite3.Connection): Database connection to use
    """
    return(returnHabits(0,db)+returnHabits(1,db) if frequency == -1 else
        returnHabits(frequency,db) )
    
def returnStreak(data:list):
    """Returns list of longest streaks for further processing

    Args:
        data (list): Response from db

    Returns:
        list: Returns list of longest streaks
    """
    return list(map(partial(dataMap,value =0),data))
    
def streakAll(db:sqlite3.Connection):
    """Returns the longest streak out of all habits

    Args:
        db (sqlite3.Connection): Database connection to use

    Returns:
        str: Longest streak
    """
    return str(max(returnStreak(requestDB("SELECT maxStreak FROM habits",db)), default="None"))

def streakHabit(value:str,db:sqlite3.Connection):
    """Returns the longest streak for a specific habit

    Args:
        value (str): name of the habit
        db (sqlite3.Connection): Database connection to use

    Returns:
        str: Longest streak
    """
    return str(max(requestDB("SELECT maxStreak FROM habits WHERE name=?",db,(value,)),default=["None",])[0])

def longestStreak(value:str,db:sqlite3.Connection):
    """Evaluates the value and returns the corresponding function

    Args:
        value (str): Value entered by user
        db (sqlite3.Connection): Database connection to use

    Returns:
        function: Calls a function
    """

    return (streakAll(db) if value == "all" else
            streakHabit(value,db)
            )
    