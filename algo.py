import kociemba


def solve_cube(cube_data, face_order):
    
    if len(cube_data) != 6:
        print("Incomplete cube data")
        return

    # Step 1: Determine color-to-face mapping from centers
    color_to_face = {}
    for i in range(6):
        center_color = cube_data[i][4]
        color_to_face[center_color] = face_order[i]

    # building string
    cube_string = ""
    for face in cube_data:
        for sticker in face:
            if sticker not in color_to_face:
                print("Unknown color detected:", sticker)
                return
            cube_string += color_to_face[sticker]

    print("Cube String:", cube_string)
    
    try:
        solution = kociemba.solve(cube_string)
        if cube_string == "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB":
            print("Cube already in solved state")
        else:
            print("Solution:", solution)
    except Exception as e:
        print("Invalid cube state:", e)