## packages import
import cv2
import pandas as pd

# Reading an image
img_path = "colorful_image.jpg"
img = cv2.imread(img_path)

if img is None:
    print("Error: Image not found!")
    exit()

clicked = False
# Initializing the pointers and color components to 0
r = g = b = x_pos = y_pos = 0

# Reading the CSV file
index = ["colors", "color_name", "hex", "R", "G", "B"]
dataset = pd.read_csv('colors.csv', names=index)

def get_color(R, G, B):
    minimum = 10000
    color_name = None  # Initialize color_name
    for i in range(len(dataset)):
        d = abs(R - int(dataset.iloc[i]["R"])) + abs(G - int(dataset.iloc[i]["G"])) + abs(B - int(dataset.iloc[i]["B"]))
        if d <= minimum:
            minimum = d
            color_name = dataset.iloc[i]["color_name"]
    return color_name

## To get the x and y coordinates of the mouse double click
def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow('image', img)
    if clicked:
        # cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)

        # Creating text string to display (Color name and RGB values)
        text = get_color(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        # cv2.putText(img, text, start, font(0-7), fontScale, color, thickness, lineType)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors we will display text in black color
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(20) & 0xFF == 27:  # Exit on 'Esc' key
        break

cv2.destroyAllWindows()