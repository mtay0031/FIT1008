from island import Island
from data_structures.bst import *
from data_structures.heap import MaxHeap
from data_structures.referential_array import ArrayR

class Mode2Navigator:
    """
    Mode2Navigator is a class designed for simulating pirate battles in the Davy Back Fight. It manages the distribution 
    of crews across islands to maximize profits. The class uses a combination of arrays and a max heap data structure to 
    efficiently make decisions based on island properties and the number of pirate captains involved.

    Data Structures used:
    - MaxHeap: Used to keep track of islands with their corresponding scores.
      By using MaxHeap, it allows us to efficiently select the island with the highest score. 
      In Mode2, this is crucial because we want to choose the most profitable island for each pirate captain.
      Insertion and deletion of the maximum element, have a time complexity of O(log N), where N is the number of islands. 
      This is much more efficient than traverse the entire list of islands to find the best option.

    - ArrayR: Utilized for temporary storage of scores and island data.
      It is designed to store tuples of scores and islands, providing an organized and memory-efficient way to manage these pairs.

    Example:
    In the Davy Back Fight, you have a crew of pirates and a list of islands with varying marines and money. Your goal is 
    to simulate a day of battle, where you distribute your crew to different islands to maximize your profits. Mode2Navigator 
    helps you achieve this by calculating island scores, choosing the most profitable actions, and updating island properties 
    accordingly.
    
    n_pirates = 5
    islands = [Island("A", 80, 10), Island("B", 150, 15), Island("C", 250, 30)]
    crew = 200

    when add_islands(), 
    the island list from [] to 
    [Island(name='A', money=80, marines=10), Island(name='B', money=150, marines=15), Island(name='C', money=250, marines=30)]
    
    when simulate_day(),
    the score array after the first iteration to calculate the optimum score
    showing (score we can get, island to attack)
    [(460.0, Island(name='A', money=80, marines=10)), (520.0, Island(name='B', money=150, marines=15)), (590.0, Island(name='C', money=250, marines=30))]

    the second iteration for every pirates to choose island to attack, the heap retrieves the island with maximum score every time
    (590.0, Island(name='C', money=250, marines=30)) -> (520.0, Island(name='B', money=150, marines=15)) -> (460.0, Island(name='A', money=80, marines=10))
    -> (400, Island(name='B', money=0.0, marines=0)) -> (400, Island(name='A', money=0.0, marines=0))

    finally, the island each pirates choose is as the result
    [(Island(name='C', money=0.0, marines=0), 30), (Island(name='B', money=0.0, marines=0), 15), (Island(name='A', money=0.0, marines=0), 10), 
    (Island(name='B', money=0.0, marines=0), 0), (Island(name='A', money=0.0, marines=0), 0)]
    The order of the list is  sequentially following of the order. (The plundered island, sent crew (0 if no island was selected))

    Complexity: see each method doc string
    """
    def __init__(self, n_pirates: int):
        """
        Initialise the attributes in Mode 2 Navigator.

        :Args:
        n_pirates: the number of pirates in the Davy Back Fight

        :Complexity:
        Best/Worst Case: O(1) only involves variable assignment as constant time operations 
        """
        self.n_pirates = n_pirates
        self.islands = []  # Create a list to store the added islands 


    def add_islands(self, islands: list[Island]):
        """
        Add the given islands into the list of islands we have.

        :Args:
        islands: a list of islands to be added

        :Complexity:
        Best/Worst Case: O(N + I) N is the number of islands, I is the length of the input islands list
        We iter through the number of islands and the input islands, checking the existence of islands and add to the list 
        """
        # iter through the given islands list to add them one by one
        # O(I) I is the length of the given input islands
        for island in islands:

            # traverse to check if the island exists in the list 
            # O(N) N is the length of the self.islands list 
            if island not in self.islands:
                # add the island into the list self.islands O(1)
                self.islands.append(island)
            else:
                raise KeyError("Island exists")


    def simulate_day(self, crew: int) -> list[tuple[Island, int]]:
        """
        Simulate a day of the Davy Back Fight. 

        :Args:
        crew: the size of the crew for every pirate captain

        :Return: A list of tuples containing the choice made (Island object, number of crews sent to the islands)
        
        :Complexity:
        Best Case: O(N + C) N is the length of the islands list, C is the number of pirates
        when there is no need to swap in the heap when the islands are all getting to their right position
        Worst Case: O(N + C log N) N is the length of the islands list, C is the number of pirates
        we iterate through the list of island, iterate through the number of pirates, 
        construct the heap to get the most profitable match with highest score
        """
        chosen_island = []

        # store the computed score and the correspond island
        score_arr = ArrayR(len(self.islands))

        index = 0
        # iter through the list of islands O(N)
        for island in self.islands:
            if island.marines > 0:
                ratio = island.money / island.marines
            else:
                ratio = island.money # avoid zero division

            sent_crew = min(crew, island.marines) # compute the crew to be sent to the island O(1)

            remaining_crew = crew - sent_crew # the crew left after we sent the amount of crews to the island
            money_looted = ratio * sent_crew # calculate the money we can get if we sent the crew

            score = max(2 * remaining_crew, (2 * remaining_crew + money_looted)) # calculate the score 

            score_arr[index] = (score, island) # add the tuple into the array
            index += 1 

        # O(N log N) N is the length of the islands, we iterate N times to swap the islands through log N depth
        score_heap = MaxHeap.heapify(score_arr) # heapify to sort the islands according to the score we can get
        
        # loop for every pirates 
        for _ in range(self.n_pirates):
            # get the island with highest score pirate going to attack 
            # O(log N) sink until the bottom of heap, which is log N depth
            best_pirate = score_heap.get_max()
            best_score = best_pirate[0] # get the score from the arr
            best_island = best_pirate[1] # get the island object from the arr

            sent_crew = min(crew, best_island.marines) # get the crew to be sent 
            remaining_crew = crew - sent_crew
            money_looted = best_score - 2*remaining_crew 

            # update the islands money and marines after looted
            best_island.money -= money_looted 
            best_island.marines -= sent_crew

            chosen_island.append((best_island, sent_crew))

            # after the island has been looted
            if best_island.marines > 0:
                ratio = best_island.money/best_island.marines
            else:
                ratio = best_island.money
        
            sent_crew = min(crew, island.marines)
            remaining_crew = crew - sent_crew
            money_looted = ratio * sent_crew
            score = max(2*crew, (2*remaining_crew + money_looted))

            # add the island back to the heap for pirates to choose to attack
            score_heap.add((score, best_island)) 
            # O(log N) the islands rise to its correct position and traverse through the depth of heap log N 

        return chosen_island
            
