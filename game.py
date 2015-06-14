from config import getDefaultShips

class PlayerException(Exception):
    pass

class SystemException(Exception):
    pass

class Game(object):
    def __init__(self, player1, player2):
        (self.player1,
         self.player2) = self.players = (player1, player2)

        self.winner = None
        self.loser = None

        self.turns = None

    def playGame(self):
        try:
            # Step 1
            # Place ships for both players
            self._placeShips()

            # Step 2
            # Take turns blowing ships out of the water
            self._takeTurns()
            return self.winner, self.loser
        except Exception, e:
            print e
            if self.winner and self.loser:
                return self.winner, self.loser
            else:
                raise SystemException('Unable to determine winner')

    def _placeShips(self):
        for player in self.players:
            try:
                for i in xrange(100):
                    player._setShips(getDefaultShips())
                    player.placeShips()

                    if player._allShipsPlacedLegally():
                        for ship in player.ships:
                            print ship.locations
                        break
                else:
                    raise PlayerException("%s failed to place ships after 100 tries" % player.name)
            except:
                self.loser = player
                self.winner = self.player2 if player == self.player1 else self.player1
                raise

    def _takeTurns(self):
        count = -1
        while True:
            count += 1
            offensivePlayer = self.players[count % 2]
            defensivePlayer = self.players[(count + 1) % 2]

            shot = offensivePlayer.getShot()
            hit, sunk = defensivePlayer._checkIsHit(shot)

            if hit:
                offensivePlayer.shotHit(shot)
            else:
                offensivePlayer.shotMissed(shot)

            if sunk:
                offensivePlayer.shipSunk(sunk)
                done = defensivePlayer._checkAllShipsSunk()
                if done:
                    # Game Over

                    self.winner = offensivePlayer
                    self.loser = defensivePlayer
                    self.turns = count + 1 # 0 based count

                    self.winner.gameWon()
                    self.loser.gameLost()
