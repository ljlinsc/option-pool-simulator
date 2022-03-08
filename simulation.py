import random
from typing import List

from liquidity_provider import LiquidityProvider
from option_pool import OptionPool
from transaction import Transaction

class Simulation:
    def __init__(self, num_liquidity_providers: int, underlying_asset: str, num_epochs: int) -> None:
        self.actors = []
        self.option_pool = OptionPool(underlying_asset)
        self.num_epochs = num_epochs

        # Create liquidity providers
        for i in range(num_liquidity_providers):
            self.actors.append(LiquidityProvider(self.option_pool))

    def run(self) -> List[Transaction]:
        transactions: List[Transaction] = []

        # Run simulation
        for epoch in range(self.num_epochs):
            random.shuffle(self.actors)
            for actor in self.actors:
                transactions.append(actor.start_epoch(epoch))

            random.shuffle(self.actors)
            for actor in self.actors:
                transactions.append(actor.end_epoch(epoch))

        return transactions
