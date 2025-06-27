import sys
import random
from monte_carlo_tree_search import MCTS, Node #Uses https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1 - Thanks Luke Harold Miles!

class FateStonesBoard(Node):

    def __init__(self, playerDiePool, opponentDiePool, playerSelection, opponentSelection, playerValue, opponentValue):
        self.playerDiePool = playerDiePool
        self.opponentDiePool = opponentDiePool
        self.playerSelection = playerSelection
        self.opponentSelection = opponentSelection
        self.playerValue = playerValue
        self.opponentValue = opponentValue

    def find_children(self):
        #print("Finding children for:", self)
        boardStates = set()
        if self.is_terminal():
            return boardStates
        if self.playerSelection is None:
            for playerSelectionIndex in range(len(self.playerDiePool)):
                for opponentSelectionIndex in range(len(self.opponentDiePool)):
                    newBoardState = FateStonesBoard(self.playerDiePool, self.opponentDiePool, playerSelectionIndex, opponentSelectionIndex, None, None)
                    #print(f"Add board state {newBoardState}")
                    boardStates.add(newBoardState)
            return boardStates
        if self.playerValue is None:
            for playerRolledFace in range(6):
                for opponentRolledFace in range(6):
                    if self.playerSelection >= len(self.playerDiePool):
                        print(f"ERROR: trying to evaluate die {self.playerSelection} when there are only {len(self.playerDiePool)} dice")
                        quit()
                    if self.opponentSelection >= len(self.opponentDiePool):
                        print(f"ERROR: trying to evaluate die {self.opponentSelection} when there are only {len(self.opponentDiePool)} dice")
                        quit()
                    playerValue = int(self.playerDiePool[self.playerSelection][playerRolledFace])
                    opponentValue = int(self.opponentDiePool[self.opponentSelection][opponentRolledFace])
                    newBoardState = FateStonesBoard(self.playerDiePool, self.opponentDiePool, self.playerSelection, self.opponentSelection, playerValue, opponentValue)
                    #print(f"Add board state {newBoardState}")
                    boardStates.add(newBoardState)
            return boardStates
        #There was a tie, so we need to roll-off. If playerValue and playerSelection are set, and its not a tie, then we should be in the terminal state
        if self.playerValue == self.opponentValue:
            if(len(self.playerDiePool) <= 0 or len(self.opponentDiePool) <= 0):
                print (f"Error, empty die pools attempting to be rolled out")
                quit()
            if len(self.playerDiePool) <= self.playerSelection:
                print (f"Error, trying to pop {self.playerSelection} from pool with only {len(self.playerDiePool)} values")
                quit()
            if len(self.opponentDiePool) <= self.opponentSelection:
                print (f"Error, trying to pop {self.opponentSelection} from pool with only {len(self.opponentDiePool)} values")
                quit()
            playerNewDiePool = self.playerDiePool.copy()
            playerNewDiePool.pop(self.playerSelection)
            opponentNewDiePool = self.opponentDiePool.copy()
            opponentNewDiePool.pop(self.opponentSelection)
            newBoardState = FateStonesBoard(playerNewDiePool, opponentNewDiePool, None, None, None, None)
            boardStates.add(newBoardState)
        return boardStates

    def find_random_child(self):
        if self.is_terminal():
            return None
        boards = self.find_children()
        if boards is None or len(boards) == 0:
            return None
        setIndex = random.randrange(len(boards))
        checkIndex = 0
        for boardOption in boards:
            if checkIndex == setIndex:
                return boardOption
            checkIndex+=1
        return None

    def is_terminal(self):
        if len(self.playerDiePool) <= 0: 
            return True
        if self.playerValue is None or self.opponentValue is None:
            return False
        return self.playerValue != self.opponentValue

    def reward(self):
        if not self.is_terminal():
            raise RuntimeError(f"reward called on nonterminal board {self}")
        if len(self.playerDiePool) <= 0: #We ran out of dice, it's a tie
            return .5
        if self.playerValue > self.opponentValue:
            return 1 #Could consider just returning playValue - opponentValue, but I'm using the "it's not how, it's how many" approach
        elif self.opponentValue:
            return 0
        elif self.playerValue == self.opponentValue:
            return .5
        return 0
    
    def __hash__(self):
        val = ""
        for die in self.playerDiePool:
            val += die
        for die in self.opponentDiePool:
            val += die
        if self.playerSelection is not None:
            val += str(self.playerSelection)
        else:
            val += "3"
        if self.opponentSelection is not None:
            val += str(self.opponentSelection)
        else:
            val += "3"
        if self.playerValue is not None:
            val += str(self.playerValue)
        else:
            val += "7"
        if self.opponentValue is not None:
            val += str(self.opponentValue)
        else:
            val += "7"
        return int(val)
    
    def __eq__(node1, node2):
        return hash(node1) == hash(node2)
    
    def __str__(self):
        resultLog = ""
        for player1Index in range(3):
            if(len(self.playerDiePool) > player1Index):
                resultLog += self.playerDiePool[player1Index]
            resultLog += ","
        for player2Index in range(3):
            if(len(self.opponentDiePool) > player2Index):
                resultLog += self.opponentDiePool[player2Index]
            resultLog += ","
        if self.playerSelection is not None:
            resultLog += str(self.playerSelection) + ", " + str(self.opponentSelection) + ","
        else:
            resultLog += ",,"
        if self.playerValue is not None:
            resultLog += str(self.playerValue) + ", " + str(self.opponentValue) + ","
        else:
            resultLog += ",,"
        resultLog += str(self.is_terminal())
        return resultLog

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

def getSelectionFromRobotRandomly(playerDiePool):
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

def getSelectionFromRobotMCTS(playerDiePool, opponentDiePool):
    tree = MCTS()
    board = FateStonesBoard(playerDiePool, opponentDiePool, None, None, None, None)
    for rolloutIndex in range(10):
        #print (f"Rolling out {rolloutIndex}")
        tree.do_rollout(board)
    board = tree.choose(board)
    return board.playerSelection

def getSelectionFromRobot(playerDiePool, opponentDiePool, useMCTS):
    return getSelectionFromRobotMCTS(playerDiePool, opponentDiePool) if useMCTS else getSelectionFromRobotRandomly(playerDiePool)

def playRound(playerOneDice, playerOneHuman, playerTwoDice, playerTwoHuman, resultsPath, numMCTS):
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
    playerOneChoice = getSelectionFromHuman(playerOneDice, playerTwoDice) if playerOneHuman else getSelectionFromRobot(playerOneDice, playerTwoDice, numMCTS > 0)
    playerTwoChoice = getSelectionFromHuman(playerTwoDice, playerOneDice) if playerTwoHuman else getSelectionFromRobot(playerTwoDice, playerOneDice, numMCTS > 1)

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
        playRound(playerOneDice, playerOneHuman, playerTwoDice, playerTwoHuman, resultsPath, numMCTS)
    else:
        resultText = "Player 1 won with " + str(playerOneResult) + " over P2's " + str(playerTwoResult) if playerOneResult > playerTwoResult else "Player 2 won with " + str(playerTwoResult) + " over P1's " + str(playerOneResult)
        print(resultText)

def populateDiePool(playerDiePool, sourceDiePool):
    playerDiePool.append(sourceDiePool.pop(random.randrange(len(sourceDiePool))))

def runGameEpisode(faceOptions, playerOneHuman, playerTwoHuman, resultsPath, numMCTS):
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
    playRound(playerOneDice, playerOneHuman, playerTwoDice, playerTwoHuman, resultsPath, numMCTS)

numHumans = 2
numGames = 1
outputPath = ""
numMCTS = 0
if len(sys.argv) >= 3:
    numHumans = int(sys.argv[2])
if len(sys.argv) >= 4:
    numGames = int(sys.argv[3])
if len(sys.argv) >= 5:
    outputPath = sys.argv[4]
if len(sys.argv) >= 6:
    numMCTS = int(sys.argv[5])
for _ in range(numGames):
    runGameEpisode(sys.argv[1], numHumans > 0, numHumans > 1, outputPath, numMCTS)