from island import Island
from data_structures.heap import MaxHeap
class Mode1Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.islands = islands
        self.crew = crew
        self.heap = MaxHeap(len(islands))
        for island in islands:
            self.heap.add((self.calculate_profitability(island, 0), island))

    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Student-TODO: Best/Worst Case
        """
        selected_islands = []
        remaining_crew = self.crew

        while remaining_crew > 0 and len(self.heap) > 0:
            profit, island = self.heap.get_max()

            if remaining_crew >= island.marines:
                pirates = island.marines
            else:
                pirates = remaining_crew

            selected_islands.append((island, pirates))
            remaining_crew -= pirates

        return selected_islands
     

    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Student-TODO: Best/Worst Case
        """
        profit_list = []

        for crew_size in crew_numbers:
            self.crew = crew_size
            selected_islands = self.select_islands()
            total = sum(min(island.money, island.marines * pirates) for island, pirates in selected_islands)
            profit_list.append(total)

        return profit_list


    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        for i in range(len(self.islands)):
            if self.islands[i].name == island.name:
                self.islands[i].money , self.islands[i].marines = new_money, new_marines
                self.heap = MaxHeap(len(self.islands))
                for i, island in enumerate(self.islands):
                    self.heap.add((self.calculate_profitability(island, 0), island))
                break
    

    def calculate_profitability(self, island, pirates):
        pirate_to_marine_ratio = min(pirates / island.marines, 1)
        money = min((pirate_to_marine_ratio* island.money) , island.money)
        #profitability = pirate_to_marine_ratio * money
        return money
