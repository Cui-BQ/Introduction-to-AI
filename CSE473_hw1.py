# data field for counting
illegalCount = 0
repeatedCount = 0
totalCount = 0

# recursive depth-first search function
def missionaryCannibalProblem(state):
    global totalCount
    global illegalCount 
    global repeatedCount
    totalCount += 1 

    # It checks first if the most recent added state is the goal.
    if state[-1] == (0, 0, "R"):
        print(state)
        print("illegal states: %d, repeated states: %d, total states searched: %d" %(illegalCount, repeatedCount, totalCount-illegalCount-repeatedCount))
        print()
        return

    # It checks if the most recent added state is illegal.
    if state[-1][1] != state[-1][0] and (state[-1][0] == 1 or state[-1][0] == 2):
        illegalCount += 1
        return

    # It checks if the most recent added state is in the state space.
    if state[-1][0] > 3 or state[-1][0] < 0 or state[-1][1] > 3 or state[-1][1] < 0:
        totalCount -= 1
        return 

    # It checks if the most recent added state is the same as an ancestor state on the same path.
    if state[-1] in state[:-1]:
        repeatedCount += 1
        return 

    # If the boat is on the Left side, then recursivly do the following actions
    if state[-1][2] == "L":
        # MCR
        missionaryCannibalProblem(state + [(state[-1][0]-1, state[-1][1]-1, "R")])
        # MMR
        missionaryCannibalProblem(state + [(state[-1][0]-2, state[-1][1], "R")])
        # CCR
        missionaryCannibalProblem(state + [(state[-1][0], state[-1][1]-2, "R")])
        # MR
        missionaryCannibalProblem(state + [(state[-1][0]-1, state[-1][1], "R")])
        # CR
        missionaryCannibalProblem(state + [(state[-1][0], state[-1][1]-1, "R")])

    # If the boat is on the Right side, then recursivly do the following actions
    if state[-1][2] == "R":
        # MCL
        missionaryCannibalProblem(state + [(state[-1][0]+1, state[-1][1]+1, "L")])
        # MML
        missionaryCannibalProblem(state + [(state[-1][0]+2, state[-1][1], "L")])
        # CCL
        missionaryCannibalProblem(state + [(state[-1][0], state[-1][1]+2, "L")])
        # ML
        missionaryCannibalProblem(state + [(state[-1][0]+1, state[-1][1], "L")])
        # CL
        missionaryCannibalProblem(state + [(state[-1][0], state[-1][1]+1, "L")])    
    return

# Main Function
if __name__ == '__main__':
    s = [(3, 3, "L")]
    missionaryCannibalProblem(s)