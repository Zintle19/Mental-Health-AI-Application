import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import tkinter.messagebox as messagebox

mood_data = []


def mood_tracker(main_content_frame):
    # Clear the main content frame
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Header
    header_label = ctk.CTkLabel(main_content_frame, text="Mood Tracker", font=("Arial", 24, "bold"))
    header_label.pack(pady=10)

    mood_label = ctk.CTkLabel(main_content_frame, text="How are you feeling today?", font=("Arial", 16))
    mood_label.pack(pady=10)

    # Dropdown for selecting mood
    moods = ["Happy", "Calm", "Confident", "Inspired", "Sad", "Fear", "Anger", "Shame", "Disgusted",
             "Indecisive", "Anxious", "Depressed", "Confused"]
    mood_colors = {
        "Happy": "#FFD700", "Calm": "#98FB98", "Confident": "#87CEEB", "Inspired": "#FF69B4",
        "Sad": "#4682B4", "Fear": "#FF4500", "Anger": "#DC143C", "Shame": "#8B0000",
        "Disgusted": "#556B2F", "Indecisive": "#A9A9A9", "Anxious": "#FF8C00",
        "Depressed": "#483D8B", "Confused": "#9370DB"
    }
    mood_var = ctk.StringVar(value="Select a Mood")
    mood_dropdown = ctk.CTkOptionMenu(main_content_frame, values=moods, variable=mood_var)
    mood_dropdown.pack(pady=10)

    custom_mood_label = ctk.CTkLabel(main_content_frame, text="Feeling something else?", font=("Arial", 14))
    custom_mood_label.pack(pady=5)

    custom_mood_entry = ctk.CTkEntry(main_content_frame)
    custom_mood_entry.pack(pady=5)

    # Graph area
    graph_frame = ctk.CTkFrame(main_content_frame)
    graph_frame.pack(pady=20, fill="both", expand=True)

    figure, ax = plt.subplots(figsize=(6, 4), dpi=100)

    def update_graph():
        if not mood_data:
            return

        # Prepare data
        times = [entry["time"] for entry in mood_data]
        moods_list = [entry["mood"] for entry in mood_data]
        colors = [mood_colors.get(mood, "#D3D3D3") for mood in moods_list]

        # Clear and update graph
        ax.clear()
        ax.bar(times, [1] * len(times), color=colors, tick_label=moods_list)
        ax.set_title("Mood Tracker", fontsize=16, fontweight="bold")
        ax.set_xlabel("Time & Date", fontsize=12)
        ax.set_ylabel("Mood", fontsize=12)
        ax.tick_params(axis="x", rotation=45)
        canvas.draw()

    canvas = FigureCanvasTkAgg(figure, graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Function to log mood
    def log_mood():
        selected_mood = mood_var.get()
        custom_mood = custom_mood_entry.get().strip()
        mood_to_log = custom_mood if custom_mood else selected_mood

        if not mood_to_log or mood_to_log == "Select a Mood":
            messagebox.showwarning("Invalid Input", "Please select or enter a valid mood.")
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mood_data.append({"mood": mood_to_log, "time": timestamp})
            with open("mood_data.txt", "a") as file:
                file.write(f"{timestamp}, {mood_to_log}\n")
            messagebox.showinfo("Mood Logged", f"Your mood '{mood_to_log}' has been recorded!")
            update_graph()

    submit_button = ctk.CTkButton(main_content_frame, text="Log Mood", command=log_mood, fg_color="#FFC0CB")
    submit_button.pack(pady=10)

    # Initial graph update
    update_graph()