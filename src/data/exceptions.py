
class TicTacToeException(RuntimeError):
    pass

class InvalidBoard(TicTacToeException):
    pass

class InvalidSymbolBoard(InvalidBoard):
    pass

class InvalidLinesSize(InvalidBoard):
    pass

class InvalidMove(TicTacToeException):
    pass

class InvalidIndexBoard(InvalidMove):
    pass

class OccupiedCell(InvalidMove):
    pass

class GameOver(TicTacToeException):
    pass
