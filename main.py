import customtkinter as ctk
import cv2
import face_recognition
import sqlite3
import os
import subprocess
import numpy as np
from tkinter import messagebox
import pickle  # For encoding face as binary blob

# Create necessary directories
os.makedirs("user_data/faces", exist_ok=True)

# Database setup
DB_PATH = "user_data/users.db"

# Create database if it doesn't exist
if not os.path.exists(DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE users (
                username TEXT PRIMARY KEY,
                password TEXT,
                face_encoding BLOB
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
        exit(1)

# Function to register user
def register_user(username, password, face_image=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Save face encoding if face_image is provided
    face_encoding = None
    if face_image is not None:
        # Get the face encoding using face_recognition
        face_encodings = face_recognition.face_encodings(face_image)
        if face_encodings:
            face_encoding = face_encodings[0]
            # Convert numpy array to binary format
            face_encoding = pickle.dumps(face_encoding)

    # Insert user into database
    try:
        cursor.execute("INSERT INTO users (username, password, face_encoding) VALUES (?, ?, ?)",
                       (username, password, face_encoding))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        conn.close()

# Function to capture face
def capture_face():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert to grayscale for better face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Use OpenCV's face cascade classifier to detect faces
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            # No face detected, prompt user to show face
            cv2.putText(frame, "No face detected. Please face the camera.", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            # Face detected, draw rectangle around the face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Show captured face and prompt user to confirm capture
            cv2.putText(frame, "Press 'Enter' to capture face", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Face Capture - Press 'Enter' to capture", frame)

            # Wait for the 'Enter' key to capture the face
            if cv2.waitKey(1) & 0xFF == 13:  # Enter key
                cv2.destroyAllWindows()
                cap.release()
                return frame

    cap.release()
    cv2.destroyAllWindows()
    return None

# Function to compare face with saved face encoding
def compare_face(username, frame):
    # Load the saved face encoding from database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT face_encoding FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False  # User not found

    saved_face_encoding = result[0]
    if saved_face_encoding is None:
        return False

    # Convert the saved face encoding back from binary format
    saved_face_encoding = pickle.loads(saved_face_encoding)

    # Encode the captured face
    captured_encoding = face_recognition.face_encodings(frame)
    if len(captured_encoding) == 0:
        return False  # No face detected

    # Compare the captured face with the saved face encoding
    matches = face_recognition.compare_faces([saved_face_encoding], captured_encoding[0])
    return matches[0]

# Main GUI
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition App")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # Initialize register frame
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.register_label = ctk.CTkLabel(self.register_frame, text="Register New User", font=("Arial", 18))
        self.register_label.pack(pady=12, padx=10)

        self.register_username_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Username")
        self.register_username_entry.pack(pady=12, padx=10)

        self.register_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.register_password_entry.pack(pady=12, padx=10)

        self.register_face_recognition_var = ctk.CTkCheckBox(self.register_frame, text="Enable Face Recognition")
        self.register_face_recognition_var.pack(pady=12, padx=10)

        self.register_submit_button = ctk.CTkButton(self.register_frame, text="Register", command=self.register)
        self.register_submit_button.pack(pady=12, padx=10)

        # Clickable label to go to login window
        self.login_label = ctk.CTkLabel(self.register_frame, text="Already have an account? Login here", font=("Arial", 12), text_color="blue", cursor="hand2")
        self.login_label.pack(pady=10)
        self.login_label.bind("<Button-1>", self.open_login)

    def register(self):
        # Access the username and password from the registration form
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()

        # Validation: Ensure fields are not empty
        if not username or not password:
            messagebox.showerror("Error", "Please fill out all fields!")
            return

        # If face recognition is enabled, capture face image
        face_image = None
        if self.register_face_recognition_var.get():
            face_image = capture_face()
            if face_image is None:
                messagebox.showerror("Error", "Face capture failed!")
                return

        # Register user with face image (if provided)
        register_user(username, password, face_image)

        # Navigate to the dashboard after successful registration
        self.open_dashboard(username)

    def open_login(self, event):
        self.register_frame.pack_forget()  # Hide register frame
        login_window = LoginWindow(self)  # Open login window
        login_window.grab_set()  # Make sure the login window stays on top and blocks the main window until it's closed

    def open_dashboard(self, username):
        self.register_frame.pack_forget()  # Hide current frame
        subprocess.run(["python", "dashboard.py", username])  # Open the dashboard window in a separate process

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.login_label = ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 18))
        self.login_label.pack(pady=12, padx=10)

        self.login_username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.login_username_entry.pack(pady=12, padx=10)

        self.login_password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.login_password_entry.pack(pady=12, padx=10)

        self.login_password_var = ctk.CTkCheckBox(self.login_frame, text="Login with Password")
        self.login_password_var.select()  # Default to password login
        self.login_password_var.pack(pady=10)

        self.login_face_recognition_var = ctk.CTkCheckBox(self.login_frame, text="Login with Face Recognition")
        self.login_face_recognition_var.pack(pady=10)

        self.login_submit_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_submit_button.pack(pady=12, padx=10)

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        # Check login using password
        if self.login_password_var.get():
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            conn.close()

            if result is None or result[0] != password:
                messagebox.showerror("Error", "Incorrect username or password!")
                return

        # Check login using face recognition
        if self.login_face_recognition_var.get():
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT face_encoding FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            conn.close()

            if result is None:
                messagebox.showerror("Error", "User not found!")
                return

            saved_face_encoding = result[0]
            if saved_face_encoding is None:
                messagebox.showerror("Error", "No face encoding found for user!")
                return

            # Capture face and compare
            face_image = capture_face()
            if face_image is None or not compare_face(username, face_image):
                messagebox.showerror("Error", "Face recognition failed!")
                return

        messagebox.showinfo("Success", "Login successful!")
        self.destroy()  # Close the login window

        # Open the dashboard after successful login
        subprocess.run(["python", "dashboard.py", username])  # Open dashboard in a new process

if __name__ == "__main__":
    app = App()
    app.mainloop()
