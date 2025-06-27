import sys
import random

def getSelectionFromHuman(playerDiePool, opponentDiePool):
    print("Your dice:")
    index = 1
    for die in playerDiePool:
        print("" + str(index) + ": " + die)
        index += 1
    print("\nOpponent dice:")
    for die in opponentDiePool:
        print(die)
    print("\nYour Selection:")
    selection = int(input())
    return selection-1

def getSelectionFromRobot(playerDiePool, opponentDiePool):
    max = 0
    maxIndicies = []
    for index in range(len(playerDiePool)):
        die = playerDiePool[index]
        value = 0
        for stringIndex in range(len(die)):
            value += int(die[stringIndex])
        if(value > max):
            maxIndicies = [index]
            max = value
        elif(value == max):
            maxIndicies.append(index)
    return maxIndicies[random.randrange(len(maxIndicies))]

def playRound(playerOneDice, playerOneHuman, playerTwoDice, playerTwoHuman, resultsPath):
    resultLog = ""
    if(len(playerOneDice) <= 0 or len(playerTwoDice) <= 0):
        print("No dice left to play! Scratch round")
        return
    for player1Index in range(3):
        if(len(playerOneDice) > player1Index):
            resultLog += playerOneDice[player1Index]
        resultLog += ","
    for player2Index in range(3):
        if(len(playerTwoDice) > player2Index):
            resultLog += playerTwoDice[player2Index]
        resultLog += ","
    playerOneChoice = getSelectionFromHuman(playerOneDice, playerTwoDice) if playerOneHuman else getSelectionFromRobot(playerOneDice, playerTwoDice)
    playerTwoChoice = getSelectionFromHuman(playerTwoDice, playerOneDice) if playerTwoHuman else getSelectionFromRobot(playerTwoDice, playerOneDice)

    resultLog += str(playerOneChoice) + ","
    resultLog += str(playerTwoChoice) + ","

    playerOneDie = playerOneDice.pop(playerOneChoice)
    playerTwoDie = playerTwoDice.pop(playerTwoChoice)

    print("Player 1 Die: " + str(playerOneDie))
    print("Player 2 Die: " + str(playerTwoDie))

    playerOneResult = int(playerOneDie[random.randrange(6)])
    playerTwoResult = int(playerTwoDie[random.randrange(6)])

    resultLog += str(playerOneResult) + ","
    resultLog += str(playerTwoResult) + "\n"

    if(len(resultsPath) > 0):
        with open(resultsPath, "a") as resultsFile:
                resultsFile.write(resultLog)

    print("Player 1 Result: " + str(playerOneResult))
    print("Player 2 Result: " + str(playerTwoResult))

    if playerOneResult == playerTwoResult:
        print("Players tied!")
        print("\n\nNext Round:")
        playRound(playerOneDice, playerOneHuman, playerTwoDice, playerTwoHuman, resultsPath)
    else:
        resultText = "Player 1 won with " + str(playerOneResult) + " over P2's " + str(playerTwoResult) if playerOneResult > playerTwoResult else "Player 2 won with " + str(playerTwoResult) + " over P1's " + str(playerOneResult)
        print(resultText)

def populateDiePool(playerDiePool, sourceDiePool):
    playerDiePool.append(sourceDiePool.pop(random.randrange(len(sourceDiePool))))

def runGameEpisode(faceOptions, playerOneHuman, playerTwoHuman, resultsPath):
    diceOptions=[]
    with open(faceOptions) as facesFile:
        for line in facesFile:
            dieType = line.strip().replace(" ", "")
            diceOptions.append(dieType)
    if len(diceOptions) < 6:
        print("Not enough dice to play")
        quit
    playerOneDice = []
    playerTwoDice = []
    for _ in range(3):
        populateDiePool(playerOneDice, diceOptions)
        populateDiePool(playerTwoDice, diceOptions)
    playRound(playerOneDice, playerOneHuman, playerTwoDice, playerTwoHuman, resultsPath)

numHumans = 2
numGames = 1
outputPath = ""
if len(sys.argv) >= 3:
    numHumans = int(sys.argv[2])
if len(sys.argv) >= 4:
    numGames = int(sys.argv[3])
if len(sys.argv) >= 5:
    outputPath = sys.argv[4]
for _ in range(numGames):
    runGameEpisode(sys.argv[1], numHumans > 0, numHumans > 1, outputPath)