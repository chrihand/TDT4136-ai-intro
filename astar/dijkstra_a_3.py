# Dijkstra algorithm, difference is that the herustic is not calculated
# Also shows which nodes has been opened and which is closed.

import heapq


# The main dijkstra algorithm
def run_dijkstra(board, start_node, end_node):

    if not isinstance(board, list):  # Make sure the board is represented as a list
        return "Board must be a list"

    board_width = len(board[0])  # Get the width of the board
    board_height = len(board)  # Get the height of the board

    closed_node = set()  # The closed nodes

    priority_queue = []   # The opened nodes
    heapq.heapify(priority_queue)
    heapq.heappush(priority_queue, (start_node.f, start_node))

    came_from = {}  # The current road from start to end

    start_node.g = 0
    start_node.f = start_node.g

    while priority_queue:  # Start searching if the opened nodes is not empty
        current_node = heapq.heappop(priority_queue)[1]  # Chose a current node, based on the node with the lowest f value in the opened queue

        if current_node == end_node:  # If the current node is also the end node, then the board should be drawn and stop searching
            display_path(came_from, current_node, board, priority_queue, closed_node)
            break

        closed_node.add(current_node)

        adj_nodes = get_adjacent_nodes(current_node, board_width, board_height, board)

        for adj_node in adj_nodes:  # If the adjacent node is already closed, then don't calculate it again
            if adj_node in closed_node:
                continue

            temp_gscore = current_node.g + adj_node.cost  # Set a tentativ g score for the adjacent node

            if adj_node.walkable and adj_node not in came_from:  # Update the node if it is walkable and not already update
                came_from[adj_node] = current_node
                adj_node.g = temp_gscore
                adj_node.f = adj_node.g

                heapq.heappush(priority_queue, (adj_node.f, adj_node)) # Add the node to the open queue

            elif temp_gscore >= adj_node.g:  # If tentativ cost is less than the g score, then choose new node
                continue


def get_adjacent_nodes(current_node, board_w, board_h, board):  # Find the adjacent nodes from the current
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


def display_path(came_from, current, board, opend, closed):  # Make the board with colors and O for the nodes in the path
    node_path = [current]
    board_string = ""
    while current in came_from.keys():  # Find all nodes in the path and add to a list
        current = came_from[current]
        node_path.append(current)

    for node in node_path:  # Change colors for the path
        if node.character == "A":
            node.character = color(32, "A")
        elif node.character == "B":
            node.character = color(32, "B")
        else:
            node.character = color(31, "O")

    for node in opend:  # Change character if node is in open
        if node not in node_path:
            node[1].character = color(34, "*")

    for node in closed:  # Change character if node is closed
        if node not in node_path:
            node.character = color(36, "x")

    for nodes in board:  # Change the board to a string in stead of list
        for node in nodes:
            board_string += node.character
        board_string += "\n"

    print(board_string)


def color(colors, string):  # Change colors of nodes
    return "\033[" + str(colors) + "m" + string + "\033[0m"


def read_board(board_id='1-1'):  # Read the board and appends to lists, finds the start and end nodes
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


class Node(object):  # Create a node object

    def __init__(self, x, y, character):  # Set and create different values for object
        self.x = x
        self.y = y
        self.character = character
        self.start = character == "A"
        self.end = character == "B"
        self.walkable = character != "#"
        self.f = 0
        self.g = 0
        self.cost = 0
        self.set_node_cost()

    def __lt__(self, other): # Compare the current value with other, less than
        return self.f < other.f

    def __gt__(self, other):  # Compare the current value with other, greater than
        return self.f > other.f

    def __str__(self):
        # return 'Node(%i, %i, %s, %i, %i, %i): %s' % \
        # (self.x, self.y, self.character, self.f, self.g, self.h, self.walkable)
        # return '%s: %i' % (self.character, self.f)
        return self.character

    def __repr__(self):
        return self.__str__()

    def set_node_cost(self): # Set the cost depending on the character
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

if __name__ == "__main__":  # Create board and run dijkstra
    board_data = read_board(board_id="2-4")  # run_board returns board, start, end as a tuple
    run_dijkstra(*board_data)  # tuple unpacking, spread tuple as arguments
