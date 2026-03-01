import cv2
import numpy as np

FACE_ORDER = ["F", "R", "B", "L", "U", "D"]

# cube data (6 faces × 9 cells)
cube_data = []


#  COLOR CLASSIFICATION 
def classify_color(hsv):
    h, s, v = hsv

    if v > 180 and s < 40:
        return 'w'   # white
    if h < 10 or h > 160:
        return 'r'
    if 10 < h < 25:
        return 'o'
    if 25 < h < 40:
        return 'y'
    if 40 < h < 85:
        return 'g'
    if 85 < h < 140:
        return 'b'

    return '?'  #if unknown



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








#main func to capture frame first, generate grid and display,  
def main():

    cap = cv2.VideoCapture(0)

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
        if key == 32 and capturing:  # while capturing- true, if space entered, the picture is captured. 
            colors = read_face(frame)  #9 cells colors of one face is returned in 1d array format
            cube_data.append(colors)

            print(f"Face {FACE_ORDER[face_index]} captured:", colors)

            face_index += 1

            if face_index == 6:
                break

        # exit
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    print("\nFINAL CUBE DATA:\n")
    print_cube()




#  PRINT RESULT
def print_cube():

    # convert faces into 3 rows output
    rows = [[], [], []]

    for face in cube_data:
        rows[0].extend(face[0:3])  
        rows[1].extend(face[3:6])
        rows[2].extend(face[6:9])

    for r in rows:
        print(" ".join(r))


if __name__ == "__main__":
    main()