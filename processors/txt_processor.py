from typing import List


class TXTProcessor:
    def getDates(self) -> List[str]:
        file = open('data/dates.txt', 'r')
        dates = [line[:-1] for line in file.readlines()]
        file.close()
        return dates
