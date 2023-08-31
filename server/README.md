# Connect4 Backend

### Application flowchart
- Create a player
  - Creates a player if not existing
  - Shows player statistics (username, wins, losses, etc)
- Play a game
  - Creates a game room if non with only 1 player exists
    - Show a waiting for more players to join loader
  - if a game room exists with 1 player, join that room (add player to that game)
    - Start game for all players in the room (start game for the 2 players)