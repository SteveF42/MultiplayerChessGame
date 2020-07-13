class Game:
    def __init__(self, gameId):
        self.players = [0,1]
        self.playerNames = [None,None]
        self.ready = False
        self.id = gameId
        self.playermoves = [None,None]
        self.player1Went = False
        self.player2Went = False
        self.quit = False

    def set_player_move(self,player,move):
        '''
        type player: int[0,1]
        type move: str(rock,paper,scissors)
        rtype: None
        '''
        self.playermoves[player] = move

        if player == 0:
            self.player1Went = True
        else:
            self.player2Went = True

    def both_players_went(self):
        return True if self.player1Went and self.player2Went else False

    def get_player_move(self,p):
        '''
        type p: int[0,1]
        rtype self.playermoves rock, paper, scissors
        '''
        return self.playermoves[p]

    def readyGame(self):
        self.ready = True
    
    def quitGame(self):
        self.quit = True
    
    def winner(self):
        '''
        rtype: range(0,1,3) 3 == tie
        '''
        if not self.ready:
            return

        p1 = str(self.playermoves[0])[0].lower()
        p2 = str(self.playermoves[1])[0].lower()

        if p1 == 'r' and p2 == 's':
            return 1
        elif p1 == 'p' and p2 == 'r':
            return 1
        elif p1 == 's' and p2 == 'p':
            return 1
        elif p2 == 'r' and p1 == 's':
            return 2
        elif p2 == 'p' and p1 == 'r':
            return 2
        elif p2 == 's' and p1 == 'p':
            return 2
        else:
            return 3
    
    def reset(self):
        self.player1Went = False
        self.player2Went = False
        self.playermoves = [None,None]
    
    