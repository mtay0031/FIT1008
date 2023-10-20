from island import Island
from data_structures.bst import BinarySearchTree, BSTInOrderIterator
import math
class Mode1Navigator:
    """
    Mode1Navigator is a class for managing pirate crew distribution across islands to maximize profits. 
    It uses a Binary Search Tree (BST) to efficiently store and retrieve islands based on their profitability ratios.

    Data Structures used:
    - Binary Search Tree (BST): Stores islands, where the key is the ratio of marines to money.
    - As the ratio of marines to money of each island is unique, it can be used as the key and the island object as the value
    - The pair will be stored in bst and iterated by using BSTInorderIterator to visit the nodes, allows for efficient in-order traversal of the BST. 
      In this case, it helps in selecting profitable islands by iterating through islands in ascending order of their profitability ratio. 

    BST allows efficient storage and retrieval of islands based on their profitability ratios,
    which are calculated as marines/money. This ratio is essential for making decisions on which islands to attack. 
    The BST ensures that islands are sorted by this ratio, making it quick to find the most profitable islands.

    Example:
    islands = [Island("A", 80, 10), Island("B", 150, 15), Island("C", 250, 30)]
    crew = 40


    when select_islands(), returns [(Island(name='B', money=150, marines=15), 15), (Island(name='C', money=250, marines=30), 25)]
    we select the islands we can get the most profit, using all of the 40 crews.

    when select_islands_from_crew_numbers(), crew_numbers = [10, 20, 30], returns [100, 192, 275]
    the highest profit for each crew size will be computed

    when update_island(), it will firstly checks if the island existing in the tree by using or not,
    then update the island marines and money

    the most best/worst complexity in this module:
    Best case: O(1) it occurs in update_island() and calculate_profitability()
    Worst case: O(C*N) in select_islands_from_crew_numbers()
    * refers to each function
    In a balanced tree, the depth is minimized (log N), ensuring that operations like finding the median and selecting profitable islands are efficient.
    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Initialise the initial state of the islands and the number of crew.

        :Args:
        islands: A list of islands to be attacked
        crew: number of crew in this journey

        :Complexity:
        Best/Worst Case: O(N log N) N is the length of the islands,
        we need to traverse the tree with log N depth for each island, to find the correct position to insert it into the tree,
        iterate through the list of islands (N times)
        """
        self.island = islands
        self.crew = crew
        self.bst = BinarySearchTree()

        # iter through the list of islands O(N)
        for island in islands:
            key = island.marines/island.money
            # check if key is existing in the tree, the ratio should be unique
            # traverse to check and insert the pair O(log N)
            if key not in self.bst:
                self.bst[key] = [island]
            else:
                raise KeyError("Duplicate island")


    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Select island to attack.

        Returns: A list contains tuple having a pair of island and the number of crew

        :Complexity:
        Best Case: O(log N) N is the length of islands, if the tree is balanced, 
        we iter through the depth of the tree which is log N.
        Worst Case: O(N) N is the length of islands, if the tree is unbalanced, 
        we need to iterate all the way through the tree until the last node.
        """
        selected_islands = []
        remaining_crew = self.crew

        # iter through the tree by using iterator O(N)
        for island_list in BSTInOrderIterator(self.bst.root):
            if remaining_crew <= 0:
                break

            islands = island_list.item
            # iter each island in islands, there is only 1 island in the list so O(1)
            for island in islands:
                pirates = min(remaining_crew, island.marines)
                selected_islands.append((island, pirates))
                remaining_crew -= pirates

        return selected_islands


    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Select the islands by calculating the most profitability one.

        :Args:
        crew_numbers: the crew to sent 

        :Return: A list of money containing the amount of money we could make with the respective crew size

        :Complexity:
        Best/Worst Case: O(C*N) N is the length of islands, C is the number of crew
        the function iterates through all the nodes (islands) in bst 
        """
        # Create a list to store the result
        profit_list = []

        # iterate through the no. of crews O(C)
        for crew_size in crew_numbers:
            money_earned = 0
            remaining_crew = crew_size

            # visit every nodes in bst O(N)
            for island_node in BSTInOrderIterator(self.bst.root):
                islands = island_node.item
                # iter each island in islands, there is only 1 island in the list so O(1)
                for island in islands: 
                    available_pirates = min(remaining_crew, island.marines)
                    # calculates profitability O(1)
                    money_earned += self.calculate_profitability(island, available_pirates)
                    remaining_crew -= available_pirates

                # if no crew left, no attack
                if remaining_crew <= 0:
                    break

            # add the result into the list
            profit_list.append(math.ceil(money_earned))

        return profit_list


    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Update the given island marines and money.

        :Args: 
        island: the island to be updated
        new_money: the money value to be updated into the island
        new_marines: the number of marines to be updated into the island
    
        :Raise:
        KeyError: if the island is not existing in the tree

        :Return: None

        :Complexity:
        Best Case: O(1) if the island is found at the first place (root)
        Worst Case: O(log N) N is the number of islands,
        to traverse through the tree, it loops depth of the tree which is log N
        """
        try:
            # try to get the item with the original key to check if it is existing
            update_island = self.bst.__getitem__(island.marines/island.money)
        except KeyError:
            # is not raise KeyError
            raise KeyError("Island not found")
        
        for island in update_island: # O(1) as there will only have one island object
            island.marines = new_marines
            island.money = new_money

        # # Search for the island based on the unique key
        # island_list = self.bst.root

        # if island_list is not None:
        #     # Iterate through the list of islands to find the matching island
        #     for existing_island in island_list.item:
        #         if existing_island == island:
        #             # Update the island's properties
        #             existing_island.money = new_money
        #             existing_island.marines = new_marines
        #             break
    

    def calculate_profitability(self, island: Island, pirates: int) -> None:
        """
        Calculate the profit by sending a number of crews to the island.

        :Args:
        island: the island to be attacked
        pirates: the number of crews to be sent

        :Return: None

        :Complexity:
        Best/Worst Case: O(1)
        The calculation takes constant time as it does not depend on the number of islands or crew members.
        """
        # calculate the profit by using the given formula
        money = min((pirates / island.marines* island.money) , island.money)
        print(math.ceil(money))
        return math.ceil(money)
    
    