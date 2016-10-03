# A* algorithm for finding best path with obstacles and no cost on nodes

import heapq


# The main astar algorithm
def run_astar(board, start_node, end_node):

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
    start_node.f = start_node.g + heuristic(start_node, end_node)

    while priority_queue:  # Start searching if the opened nodes is not empty
        current_node = heapq.heappop(priority_queue)  # Chose a current node, based on the node with the lowest f value in the opened queue

        if current_node == end_node:  # If the current node is also the end node, then the board should be drawn and stop searching
            display_path(came_from, current_node, board)
            break

        closed_node.add(current_node)

        adj_nodes = get_adjacent_nodes(current_node, board_width, board_height, board)  # Find the adjacent nodes to the current

        for adj_node in adj_nodes:  # If the adjacent node is already closed, then don't calculate it again
            if adj_node in closed_node:
                continue

            temp_gscore = current_node.g + adj_node.cost

            if adj_node.walkable and adj_node not in came_from:  # Update the node if it is walkable and not already update
                came_from[adj_node] = current_node
                adj_node.g = temp_gscore
                adj_node.h = heuristic(adj_node, end_node)
                adj_node.f = adj_node.g + adj_node.h

                heapq.heappush(priority_queue, adj_node)  # Add the node to the open queue

            elif temp_gscore >= adj_node.g:  # If tentativ cost is less than the g score, then choose new node
                continue


def heuristic(node, end_node):  # Calculate the heuristic, with Manhatten distance
    return abs(node.x - end_node.x) + (node.y - end_node.y)


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


def display_path(came_from, current, board):  # Make the board with colors and O for the nodes in the path
    node_path = [current]
    board_string = ""
    while current in came_from.keys():   # Find all nodes in the path and add to a list
        current = came_from[current]
        node_path.append(current)

    for node in node_path:  # Change colors for the path
        if node.character == "A":
            node.character = color(32, "A")
        elif node.character == "B":
            node.character = color(32, "B")
        else:
           node.character = color(31, "O")

    for nodes in board:  # Change the board to a string in stead of list
        for node in nodes:
            board_string += node.character

    print(board_string)


def color(color, string):  # Change colors of nodes
    return "\033[" + str(color) + "m" + string + "\033[0m"


def read_board(board_id='1-4'):  # Read the board and appends to lists, finds the start and end nodes
    file_name = 'boards/board-%s.txt' % board_id
    board = []
    start, end = None, None


    with open(file_name) as f:
        for x, line in enumerate(f.readlines()):
            temp_line = []
            for y, ch in enumerate(line):
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
        self.h = 0
        self.cost = 1

    def __lt__(self, other):  # Compare the current value with other, less than
        return self.f < other.f

    def __str__(self):
        # return 'Node(%i, %i, %s, %i, %i, %i): %s' % (self.x, self.y, self.character, self.f, self.g, self.h, self.walkable)
        # return '%s: %i' % (self.character, self.f)
        return self.character

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":  # Create board and run a*
    board_data = read_board(board_id="1-4")  # run_board returns board, start, end as a tuple
    run_astar(*board_data)  # tuple unpacking, spread tuple as arguments
