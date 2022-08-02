def new_board():
    return [[None, None, None], [None, None, None], [None, None, None]]

def render(board):
    print('   0 1 2\n   -----')
    for row in range(3):
        print(row, end="| ")
        for i in board[row]:
            if i is not None:
                print(i, end=" ")
            else:
                print(" ", end=" ")
        print("|")  
    print("   -----")

def get_move():
    return (
        int(input("What is your move's row: ")),
        int(input("What is your move's column: "))
    )


def make_move(board, move_coords, player):
    copy = [*board]
    if copy[move_coords[0]][move_coords[1]] is not None:
        print(f"Exception: Can't make move {move_coords}, square already taken!")
        quit(1)

    copy[move_coords[0]][move_coords[1]] = player
    return copy

def get_winner(board):
    # Getting all the straigt lines in a board
    lines = [*board] # Horizontal
    lines.extend([[board[j][i] for j in range(3)] for i in range(3)]) # Vertical
    lines.append([board[i][i] for i in range(3)]) # Diagonal
    for line in lines:
        # check if all the els are same
        if None not in line and len(set(line)) == 1:
            return line[0]
    return None

def is_board_full(board):
    for row in board:
        if None in row:
            return False
    return True

def main():
    # Need to run this game on a loop
    board = new_board()
    current_player = "X"
    while True:
        render(board)
        move_co_ords = get_move()
        board = make_move(board, move_co_ords, current_player)
        
        winner = get_winner(board)
        if winner is not None:
            print(f"\nWinner is {winner}")
            break
        
        if is_board_full(board):
            print("\nIt's a draw!!")
            break
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
