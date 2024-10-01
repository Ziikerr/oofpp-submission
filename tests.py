import Habit, Analytics, pytest, Database, Additional

class Test:
    
    def setup_method(self):
        self.db = Database.connectDB("testDB")
        self.habitList = []
        Database.createTables(self.db)
        Database.populateTables(self.db)
        Additional.retrieveHabits(self.db,self.habitList)
        
    @pytest.mark.parametrize('value', [True,False])
    def testTask_setCompleted(self,value):
        testTask = Habit.Task("testID","testName")
        testTask.setCompleted(value,self.db)

    def testHabit_createTaskTrue(self):
        testTask = Habit.Task("testID","testName")
        testHabit = Habit.Habit("testHabit","testHabit",0)
        assert testHabit.createTask(testTask,self.db) == True
    
    def testHabit_createTaskFalse(self):
        testTask = Habit.Task("testID","testName")
        testHabit = Habit.Habit("testHabit","testHabit",0)
        testHabit.taskList.append(testTask)
        assert testHabit.createTask(testTask,self.db) == False
        
    def testHabit_checkTask(self):
        testTask = Habit.Task("testID","testName")
        testHabit = Habit.Habit("testHabit","testHabit",0)
        testHabit.taskList.append(testTask)
        testHabit.checkTask(testTask)

    def testHabit_completeTask(self):
        testTask = Habit.Task("testID","testName")
        testHabit = Habit.Habit("testHabit","testHabit",0)
        testHabit.taskList.append(testTask)
        testHabit.completeTask(testTask,self.db)

    def testHabit_deleteTask(self):
        testTask = Habit.Task("testID","testName")
        testHabit = Habit.Habit("testHabit","testHabit",0)
        testHabit.taskList.append(testTask)
        testHabit.deleteTask(testTask,self.db)

    @pytest.mark.parametrize('value', [True,False])
    def testHabit_setCompleted(self,value):
        testHabit = Habit.Habit("testHabit","testHabit",0)
        testHabit.setCompleted(value,self.db)

    def testHabit_streakAdd(self):
        testHabit = Habit.Habit("testHabit","testHabit",0)
        testHabit.streakAdd(self.db)

    def testHabit_streakBreak(self):
        testHabit = Habit.Habit("testHabit","testHabit",0)
        testHabit.currentStreak = 2
        testHabit.maxStreak = 2
        testHabit.streakBreak(self.db)
        assert testHabit.currentStreak == 0
        
    def test_dataMap(self):
        dataList = [["list1arg1","list1arg2"],["list2arg1","list2arg2"]]
        assert Analytics.dataMap(dataList,0) == ["list1arg1","list1arg2"]

    @pytest.mark.parametrize('frequency',[0,1])
    def test_returnHabits(self,frequency):
        Analytics.returnHabits(frequency,self.db)

    @pytest.mark.parametrize('frequency',[-1,0,1])
    def test_showHabits(self,frequency):
        Analytics.showHabits(frequency,self.db)

    def test_returnStreak(self):
        testList = [[2,]]
        Analytics.returnStreak(testList) == [2]

    def test_streakAll(self):
        Analytics.streakAll(self.db)
        
    @pytest.mark.parametrize('name',["testHabit","random"])
    def test_streakHabit(self,name):
        Analytics.streakHabit(name,self.db)

    @pytest.mark.parametrize('value',["testHabit","all"])
    def test_longestStreak(self,value):
        Analytics.longestStreak(value,self.db)

    def test_addTask(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda value: "test task")
        Additional.addTask(self.habitList[0],self.db)
    
    def test_createHabit(self, monkeypatch):
        values = iter(["TestHabit","weekly","Test task1","yes","Test task2","no"])
        monkeypatch.setattr('builtins.input', lambda value: next(values))
        Additional.createHabit(self.db,self.habitList)
    
    def test_editHabit_name(self, monkeypatch):
        habit = self.habitList[0]
        values = iter([habit.name,"name","New name"])
        monkeypatch.setattr('builtins.input', lambda value: next(values))
        Additional.editHabit(self.db,self.habitList)
        assert habit.name == "New name"
    
    def test_editHabit_freq(self, monkeypatch):
        habit = self.habitList[0]
        if habit.frequency == 0:
            newFreq = 1
        else: 
            newFreq = 0
        values = iter([habit.name,"freq"])
        monkeypatch.setattr('builtins.input', lambda value: next(values))
        Additional.editHabit(self.db,self.habitList)
        assert habit.frequency == newFreq
    
    def test_editHabit_complete(self, monkeypatch):
        habit = self.habitList[0]
        values = iter([habit.name,"complete",habit.taskList[0].name])
        monkeypatch.setattr('builtins.input', lambda value: next(values))
        Additional.editHabit(self.db,self.habitList)
        assert habit.taskList[0].isCompleted == True
    
    def test_editHabit_add(self, monkeypatch):
        habit = self.habitList[0]
        values = iter([habit.name,"add","task"])
        monkeypatch.setattr('builtins.input', lambda value: next(values))
        Additional.editHabit(self.db,self.habitList)
    
    def test_editHabit_remove(self, monkeypatch):
        habit = self.habitList[0]
        listLength = len(habit.taskList)
        values = iter([habit.name,"remove",habit.taskList[0].name])
        monkeypatch.setattr('builtins.input', lambda value: next(values))
        Additional.editHabit(self.db,self.habitList)
        assert len(habit.taskList) < listLength 

    def test_editHabit_delete(self, monkeypatch):
        habit = self.habitList[0]
        listLength = len(self.habitList)
        values = iter([habit.name,"delete"])
        monkeypatch.setattr('builtins.input', lambda value: next(values))
        Additional.editHabit(self.db,self.habitList)
        assert len(self.habitList) < listLength
    
    def teardown_method(self):
        Database.destroyDB(self.db)
        self.db.close()