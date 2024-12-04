import cv2
import os
import sqlite3
import numpy as np
import customtkinter as ctk
from tkinter import messagebox
from dashboard import Dashboard  # Import the Dashboard class

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x500")

        # UI Components
        ctk.CTkLabel(self, text="Login", font=("Arial", 24)).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login with Password", command=self.login_with_password).pack(pady=10)
        ctk.CTkButton(self, text="Login with Face", command=self.login_with_face).pack(pady=10)

    def login_with_password(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.destroy()
            Dashboard(username).mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def login_with_face(self):
        username = self.username_entry.get()
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        if not user:
            messagebox.showerror("Error", "User not found.")
            return
        face_path = user[3]
        if not os.path.exists(face_path):
            messagebox.showerror("Error", "Face data not found. Please register again.")
            return
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Info", "Look at the camera for face recognition.")
        match = False
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (100, 100))
                face_array = np.load(face_path)
                match = np.any([np.array_equal(face, saved_face) for saved_face in face_array])
                if match:
                    break
            if match or cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        if match:
            messagebox.showinfo("Success", "Face recognized! Login successful!")
            self.destroy()
            Dashboard(username).mainloop()
        else:
            messagebox.showerror("Error", "Face not recognized.")

if __name__ == "__main__":
    app = Login()
    app.mainloop()
