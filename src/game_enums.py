from enum import Enum
 
class MatchResponse(Enum):
    EXACT = "Exact Match"  
    PARTIAL = "Partial Match"
    NO_MATCH = "No Match"  
 
EXACT = MatchResponse.EXACT
PARTIAL = MatchResponse.PARTIAL
NO_MATCH = MatchResponse.NO_MATCH

class GameStatus(Enum):
    WON = 'WON'
    LOST = 'LOST'
    IN_PROGRESS = 'IN_PROGRESS'
    
WON = GameStatus.WON
LOST = GameStatus.LOST
IN_PROGRESS = GameStatus.IN_PROGRESS
