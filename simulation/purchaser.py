import random

from simulation.option_pool import OptionPool


class Purchaser:
    def __init__(self, id: int, option_pool: OptionPool) -> None:
        self.id = id
        self.option_pool = option_pool
        self.profit = 0

    def start_epoch(self, date: str) -> None:
        self.option_pool.purchase_call_option(
            date,
            self.id,
            self.generate_random_option_index()
        )

    def end_epoch(self, date: str) -> None:
        self.option_pool.exercise_call_option(
            date,
            self.id
        )

    def generate_random_option_index(self) -> float:
        '''
        Randomly pick a number from [0, 58) to 
        '''
        return random.randrange(58)
