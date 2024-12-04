import customtkinter as ctk
from datetime import datetime

# Initialize the main app
app = ctk.CTk()
app.title("Mental Health AI")
app.geometry("700x600")

# Functionality for Emotion Tracking
def track_emotion(emotion):
    response_label.configure(text=f"You feel {emotion}. Take a deep breath and try a guided exercise.")
    
def save_journal():
    entry_text = journal_entry.get("1.0", "end").strip()
    if entry_text:
        with open("journal_entries.txt", "a") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {entry_text}\n")
        journal_entry.delete("1.0", "end")
        response_label.configure(text="Journal entry saved!")

# Guided Exercises
def guided_exercise():
    response_label.configure(text="Try this: Close your eyes, inhale deeply for 4 seconds, hold for 4 seconds, exhale for 6 seconds.")

# Chatbot functionality
def chatbot_response():
    user_input = chatbot_input.get()
    if user_input.strip():
        response_label.configure(text=f"AI: That's a good point. Have you considered focusing on one positive thing today?")
        chatbot_input.delete(0, "end")

# Set up main sections
header_label = ctk.CTkLabel(app, text="Mental Health AI", font=("Arial", 24, "bold"))
header_label.pack(pady=10)

# Emotion Tracking Section
emotion_label = ctk.CTkLabel(app, text="How are you feeling today?", font=("Arial", 16))
emotion_label.pack(pady=10)

emotions_frame = ctk.CTkFrame(app)
emotions_frame.pack(pady=10)

emotions = ["Happy", "Sad", "Anxious", "Calm", "Angry"]
for emotion in emotions:
    btn = ctk.CTkButton(emotions_frame, text=emotion, command=lambda e=emotion: track_emotion(e))
    btn.pack(side="left", padx=5)

# Journaling Section
journal_label = ctk.CTkLabel(app, text="Write down your thoughts:", font=("Arial", 16))
journal_label.pack(pady=10)

journal_entry = ctk.CTkTextbox(app, width=600, height=100)
journal_entry.pack(pady=5)

save_button = ctk.CTkButton(app, text="Save Entry", command=save_journal)
save_button.pack(pady=5)

# Guided Exercise Button
exercise_button = ctk.CTkButton(app, text="Try a Guided Exercise", command=guided_exercise)
exercise_button.pack(pady=10)

# Chatbot Section
chatbot_label = ctk.CTkLabel(app, text="Chat with AI:", font=("Arial", 16))
chatbot_label.pack(pady=10)

chatbot_frame = ctk.CTkFrame(app)
chatbot_frame.pack(pady=10)

chatbot_input = ctk.CTkEntry(chatbot_frame, width=500)
chatbot_input.pack(side="left", padx=5)

chatbot_button = ctk.CTkButton(chatbot_frame, text="Send", command=chatbot_response)
chatbot_button.pack(side="left", padx=5)

# Response Label
response_label = ctk.CTkLabel(app, text="", font=("Arial", 14), wraplength=600)
response_label.pack(pady=10)

# Run the App
app.mainloop()
