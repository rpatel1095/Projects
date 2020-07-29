# Author: Rajan Patel
import random
import time
import sys



# Print Player Stats after each game
def print_player_stats( wordToGuess, playerOneWinCount, playerOneLoseCount):
    print("The Correct word was: " , wordToGuess , "\n")
    print("----PLAYER STATS----------")
    print("| Player 1 Win Count: " , playerOneWinCount , "   |")
    print("| Player 1 Lose Count: " , playerOneLoseCount , "  |")
    print("--------------------------" + "\n")

# All console game statements for Hangman game
def print_game_statements(statement):

    if statement == 6:
        print(
        """
           ___
          |    |      
          |          
          |       
          |    
          |   
         _|_
        |   |______
        |          |
        |__________|
        """
        )

    elif statement == 5:
        print(
        """ 
           ___
          |    |      
          |    0      
          |        
          |    
          |   
         _|_
        |   |______
        |          |
        |__________|
        """
        )
    elif statement == 4:
        print(
        """ 
           ___
          |    |      
          |    0      
          |    |     
          |    
          |   
         _|_
        |   |______
        |          |
        |__________|
        """
        )
    elif statement == 3:
        print(
        """ 
           ___
          |    |      
          |    0      
          |   /|     
          |    
          |   
         _|_
        |   |______
        |          |
        |__________|
        """
        )

    elif statement == 2:
        print(
         """ 
           ___
          |    |      
          |    0      
          |   /|\     
          |    
          |   
         _|_
        |   |______
        |          |
        |__________|
        """
        )

    elif statement == 1:
        print(
        """ 
           ___
          |    |      
          |    0      
          |   /|\     
          |   /
          |   
         _|_
        |   |______
        |          |
        |__________|
        """
        )

    elif statement == 0:
        print(
        """
          .___.
       ,-^     ^-. 
      /           \     
     /             \    
    |   \/    \/    |
    |   /\    /\    |
     \             / 
      \     |     /
       |         |
       |         |
        \ +-+-+ /
         ^-----^
          R.I.P
    """
    )

    elif statement == 100:
        print(""" 
         __        _____ _   _ _   _ _____ ____  
         \ \      / /_ _| \ | | \ | | ____|  _ \ 
          \ \ /\ / / | ||  \| |  \| |  _| | |_) |
           \ V  V /  | || |\  | |\  | |___|  _ < 
            \_/\_/  |___|_| \_|_| \_|_____|_| \_\ 
         """ + "\n" )

#Prompt Player to select Category for word
def prompt_category():
    # Categories for hangman game and players
    category = ["colors", "countries"]

    # One Player Option Categories
    playerCategory = input("Choose a category [" + ", ".join(category) + "]" + " \n" + "Enter Category Here: ").lower()
    if playerCategory not in category:
        while True:
            playerCategory = input("Invalid Category! Choose from list of options [" + ", ".join(category) + "]" + "\n"
                                   + "Enter Category: ").lower()
            if playerCategory in category:
                break
    return playerCategory

#Prompt user for letter guessed and validate
def prompt_letter_guessed (aGuess):

    # Letter Guessed by Player
    letterGuessed = input("Player 1: Guess a Letter: ").lower()
    if letterGuessed.strip().lower() == "end":
        exit(0)
    while not letterGuessed.isalpha():
        letterGuessed = input("Player 1 didn't enter a letter" + "\n" + "Guess a Letter: ").lower()
        if letterGuessed.strip().lower() == "end":
            exit(0)
    while len(letterGuessed) > 1:
        letterGuessed = input("Player 1 entered more than one Character!" + "\n" + "Guess a Letter: ").lower()
        if letterGuessed.strip().lower() == "end":
            exit(0)

    while letterGuessed in aGuess:
        letterGuessed = input("Player 1, You already guessed this letter!" + "\n" +
                              "Guess another Letter: ").lower()
        if letterGuessed.strip().lower() == "end":
            exit(0)
        while not letterGuessed.isalpha():
            letterGuessed = input("Player 1 didn't enter a letter" + "\n" + "Guess a Letter: ").lower()
            if letterGuessed.strip().lower() == "end":
                exit(0)
        while len(letterGuessed) > 1:
            letterGuessed = input("Player 1 entered more than one Character!" + "\n" + "Guess a Letter: ").lower()
            if letterGuessed.strip().lower() == "end":
                exit(0)
    return letterGuessed

# Prompt user to play again
def prompt_play_again():
    playerYesOrNo = ["yes", "no"]
    print("Continue Playing?" + "\n" + "If you enter NO, Program will terminate and delete all stats")
    playerDecision = input("Yes or No: ").lower().strip()
    if playerDecision not in playerYesOrNo:
        while True:
            playerDecision = input("Invalid Response! Choose Yes or No: ")
            if playerDecision in playerYesOrNo:
                break
    if playerDecision.lower().strip() == "yes":
        return True
    print("Game has ENDED and Stats will be Reset")
    exit(0)


# Select Random Word from Category Chosen by player
def select_random_word(playerCategory):
    # Open Files and by Category and Store into array
    categoryPath = playerCategory + ".txt"

    with open(categoryPath, 'r') as categoryFile:
        listOfWords = [line.rstrip('\n') for line in categoryFile]

    # Choose word by random index
    lengthOfList = len(listOfWords)
    randomIndex = random.randint(0, lengthOfList - 1)

    # word to Guess One Player
    wordToGuess = listOfWords.pop(randomIndex).lower()

    return wordToGuess

def remove_invalid_chars(word, invalidChars):
    for char in invalidChars:
        if char in word:
            word.remove(char)

def initialize_game(playerCategory, numberOfLives):
    # Terminate Game and Round Rules
    print("\n" + "------------------GAME COMMANDS------------------")
    print("Type 'END' to Terminate Game and Remove All Stats")
    print("-------------------------------------------------")

    # Game Start Sequence
    print("Game will Start in:")
    startSequence = "3 2 1"
    for char in startSequence:
        sys.stdout.write(char + "\n")
        time.sleep(.4)
    print("You've chosen the category:", playerCategory + "\n" + "View Board and Guess letter below")
    print_game_statements(numberOfLives)

# Create letter board _ _ _ _ based on word chosen
def create_letter_board(wordToGuessPlayer, listOfAlpha):
    wordToGuessPlayer = wordToGuessPlayer.replace(" ", "   ")
    wordToGuessPlayer = wordToGuessPlayer.replace("'", "' ")
    wordToGuessPlayer = wordToGuessPlayer.replace("-", "- ")
    wordToGuessPlayer = wordToGuessPlayer.replace(",", ", ")
    wordToGuessPlayer = wordToGuessPlayer.replace("&", "& ")
    for x in range(len(listOfAlpha)):
        wordToGuessPlayer = wordToGuessPlayer.replace(listOfAlpha[x], '_ ')
    return wordToGuessPlayer

# Logic for hangman_game
def hangman_game():
    # Global Variables
    playing = True
    playerOneWinCount = 0
    playerOneLoseCount = 0

    while playing:
        playerCategory = prompt_category()

        # Max Number of lives
        numberOfLives = 6

        # Select Random word based on category chosen by player
        wordToGuess = select_random_word(playerCategory)

        # Change word to Guess to blank values
        wordToGuessPlayer = wordToGuess
        listOfAlpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                       'u', 'v', 'w', 'x', 'y', 'z']
        invalidChars = [' ', ',', '&', "'", '-', '/','(',')']
        aGuess = []
        firstCount = 1

        # List of letters in word to Guess
        lettersInWord = list(set(wordToGuess))
        remove_invalid_chars(lettersInWord, invalidChars)

        # Guess Checker to get letter index for program
        wordToGuessChecker = wordToGuess
        wordToGuessChecker = wordToGuessChecker.replace(" ", "   ")
        wordToGuessChecker = wordToGuessChecker.replace("'", "' ")
        wordToGuessChecker = wordToGuessChecker.replace("-", "- ")
        wordToGuessChecker = wordToGuessChecker.replace(",", ", ")
        wordToGuessChecker = wordToGuessChecker.replace("&", "& ")
        for x in range(len(listOfAlpha)):
            wordToGuessChecker = wordToGuessChecker.replace(listOfAlpha[x], listOfAlpha[x] + ' ').strip()

        # Start game
        initialize_game(playerCategory, numberOfLives)
        wordToGuessPlayer = create_letter_board(wordToGuessPlayer, listOfAlpha)
        print("\n" + wordToGuessPlayer + "\n")

        # While Player still has lives
        while numberOfLives !=0:

            # Letter Guessed by Player
            letterGuessed = prompt_letter_guessed(aGuess)
            firstCount += 1

            # Check if letter exists in list of letters of the word chosen
            if letterGuessed in lettersInWord:
                letterPosition = [let for let, char in enumerate(wordToGuessChecker) if char == letterGuessed]
                lettersInWord.remove(letterGuessed)
                listOfAlpha.remove(letterGuessed)
                for x in range(len(letterPosition)):
                    wordToGuessPlayer = list(wordToGuessPlayer)
                    wordToGuessPlayer[letterPosition[x]] = letterGuessed
                    wordToGuessPlayer = "".join(wordToGuessPlayer)
            else:
                listOfAlpha.remove(letterGuessed)
                numberOfLives -= 1
            aGuess.append(letterGuessed)
            print_game_statements(numberOfLives)

            # Print Round Stats: Number of Lives and Letters Guessed
            print("\n" + "-------------ROUND STATS-------------")
            print("| Number of Lives Remaining: ",numberOfLives)
            print("| Letters Guessed: " , " ".join(aGuess))
            print("-------------------------------------")
            print("\n" + wordToGuessPlayer + "\n")

            if numberOfLives > 0 and len(lettersInWord) == 0:
                numberOfLives = 100
                print_game_statements(numberOfLives)
                playerOneWinCount += 1
                print_player_stats(wordToGuess, playerOneWinCount, playerOneLoseCount)
                if prompt_play_again():
                    break

            if numberOfLives == 0:
                print_game_statements(numberOfLives)
                playerOneLoseCount += 1
                print_player_stats(wordToGuess, playerOneWinCount, playerOneLoseCount)
                if prompt_play_again():
                    break

hangman_game()
