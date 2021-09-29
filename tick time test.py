import datetime

ticks = 1530488
seconds = ticks/100
print(datetime.timedelta(seconds=seconds.__round__()))


# ## sys tick to time ###
# uptime = get('192.168.1.1', ['1.3.6.1.2.1.1.3.0'], hlapi.CommunityData('private_cisco'))
# seconds = uptime["1.3.6.1.2.1.1.3.0"]/100
# print("time :", datetime.timedelta(seconds=seconds.__round__()), "timer")
# #######################
