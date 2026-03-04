import cv2
import numpy as np
import kociemba
from algo import solve_cube




FACE_ORDER = ["U", "R", "F", "D", "L", "B"]

# cube data (6 faces × 9 cells)
cube_data = []


#  COLOR CLASSIFICATION 
def classify_color(hsv):
    h, s, v = hsv

    if s < 60 and v > 150:
        return 'w'
    if (0 <= h < 4) or (170 <= h <= 179):
        return 'r'
    if 4 <= h < 24:
        return 'o'
    if 25 <= h < 40:
        return 'y'
    if 40 <= h < 85:
        return 'g'
    if 90 <= h < 130:
        return 'b'

    return '?'  #if unknown
#____________________________________________________________________________________________________________________________________________________________________________________________



# READ 3x3 GRID COLORS 
def read_face(frame):
    h, w, _ = frame.shape
    #height, width, color channels(ignored variable)

    size = 300
    start_x = w//2 - size//2
    start_y = h//2 - size//2

    face_colors = []

    cell = size // 3

    for row in range(3):
        for col in range(3):

            x1 = start_x + col * cell + 20                   #  ____________
            y1 = start_y + row * cell + 20                   # | x1______   |
            x2 = x1 + cell - 40                              # |  :used :   |
            y2 = y1 + cell - 40                              # |  :_____:   |
                                                             # |x2__________|
            roi = frame[y1:y2, x1:x2] # extracting area of 1 block out of 9 blocks  - ffirst horizontal - y and then those fromm x.

            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)  # convert bgr to hsv to be not effected by the light using cvtColor. 

            # now need to convert all 9 rois(3d array form) to 2d array form (index and color)
            #reshape(-1,3) second dim must have exactly 3 charateristics(hue, sat, val); first dim = -1: calculate this dimension on your own. 


            avg = np.mean(hsv.reshape(-1,3), axis=0) 

            # we get avg values of h,s,v and that is sent to classify_color() for getting eact color   
            color = classify_color(avg)
            face_colors.append(color)

            # appended to face_color- 1d array and returned at last 

    return face_colors



#____________________________________________________________________________________________________________________________________________________________________________________________


def draw_grid(frame, face_name):
    h, w, _ = frame.shape

    size = 300
    start_x = w//2 - size//2  # for scanning, 'w//2 - middle of cube. to get starting of cube - w//2 - size of cube/2'. smly h also. 
    start_y = h//2 - size//2

    cell = size // 3

    # draw outer square
    cv2.rectangle(frame,
                  (start_x, start_y),
                  (start_x+size, start_y+size),
                  (0,255,0), 2)

    # draw grid lines
    for i in range(1,3):
        cv2.line(frame,
                 (start_x+i*cell, start_y),
                 (start_x+i*cell, start_y+size),
                 (0,255,0),2)    # color of box and it's thickness.     

        cv2.line(frame,
                 (start_x, start_y+i*cell),
                 (start_x+size, start_y+i*cell),
                 (0,255,0),2)

    cv2.putText(frame,
                f"Show Face: {face_name}",
                (30,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,255,0),2)
    
    # puttext(frame, text, starting point, fontfamily, size, color, thickness)




#____________________________________________________________________________________________________________________________________________________________________________________________




#main func to capture frame first, generate grid and display,  
def main():

    cap = cv2.VideoCapture(2)

    print("Press 'c' to start cube capture")

    capturing = False
    face_index = 0

    while True:
        # ret is state if camera is still capturing or not 
        # frame - 2d array to capture state of image 
        ret, frame = cap.read()
        if not ret:
            break

        #frame = cv2.flip(frame,1)

        if capturing and face_index < 6:
            draw_grid(frame, FACE_ORDER[face_index]) 

        cv2.imshow("Cube Scanner", frame)   #grid displyed.

        #capturing- false until now- state and grid made ready for capture 

        key = cv2.waitKey(1) & 0xFF   #after waiting for atleast a second to let the grid be shown and if the user presses c: capture starts
        # start capture
        if key == ord('c'):
            capturing = True
            print("Capture started")

        # capture face
        if key == 32 and capturing and face_index < 6:  # while capturing- true, if space entered, the picture is captured. 
            colors = read_face(frame)  #9 cells colors of one face is returned in 1d array format
            cube_data.append(colors)

            print(f"Face {FACE_ORDER[face_index]} captured:", colors)

            face_index += 1

            if face_index == 6:
                # pass collected data into the solver function defined in algo.py
                solve_cube(cube_data, FACE_ORDER)
                break


        # if wrong data captured - press z to go back. 
        if key == ord('z') and capturing:
            if face_index > 0:
                face_index -= 1
                removed_face = cube_data.pop()
                print(f"Removed Face {FACE_ORDER[face_index]}:", removed_face)
                print("Retake this face.")
            else:
                print("No face to remove.")

        # exit
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    

#____________________________________________________________________________________________________________________________________________________________________________________________
# def solve_cube():
#     if len(cube_data) != 6:
#         print("Incomplete cube data")
#         return

#     # Step 1: Determine color-to-face mapping from centers
#     color_to_face = {}

#     for i in range(6):
#         center_color = cube_data[i][4]  # middle of 3x3
#         color_to_face[center_color] = FACE_ORDER[i]

#     # Step 2: Convert entire cube
#     cube_string = ""

#     for face in cube_data:
#         for sticker in face:
#             if sticker not in color_to_face:
#                 print("Unknown color detected:", sticker)
#                 return
#             cube_string += color_to_face[sticker]

#     print("Cube String:", cube_string)

#     try:
#         solution = kociemba.solve(cube_string)
#         print("Solution:", solution)
#     except Exception as e:
#         print("Invalid cube state:", e)


if __name__ == "__main__":
    main()