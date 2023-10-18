from island import Island
from algorithms import binary_search
from data_structures.bst import *
from data_structures.heap import MaxHeap
from data_structures.aset import ASet
import math

class Mode2Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, n_pirates: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.n_pirates = n_pirates
        self.islands =  BinarySearchTree()
        self.captains = []
    
    
    def add_islands(self, islands: list[Island]):
        """
        Student-TODO: Best/Worst Case
        """
        for island in islands:
            key = island.name
            if key not in self.islands:
                self.islands[key] = island
            else:
                raise KeyError("Island exists")

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        Student-TODO: Best/Worst Case
        """
        result = []

        while self.n_pirates > 0:
            best_profit = 0
            best_island = None
            best_sent_crew = 0

            profitable_islands = MaxHeap(self.n_pirates)
            # Create a list of islands that have positive marines
            for island in BSTInOrderIterator(self.islands.root):
                if island.item.marines > 0:
                    profitable_islands.add(island.item)

            if not profitable_islands:
                # No profitable islands remaining, assign a score of 200 to all remaining pirates
                result.extend([(None, 0)] * self.n_pirates)
                break

            island = profitable_islands.get_max()
            # Calculate the profit for each island
            profit = self.calculate_profitability(island, crew)
            if profit > best_profit:
                best_profit = profit
                best_island = island
                best_sent_crew = min(crew, island.marines)

            # Reduce island resources and add the result to the list
            best_island.money -= self.calculate_profitability(island, best_sent_crew)
            best_island.marines -= best_sent_crew
            result.append((best_island, best_sent_crew))

            self.n_pirates -= 1

        return result

    def calculate_profitability(self, island, pirates):
        money = min((pirates / island.marines* island.money) , island.money)
        return math.ceil(money)
    
    def calculate_score(self, remaining_crew, money_looted):
        score = 2 * remaining_crew + money_looted
        return score
    
    def get_profitable_islands(self, crew):
        profitable_island = MaxHeap(len(self.islands))

        for island in BSTInOrderIterator(self.islands.root):
            if island.item.marines > 0:
                profitable_island.add(island.item)

        return profitable_island
