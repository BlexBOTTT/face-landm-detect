import cv2
import mediapipe as mp

# Initialize mediapipe drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Define a custom drawing specification for your contours
my_drawing_specs = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)

# Open a connection to the default camera (camera index 0)
cap = cv2.VideoCapture(0)

# Initialize the FaceMesh model from mediapipe
mp_face_mesh = mp.solutions.face_mesh

# Configure FaceMesh parameters
with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
) as face_mesh:
    # Main loop for video capture
    while cap.isOpened():
        # Read a frame from the camera
        success, image = cap.read()
        if not success:
            break

        # Process the image with FaceMesh
        results = face_mesh.process(image)

        # Check if any faces are detected
        if results.multi_face_landmarks:
            # Iterate over detected faces
            for face_landmarks in results.multi_face_landmarks:
                # Draw the face mesh tesselation
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )

                # Draw the face mesh contours using the custom drawing spec
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=my_drawing_specs
                )

        # Display the flipped image
        cv2.imshow("Video Capture", cv2.flip(image, 1))

        # Break the loop if 'q' is pressed
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
