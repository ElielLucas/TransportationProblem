from math import sqrt, pow, gcd
from random import SystemRandom
import pandas as pd
import numpy as np

class Point: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self) -> str:
        return "x: " + str(self.x) + "    y: " + str(self.y) 

class line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
 
def onLine(l1, p):
    if (p.x <= max(l1.p1.x, l1.p2.x)
        and p.x <= min(l1.p1.x, l1.p2.x)
        and (p.y <= max(l1.p1.y, l1.p2.y) and p.y <= min(l1.p1.y, l1.p2.y))
        ):
        return True
    return False
 
def direction(a, b, c):
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if val == 0:
        return 0
    elif val < 0:
        return 2
    return 1
 
def isIntersect(l1, l2):
    dir1 = direction(l1.p1, l1.p2, l2.p1)
    dir2 = direction(l1.p1, l1.p2, l2.p2)
    dir3 = direction(l2.p1, l2.p2, l1.p1)
    dir4 = direction(l2.p1, l2.p2, l1.p2)
 
    if dir1 != dir2 and dir3 != dir4:
        return True

    return (dir1 == 0 and onLine(l1, l2.p1)
            or dir2 == 0 and onLine(l1, l2.p2)
            or dir3 == 0 and onLine(l2, l1.p1)
            or dir4 == 0 and onLine(l2, l1.p2))
 
def checkInside(poly, n, p):
    if n < 3:
        return False

    exline = line(p, Point(9999, p.y))
    count = 0
    i = 0
    while True:
        side = line(poly[i], poly[(i + 1) % n])
        if isIntersect(side, exline):
            if (direction(side.p1, p, side.p2) == 0):
                return onLine(side, p)
            count += 1
        i = (i + 1) % n
        if i == 0:
            break

    return count & 1

def cross(p1: Point, p2: Point) -> float:
    return p1.x * p2.y - p2.x * p1.y

def pol_area(points) -> float:
    ans = 0.0
    for i in range(2, len(points)):
        p1 = Point(points[i].x - points[0].x, points[i].y - points[0].y)
        p2 = Point(points[i - 1].x - points[0].x, points[i - 1].y - points[0].y)
        ans += cross(p1=p1, p2=p2)
    
    ans /= 2
    if ans < 0:
        ans *= -1
    return ans    

def bounds(points) -> int:
    ans = len(points)
    for i in range(len(points)):
        dx = (points[i].x - points[(i + 1) % len(points)].x)
        dy = (points[i].y - points[(i + 1) % len(points)].y)
        ans += abs(gcd(dx, dy)) - 1
    return ans

def get_pick(points) -> int:
    return pol_area(points=points) + 1 - bounds(points=points) // 2

def get_point(lim_x_left: int, lim_x_right: int, lim_y_down: int, lim_y_up: int, n: int):
    points = []
    for _ in range(4):
        x = SystemRandom().randint(lim_x_left, lim_x_right)
        y = SystemRandom().randint(lim_y_down, lim_y_up)
        points.append(Point(x, y))
    
    while get_pick(points=points) < n:
        points = []
        for _ in range(4):
            x = SystemRandom().randint(lim_x_left, lim_x_right)
            y = SystemRandom().randint(lim_y_down, lim_y_up)
            points.append(Point(x, y))
    
    left_most, right_most = lim_x_right + 1, lim_x_left - 1
    lowest, highest = lim_y_up + 1, lim_y_down - 1
    for i in points:
        left_most = min(left_most, i.x)
        right_most = max(right_most, i.x)
        lowest = min(lowest, i.y)
        highest = max(highest, i.y)
    
    ans = []
    for _ in range(n):
        x = SystemRandom().randint(left_most, right_most)
        y = SystemRandom().randint(lowest, highest)
        p = Point(x, y)
        while not checkInside(points, 4, p):
            x = SystemRandom().randint(left_most, right_most)
            y = SystemRandom().randint(lowest, highest)
            p = Point(x, y)
        ans.append(p)
    
    return ans

def distance(p1: Point, p2: Point):
    return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2))

def get_cost(points_orig, n, points_dest, m):
    matrix = []
    for i in range(n):
        aux = []
        for j in range(m):
            aux.append(distance(points_orig[i], points_dest[j]))
        matrix.append(aux)

    return matrix


def savetocsv(filename, mat):
    arr = np.array([np.array(xi) for xi in mat])
    pd.DataFrame(arr).to_csv("./dados/" + filename + ".csv", index=None)


def main():
    orig = int(input("Quantidade origens: "))
    trans = int(input("Quantidade transbordos: "))
    port = int(input("Quantidade portos: "))
    clients = int(input("Quantidade clientes: "))

    points_orig = get_point(lim_x_left=-100, lim_x_right=100,
                            lim_y_down=-100, lim_y_up=100, n=orig)
    
    points_transbordo = get_point(lim_x_left=-250, lim_x_right=250,
                            lim_y_down=-250, lim_y_up=250, n=trans)
    
    points_porto = get_point(lim_x_left=-1000, lim_x_right=1000,
                            lim_y_down=-1000, lim_y_up=1000, n=port)
    
    cost_orig_trans = get_cost(points_orig=points_orig, n=orig, points_dest=points_transbordo, m=trans)
    cost_transbordo_porto = get_cost(points_orig=points_transbordo, n=trans, points_dest=points_porto, m=port)
    cost_orig_porto = get_cost(points_orig=points_orig, n=orig, points_dest=points_porto, m=port)

    savetocsv('origem_transbordo', cost_orig_trans)
    savetocsv('transbordo_porto', cost_transbordo_porto)
    savetocsv('origem_porto', cost_orig_porto)

    supply = [SystemRandom().randint(100, 1000) for _ in range(orig)]
    cap_trans = [SystemRandom().randint(100, 1000) for _ in range(trans)]
    cap_porto = [SystemRandom().randint(100, 1000) for _ in range(port)]
    demmand = [SystemRandom().randint(100, 1000) for _ in range(clients)]

    sum_supply, sum_demmand = sum(supply), sum(demmand)
    if sum(supply) < sum(demmand):
        for i in range(orig):
            supply[i] += (sum_demmand - sum_supply) // orig
        supply[0] += (sum_demmand - sum_supply) % orig
    aux = np.array(supply)
    pd.DataFrame(aux).to_csv("./dados/supply.csv", index=None)
    
    t = SystemRandom().randint(1, trans)
    for _ in range(t):
        cap_trans[SystemRandom().randint(1, trans) - 1] = sum_demmand
    aux = np.array(cap_trans)
    pd.DataFrame(aux).to_csv("./dados/cap_transbordo.csv", index=None)

    t = SystemRandom().randint(1, port)
    for _ in range(t):
        cap_porto[SystemRandom().randint(1, port) - 1] = sum_demmand
    aux = np.array(cap_porto)
    pd.DataFrame(aux).to_csv("./dados/cap_porto.csv", index=None)
    
    pd.DataFrame(demmand).to_csv("./dados/demand.csv", index=None)


if __name__ == "__main__":
    main()
