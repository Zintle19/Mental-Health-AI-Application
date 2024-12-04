import customtkinter as ctk
from mood_tracker import mood_tracker
from journal import journal_section
from conversational_bot import conversational_bot
from history import history_section
from PIL import Image
import sys  # Import sys module to access command-line arguments

def create_dashboard(username):
    # Initialize the root window
    root = ctk.CTk()
    root.title("Mental Health Dashboard")
    root.geometry("1200x700")

    # Sidebar frame
    sidebar_frame = ctk.CTkFrame(root, width=250, fg_color="#E6E6FA")
    sidebar_frame.pack(side="left", fill="y")

    # Frame for the "Welcome User" section
    welcome_frame = ctk.CTkFrame(sidebar_frame, fg_color="#87CEEB", height=100)
    welcome_frame.pack(fill="x")

    # Welcome label, display the dynamic username
    welcome_label = ctk.CTkLabel(
        welcome_frame, text=f"Welcome, {username}!", font=("Arial", 18, "bold"), text_color="black"
    )
    welcome_label.pack(pady=20)

    # Frame for navigation buttons
    nav_buttons_frame = ctk.CTkFrame(sidebar_frame, fg_color="#F5F5F5")
    nav_buttons_frame.pack(fill="both", expand=True, pady=10, padx=10)

    # Main content frame
    main_content_frame = ctk.CTkFrame(root, fg_color="#FFFFFF")
    main_content_frame.pack(side="right", fill="both", expand=True)

    # Load icons for buttons
    def load_icon(path):
        try:
            return ctk.CTkImage(light_image=Image.open(path), size=(30, 30))
        except Exception as e:
            print(f"Error loading icon: {e}")
            return None

    # Use forward slashes or double backslashes
    mood_icon = load_icon("Mood tracker icon.png")
    journal_icon = load_icon("journal_section icon.png")
    bot_icon = load_icon("Chatbot icon.png")
    history_icon = load_icon("history icon.png")

    # Navigation buttons
    ctk.CTkButton(
        nav_buttons_frame,
        text="Mood Tracker",
        image=mood_icon,
        compound="left",
        fg_color="#FFC0CB",
        command=lambda: mood_tracker(main_content_frame),
    ).pack(pady=10, fill="x")

    ctk.CTkButton(
        nav_buttons_frame,
        text="Personal Journal",
        image=journal_icon,
        compound="left",
        fg_color="#87CEEB",
        command=lambda: journal_section(main_content_frame),
    ).pack(pady=10, fill="x")

    ctk.CTkButton(
        nav_buttons_frame,
        text="Conversational Bot",
        image=bot_icon,
        compound="left",
        fg_color="#FFC0CB",
        command=lambda: conversational_bot(main_content_frame),
    ).pack(pady=10, fill="x")

    ctk.CTkButton(
        nav_buttons_frame,
        text="History",
        image=history_icon,
        compound="left",
        fg_color="#87CEEB",
        command=lambda: history_section(main_content_frame),
    ).pack(pady=10, fill="x")

    # Start with Mood Tracker as the default view
    mood_tracker(main_content_frame)

    root.mainloop()


# Main loop to start the dashboard
if __name__ == "__main__":
    # Check if username was passed as a command-line argument
    if len(sys.argv) < 2:
        print("Error: No username passed to dashboard.")
        exit(1)

    # Get the username from the command-line argument
    username = sys.argv[1]
    create_dashboard(username)
