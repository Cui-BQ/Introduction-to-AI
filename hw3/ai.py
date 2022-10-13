from os import stat
import time
import random 
import io

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        pass

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

    # trace back the path to find the parent state of a certain state.
    class path:
        def __init__(self, hole, parent):
            self.hole = hole
            self.parent = parent

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately 
    def move(self, a, b, a_fin, b_fin, t):
        #For test only: return a random move
        #r = []
        #for i in range(6):
        #    if a[i] != 0:
        #        r.append(i)
        # To test the execution time, use time and file modules
        # In your experiments, you can try different depth, for example:
        #f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # Make sure to clean the file before each of your experiment
        #for d in [3, 5, 7]: #You should try more
        #    f.write('depth = '+str(d)+'\n')
        #    t_start = time.time()
        #    self.minimax(depth = d)
        #    f.write(str(time.time()-t_start)+'\n')
        #f.close()
        #return r[random.randint(0, len(r)-1)]
        #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        #and remove timing code. 
        
        #Comment all the code above and start your code here
        start_time = time.time()
        state = self.state(a, b, a_fin, b_fin)
        # t = 100000, for timeing test.

        # I choice depth = 9, initial alpha = -10000, initial beta = 10000
        action = self.minimax(9, -10000, 10000, state, True, t, start_time, 0, self.path(-1, None))
        parent = action[1]
        while (parent.parent != None):
            if (parent.parent.parent == None): break
            parent = parent.parent
        
        #record depth and time.
        f = open('time.txt', 'a')
        f.write('depth = '+str(9)+'\n')
        f.write(str(time.time()-start_time)+'\n')
        f.close()
        return parent.hole

    # Alphabeta minimax function
    #Input:
    # depth: how deep will the minimax search down.
    # a: alpha
    # b: beta
    # state: the current state
    # maximizing: (boolean) True if search maxValue otherwises search minValue
    # t: search time limit (ms)
    # start_time: The time when the initial minimax start
    # again: (boolean) True if the next state of the current state get a chance to move again.
    # path: the record the parent state path of the current state.
    def minimax(self, depth: int, a: int, b: int, state: state, maximizing, t: int, start_time: float, again: int, path: path):
        #example: doing nothing but wait 0.1*depth sec

        # If terminal or hit time limit, then return the evaluate value.
        if depth <= 0 or state.a_fin > 36 or state.a_fin > 36 or (time.time()-start_time)*1000 >= t:
             return self.eval(state, maximizing, again), path

        # DO maximizing search only if:
        # This search is for maximizing Value AND minimizing Value didn't get a chance to move again.
        # This search is initially for minimizing Value BUT maximizing Value get a chance to move again.
        if ((maximizing and again == 0) or (not maximizing and again == 1)):
            maxValue = -10000
            maxPath = None
            for child in self.get_successors(state, True, path):
                value = self.minimax(depth-1, a, b, child[0], False, t, start_time, child[1], child[2])
                if (maxValue < value[0]):
                     maxValue = value[0]
                     maxPath = value[1]
                a = max(a, value[0])
                if b <= a:
                    break
            return maxValue, maxPath

        # DO minimizing search only if:
        # This search is for minimizing Value AND maximizing Value didn't get a chance to move again.
        # This search is initially for maximizing Value BUT minimizing Value get a chance to move again.
        else:
            minValue = 10000
            minPath = None
            for child in self.get_successors(state, False, path):
                value = self.minimax(depth-1, a, b, child[0], True, t, start_time, child[1], child[2])
                if (minValue > value[0]):
                    minValue = value[0]
                    minPath = value[1]
                b = min(b, value[0])
                if b <= a:
                    break
            return minValue, minPath



    # heuristic function
    #Input:
    # state: the state to evaluate.
    # minimizing: (boolean) True if state belong to minimizing Value.
    # again: (boolean) True if the player who reached this state can move again.
    def eval(self, state: state, minimizing, again) -> int:
        # Basic evaluate different between a Kalah hole and b Kalah hole.
        score = state.a_fin - state.b_fin
        
        # if maximizing get a change to move again, then get 6 bonus scores
        if (not minimizing and again == 1): score = score + 6
        # if minimizing get a change to move again, then get 6 penalty scores
        if (minimizing and again == 1): score = score - 6
        return score


    #Input:
    # state: the state to find successors.
    # a_turn: (boolean) True if state belong to maximizing Value.
    # path: for trace back the successors's parent state
    def get_successors(self, state: state, a_turn, path):
        successors = []
        if a_turn:
            for i in range(6):
                if state.a[i] != 0:
                    successors.append(self.get_next_state(state, i, path))
        else:
            for i in range(6, 12):
                if state.b[i%6] != 0:
                    successors.append(self.get_next_state(state, i, path))

        # rearrange the successor list, so the successor who has a chance to move again will locate
        # in front of the successor list. This will speed up the alpha beta pruning.
        p = 0
        for i in range(len(successors)):
            if successors[i][1]:
                temp = successors[p]
                successors[p] = successors[i]
                successors[i] = temp
                p += 1

        return successors


    #Input:
    # current_state: the current state.
    # hole: (in range(0: 12), 0-5 for a[], 6-11 for b[]). 
    #       Pick this hole and calculate the next state based on the current state
    # path: for trace back the parent state
    def get_next_state(self, current_state: state, hole: int, parent: path):
        stones: int = 0
        holes: list[int] = []
        
        index = hole 
        if (hole <= 5): # The current state is a's
            stones = current_state.a[hole]
            holes = current_state.a[hole:] + [current_state.a_fin] + current_state.b + current_state.a[:hole]
        else: # The current state is b's
            index = hole-6
            stones = current_state.b[hole-6]
            holes = current_state.b[hole-6:] + [current_state.b_fin] + current_state.a + current_state.b[:hole-6]

        # picking up all the stones
        holes[0] = 0
        count: int = 1 
        last_hole: int = -1
        again = False

        # distribute stones to all holes 
        while count <= stones:
            holes[count % 13] += 1
            if (count == stones):
                last_hole = count % 13
            count += 1

        # If your last stone lands in your own Kalah, you get an extra turn.
        if (last_hole == 6 - index):
            again = True

        # If your last stone lands in your own empty hole, 
        elif (holes[last_hole] == 1 and (last_hole+index < 6 or last_hole >= 6-index+7)):
            op = holes[7-index:13-index]
            oi = index+last_hole
            
            if oi > 5: oi = last_hole+index-13
            # you take all the stones in the opponent's opposite hole and the last stone and put them in your Kalah.
            holes[6 - index] += holes[last_hole] + op[5-oi]
            holes[last_hole] = 0
            op[5-oi] = 0
            holes[7-index:13-index] = op

        # If you run out of stones on your side, 
        # the opponent takes all the stones left on his side and puts them in his Kalah
        if (sum(holes[7-index:13-index]) == 0):
            holes[6 - index] += sum(holes[13-index:] + holes[:6-index])

        if ((sum(holes[13-index:] + holes[:6-index])) == 0):
            if (hole <= 5): current_state.b_fin += sum(holes[7-index:13-index])
            else: current_state.a_fin += sum(holes[7-index:13-index])

        # return state
        if (hole <= 5):
            return self.state((holes[13-index:] + holes[:6-index]), holes[7-index:13-index], holes[6 - index], current_state.b_fin), again, self.path(index, parent)
        else:
            return self.state(holes[7-index:13-index], (holes[13-index:] + holes[:6-index]), current_state.a_fin, holes[6 - index]), again, self.path(index, parent)     
