import math
from functools import reduce
import random
import matplotlib.pyplot as plt



class Job:
    def __init__(self, id, period,executionTime):
        self.id =  id
        self.period = period
        self.executionTime = executionTime
        self.remaningTime = self.executionTime
    def setStartTime(self,time=0):
        self.startTime = time 
        self.deadline = self.startTime+self.period
    def setSlackTime(self,CurrentTime):
        self.slackTime = self.deadline-CurrentTime-self.remaningTime

def getJobList():
    print("Give Number Of Jobs!")
    numberOfJobs =  int(input())
    hash_mapJobs = {}
    if not type(numberOfJobs) is int:
        raise TypeError("Only integers are allowed") 

    for i in range(numberOfJobs):
        increment = i+1
        print("Give the execution time of job:",increment)
        execTime = int(input())
        if not type(execTime) is int:
            raise TypeError("Only integers are allowed")
        print("Give the period time of job:",increment)
        period = int(input())
        if not type(period) is int:
            raise TypeError("Only integers are allowed")
        job = Job(increment,period,execTime)
        hash_mapJobs[increment] = job     
    return hash_mapJobs


def isScheduleableEDF(joblist):
    total=0
    for Job in joblist.values():
        total+=float(Job.executionTime/Job.period)
        
        
    if(total<=1):
            print("EDF works!")
            return True
    else:
            print("Cannot schedule with EDF")
            return False
def createGanthChart(ganttData,algo):
    # Generate unique colors for each job
    unique_jobs = set(entry[0] for entry in ganttData if entry[0] != "Idle")
    color_map = {job_id: (random.random(), random.random(), random.random()) for job_id in unique_jobs}
    color_map["Idle"] = (0.8, 0.8, 0.8)  # Gray color for Idle periods

    fig, ax = plt.subplots(figsize=(15, 2))  # Horizontal layout

    # Place jobs side by side (all on the same row)
    for entry in ganttData:
        if len(entry) == 3:  # Proper entry with start and end
            job_id, start, end = entry
        elif len(entry) == 2:  # Entry missing `end` time
            job_id, start = entry
            # Determine the next available "end" time from ganttData or assume 1 unit duration
            index = ganttData.index(entry)
            if index < len(ganttData) - 1:
                next_start = ganttData[index + 1][1]  # Start of the next entry
                end = next_start
            else:
                end = start + 1  # Default to 1 unit if this is the last entry

        color = color_map[job_id]
        ax.broken_barh([(start, end - start)], (0.2, 0.6), facecolors=color)  # Single row
        ax.text((start + end) / 2, 0.5, f"{job_id}", color="white", weight="bold", ha="center", va="center")

    # Set x-axis ticks
    max_time = max(end for entry in ganttData for end in (entry[2:] or [entry[1] + 1]))
    ax.set_xticks(range(0, max_time + 1, 1))  # Ticks every 1 unit
    ax.set_xticklabels([str(x) if x % 5 == 0 else "" for x in range(0, max_time + 1)])  # Label every 5th tick
    ax.set_yticks([])  # No vertical ticks
    ax.set_ylim(0, 1)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart of Job Execution:"+algo)
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def lcm_multiple(numbers):
    return reduce(lambda x, y: abs(x * y) // math.gcd(x, y), numbers)


def EDF_simulation(Jobs):
    lcm = []
    readyQueue = []
    ganttData = []
    for Job in Jobs.values():
        lcm.append(Job.period)

    
    simulationTime = lcm_multiple(lcm)

    for time in range(simulationTime):
        jobCameFlag = False
        for job in Jobs.values():
            if time % job.period == 0:  # Job arrives
                print(f"Job {job.id} arrives at time {time}")
                job.setStartTime(time)
                job.remainingTime = job.executionTime
                readyQueue.append(job)
                jobCameFlag =True
        if jobCameFlag:
            readyQueue.sort(key=lambda x: x.deadline)
        if readyQueue:
            currentJob = readyQueue[0]
            if not ganttData or ganttData[-1][0] != currentJob.id:
                ganttData.append((currentJob.id, time))  # Start a new segment
            currentJob.remainingTime -= 1
            if currentJob.remainingTime == 0:
                ganttData[-1] = (currentJob.id, ganttData[-1][1], time + 1)
                print(f"Job {currentJob.id} completes at time {time+1}")
                readyQueue.pop(0)
        else:
            print(f"At time {time}, CPU is idle")
            if not ganttData or ganttData[-1][0] != "Idle":
                ganttData.append(("Idle", time))  # Start a new idle segment
                ganttData[-1] = ("Idle", ganttData[-1][1], time + 1)  # Extend idle segment
    print("\nSimulation complete! Plotting Gantt Chart...")
    createGanthChart(ganttData,"EDF")

def LLF_simulation(Jobs):
    lcm = []
    readyQueue = []
    ganttData = []
    for Job in Jobs.values():
        lcm.append(Job.period)
    simulationTime = lcm_multiple(lcm)
    for time in range(simulationTime):
        for job in Jobs.values():
            if time % job.period == 0:  # Job arrives
                print(f"Job {job.id} arrives at time {time}")
                job.setStartTime(time)
                job.remainingTime = job.executionTime
                readyQueue.append(job)
        for queuedJob in readyQueue:
            queuedJob.setSlackTime(time)
        readyQueue.sort(key=lambda x: x.slackTime)
        if readyQueue:
            currentJob = readyQueue[0]
            if not ganttData or ganttData[-1][0] != currentJob.id:
                ganttData.append((currentJob.id, time))  # Start a new segment
            currentJob.remainingTime -= 1
            if currentJob.remainingTime == 0:
                ganttData[-1] = (currentJob.id, ganttData[-1][1], time + 1)
                print(f"Job {currentJob.id} completes at time {time+1}")
                readyQueue.pop(0)
        else:
            print(f"At time {time}, CPU is idle")
            if not ganttData or ganttData[-1][0] != "Idle":
                ganttData.append(("Idle", time))  # Start a new idle segment
                ganttData[-1] = ("Idle", ganttData[-1][1], time + 1)
    print("\nSimulation complete! Plotting Gantt Chart...")
    createGanthChart(ganttData,"LLF")



def main():
    Joblist = getJobList()

    if(isScheduleableEDF(Joblist)):
        EDF_simulation(Joblist)
        LLF_simulation(Joblist)

if __name__=="__main__":
    main()