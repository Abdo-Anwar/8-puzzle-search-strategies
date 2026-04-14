from queue import Queue
import heapq
import math

N = 362880 #9! all possible states
fact = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880] #factorials
par = [-1] * N #parent array for BFS and DFS 
iterativeDFS_par = {} # parentstate :(childstate, limit) 
COLOR = {
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "DEFAULT": "\033[39m",
} #ANSII escape character text color codes
BACKCOLOR = {
    "BACKGROUND_BLACK": "\033[40m",
    "BACKGROUND_RED": "\033[41m",
    "BACKGROUND_GREEN": "\033[42m",
    "BACKGROUND_YELLOW": "\033[43m",
    "BACKGROUND_BLUE": "\033[44m",
    "BACKGROUND_MAGENTA": "\033[45m",
    "BACKGROUND_CYAN": "\033[46m",
    "BACKGROUND_WHITE": "\033[47m",
    "BACKGROUND_DEFAULT": "\033[49m",
} #ANSII escape character background color codes
def get_state(grid): #from grid to state number
    unused = [0, 1, 2, 3, 4, 5, 6, 7, 8] 
    answer = 0
    for i in range(9):
        answer += unused.index(grid[i]) * fact[8 - i] #
        unused.remove(grid[i])
    return answer

def get_grid(state_number): #from state number to grid
    unused = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    grid = []
    current_number = state_number
    for i in range(9):
        current = current_number // fact[8 - i] # determine which unused number to use 
        current_number %= fact[8 - i] # update current number 
        grid.append(unused[current])
        unused.remove(unused[current])
    return grid

def get_path(goal): #follow parent to find path
    path = [goal] 
    current_node = goal
    while par[current_node] != -1:
        current_node = par[current_node]
        path.append(current_node)
    path.reverse()
    return path

def print_grid(grid, past):
    for i in range(0, 9, 3):
        print(BACKCOLOR["BACKGROUND_WHITE"], end = "")
        for j in range(3):
            backcolor = BACKCOLOR["BACKGROUND_WHITE"]
            color = COLOR["GREEN"]
            if (grid[i + j] != past[i + j]):
                color = COLOR["RED"]
            if(grid[i + j] == 0):
                print(color, "x", COLOR["BLUE"], end = "")
            else:
                print(color, grid[i + j], COLOR["BLUE"], end = "")
        print(BACKCOLOR["BACKGROUND_DEFAULT"])

def show_path(path, interactive): #print list of states
    past_grid = path[0]
    print("Steps:")
    for node in path:
        print_grid(get_grid(node), get_grid(past_grid))
        print()
        if(interactive): # if interactive wait for user input between steps
            input("Press Enter to continue...")
        past_grid = node

def get_neighbours(state): #get list of states of neighbours
        grid = get_grid(state)
        neighbours = []
        for i in range(9):
            if grid[i] == 0: # find blank tile
                x = i // 3 # row
                y = i % 3 # column
                if y > 0: #left
                    grid[i - 1], grid[i] = grid[i], grid[i - 1] # swap
                    neighbours.append(get_state(grid)) # add new state
                    grid[i - 1], grid[i] = grid[i], grid[i - 1] # swap back
                if y < 2: #right
                    grid[i + 1], grid[i] = grid[i], grid[i + 1]
                    neighbours.append(get_state(grid))
                    grid[i + 1], grid[i] = grid[i], grid[i + 1]
                if x > 0: #up
                    grid[i - 3], grid[i] = grid[i], grid[i - 3]
                    neighbours.append(get_state(grid))
                    grid[i - 3], grid[i] = grid[i], grid[i - 3]
                if x < 2: #down
                    grid[i + 3], grid[i] = grid[i], grid[i + 3]
                    neighbours.append(get_state(grid))
                    grid[i + 3], grid[i] = grid[i], grid[i + 3]
                break
        return neighbours

def bfs(start, goal):
    frontier = Queue()
    frontier.put(start)
    seen = {start}
    while frontier.qsize():
        current_node = frontier.get()
        if current_node == goal:
            inp = input("do you want interactive steps? (y/n): ")
            if inp.lower() == 'y':
                print("Interactive Steps:") 
            if inp.lower() == 'n':
                print("Full Steps:")
            show_path(get_path(goal), inp.lower() == 'y')
            print("BFS Path length:", len(get_path(goal)))
            return 1
        neighbours = get_neighbours(current_node)
        for next in neighbours:
            if not (next in seen):
                par[next] = current_node
                frontier.put(next)
                seen.add(next)
    return 0

def dfs(start, goal):
    print("DFS solution:")
    frontier = [start]
    seen = {start}
    while len(frontier):
        current_node = frontier[-1]
        frontier.pop()
        if current_node == goal:
            inp = input("do you want interactive steps? (y/n): ")
            if inp.lower() == 'y':
                print("Interactive Steps:") 
            if inp.lower() == 'n':
                print("Full Steps:")
            show_path(get_path(goal), inp.lower() == 'y')
            print("DFS Path length:", len(get_path(goal)))
            return 1
        neighbours = get_neighbours(current_node)
        for next in neighbours:
            if not (next in seen):
                par[next] = current_node
                frontier.append(next)
                seen.add(next)
    print("Goal not found")
    return 0

def get_iterativeDFS_path(goal):
    path = [goal]
    current_node = goal
    limit = 0
    while (current_node, limit) in iterativeDFS_par:
        current_node = iterativeDFS_par[(current_node, limit)]
        limit = limit + 1
        path.append(current_node)
    path.reverse()
    return path

def DLS(start, goal, limit):
    frontier = [[start, limit]]
    while len(frontier):
        current_node = frontier[-1]
        frontier.pop()
        if current_node[0] == goal:
            return 1
        neighbours = get_neighbours(current_node[0])
        if current_node[1] > 0:
            for next in neighbours:
                iterativeDFS_par[(next, current_node[1] - 1)] = current_node[0]
                frontier.append([next, current_node[1] - 1])
    return 0

def iterativeDFS(start, goal):
    i = 0
    MAX_DEPTH = 30
    iterativeDFS_par = {}
    for i in range(MAX_DEPTH):
        if DLS(start, goal, i):
            return i
    return -1

def heuristic(state, heuristic_type="Man"): # return h for getting each tile in current grid to its goal position
    grid = get_grid(state)
    h = 0
    for i, val in enumerate(grid):
        if val == 0:  # skip blank tile
            continue
        x_current, y_current = divmod(i, 3)   # divmod tells position in the grid
        x_goal, y_goal = divmod(val, 3)
        if heuristic_type == "Man":
            h += abs(x_current - x_goal) + abs(y_current - y_goal)
        elif heuristic_type == "Euc":
            h += math.sqrt((x_current - x_goal)**2 + (y_current - y_goal)**2)
    return h

def a_star(start, goal, heuristic_type="Man"):
    global par
    par = [-1] * N  # initialize parent array
    frontier = []   # priority queue (min-heap)
    heapq.heappush(frontier, (0, start)) # (f_cost, state)
    g_cost = {start: 0}
    nodes_expanded = 0  # to compare between manhattan and euclidean

    while frontier:
        f, current = heapq.heappop(frontier)
        nodes_expanded += 1

        if current == goal:
            path = get_path(goal)
            print("--------------------------------")
            if heuristic_type == "Man":
                print("A* (Manhattan) solution:")
                inp = input("do you want interactive steps? (y/n): ")
                if inp.lower() == 'y':
                    print("Interactive Steps:") 
                if inp.lower() == 'n':
                    print("Full Steps:")
                show_path(path, inp.lower() == 'y')
                print("A* (Manhattan) Path length:", len(path))
                print("A* (Manhattan) Nodes expanded:", nodes_expanded)
            if heuristic_type == "Euc":
                print("A* (Euclidean) solution:")
                inp = input("do you want interactive steps? (y/n): ")
                if inp.lower() == 'y':
                    print("Interactive Steps:") 
                if inp.lower() == 'n':
                    print("Full Steps:")
                show_path(path, inp.lower() == 'y')
                print("A* (Euclidean) Path length:", len(path))
                print("A* (Euclidean) Nodes expanded:", nodes_expanded)
            
            return path, nodes_expanded

        for neighbor in get_neighbours(current):
            new_cost = g_cost[current] + 1
            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                f_cost = new_cost + heuristic(neighbor, heuristic_type)
                heapq.heappush(frontier, (f_cost, neighbor))
                par[neighbor] = current
    print("A* Solution:")
    print("Goal not found")
    print("Nodes expanded:", nodes_expanded)
    return None, nodes_expanded

print(COLOR["BLUE"])
start = get_state([1, 2, 3, 4, 0, 5, 6, 7, 8])
start1 = get_state([1, 2, 5, 4, 0, 8, 3, 6, 7])
start2 = get_state([8, 7, 6, 5, 4, 3, 2, 1, 0])
testcase = get_state([3, 1, 2, 4, 8, 0, 6, 5, 7])
goal = 0

dfs (testcase, goal)

# a_star(start2, goal, "Man")
a_star(start2, goal, "Euc")
# dfs(start, goal)
# bfs(start, goal)



# v = iterativeDFS(start, goal)
# if  (v != -1):
#     print("IDFS done")
#     print(v + 1)
#     iterativeDFS_path = get_iterativeDFS_path(goal)
#     #show_path(iterativeDFS_path)



