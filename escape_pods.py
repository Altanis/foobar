'''
Escape Pods
===========

You've blown up the LAMBCHOP doomsday device and relieved the bunnies of their work duries -- and now you need to escape from the space station as quickly and as orderly as possible! The bunnies have all gathered in various locations throughout the station, and need to make their way towards the seemingly endless amount of escape pods positioned in other parts of the station. You need to get the numerous bunnies through the various rooms to the escape pods. Unfortunately, the corridors between the rooms can only fit so many bunnies at a time. What's more, many of the corridors were resized to accommodate the LAMBCHOP, so they vary in how many bunnies can move through them at a time. 

Given the starting room numbers of the groups of bunnies, the room numbers of the escape pods, and how many bunnies can fit through at a time in each direction of every corridor in between, figure out how many bunnies can safely make it to the escape pods at a time at peak.

Write a function solution(entrances, exits, path) that takes an array of integers denoting where the groups of gathered bunnies are, an array of integers denoting where the escape pods are located, and an array of an array of integers of the corridors, returning the total number of bunnies that can get through at each time step as an int. The entrances and exits are disjoint and thus will never overlap. The path element path[A][B] = C describes that the corridor going from A to B can fit C bunnies at each time step.  There are at most 50 rooms connected by the corridors and at most 2000000 bunnies that will fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time step.  (Note that in this example, room 3 could have sent any variation of 8 bunnies to 4 and 5, such as 2/6 and 6/6, but the final solution remains the same.)
'''

from collections import deque

CORRIDOR_CAPACITY = 2000001


class EscapePods:
    def __init__(self, entrances, exits, path):
        n = len(path)
        m = n + 2

        # Create the graph matrix with capacity values
        self.graph = [[0] * m for _ in range(m)]

        # Fill in the capacity values based on the given path
        for i in range(n):
            for j in range(n):
                self.graph[i + 1][j + 1] = path[i][j]

        # Set the capacity of the corridors from the entrances to the source
        for num in entrances:
            self.graph[0][num + 1] = CORRIDOR_CAPACITY

        # Set the capacity of the corridors from the exits to the sink
        for num in exits:
            self.graph[num + 1][m - 1] = CORRIDOR_CAPACITY

        self.size = m

    def bfs(self):
        # Perform breadth-first search to find an augmenting path

        parents = [-1] * self.size  # Array to store the parent nodes
        queue = deque([0])  # Start the queue with the source node

        while queue and parents[-1] == -1:
            u = queue.popleft()  # Dequeue the front node
            for v in range(self.size):
                if self.graph[u][v] > 0 and parents[v] == -1:
                    # If there is a capacity in the edge and v has not been visited
                    queue.append(v)  # Enqueue v
                    parents[v] = u  # Set the parent of v as u

        # Build the augmenting path from the sink to the source
        path = []
        u = parents[-1]
        while u != 0:
            if u == -1:
                return None  # If the source is not reachable from the sink, return None
            path.append(u)  # Append the node to the path
            u = parents[u]  # Move to the parent node

        path.reverse()  # Reverse the path to start from the source
        return path

    def solve(self):
        max_flow = 0
        path = self.bfs()

        while path:
            cap = CORRIDOR_CAPACITY
            u = 0

            # Find the minimum capacity along the augmenting path
            for v in path:
                cap = min(cap, self.graph[u][v])
                u = v

            max_flow += cap
            u = 0

            # Update the residual capacities and reverse edges along the augmenting path
            for v in path:
                self.graph[u][v] -= cap
                self.graph[v][u] += cap
                u = v

            path = self.bfs()  # Find the next augmenting path

        return max_flow


def solution(entrances, exits, path):
    escape_pods = EscapePods(entrances, exits, path)
    res = escape_pods.solve()
    return res
