# FateStones

## Elements

### Dice
Represented as a 6-digt number, with each digit's value (1-6) representing the number of pipes on a face. No digit may be higher in value than a digit to the right of it. So `123456` is a standard die. Other valid dice would be `111111`, `113355`, `234566`, etc. `654321` is not valid, as there are digits whose values are less than those to their left.

There are 462 unique dice available in this set.

### The Game
1. Each player draws 3 dice from a bag. 
2. The players can inspect each die they and their opponent have.
3. Each player secretly selects a die to roll. They reveal their selections simultaneously.
4. The players roll their dice, and compare results. Whomever has the higher result wins.
5. If the players die, the repeat steps 3 and 4 until a winner is determined, or the players run out of dice.
6. If the players run out of dice, then the round is a scratch. Restart the game from step 1.

## Story

### Input
- 3 dice, encoded as mentioned above, representing the player's dice
- 3 dice, encoded as mentioned above, representing the player's opponent's dice

### Output
- The encoding of a die which matches one of the players three dice
- The encoding of a die which matches one of the opponents three dice
Hm... This will encourage the model to pick the worst die from its opponents set. That's unlikely to yield cood results.

### Reward function
- Roll the players and the opponents dice. The reward is `player_value - opponent_value`.