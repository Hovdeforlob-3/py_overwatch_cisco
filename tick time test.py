import datetime

ticks = 1351194
seconds = ticks/100
print(datetime.timedelta(seconds=seconds.__round__()))



