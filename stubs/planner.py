from queue import PriorityQueue
from typing import List, Tuple, TypeVar, Dict
from localization import GridLocation, SignedDistanceGrid, RealLocation
import heapq

from localization.types import euclidean_distance

T = TypeVar('T')

class NoPathFoundException(Exception):
    pass


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def is_empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


class AStarPlanner:
    def __init__(self, map_:SignedDistanceGrid=None, sdf_weight:float=0.0):
        self.map = map_
        self.sdf_weight = sdf_weight

    def update_map(self, map:SignedDistanceGrid):
        self.map = map

    def heuristic(self, a:GridLocation, b:GridLocation) -> float:
        return euclidean_distance(a, b)

    def plan(self, start:RealLocation, goal:RealLocation) -> List[RealLocation]:
        '''Plan in real coordinates.'''
        path = self.plan_grid(self.map.real_to_grid(start), self.map.real_to_grid(goal))
        return [self.map.grid_to_real(wp) for wp in path]

    def plan_grid(self, start:GridLocation, goal:GridLocation) -> List[GridLocation]:
        '''Plan in grid coordinates.'''
        if not self.map:
            raise RuntimeError('Planner map is not initialized.')

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from: Dict[GridLocation, GridLocation] = {}
        cost_so_far: Dict[GridLocation, float] = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.is_empty():
            current: GridLocation = frontier.get()

            if current == goal:
                break

            for next, step_cost, sdf in self.map.neighbours(current):
                new_cost = cost_so_far[current] + step_cost + self.sdf_weight*(1/(sdf))
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current
        
        if goal not in came_from:
            raise NoPathFoundException

        return self.reconstruct_path(came_from, start, goal)

    def reconstruct_path(self,
                         came_from:Dict[GridLocation, GridLocation],
                         start:GridLocation, goal:GridLocation) -> List[GridLocation]:
        current: GridLocation = goal
        path: List[GridLocation] = []
        
        while current != start:
            path.append(current)
            current = came_from[current]
            
        # path.append(start)
        path.reverse()
        return path