import math



# Defines state.
class State:

    def __init__(self, x: int, y: int, g: float, h: float, parent_state):
        # x coordinate of this state
        self.x = x
        # y coordinate of this state
        self.y = y
        # sum of edge costs from start to this state
        self.g = g
        # estimate of lowest cost path from this state to goal
        self.h = h
        # estimate of lowest cost path from start point to goal if go through this state
        self.f = g + h
        # the parent state
        self.parent_state: State = parent_state

    # toString, output state infor
    def __str__(self):
        if self.parent_state == None:
            return "state(%s, %s), NO parent state, g: %s, h: %s, f: %s" %(
                self.x, self.y, 
                self.g, self.h, self.f)
        return "state(%s, %s), parent state(%s, %s), g: %s, h: %s, f: %s" %(
            self.x, self.y, 
            self.parent_state.x, self.parent_state.y,
            self.g, self.h, self.f)





# Steve Tanimoto’s    
class A_start_search:

    # Constructs a new A_start_search with the associated file "str".
    # @param str: the file name.
    def __init__(self, file: str):
        f = open(file, "r")

        # Read and store the start point
        self.start: list[int] = [int(s) for s in f.readline().split()]
        # Read and store the end point
        self.goal: list[int] = [int(s) for s in f.readline().split()]
        # Read and store the number of obstacles
        self.num_obstacles = int(f.readline().split()[0])

        # Read and store the obstacles in rectangle form.
        self.obstacles = [] 
        for i in range(self.num_obstacles):
            obstacle_point = f.readline().split()
            obstacle = []
            for j in range(4):
                obstacle.append([obstacle_point[j*2], obstacle_point[j*2+1]])
            self.obstacles.append(obstacle)
        
        # Store the obstacle lines that make up the obstacles.
        self.obstacles_lines = []
        # Store the coordinate of the obstacles.
        self.point_set = []
        for obstacle in self.obstacles:
            self.obstacles_lines.append([obstacle[0], obstacle[1]])
            self.obstacles_lines.append([obstacle[1], obstacle[2]])
            self.obstacles_lines.append([obstacle[2], obstacle[3]])
            self.obstacles_lines.append([obstacle[3], obstacle[0]])

            self.point_set.append(obstacle[0])
            self.point_set.append(obstacle[1])
            self.point_set.append(obstacle[2])
            self.point_set.append(obstacle[3])

        self.open_list = []
        self.closed_list = []

        # Compute h value of statr and added start state to open list.
        start_h_value = self.__length_tow_points(self.start, self.goal)
        self.open_list.append(State(self.start[0], self.start[1], 0, start_h_value, None))



    def find_path (self):
        # If OPEN is empty, output “DONE” and stop.
        if len(self.open_list) == 0:
            print("Done, no path found")
            return

        # Find and remove the item [s,p] on OPEN having lowest p.
        lowest_p :State = self.__get_lowest()
        # Put [s,p] on CLOSED.
        self.__put_to_closed(lowest_p)

        # If s is a goal state, backtrace a path
        s = [int(lowest_p.x), int(lowest_p.y)]
        if (s == self.goal):
            path = self.__backtrace_path(lowest_p)
            self.__print_path(path)
            return

        # Generate the list L of [s',f(s')] pairs where the s' are the successors
        L = self.__generate_successors(lowest_p)

        # Insert all members of L onto OPEN.
        self.__insert_to_open_list(L)

        # Repeat above steps with the new open_list
        return self.find_path()



    # pop the state with lowest f value in open list. 
    def __get_lowest (self) -> State:
        assert(len(self.open_list) > 0)
        # helper function for sorting to return the f value of the passing state.
        def get_f (state: State):
            return state.f
        self.open_list.sort(reverse=True, key = get_f)
        return self.open_list.pop()



    # add a state to closed list
    def __put_to_closed (self, state: State):
        self.closed_list.append(state)



    # insert a list state to open list
    def __insert_to_open_list (self, states: list[State]):
        for state in states:
            self.open_list.append(state)



    # backtrace path of the passing state
    def __backtrace_path (self, state: State) -> list[list[int]]:
        path = [(state.x, state.y)]
        while (state.parent_state != None):
            state = state.parent_state
            path = [(state.x, state.y)] + path
        return path



    # print path and compute cumulative cost
    def __print_path (self, path: list[list[int]]):
        assert(self.start == [int(str) for str in path[0]])
        assert(self.goal == [int(str) for str in path[-1]])
        cost = 0
        print(" Point          Cumulative Cost")
        print("(%s, %s)          %s" %(path[0][0], path[0][1], cost))
        for i in range(len(path) - 1):
            cost += self.__length_tow_points(path[i], path[i+1])
            print("(%s, %s)          %s" %(
                path[i+1][0], path[i+1][1], cost))



    # Pythagorean theorem
    # To set destination = goal for computing h value
    def __length_tow_points (self, current: list[int], destination: list[int]) -> float:
        destination_x = int(destination[0])
        destination_y = int(destination[1])
        current_x = int(current[0])
        current_y = int(current[1])
        return math.sqrt((destination_x - current_x)**2 + (destination_y - current_y)**2)



    # Only return legal successors of State s.
    def __generate_successors (self, s: State) -> list[State]:
        # First find legal successor points. 
        # Thus, the line from s to this legal successor points wouldn't intersect with any obstacles_lines.
        possible_successor_points: list[list[int]] = self.__legal_successor_points([str(s.x), str(s.y)])

        # Make possible_points into possible_successors
        possible_successors: list[State] = []
        for point in possible_successor_points:
            g_value: float = self.__length_tow_points([s.x, s.y], [point[0], point[1]]) + s.g
            h_value: float = self.__length_tow_points([point[0], point[1]], [self.goal[0], self.goal[1]])
            successor: State = State(point[0], point[1], g_value, h_value, s)
            possible_successors.append(successor)

        # Check&Compare possible_successors with current open and closed list 
        # to see if some state already exist in open or closed list.
        return self.__compare_successors_open_closed_list(possible_successors)



    # Return all point p, if the line (s to p) wouldn't intersect with any obstacles_lines.
    def __legal_successor_points (self, currentPoint: list[int]) -> list[list[int]]:
        res = []
        point_set = []
        for obstacle in self.obstacles:
            if currentPoint in obstacle:
                i = obstacle.index(currentPoint)
                res.append(obstacle[(i+1)%4]) 
                res.append(obstacle[i-1]) 
                point_set = [x for x in self.point_set if x not in obstacle]
                break

        for point in point_set:
            intersect = False
            for line in self.obstacles_lines:
                intersect = self.__line_intersect_line([currentPoint, point], line)
                if intersect == 1: break
            if intersect == False:
                res.append(point)
        return res

    
    # Check and updata open, closed, and successors list if they have same state.
    def __compare_successors_open_closed_list (self, successors: list[State]) -> list[State]:
        for successor in successors:
            already_exist = False
            # Compare open list and successors list
            for open_state in self.open_list:
                # If successor exist in open list
                if int(open_state.x) == int(successor.x) and int(open_state.y) == int(successor.y):
                    already_exist = True
                    if successor.f > open_state.f:
                        successors.remove(successor)
                    else:
                        self.open_list.remove(open_state)
                    break

            # Only do the following if successor not found in open list 
            if already_exist == False:
                # Compare closed list and successors list 
                for closed_state in self.closed_list:
                    # If successor exist in closed list
                    if int(closed_state.x) == int(successor.x) and int(closed_state.y) == int(successor.y):
                        if successor.f > closed_state.f:
                            successors.remove(successor)
                        else:
                            self.closed_list.remove(closed_state)
                        break

        return successors



    # Algorithm from HABJAN "https://stackoverflow.com/questions/5514366/how-to-know-if-a-line-intersects-a-rectangle/23641016#23641016"
    # This method checks whether if two lines are intersect or not. Return 1 if intersect, 0 not.
    def __line_intersect_line (self, line1: list[list[int]], line2: list[list[int]]) -> int:

        if len([x for x in line1 if x in line2]) > 0:
            return 0

        l1p1_x: int = int(line1[0][0])
        l1p1_y: int = int(line1[0][1])
        l1p2_x: int = int(line1[1][0])
        l1p2_y: int = int(line1[1][1])
        l2p1_x: int = int(line2[0][0])
        l2p1_y: int = int(line2[0][1])
        l2p2_x: int = int(line2[1][0])
        l2p2_y: int = int(line2[1][1])

        q: float = (l2p2_x - l2p1_x) * (l1p1_y - l2p1_y) - (l1p1_x - l2p1_x) * (l2p2_y - l2p1_y)
        d: float = (l1p2_x - l1p1_x) * (l2p2_y - l2p1_y) - (l2p2_x - l2p1_x) * (l1p2_y - l1p1_y)

        if d == 0: return 0

        r: float = q / d
        q = (l1p2_x - l1p1_x) * (l1p1_y - l2p1_y) - (l1p1_x - l2p1_x) * (l1p2_y - l1p1_y)
        s: float = q / d

        if r < 0 or r > 1 or s < 0 or s > 1 :
            return 0

        return 1




print("data1 find path:")
test1 = A_start_search("hw2/data1")
test1.find_path()
print()

print("data2 find path:")
test2 = A_start_search("hw2/data2")
test2.find_path()
print()

print("data3 find path:")
test2 = A_start_search("hw2/data3")
test2.find_path()
print()

    