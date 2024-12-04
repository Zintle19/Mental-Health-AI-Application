import customtkinter as ctk
import cv2
import threading
import time
import subprocess  # Import subprocess to launch the login script
from PIL import Image, ImageTk

class SplashScreen(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Cartoonify Splash Screen")
        
        # Set the window to full-screen mode, but we'll resize the video to make it smaller
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        
        # Set up the splash screen background color
        self.configure(fg_color="white")
        
        # Create a white background frame that fills the screen
        self.bg_frame = ctk.CTkFrame(self, fg_color="white")
        self.bg_frame.pack(fill="both", expand=True)
        
        # Create a label to display the video
        self.video_label = ctk.CTkLabel(self.bg_frame, text="")
        self.video_label.pack(fill="both", expand=True)
        
        # Create the progress bar and pack it below the video
        self.progress_bar = ctk.CTkProgressBar(self.bg_frame, width=self.winfo_width() - 40, height=20)
        self.progress_bar.pack(pady=10, padx=20)

        # Load the video in a separate thread
        self.video_thread = threading.Thread(target=self.play_video)
        self.video_thread.start()

    def play_video(self):
        # Load the video
        self.video = cv2.VideoCapture('botbuddy.mp4')  # Path to your video file
        total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))  # Get the total number of frames in the video
        
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret:
                break

            # Resize the frame to make it smaller while maintaining aspect ratio
            width = self.winfo_width() // 4  # Resize the video to half of the window width
            height = int((width / frame.shape[1]) * frame.shape[0])  # Maintain aspect ratio

            # Resize the frame with better interpolation (INTER_CUBIC for better quality)
            frame_resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)

            # Convert the frame to RGB format (OpenCV uses BGR by default)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            # Convert the frame to a format tkinter can display
            frame_image = Image.fromarray(frame_rgb)
            frame_tk = ctk.CTkImage(frame_image, size=(width, height))

            # Update the video label with the new frame
            self.video_label.configure(image=frame_tk)
            self.video_label.image = frame_tk  # Keep a reference to avoid garbage collection

            # Update the progress bar based on the current position in the video
            current_frame = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
            progress = current_frame / total_frames
            self.progress_bar.set(progress)  # Set the progress bar position

            # Update the screen
            self.update_idletasks()

            # Slow down the frame rate to match video speed
            time.sleep(0.03)  # Adjust this based on your video frame rate

        # After the video ends, close the splash screen and open the login screen
        self.after(1000, self.open_login_screen)

    def open_login_screen(self):
        self.destroy()  # Destroy the splash screen
        # Use subprocess to open the login.py script
        subprocess.Popen(["python", "main.py"])  # Run the login script in a new process

if __name__ == "__main__":
    app = SplashScreen()
    app.mainloop()
