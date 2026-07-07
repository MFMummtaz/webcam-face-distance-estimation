import cv2

# INITIAL CONFIGURATION 
CALIBRATION_DIST = 62.0      # Target distance from lens during calibration (cm)
TARGET_REAL_WIDTH = 13.7     # Physical width of the target object/face (cm)

COLOR_VALID = (0, 255, 0)
COLOR_ALERT = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_PANEL = (0, 0, 0)
DISPLAY_FONT = cv2.FONT_HERSHEY_COMPLEX

cascade_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def calculate_focal_length(sample_distance, actual_width, pixel_width_ref):
    """Computes the camera lens focal length based on initial benchmark data."""
    lens_focal_length = (pixel_width_ref * sample_distance) / actual_width
    return lens_focal_length

def estimate_target_distance(focal_len, obj_width, current_pixel_width):
    """Calculates the real-time distance using the triangle similarity principle."""
    calculated_dist = (obj_width * focal_len) / current_pixel_width
    return calculated_dist

def detect_and_measure_face(video_frame):
    """Scans the frame for a face, draws UI bounds, and returns target pixel width."""
    measured_pixel_width = 0
    grayscale_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
    detected_faces = cascade_classifier.detectMultiScale(grayscale_frame, 1.3, 5)

    for (pos_x, pos_y, box_w, box_h) in detected_faces:
        cv2.rectangle(video_frame, (pos_x, pos_y), (pos_x + box_w, pos_y + box_h), COLOR_VALID, 2)
        measured_pixel_width = box_w
        
    return measured_pixel_width

# Establish Video Stream
camera_stream = cv2.VideoCapture(0)

calibrated_focal_len = 0.0
system_calibrated = False

print("=" * 60)
print(f"1. Align target exactly {CALIBRATION_DIST} CM away from the lens.")
print("2. Tap 'c' on your keyboard to lock in calibration.")
print("3. Tap 'q' to close the application.")
print("=" * 60)

while True:
    stream_success, video_frame = camera_stream.read()
    if not stream_success:
        print("[ERROR] Failed to grab frame from webcam.")
        break

    # Analyze the active frame
    current_pixel_width = detect_and_measure_face(video_frame)

    if not system_calibrated:
        # UI for Setup Mode
        cv2.putText(video_frame, f"Step 1: Sit {CALIBRATION_DIST} CM away", (30, 40), 
                    DISPLAY_FONT, 0.6, COLOR_PANEL, 2, cv2.LINE_AA)
        
        if current_pixel_width != 0:
            cv2.putText(video_frame, "Step 2: Press 'c' to Calibrate", (30, 70), 
                        DISPLAY_FONT, 0.6, COLOR_VALID, 2, cv2.LINE_AA)
        else:
            cv2.putText(video_frame, "Status: Finding target...", (30, 70), 
                        DISPLAY_FONT, 0.6, COLOR_ALERT, 2, cv2.LINE_AA)
    else:
        # Live tracking UI for Active Mode
        if current_pixel_width != 0:
            final_distance = estimate_target_distance(calibrated_focal_len, TARGET_REAL_WIDTH, current_pixel_width)

            cv2.line(video_frame, (30, 30), (250, 30), COLOR_ALERT, 32)
            cv2.line(video_frame, (30, 30), (250, 30), COLOR_PANEL, 28)
            cv2.putText(video_frame, f"Range: {round(final_distance, 2)} CM", (30, 35), 
                        DISPLAY_FONT, 0.6, COLOR_VALID, 2, cv2.LINE_AA)

    # Render display window
    cv2.imshow("Computer Vision Distance Meter", video_frame)

    pressed_key = cv2.waitKey(1) & 0xFF
    
    # Listen for configuration command
    if pressed_key == ord('c') and current_pixel_width != 0:
        calibrated_focal_len = calculate_focal_length(CALIBRATION_DIST, TARGET_REAL_WIDTH, current_pixel_width)
        system_calibrated = True
        print(f"[SYSTEM INITIATED] Calibration locked. Focal Length: {round(calibrated_focal_len, 2)}")
        
    # Listen for termination command
    elif pressed_key == ord('q'):
        break

# Safely close hardware links
camera_stream.release()
cv2.destroyAllWindows()
