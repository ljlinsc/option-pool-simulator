class Epoch:
    def __init__(self, epoch: int, total_value_locked: float, total_profit: float) -> None:
        self.epoch = epoch
        self.total_value_locked = total_value_locked
        self.total_profit = total_profit
