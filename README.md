# connect4-game
Play the Connect-Four game, but with a difference. Pieces stack ~~at the bottom~~ on the right side of the board. Also threw in a rudimentary chat system :)

### Features
- Plays the connect-four game (colorful board)
- Each player takes a turn
- At the end of the game, saves the game to a relational database alongside the winner (for game history)
- Chat with opponent

### To Run
The Frontend was built with React, while the Backend was built with Python

##### Frontend
- Install packages
- Run the server
```
$ npm i
$ npm start
```

##### Backend
- Activate a virtualenv
- Install requirements
- Copy .env.sample to .env
- Create a database (credentials are in .env.sample)
- Run migrations
- Run the server
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

Open a two browsers (player A vs player B), create a player (this creates/joins a room) and play against an opponent

### Improvements
- Add "waiting for opponent to join room" feedback to user
- Save the state of the board at the end of the game (for showing the finish state/replay)
- Dockerize the application
- Add a Makefile for simple, easier setup
- Improve chat design
- Increase test coverage
