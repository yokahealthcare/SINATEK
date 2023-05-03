import numpy as np
from collections import deque
import heapq
import os, time

def bfs(body, r_size, c_size, sr, sc, er, ec):
    sr = int(sr)
    sc = int(sc)
    er = int(er)
    ex = int(ec)

    # create queue
    queue = deque()
    
    # create set of visited node
    row = r_size
    col = c_size
    visited = np.zeros(shape=(row, col))

    # Directions
    dr = [-1, +1, 0, 0]
    dc = [0, 0, +1, -1]

    # initialize first node
    queue.append([sr, sc])
    visited[sr][sc] = 1
    parent = np.empty((row, col), dtype=object)

    while queue:
        rq, cq = queue.popleft()
        
        if rq == er and cq == ec:
            print("Goal Achieve!")
            return reconstructPath(parent, sr, sc, er, ec)

        # Neigh Explorer
        for i in range(4):
            rr = rq + dr[i]
            cc = cq + dc[i]

            if rr < 0 or cc < 0: continue
            if rr >= row or cc >= col: continue

            if visited[rr][cc]: continue
            for b in body:
                if b.x == cc and b.y == rr: continue

            queue.append([rr, cc])
            visited[rr][cc] = 1
            parent[rr][cc] = [rq, cq]

    return -1

def reconstructPath(parent, sr, sc, er, ec):
    path = [[er, ec]]
    while path[-1] != [sr, sc]:
        path.append(parent[path[-1][0]][path[-1][1]])

    if path[-1] == [sr, sc]:
        return path[::-1]
    return -1



"""
def plot(graph):
    os.system("cls")
    for y in range(len(graph)):
        for x in range(len(graph[0])):
            print(graph[y][x], end='')
        print()
    time.sleep(0.01)


if __name__ == "__main__":
    np.random.seed(21);
    w = 50
    h = 20

    sr = 15
    sc = 0
    er = h-1
    ec = w-1

    # map creation
    graph = np.reshape(np.array([" "]*(w*h)), (h, w))

    graph = np.array(graph);

    # obstacles creation
    for i in range(100):
        r_rand = np.random.randint(h)
        c_rand = np.random.randint(w)
        graph[r_rand][c_rand] = "#"

    graph[er][ec] = "E"

    path_to_destination = bfs(h, w, sr, sc, er, ec)

    if path_to_destination != -1:
        for pa in path_to_destination:
            pr = pa[0]
            pc = pa[1]
            if([pr, pc] != [er, ec]):
                graph[pa[0]][pa[1]] = "o"
            plot(graph)

    else:
        plot(graph)
        print(path_to_destination)
        print("Target is Impossible to reach!")

"""

