class Node:
    def __init__(self, currState, move, prevState):
        self.currState = currState #6x9 matrix to store face values
        self.move = move # strng to store movement - move to reach the currstate from prevstate  
        self.prevState = prevState #another node itself. 


#applying move 
def applymove(node, move):
    state = node.currState

    action = move[0] # like u,l,d
    location = int(move[1]) # like 1,2,4

    print("state not updated")


    if action == 'u':
        new_state = up(state, location)

    #for face in next_node.currState:
        print("state updated")
        #print(node.currState)
      

def solved_state():
    return [
        ['G'] * 9,  # 0 → Front
        ['R'] * 9,  # 1 → Right
        ['B'] * 9,  # 2 → Back
        ['O'] * 9,  # 3 → Left
        ['W'] * 9,  # 4 → Up
        ['Y'] * 9   # 5 → Down
    ]


# all rotations functions 
# | F | R | B | L | U | D |
#   0   1   2   3   4   5 faces


def up(stateMatrix, column):
    #f,u,b,d

    new_state = [face[:] for face in stateMatrix]

    F, R, B, L, U, D = 0, 1, 2, 3, 4, 5

    col = [column-4, column-1,column+2]

    # store Front column temporarily
    temp = [new_state[F][i] for i in col]

    # Down -> Front
    for i, idx in enumerate(col):
        new_state[F][idx] = new_state[D][col[i]]

    # Back -> Down
    for i, idx in enumerate(col):
        new_state[D][idx] = new_state[B][col[i]]

    # Up -> Back
    for i, idx in enumerate(col):
        new_state[B][idx] = new_state[U][col[i]]

    # temp (Front) -> Up
    for i, idx in enumerate(col):
        new_state[U][idx] = temp[i]

    print(new_state)

    return new_state


#initial testing 
initial_state = solved_state()
root = Node(solved_state(), None, None)
applymove(root, "u6")

