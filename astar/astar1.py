import heapq


def heuristic(node, end_node):
    return abs(node.x - end_node.x) + (node.y - end_node.y)


def run_astar(board, start, end):
    if not isinstance(board, list):
        return "Board must be a list"

    priority_queue = []
    heapq.heapify(priority_queue)

    start_node = start
    end_node = end
    board_width = len(board[0])
    board_height = len(board)
    #print(board_width, ' ', board_height)

    heapq.heappush(priority_queue, start_node)


    node_path = {}
    node_path[start_node] = None
    key = 0
    closed_node = set()
    #total_cost = {}
    #total_cost[start_node] = 0

    #print(priority_queue)

    while priority_queue:
        current_node = heapq.heappop(priority_queue)
        #print("curr", current_node)
        closed_node.add(current_node)

        if current_node == end_node:
            print("done")
            display_path(board, node_path)
            break

        adj_nodes = get_adjacent_nodes(current_node, board_width, board_height, board)
        #print(adj_nodes)

        for adj_node in adj_nodes:
            if adj_node in closed_node:
                continue

            temp_score = current_node.g + (current_node.g - adj_node.g)

            if adj_node.walkable and adj_node not in node_path:
                heapq.heappush(priority_queue, adj_node)

            elif temp_score >= adj_node.g:
                continue

            key += 1
            node_path.update({adj_node: key})
            adj_node.g = temp_score
            adj_node.h =heuristic(adj_node, end_node)
            adj_node.f = adj_node.g + adj_node.h

                #if adj_node in priority_queue:
                #    if adj_node.g < current_node.g:
                #        adj_node.g += 1
                #        adj_node.h = heuristic(adj_node, end_node)
                #        adj_node.f = adj_node.g + adj_node.h
                #        adj_node.parent = current_node

                #    else:
                #        adj_node.g += 1
                #        adj_node.h = heuristic(adj_node, end_node)
                #        adj_node.f = adj_node.g + adj_node.h
                #        adj_node.parent = current_node
                #heapq.heappush(priority_queue, adj_node)




    #print(priority_queue)

def get_adjacent_nodes(current_node, board_w, board_h, board):
    #print("\nCurrent", current_node)
    adj_nodes = []
    # print(current_node, board_w, board_h)
    if current_node.x > 0:
        adj_nodes.append(board[current_node.x - 1][current_node.y])

    if current_node.y > 0:
        adj_nodes.append(board[current_node.x][current_node.y - 1])

    if current_node.x < board_h - 1:
        adj_nodes.append(board[current_node.x + 1][current_node.y])

    if current_node.y < board_w - 1:
        adj_nodes.append(board[current_node.x][current_node.y + 1])

    return adj_nodes

#def update_node(adj_node, current_node, end_node):
#    adj_node.g = current_node.g
#    adj_node.h = heuristic(adj_node, end_node)
#    adj_node.f = adj_node.g + adj_node.h
#    adj_node.parent = current_node

def display_path(board, node_path):
    for node in node_path:
        node.character = "O"
    print("Board:")
    print(board)

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

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        #return 'Node(%i, %i, %s): %s' % (self.x, self.y, self.character, self.walkable)
        return self.character

    def __repr__(self):
        return self.__str__()


def read_board(board_id='1-1'):
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
    print(board)
    return board, start, end

if __name__ == "__main__":
    board_data = read_board(board_id="1-1")  # run_board returns board, start, end as a tuple
    run_astar(*board_data)  # tuple unpacking, spread tuple as arguments
