import cv2
import mediapipe as mp
import pyautogui
import time

def hand_control():
    # Initialize mediapipe hands module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)

    # Get screen size
    screen_width, screen_height = pyautogui.size()

    # Function to convert normalized coordinates to screen coordinates
    def normalize_to_screen(x, y):
        x_screen = int(x * screen_width)
        y_screen = int(y * screen_height)
        return x_screen, y_screen

    # Start capturing video
    cap = cv2.VideoCapture(0)

    # Variables for double-click and drag
    last_click_time = 0
    click_threshold = 0.25  # Time in seconds for double-click detection
    is_dragging = False
    cursor_active = True  # Control if cursor movement is active
    fist_detected = False  # To track fist state

    # Initialize last positions
    last_palm_x, last_palm_y = None, None
    last_middle_x, last_middle_y = None, None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the coordinates of the palm center
                palm_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
                palm_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

                # Normalize to screen coordinates
                current_screen_x, current_screen_y = normalize_to_screen(palm_x, palm_y)

                # Control cursor movement based on thumbs up/down
                thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

                # Check thumb position relative to wrist
                cursor_active = thumb_y < wrist_y  # Thumbs up indicates cursor active

                if cursor_active:
                    if last_palm_x is not None and last_palm_y is not None:
                        # Calculate position change for cursor movement
                        delta_x = current_screen_x - last_palm_x
                        delta_y = current_screen_y - last_palm_y
                        pyautogui.moveRel(delta_x, delta_y)

                    # Update last palm position
                    last_palm_x, last_palm_y = current_screen_x, current_screen_y

                    # Check if thumb and index finger are touching for clicking
                    index_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                    index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                    # Calculate distance between thumb and index finger tips
                    distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5

                    # Single click detection
                    if distance < 0.06:  # Adjust threshold as necessary
                        current_time = time.time()
                        if current_time - last_click_time < click_threshold:
                            pyautogui.doubleClick()
                        else:
                            pyautogui.click()

                        last_click_time = current_time

                    # Check for dragging
                    if distance < 0.08:
                        if not is_dragging:
                            is_dragging = True
                        else:
                            pyautogui.dragRel(delta_x, delta_y)
                    else:
                        is_dragging = False

                # Check for middle finger and thumb contact for scrolling
                middle_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                middle_distance = ((thumb_x - middle_x) ** 2 + (thumb_y - middle_y) ** 2) ** 0.5

                if middle_distance < 0.1:  # Increased threshold for finger contact
                    if last_middle_x is not None and last_middle_y is not None:
                        # Calculate scrolling direction based on middle finger movement
                        scroll_delta_y = int((last_middle_y - middle_y) * 2500)  # 3 times the distance at double speed
                        if scroll_delta_y != 0:
                            pyautogui.scroll(scroll_delta_y)

                    # Update last middle finger position
                    last_middle_x, last_middle_y = middle_x, middle_y
                else:
                    # Reset last middle finger position if not in contact
                    last_middle_x, last_middle_y = None, None

                # Draw hand landmarks for visualization (optional)
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        else:
            # Reset positions if no hand detected
            last_palm_x, last_palm_y = None, None
            last_middle_x, last_middle_y = None, None

        # Show the frame
        cv2.imshow("Hand Tracking", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start the hand control
#hand_control()