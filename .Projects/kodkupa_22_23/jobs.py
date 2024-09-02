"""
job_num, time = input().split()
job_num, time = int(job_num), int(time)
job_times = list(map(int, input().split()))
job_rewards = list(map(int, input().split()))

rates_dict = {}
for j in range(job_num):
    rates_dict[str(j)] = job_rewards[j]/job_times[j]
rates_dict = dict(sorted(rates_dict.items(), reverse=True))
print(rates_dict)
money = 0
while len(rates_dict) > 0 :
    priority = int(list(rates_dict.keys())[0])
    if job_times[priority] <= time :
        print(job_times[priority], job_rewards[priority])
        money += job_rewards[priority]
        time -= job_times[priority]
    else:
        del rates_dict[str(priority)]
print(money)
"""

job_num, time = input().split()
job_num, time = int(job_num), int(time)
job_times = list(map(int, input().split()))
job_rewards = list(map(int, input().split()))
rates_dict = {}

for j in range(job_num):
    rates_dict[str(j)] = job_rewards[j]*(time-job_times[j])
rates_dict = dict(sorted(rates_dict.items(), reverse=True))
#print(rates_dict)

money = 0
while len(rates_dict) > 0 :
    priority = int(list(rates_dict.keys())[0])
    for j in range(len(rates_dict)):
        rates_dict[str(j)] = job_rewards[j]*(time-job_times[j])
    rates_dict = dict(sorted(rates_dict.items(), reverse=True))
    if job_times[priority] <= time :
        #print(job_times[priority], job_rewards[priority])
        money += job_rewards[priority]
        time -= job_times[priority]
    else:
        del rates_dict[str(priority)]
print(money)