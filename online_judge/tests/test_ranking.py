import pytest
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ranking.leaderboard import Leaderboard, calculate_points

class TestRanking:
    def test_calculate_points(self):
        assert calculate_points("EASY") == 10.0
        assert calculate_points("MEDIUM") == 30.0
        assert calculate_points("HARD") == 50.0

    def test_leaderboard(self):
        lb = Leaderboard()
        now = datetime.utcnow()
        
        # User 1 solves Easy
        lb.update_score(1, "alice", 10.0, now)
        
        # User 2 solves Medium
        lb.update_score(2, "bob", 30.0, now + timedelta(minutes=5))
        
        # User 3 solves Hard
        lb.update_score(3, "charlie", 50.0, now + timedelta(minutes=10))
        
        # Charlie is 1st (50), Bob is 2nd (30), Alice is 3rd (10)
        top = lb.get_top_k(3)
        assert len(top) == 3
        assert top[0]["username"] == "charlie"
        assert top[1]["username"] == "bob"
        assert top[2]["username"] == "alice"
        
        # User 1 solves Hard + Medium -> Score = 10 + 50 + 30 = 90
        lb.update_score(1, "alice", 80.0, now + timedelta(minutes=15))
        
        top2 = lb.get_top_k(3)
        assert top2[0]["username"] == "alice"
        assert top2[1]["username"] == "charlie"
        assert top2[2]["username"] == "bob"
        
    def test_tiebreaker(self):
        lb = Leaderboard()
        now = datetime.utcnow()
        
        lb.update_score(1, "alice", 50.0, now + timedelta(minutes=10)) # Submitted later
        lb.update_score(2, "bob", 50.0, now) # Submitted earlier
        
        # Bob should be 1st because he reached the score first
        top = lb.get_top_k(2)
        assert top[0]["username"] == "bob"
        assert top[1]["username"] == "alice"
