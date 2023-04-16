# Global values
available_moves=list(range(1,10))
completed_moves_p1=[]
completed_moves_p2=[]
board='1 ┃ 2 ┃ 3\n━━━━━━━━━━\n4 ┃ 5 ┃ 6\n━━━━━━━━━━\n7 ┃ 8 ┃ 9'
gameon=False
french=False
win_list=[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]
turn=0

def display_board():
# Function that visualises the initial grid.
    print('TIC TAC TOE')
    print(board)

def lang_check():
#Function that permits the user to choose a language.
    global french
    ans=input('Type E for English. Ecrivez F pour français.')
    ans=ans.lower()
    while ans!='e' and ans!='f':
        ans=input('Invalid input. Type E for English. Ecrivez F pour français.')
        ans=ans.lower()
    else:
        if ans=='e':
            return print("English selected.")
        else:
            french=True
            return print('Français a été choisi.')

def begin_game():
# Asks the player if they want to play.
    ans='Pika!'
    global gameon
    if not french:
        while ans.lower()!='yes' and ans.lower()!='no':
            ans=input('Would you like to play a game? Enter yes or no.')
            ans=ans.lower()
        else:
            if ans=='yes':
                gameon=True
                print("Let's get cracking, shall we?")
            else:
                print('Alrighty, no tic tac toe for you.')
    else:
        while ans.lower()!='oui' and ans.lower()!='non':
            ans=input('Voulez-vous jouer? Ecrivez oui ou non.')
            ans=ans.lower()
        else:
            if ans=='oui':
                gameon=True
                print("On est va!")
            else:
                print("Er...c'est triste, mais comme vous voulez, pas des jeu pour vous.")

def player1():
    display_board()
    if french:
        choice=input('Joueur 1 : veuillez entrer un nombre entre 1 et 9 que vous voyez sur le plateau: ')
    else:
        choice=input('Player 1: please enter a number between 1-9 that you see on the board: ')
    while choice.isdigit()==False or int(choice) not in available_moves:
        if french:
            choice=input('Joueur 1 : veuillez entrer un nombre entre 1 et 9 que vous voyez sur le plateau: ')
        else:
            choice=input('Player 1: please enter a number between 1-9 that you see on the board: ')
    else:
        global board
        board=board.replace(choice, 'X')
        choice=int(choice)
        available_moves[choice-1]='X'
        completed_moves_p1.append(choice)
        print(board)

def player2():
    display_board()
    if french:
        choice=input('Joueur 2 : veuillez entrer un nombre entre 1 et 9 que vous voyez sur le plateau: ')
    else:
        choice=input('Player 2: please enter a number between 1-9 that you see on the board: ')
    while choice.isdigit()==False or int(choice) not in available_moves:
        if french:
            choice=input('Joueur 2 : veuillez entrer un nombre entre 1 et 9 que vous voyez sur le plateau: ')
        else:
            choice=input('Player 2: please enter a number between 1-9 that you see on the board: ')
    else:
        global board
        board=board.replace(choice, 'O')
        choice=int(choice)
        available_moves[choice-1]='O'
        completed_moves_p1.append(choice)
        print(board)

def win_check():
    global gameon
    for win in win_list:
        if all(num in completed_moves_p1 for num in win):
            gameon=False
            if french:
                print('Joueur 1 a gagné!')
            else:
                print('Player 1 wins!') 
                
        elif all(num in completed_moves_p2 for num in win):
            gameon=False
            if french:
                print('Joueur 2 a gagné!')
            else:
                print('Player 2 wins!')
                
        elif len(completed_moves_p1+completed_moves_p2)==9:
            gameon==False
            if french:
                print("C'est un match nul!")
                
            else:
                print("It's a draw!")
        else:
            pass

display_board()

lang_check()

begin_game()

while gameon:
    turn+=1
    player1()
    win_check()
    if not gameon:
        break
    else:
        player2()
        win_check()

if french:
        print("Merci d'avoir joué mon jeu!")
else:
        print("Thanks for playing my game!")