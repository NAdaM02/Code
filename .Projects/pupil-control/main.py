import cv2, time, csv, random, numpy as np
from screener import CustomImage, TerminalDisplay, CharacterMap
import colorama
import os, sys

global GLOBAL_last_frame_time, bottom_text, camera
bottom_text = ""

os.system('cls')
sys.stdout.write("\033[?25l")

camera = cv2.VideoCapture(0)

colorama.init()

# Game parameters
WIDTH, HEIGHT = 70, 20        # size of text screen
SHIP_X = 5                   # x-position of spaceship
BUBBLE_START_X = WIDTH - 5   # x where bubbles spawn
TARGET_SCORE = 20            # number of bubbles to hit

# Helper function: detect pupil area from an image (simple threshold & contour)
def detect_pupil_area(image, save_path=None):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (7,7), 0)

    # Canny edge detection
    edges = cv2.Canny(blurred, 30, 100)

    # Find contours from edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidate_ellipses = []

    for cnt in contours:
        if len(cnt) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            (x, y), (MA, ma), angle = ellipse
            area = np.pi * (MA/2) * (ma/2)
            aspect_ratio = max(MA, ma) / (min(MA, ma)+0.0001)
            if 0.7 < aspect_ratio < 1.5 and 100 < area < 3000:
                candidate_ellipses.append((area, ellipse))

    if not candidate_ellipses:
        return 0

    # Select the largest plausible ellipse
    best_area, best_ellipse = max(candidate_ellipses, key=lambda e: e[0])

    if save_path:
        out_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.ellipse(out_img, best_ellipse, (0, 255, 0), 2)
        cv2.imwrite(save_path, out_img)

    return best_area


# Calibration phase: measure min/max pupil area
cam = CustomImage()
print("Calibration: Look AT THE SCREEN (far). Hold still...")
time.sleep(2)
areas = []
for _ in range(50):
    img = cam.be_camera(camera).array
    areas.append(detect_pupil_area(img))
    time.sleep(0.05)
max_area = float(np.mean(areas))

print("Now focus on a NEAR target (e.g. a dot ~30cm in front).")
time.sleep(1)
areas = []
for _ in range(50):
    img = cam.be_camera(camera).array
    areas.append(detect_pupil_area(img, save_path=f"{_}.png"))
    time.sleep(0.05)
min_area = float(np.mean(areas))
if min_area < 1: min_area = 1  # avoid division by zero
print(f"Calibration done. Pupil area range ≈ [{min_area:.1f}, {max_area:.1f}].")
time.sleep(1)

# Set up terminal display
disp = TerminalDisplay(HEIGHT)
disp.clear()

# Game loop variables
bubbles = []  # list of (x,y) bubble positions
score = 0
start_time = time.time()
last_spawn = 0

# For smoothness metric
pupil_history = []

# Coordinates for pupil-feedback circle (centered near top-right)
CIRCLE_CENTER = (60, 10)
RMAX = 5

# Main game loop
frame = 0
while score < TARGET_SCORE:
    frame += 1
    current_time = time.time()

    # Spawn a new bubble every 30 frames at random height
    if frame - last_spawn > 30:
        y = random.randint(1, HEIGHT-2)
        bubbles.append([BUBBLE_START_X, y])
        last_spawn = frame

    # Read camera and detect pupil
    img = cam.be_camera(camera).array
    area = detect_pupil_area(img)
    pupil_history.append(area)
    # Clamp area to calibration range
    area = max(min(area, max_area), min_area)
    ratio = (area - min_area) / (max_area - min_area)

    # Compute spaceship vertical position (inverted: small area → high Y)
    ship_y = int((1.0 - ratio) * (HEIGHT - 1))

    # Move bubbles left
    new_bubbles = []
    for bx, by in bubbles:
        bx -= 1
        if bx > SHIP_X:
            new_bubbles.append([bx, by])
        # Check collision
        elif bx == SHIP_X and by == ship_y:
            score += 1
    bubbles = new_bubbles

    # Draw frame to CharacterMap
    cmap = CharacterMap(WIDTH, HEIGHT, filler=' ')
    # Draw spaceship (one char)
    cmap[SHIP_X, ship_y] = '*'
    # Draw bubbles
    for bx, by in bubbles:
        if 0 <= bx < WIDTH and 0 <= by < HEIGHT:
            cmap[bx, by] = 'O'
    # Draw pupil-size feedback circle (filled up to radius = ratio*RMAX)
    center_x, center_y = CIRCLE_CENTER
    fill_r = ratio * RMAX
    for dx in range(-RMAX, RMAX+1):
        for dy in range(-RMAX, RMAX+1):
            dist = (dx*dx + dy*dy)**0.5
            if dist <= fill_r:
                x = center_x + dx
                y = center_y + dy
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    cmap[x, y] = 'o'
    # Render the display
    disp.update(cmap, fps=20)

# Game over
elapsed = time.time() - start_time
disp.clear()
print(f"\nGame Over! Score: {score}, Time: {elapsed:.1f}s")

# Compute a simple smoothness metric (inverse of pupil-area stddev)
std = np.std(pupil_history) if len(pupil_history)>0 else 0.0
smoothness = 1.0 / (std+1e-3)

# Save data to CSV
with open('progress.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([time.strftime("%Y-%m-%d"), score, f"{elapsed:.2f}", f"{smoothness:.3f}"])
print("Session data saved to progress.csv.")
