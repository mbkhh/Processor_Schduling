import numpy as np
tasksName       = []
tasksPeriod     = []
tasksDeadline   = []
tasksJob        = []

multiTasksName       = []
multiTasksPeriod     = []
multiTasksDeadline   = []
multiTasksJob        = []
numberOfProcessor = 1

aperiodicArrival    = []
aperiodicLenght     = []
aperiodicPeriod = 0
aperiodicbudget = 0

simulationTime = 40

def multiProcessor_edf(examples,numberOfProcessor=1, time_limit = 40):
    T, C, D = np.array(examples[0]), np.array(examples[1]), np.array(examples[2])
    num_tasks = len(T)
    timeline = np.zeros((num_tasks, time_limit), dtype=int)
    job_queue = []
    job_counters = [0] * num_tasks  

    for time in range(time_limit):
        for i in range(num_tasks):
            if time % T[i] == 0:
                deadline = time + D[i]
                job_queue.append([deadline, time, i, C[i], job_counters[i]])
                job_counters[i] += 1
        
        job_queue = [job for job in job_queue if job[3] > 0]
        job_queue.sort()
        processors = [0] * numberOfProcessor

        for job in job_queue:
            deadline, release_time, task_id, remaining_time, job_id = job
            
            for p in range(numberOfProcessor):
                if processors[p] == 0:
                    timeline[task_id][time] = p + 1  
                    job[3] -= 1  
                    processors[p] = 1  
                    break

    return timeline.tolist()
def multiProcessor_pfair(examples,numberOfProcessor=1, time_limit = 40):
    T, C, D = np.array(examples[0]), np.array(examples[1]), np.array(examples[2])
    num_tasks = len(T)
    weights = [C[i] / T[i] for i in range(num_tasks)]
    timeline = np.zeros((num_tasks, time_limit), dtype=int)

    executions = [0] * num_tasks  
    job_queue = [[] for _ in range(num_tasks)]  

    for time in range(time_limit):
        # Release new jobs
        for i in range(num_tasks):
            if time % T[i] == 0:
                job_queue[i].append([time, time + D[i], C[i]])

        lags = []
        for i in range(num_tasks):
            if any(job[2] > 0 for job in job_queue[i]):
                lag = time * weights[i] - executions[i]
                if lag > 0:
                    lags.append((lag, i))

        lags.sort(reverse=True)

        busy_processors = 0
        for lag, task_id in lags:
            if busy_processors >= numberOfProcessor:
                break

            for job in job_queue[task_id]:
                if job[2] > 0:
                    timeline[task_id][time] = busy_processors + 1 
                    job[2] -= 1
                    executions[task_id] += 1
                    busy_processors += 1
                    break  

    return timeline.tolist()
def rm_scheduler_aperiodic(examples,Aperiod=0,Budget=0,aperiodicArrivals=[],aperiodicLenght=[],serverType='Dumb', time_limit = 40):
    T, C = np.array(examples[0]), np.array(examples[1])
    T2 = np.append(T,np.array(Aperiod))
    print(T2)
    sortedT = np.argsort(T2)
    timeline = np.zeros((T.size ,  time_limit),dtype=int)
    aperiodicTimeline = np.zeros(  time_limit,dtype=int)
    aperiodicBudgetTimeline = np.zeros(  time_limit,dtype=int)
    miss = np.zeros(time_limit,dtype=int)
    arrived = np.zeros(T.size)
    remaining = np.zeros(T.size)
    
    aperiodicRemaining = 0
    remainingBudget = 0

    for t in range(time_limit):
        for i in range(len(aperiodicArrivals)):
            if(aperiodicArrivals[i] == t):
                aperiodicRemaining += aperiodicLenght[i]
        if(t%Aperiod==0):
            remainingBudget = Budget
                
        for i in range(T.size):
            if(t % T[i] == 0):
                arrived[i] += 1
            
        for i in range(T2.size):
            aperiodicBudgetTimeline[t] = remainingBudget 
            print(aperiodicRemaining)
            if(sortedT[i] == len(T)): #aperioodic
                if(aperiodicRemaining > 0 and remainingBudget > 0):
                    aperiodicRemaining -= 1
                    remainingBudget -= 1
                    aperiodicTimeline[t] = 1
                    break
                else:
                    if(serverType == "Dumb"):
                        remainingBudget = 0
                    else:
                        if remainingBudget > 0:
                            remainingBudget -= 1
                continue

            if (remaining[sortedT[i]] != 0 or arrived[sortedT[i]] != 0):
                if(remaining[sortedT[i]] == 0):
                    arrived[sortedT[i]] -=1
                    remaining[sortedT[i]] = C[sortedT[i]]
                remaining[sortedT[i]] -=1
                timeline[sortedT[i]][t] = 1 
                if(arrived[sortedT[i]] != 0):
                    miss[t] = 1
                break
    
    missed = miss.tolist()
    result = timeline.tolist()
    result.append(aperiodicTimeline.tolist())
    result.append(aperiodicBudgetTimeline.tolist())
    result.append(missed)
    return result



def rm_scheduler(examples, time_limit = 40):
    T, C = np.array(examples[0]), np.array(examples[1])
    sortedT = np.argsort(T)
    timeline = np.zeros((T.size ,  time_limit),dtype=int)
    miss = np.zeros(time_limit,dtype=int)
    arrived = np.zeros(T.size)
    remaining = np.zeros(T.size)
    
    for t in range(time_limit):
        for i in range(T.size):
            if(t % T[sortedT[i]] == 0):
                arrived[sortedT[i]] += 1
            
        for i in range(T.size):
            if (remaining[sortedT[i]] != 0 or arrived[sortedT[i]] != 0):
                if(remaining[sortedT[i]] == 0):
                    arrived[sortedT[i]] -=1
                    remaining[sortedT[i]] = C[sortedT[i]]
                remaining[sortedT[i]] -=1
                timeline[sortedT[i]][t] = 1 
                if(arrived[sortedT[i]] != 0):
                    miss[t] = 1
                break
    
    missed = miss.tolist()
    result = timeline.tolist()
    result.append(missed)
    return result

def dm_scheduler_aperiodic(examples,Aperiod=0,Budget=0,aperiodicArrivals=[],aperiodicLenght=[],serverType='Dumb', time_limit = 40):
    T, C, D = np.array(examples[0]), np.array(examples[1]), np.array(examples[2])
    T2 = np.append(D,np.array(Aperiod))
    print(T2)
    sortedT = np.argsort(T2)
    timeline = np.zeros((T.size ,  time_limit),dtype=int)
    aperiodicTimeline = np.zeros(  time_limit,dtype=int)
    aperiodicBudgetTimeline = np.zeros(  time_limit,dtype=int)
    miss = np.zeros(time_limit,dtype=int)
    arrived = np.zeros(T.size)
    remaining = np.zeros(T.size)
    
    aperiodicRemaining = 0
    remainingBudget = 0

    for t in range(time_limit):
        for i in range(len(aperiodicArrivals)):
            if(aperiodicArrivals[i] == t):
                aperiodicRemaining += aperiodicLenght[i]
        if(t%Aperiod==0):
            remainingBudget = Budget
                
        for i in range(T.size):
            if(t % T[i] == 0):
                arrived[i] += 1
            
        for i in range(T2.size):
            aperiodicBudgetTimeline[t] = remainingBudget 
            print(aperiodicRemaining)
            if(sortedT[i] == len(T)): #aperioodic
                if(aperiodicRemaining > 0 and remainingBudget > 0):
                    aperiodicRemaining -= 1
                    remainingBudget -= 1
                    aperiodicTimeline[t] = 1
                    break
                else:
                    if(serverType == "Dumb"):
                        remainingBudget = 0
                    else:
                        if remainingBudget > 0:
                            remainingBudget -= 1
                continue

            if (remaining[sortedT[i]] != 0 or arrived[sortedT[i]] != 0):
                if(remaining[sortedT[i]] == 0):
                    arrived[sortedT[i]] -=1
                    remaining[sortedT[i]] = C[sortedT[i]]
                remaining[sortedT[i]] -=1
                timeline[sortedT[i]][t] = 1 
                if(arrived[sortedT[i]] != 0):
                    miss[t] = 1
                break
    
    missed = miss.tolist()
    result = timeline.tolist()
    result.append(aperiodicTimeline.tolist())
    result.append(aperiodicBudgetTimeline.tolist())
    result.append(missed)
    return result

def dm_scheduler(examples, time_limit = 40):
    T, C, D = np.array(examples[0]), np.array(examples[1]), np.array(examples[2])
    sortedT = np.argsort(D)
    timeline = np.zeros((T.size ,  time_limit),dtype=int)
    miss = np.zeros(time_limit,dtype=int)
    arrived = np.zeros(T.size)
    remaining = np.zeros(T.size)
    totalDone = np.zeros(T.size)
    for t in range(time_limit):
        for i in range(T.size):
            if(t % T[sortedT[i]] == 0):
                arrived[sortedT[i]] += 1
        for i in range(T.size):
            if (remaining[sortedT[i]] != 0 or arrived[sortedT[i]] != 0):
                if(remaining[sortedT[i]] == 0):
                    arrived[sortedT[i]] -=1
                    remaining[sortedT[i]] = C[sortedT[i]]
                remaining[sortedT[i]] -=1
                timeline[sortedT[i]][t] = 1 
                if(t >= (totalDone[sortedT[i]]*T[sortedT[i]] + D[sortedT[i]])):
                    miss[t] = 1
                if(remaining[sortedT[i]] == 0):
                    totalDone[sortedT[i]] +=1
                break
    
    missed = miss.tolist()
    result = timeline.tolist()
    result.append(missed)
    return result


def ed_scheduler(examples, time_limit = 40):
    T, C, D = np.array(examples[0]), np.array(examples[1]), np.array(examples[2])
    timeline = np.zeros((T.size ,  time_limit),dtype=int)
    miss = np.zeros(time_limit,dtype=int)
    arrived = np.zeros(T.size)
    remaining = np.zeros(T.size)
    totalDone = np.zeros(T.size)
    for t in range(time_limit):
        for i in range(T.size):
            if(t % T[i] == 0):
                arrived[i] += 1
        pri = totalDone*T + D
        sortedT = np.argsort(pri)
        for i in range(T.size):
            if (remaining[sortedT[i]] != 0 or arrived[sortedT[i]] != 0):
                if(remaining[sortedT[i]] == 0):
                    arrived[sortedT[i]] -=1
                    remaining[sortedT[i]] = C[sortedT[i]]
                remaining[sortedT[i]] -=1
                timeline[sortedT[i]][t] = 1 
                if(t >= (totalDone[sortedT[i]]*T[sortedT[i]] + D[sortedT[i]])):
                    miss[t] = 1
                if(remaining[sortedT[i]] == 0):
                    totalDone[sortedT[i]] +=1
                break
    missed = miss.tolist()
    result = timeline.tolist()
    result.append(missed)
    return result


def ap_rm_scheduler(examples, ap_task_time, ap_task_jobs, time_limit = 40):
    T, C = np.array(examples[0]), np.array(examples[1])
    sortedT = np.argsort(T)
    timeline = np.zeros((T.size ,  time_limit),dtype=int)
    miss = np.zeros(time_limit,dtype=int)
    interupt = np.zeros(time_limit,dtype=int)
    arrived = np.zeros(T.size)
    remaining = np.zeros(T.size)
    
    interuptRemain = 0
    for t in range(time_limit):
        for i in range(T.size):
            if(t % T[sortedT[i]] == 0):
                arrived[sortedT[i]] += 1
        for i in range(T.size):
            if interuptRemain != 0 or (t == ap_task_time and ap_task_jobs != 0):
                if(interuptRemain == 0):
                    interuptRemain = ap_task_jobs
                interuptRemain -= 1
                interupt[t] = 1
                break
            elif (remaining[sortedT[i]] != 0 or arrived[sortedT[i]] != 0):
                if(remaining[sortedT[i]] == 0):
                    arrived[sortedT[i]] -=1
                    remaining[sortedT[i]] = C[sortedT[i]]
                remaining[sortedT[i]] -=1
                timeline[sortedT[i]][t] = 1 
                if(arrived[sortedT[i]] != 0):
                    miss[t] = 1
                break
    
    missed = miss.tolist()
    interupt = interupt.tolist()
    result = timeline.tolist()
    result.append(interupt)
    result.append(missed)
    return result

