import socket
import sys

def new_board():
    return [[None, None, None], [None, None, None], [None, None, None]]

def render(board):
    print('   0 1 2\n   -----')
    for row in range(3):
        print(row, end="| ")
        for i in board[row]:
            if i:
                print(i, end=" ")
            else:
                print(" ", end=" ")
        print("|")  
    print("   -----")

def get_move():
    while True:
        try:
            return (
                int(input("What is your move's row: ")),
                int(input("What is your move's column: "))
            )
        except:
            print("Enter a valid input!!")

def is_valid_move(row, col, board):
    return 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] is None

def make_move(board, move_coords, player):
    copy = [*board]
    copy[move_coords[0]][move_coords[1]] = player
    return copy

def get_winner(board):
    # Getting all the straigt lines in a board
    lines = [
            *board,                                                         # Horizontal
            *[[board[j][i] for j in range(3)] for i in range(3)],           # Vertical
            [board[i][i] for i in range(3)],                                # Diagonal 1
            [board[i][j] for i, j in zip(range(0, 3), range(2, -1, -1))],   # Diagonal 2
    ]
    for line in lines:
        # check if all the els are same and none of them is "None"
        if None not in line and len(set(line)) == 1:
            return line[0]
    return None

def is_board_full(board):
    for row in board:
        if None in row:
            return False
    return True

def host_game(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, _ = s.accept()
    return conn, s
    
def connect_game(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def play_game(board, player):
    while True:
        move_co_ords = get_move()
        if is_valid_move(*move_co_ords, board):
            board = make_move(board, move_co_ords, player)
            render(board)
            break
        else:
            print("\nPlease enter a valid move\n")
            continue
    return board

def is_game_over(board, player):
    winner = get_winner(board)
    if winner:
        if winner == player:
            print("\nYou Won!!")
        else:
            print("\nYou Lose!!")
        return True
    if is_board_full(board):
        print("\nIt's a draw!!")
        return True
    return False

def update_board(client):
    print("\nOpponent's Turn")
    data = client.recv(5000)
    if not data:
        sys.exit("Connection error!!")    
    board = eval(data.decode("utf-8"))
    render(board)
    return board

def main():
    HOST = "192.168.0.108"
    PORT = 8080
    board = new_board()
    if input("Do you want to host a game or connect to a game? (h, c): ") == "h":
        client, server = host_game(HOST, PORT)
        player = "X"
        render(board)
        for i in range(1, 10):
            if i % 2:
                board = play_game(board, player)
                client.sendall(str(board).encode("utf-8"))
            else:
                board = update_board(client)

            if is_game_over(board, player):
                break
        
        server.close()
        client.close()
    else:
        client = connect_game(HOST, PORT)
        player = "O"
        render(board)
        for i in range(1, 10):
            if not i % 2:
                board = play_game(board, player)
                client.sendall(str(board).encode("utf-8"))
            else:
                board = update_board(client)

            if is_game_over(board, player):
                break
        
        client.close()

if __name__ == "__main__":
    main()
