import heapq


def run_astar(board, start_node, end_node):
    if not isinstance(board, list):
        return "Board must be a list"

    board_width = len(board[0])
    board_height = len(board)

    closed_node = set()

    priority_queue = []
    heapq.heapify(priority_queue)
    heapq.heappush(priority_queue, (start_node.f, start_node))

    came_from = {}

    start_node.g = 0
    start_node.f = start_node.g + heuristic(start_node, end_node)

    while priority_queue:
        # print(priority_queue)
        current_node = heapq.heappop(priority_queue)[1]
        # print("curr", current_node)

        if current_node == end_node:
            display_path(came_from, current_node, board)
            break

        closed_node.add(current_node)
        # print(closed_node)

        adj_nodes = get_adjacent_nodes(current_node, board_width, board_height, board)
        # print(adj_nodes)

        for adj_node in adj_nodes:
            if adj_node in closed_node:
                continue

            temp_gscore = current_node.g + adj_node.cost

            if adj_node.walkable and adj_node not in came_from:
                # Update node cost
                came_from[adj_node] = current_node
                adj_node.g = temp_gscore
                adj_node.h = heuristic(adj_node, end_node)
                adj_node.f = adj_node.g + adj_node.h

                heapq.heappush(priority_queue, (adj_node.f, adj_node))

            elif temp_gscore >= adj_node.g:
                continue


def heuristic(node, end_node):
    return abs(node.x - end_node.x) + (node.y - end_node.y)


def get_adjacent_nodes(current_node, board_w, board_h, board):
    adj_nodes = []

    if current_node.x > 0:
        adj_nodes.append(board[current_node.x - 1][current_node.y])

    if current_node.y > 0:
        adj_nodes.append(board[current_node.x][current_node.y - 1])

    if current_node.x < board_h - 1:
        adj_nodes.append(board[current_node.x + 1][current_node.y])

    if current_node.y < board_w - 1:
        adj_nodes.append(board[current_node.x][current_node.y + 1])

    return adj_nodes


def display_path(came_from, current, board):
    node_path = [current]
    board_string = ""
    while current in came_from.keys():
        current = came_from[current]
        node_path.append(current)

    for node in node_path:
        if node.character == "A":
            node.character = color(32, "A")
        elif node.character == "B":
            node.character = color(32, "B")
        else:
            node.character = color(31, "O")

    for nodes in board:
        for node in nodes:
            # string1 = ' (%s %i) ' % (node.character, node.cost)
            board_string += node.character
        board_string += "\n"

    print(board_string)


def color(colors, string):
    return "\033[" + str(colors) + "m" + string + "\033[0m"


def read_board(board_id='1-1'):
    file_name = 'boards/board-%s.txt' % board_id
    board = []
    start, end = None, None

    with open(file_name) as f:
        for x, line in enumerate(f.readlines()):
            temp_line = []
            for y, ch in enumerate(line.rstrip()):
                temp_node = Node(x, y, ch)
                temp_line.append(temp_node)
                if temp_node.start:
                    start = temp_node
                if temp_node.end:
                    end = temp_node
            board.append(temp_line)
    # print(board)
    return board, start, end


class Node(object):

    def __init__(self, x, y, character):
        self.x = x
        self.y = y
        self.character = character
        self.start = character == "A"
        self.end = character == "B"
        self.walkable = character != "#"
        self.f = 0
        self.g = 0
        self.h = 0
        self.cost = 0
        self.set_node_cost()

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __str__(self):
        # return 'Node(%i, %i, %s, %i, %i, %i): %s' % \
        # (self.x, self.y, self.character, self.f, self.g, self.h, self.walkable)
        return '%s: %i' % (self.character, self.f)
        # return self.character

    def __repr__(self):
        return self.__str__()

    def set_node_cost(self):
        if self.character == "w":
            self.cost = 100
        elif self.character == "m":
            self.cost = 50
        elif self.character == "f":
            self.cost = 10
        elif self.character == "g":
            self.cost = 5
        elif self.character == "r":
            self.cost = 1
        else:
            self.cost = 1

if __name__ == "__main__":
    board_data = read_board(board_id="2-2")  # run_board returns board, start, end as a tuple
    run_astar(*board_data)  # tuple unpacking, spread tuple as arguments
