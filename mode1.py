from island import Island
from data_structures.bst import BinarySearchTree, BSTInOrderIterator
from algorithms.binary_search import binary_search
import math
class Mode1Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.island = islands
        self.crew = crew
        self.bst = BinarySearchTree()

        for island in islands:
            key = island.marines/island.money
            if key not in self.bst:
                self.bst[key] = [island]
            else:
                self.bst[key].append(island)


    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Student-TODO: Best/Worst Case
        """
        selected_islands = []
        remaining_crew = self.crew

        for island_list in BSTInOrderIterator(self.bst.root):
            if remaining_crew <= 0:
                break

            islands = island_list.item
            for island in islands:
                pirates = min(remaining_crew, island.marines)
                selected_islands.append((island, pirates))
                remaining_crew -= pirates

        return selected_islands


    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Student-TODO: Best/Worst Case
        """
        profit_list = []

        for crew_size in crew_numbers:
            money_earned = 0
            remaining_crew = crew_size

            for island_node in BSTInOrderIterator(self.bst.root):
                islands = island_node.item
                for island in islands:
                    available_pirates = min(remaining_crew, island.marines)
                    money_earned += self.calculate_profitability(island, available_pirates)
                    remaining_crew -= available_pirates
                if remaining_crew <= 0:
                    break
            profit_list.append(math.ceil(money_earned))

        return profit_list


    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """

        position = binary_search(self.island, island)

        if position == -1:
            raise KeyError ("Island not found")
        
        island.money = new_money
        island.marines = new_marines
    

    def calculate_profitability(self, island, pirates):
        # pirate_to_marine_ratio = min( 1)
        money = min((pirates / island.marines* island.money) , island.money)
        return math.ceil(money)
