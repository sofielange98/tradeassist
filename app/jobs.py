from app.modules.DailyCheck import DailyCheck

def job1():
    print("Checking")
    checker = DailyCheck()
    checker.execute()