from Additional import retrieveHabits, createHabit, editHabit
from Analytics import showHabits, longestStreak
import Database
from Habit import Habit

habitList: list[Habit]=[]
connection = Database.connectDB("HabitApp")

def main():
    Database.createTables(connection)
    
    retrieveHabits(connection,habitList)
    whileCheck = True
    while whileCheck == True:
        print("To create a habit enter \"create\"")
        print("To edit a habit enter \"edit\"")
        print("To display habits enter \"display\"")
        print("To display longest streak enter \"streak\"")
        print("To close the app enter \"exit\"\n")
        command = input("Waiting for input: ")
        match command.lower():
            case "create": 
                createHabit(connection,habitList)
            case "edit": 
                editHabit(connection,habitList)
            case "display": 
                frequency = input("Enter habit frequency(daily/weekly/any): ")
                match frequency.lower():
                    case "daily": print("List of daily habits: "+str(showHabits(0,connection)))
                    case "weekly": print("List of weekly habits: "+str(showHabits(1,connection)))
                    case "any": print("List of all habits: "+str(showHabits(-1,connection)))
                    case _: print("Incorrect value entered")
            case "streak": 
                print("Enter the name of the habit to see its longest streak. Enter \"all\" to see the overall longest streak")
                value = input("Waiting for input: ")
                print("Longest streak: "+longestStreak(value,connection))
            case "exit": whileCheck = False
            case _: print("Incorrect command entered")
        print()

main()