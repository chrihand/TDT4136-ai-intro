try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q


def heuristic(node, end_node):
    return abs(node.x - end_node.x) + (node.y - end_node.y)


def run_astar(board):
    if not isinstance(board, list):
        return "Board must be a list"

    priority_queue = Q.PriorityQueue()
    start_node = ""
    end_node = ""
    board_width = len(board[0])
    board_height = len(board)


    for i in board:
        for j in i:
            if j.start:
                start_node = j
            if j.end:
                end_node = j

    priority_queue.put(start_node, 0)

    node_from = {}
    total_cost = {}
    node_from[start_node] = None
    total_cost[start_node] = 0

    while not priority_queue.empty():
        current_node = priority_queue.get()

        if current_node == end_node:
            break

        get_adjacent_nodes(current_node, board_width, board_height)


def get_adjacent_nodes(current_node, board_w, board_h):
    nodes = []
    print(current_node, board_w, board_h)
    if current_node.x > 0:
        nodes.append(current_node.x - 1)

    if current_node.y > 0:
        nodes.append(current_node.y - 1)

    if current_node.x < board_h:
        nodes.append(current_node.x + 1)

    print(current_node.y)
    print(board_h)
    if current_node.y < board_w:
        nodes.append(current_node.y + 1)

    print(nodes)



class Node(object):

    def __init__(self, x, y, character):
        self.x = x
        self.y = y
        self.character = character
        self.start = character == "A"
        self.end = character == "B"
        self.walkable = character != "#"

    def __str__(self):
        return 'Node(%i, %i, %s): %s' % (self.x, self.y, self.character, self.walkable)
        #return self.character

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

    start = ""
    end = ""

    #print(board)

    run_astar(board)
