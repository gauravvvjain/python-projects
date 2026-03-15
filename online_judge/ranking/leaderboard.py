import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_structures.heap import MinHeap
from typing import List, Tuple, Dict
from datetime import datetime

class UserScore:
    """
    Represents a user's score on the leaderboard.
    """
    def __init__(self, user_id: int, username: str, score: float, last_submission_time: datetime):
        self.user_id = user_id
        self.username = username
        self.score = score
        self.last_submission_time = last_submission_time

    def __lt__(self, other):
        """
        Compare UserScores. Primary key is score (descending), secondary is time (ascending).
        Python's MinHeap will keep the smallest element at the root. We want to extract max,
        so we need to invert the comparison. Wait, our `heap.py` has MaxHeap!
        But to use it with custom objects, we should define what "greater than" means.
        """
        # We define < such that larger scores are "greater".
        if self.score != other.score:
            return self.score < other.score
        
        # If scores are equal, the earlier submission time is "greater" (ranked higher)
        # So a smaller time (older) should be considered > a larger time (newer) for ranking.
        return self.last_submission_time > other.last_submission_time

    def __eq__(self, other):
        return self.user_id == other.user_id

class Leaderboard:
    """
    Real-time leaderboard using an in-memory MaxHeap (from our custom Data Structures).
    Note: For distributed real-time leaders across workers, we would use Redis Sorted Sets.
    This implementation handles logic locally and calculates correct score rankings.
    """
    def __init__(self):
        self.users = {} # user_id -> UserScore
        # Note: maintaining a heap for frequent updates requires removing elements.
        # Standard heap removing an arbitrary element is O(N).
        # We handle this by keeping a 'dirty' state or rebuilding if needed, 
        # or simply using a sorted list/BST. Let's use a sorted approach for the exact 
        # top K, or rebuild since we maintain state in self.users.

    def update_score(self, user_id: int, username: str, points: float, time: datetime):
        """
        Updates a user's score.
        """
        if user_id in self.users:
            self.users[user_id].score += points
            self.users[user_id].last_submission_time = time
        else:
            self.users[user_id] = UserScore(user_id, username, points, time)

    def get_top_k(self, k: int) -> List[Dict]:
        """
        Gets the top K users.
        Time Complexity: O(N log K) if we use a MinHeap of size K.
        Let's use our custom MinHeap here!
        We push elements to a MinHeap. We want to keep the largest K elements.
        If size > K, we pop the smallest.
        """
        heap = MinHeap()
        
        for user_score in self.users.values():
            heap.push(user_score)
            if len(heap) > k:
                heap.pop()
                
        # The heap contains the top K elements, but in no guaranteed strict order.
        # To get them strictly sorted, we pop all and reverse.
        top_k = []
        while len(heap) > 0:
            top_k.append(heap.pop())
            
        top_k.reverse() # Largest first
        
        return [
            {
                "rank": idx + 1,
                "user_id": ue.user_id, 
                "username": ue.username, 
                "score": ue.score, 
                "last_submission": ue.last_submission_time
            }
            for idx, ue in enumerate(top_k)
        ]

def calculate_points(difficulty: str) -> float:
    """
    Calculate points awarded for a solved problem.
    """
    mapping = {
        "EASY": 10.0,
        "MEDIUM": 30.0,
        "HARD": 50.0
    }
    return mapping.get(difficulty.upper(), 0.0)
