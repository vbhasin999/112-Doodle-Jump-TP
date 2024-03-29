# 112-TURTLE-DUEL

## Project Description
A vertical scroller game where the player controls the main character to jump on randomly generated platforms while avoiding enemy characters and falling down (Similar to the popular game “Doodle Jump”).
All the files needed to run the game are in the folder, and they do not need to be initialized in any way. The game uses the external module "Pygame"
To play the game the file "TermProj.py" should be run in an editor
The main menu screen has four options "Play", "AI Mode", "Leaderboard" and "Quit". These options are to be navigated using the "Up" and "Down" arrow keys. The highlighted option is displayed in Yellow, and will be launched when the "Return" key is pressed.
The "Play" option starts the game. The main character is controlled using the arrow keys "Left", "Right" and "Up". If the player moves off the bounds of one side of the screen the character wraps around. The character automatically jumps when it collides with a platform. Moving platforms are generated at certain intervals and the player can interact with them in the same way as regular platforms. Enemy characters are generated at certain intervals and a collision with enemy characters will result in a "Game Over". Collision with enemy characters and falling off the bottom of the screen results in a "Game over". The user can press the Space bar to shoot projectiles which shoot upwards. These projectiles will eliminate enemy characters and add to the player's score.
When presented with the "Game Over" screen the user can see their score and the overall high score. They have two options: "Restart" and "Quit". Restarting launches the main game loop again and the "Quit" option takes the user back to the main menu.
The "AI Mode" option launches a mode where AI controls the character and plays the game. The AI detects the closest platform to jump to based on the characters current position but avoids platforms too high up the screen or too close to enemy characters. Note that restarting on the game over screen calls the normal game and to start the AI mode again the user should return to the main menu and access it from there.
The "Leaderboard" option allows the user to see the five highest scores that have been logged on the game. To go back to the main menu the user can click anywhere on the screen.
The "Quit" option quits the game.

## Demo
Watch the demo video [here](https://www.youtube.com/watch?v=GpPHu8sspqY&t=43s&ab_channel=VedantBhasin)
