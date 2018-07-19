import cv2
capture = cv2.VideoCapture(0)

while True:
    ret, image = capture.read()
    cv2.imshow('Camera stream', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
width, height = image.shape
scale = 640.0 / width
image = cv2.resize(image, (0,0), fx=scale, fy=scale)

t = 100 # threshold for Canny Edge Detection algorithm
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blured = cv2.medianBlur(grey, 15)

# Create 2x2 grid for all previews
grid = np.zeros([2*h, 2*w, 3], np.uint8)

grid[0:h, 0:w] = image
# We need to convert each of them to RGB from greyscaled 8 bit format
grid[h:2*h, 0:w] = np.dstack([cv2.Canny(grey, t / 2, t)] * 3)
grid[0:h, w:2*w] = np.dstack([blured] * 3)
grid[h:2*h, w:2*w] = np.dstack([cv2.Canny(blured, t / 2, t)] * 3)
sc = 1 # Scale for the algorithm
md = 30 # Minimum required distance between two circles
# Accumulator threshold for circle detection. Smaller numbers are more
# sensitive to false detections but make the detection more tolerant.
at = 40
circles = cv2.HoughCircles(blured, cv2.HOUGH_GRADIENT, sc, md, t, at)
if circles is not None:
    circle = circles[0][0]
    x, y, radius = int(circle[0]), int(circle[1]), int(circle[2])
    print(x, y, radius)

    cv2.circle(image, [x, y], radius, (0, 0, 255), 1)
    cv2.circle(image, [x, y], 1, (0, 0, 255), 1)