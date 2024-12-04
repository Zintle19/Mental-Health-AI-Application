import customtkinter as ctk
import os


def history_section(main_content_frame):
    # Clear the main content frame
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Header
    header_label = ctk.CTkLabel(main_content_frame, text="Journal History", font=("Arial", 24, "bold"))
    header_label.pack(pady=10)

    # Frame for displaying journal history
    history_frame = ctk.CTkFrame(main_content_frame, fg_color="white")
    history_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Textbox to display journal history
    history_textbox = ctk.CTkTextbox(history_frame, width=600, height=400, state="disabled")
    history_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    # Function to load and display journal entries
    def load_journal_entries():
        history_textbox.configure(state="normal")  # Enable the textbox for writing
        history_textbox.delete("1.0", "end")  # Clear the textbox

        if os.path.exists("journal_entries.txt"):
            with open("journal_entries.txt", "r") as file:
                entries = file.readlines()
                if entries:
                    for entry in entries:
                        history_textbox.insert("end", entry)
                else:
                    history_textbox.insert("end", "No journal entries found.")
        else:
            history_textbox.insert("end", "Your journal is empty. Start by writing your first journal entry!")

        history_textbox.configure(state="disabled")  # Disable the textbox to make it read-only

    # Load entries when the section is loaded
    load_journal_entries()