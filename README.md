# Building-Blocks
For INNERVE 2021 CS/IT Game

# Mac (Tested on M1)
Make virtual env using `requirements.txt`, then use this command to create the executable - `pyinstaller -F --clean --noconfirm --add-data "templates:templates" --add-data "static:static" --add-data "database.ini:." app.py` 

# Running instructions
While pressing the `Shift` key, right click on the executable and select open. Select Run when prompted. Once the Terminal opens up, open Google Chrome and go to `http://localhost:5000`. This should start the game
