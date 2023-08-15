import math
from datetime import datetime
current = int("1691695968")
starttime = int("1691692200")

#dtcurrent = datetime.utcfromtimestamp(current)
#dtstart = datetime.utcfromtimestamp(starttime)

time_difference = current - starttime
dtcurrent = datetime.utcfromtimestamp(current)
dtstart = datetime.utcfromtimestamp(starttime)
minutes_difference = time_difference.total_seconds() / 60.0
minutes = math.ceil(minutes_difference)
print("Difference in minutes:", minutes)