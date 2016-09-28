
def run_astar(board):
    if not isinstance(board, list):
        return "Board must be a list"


class Node(object):

    def __init__(self, x, y, character):
        self.x = x
        self.y = y
        self.character = character
        self.start = character == "A"
        self.end = character == "B"
        self.walkable = character != "#"

    def __str__(self):
        #return 'Node(%i, %i, %s): %s' % (self.x, self.y, self.character, self.walkable)
        return self.character

    def __repr__(self):
        return self.__str__()


def read_board(board_id='1-1'):
    file_name = 'boards/board-%s.txt' % board_id
    board = []

    with open(file_name) as f:
        for x, line in enumerate(f.readlines()):
            temp_line = []
            for y, ch in enumerate(line):
                temp_node = Node(x, y, ch)
                temp_line.append(temp_node)
            board.append(temp_line)

    return board

if __name__ == "__main__":
    board = read_board(board_id="1-1")
    print(board)

    run_astar(board)