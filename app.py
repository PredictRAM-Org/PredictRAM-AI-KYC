import streamlit as st
import cv2
import face_recognition

# Function to perform face recognition on the uploaded ID proof
def recognize_from_id_proof(uploaded_file):
    image = face_recognition.load_image_file(uploaded_file)
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) > 0:
        return face_encodings[0]
    else:
        return None

# Function to perform face recognition on live video
def recognize_from_live_video(id_proof_features):
    cap = cv2.VideoCapture(0)
    while st.checkbox("Enable Camera"):
        ret, frame = cap.read()

        # Find faces in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare the face in the live video with the ID proof features
            match = face_recognition.compare_faces([id_proof_features], face_encoding)
            if match[0]:
                return True

        # Display the live video
        st.image(frame, channels="BGR", use_column_width=True)

# Main Streamlit app
def main():
    st.title("Face Recognition App")

    # Upload ID Proof
    uploaded_file = st.file_uploader("Upload ID Proof", type=["jpg", "png"])

    if uploaded_file is not None:
        # Perform face recognition on the uploaded ID proof
        id_proof_features = recognize_from_id_proof(uploaded_file)

        # Display a message if ID proof features are extracted successfully
        if id_proof_features is not None:
            st.success("ID proof features extracted successfully.")

            # Display live video from the user's camera
            st.header("Live Video Verification")
            st.info("Please allow access to your camera.")
            face_match = recognize_from_live_video(id_proof_features)

            # Display the result
            if face_match:
                st.success("Identity verified. Access granted.")
            else:
                st.error("Identity not verified. Access denied.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
