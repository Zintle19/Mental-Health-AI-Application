import customtkinter as ctk
from PIL import Image, ImageTk
import datetime
import tkinter.messagebox as messagebox
import os

def journal_section(main_content_frame):
    # Clear the main content frame
    for widget in main_content_frame.winfo_children():
        widget.destroy()

    # Header
    header_label = ctk.CTkLabel(main_content_frame, text="Personal Journal", font=("Arial", 24, "bold"))
    header_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Slideshow frame
    slideshow_frame = ctk.CTkFrame(main_content_frame, fg_color="white", width=300, height=400)
    slideshow_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Journal frame
    journal_frame = ctk.CTkFrame(main_content_frame, fg_color="white", width=600, height=400)
    journal_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Add slideshow images
    image_files = [r"F:\Mental Health AI Application\Journal 1.jpg", r"F:\Mental Health AI Application\Journal 2.jpg", r"F:\Mental Health AI Application\Journal 3.jpg", r"F:\Mental Health AI Application\Journal 4.jpg", r"F:\Mental Health AI Application\Journal 5.jpg", r"F:\Mental Health AI Application\Journal 6.jpg"]
    images = []

    for img_path in image_files:
        try:
            img = Image.open(img_path)
            img = img.resize((400, 400), Image.LANCZOS)
            images.append(ImageTk.PhotoImage(img))
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")

    # Current image index
    current_image_index = 0

    # Function to display the next image
    def next_image():
        nonlocal current_image_index
        if images:
            current_image_index = (current_image_index + 1) % len(images)
            slideshow_label.configure(image=images[current_image_index])
        main_content_frame.after(3000, next_image)  # Automatically switch images every 3 seconds

    # Label to display images
    slideshow_label = ctk.CTkLabel(slideshow_frame, image=images[0] if images else None, text="")
    slideshow_label.pack(fill="both", expand=True)

    # Start the slideshow
    if images:
        next_image()

    # Journal input section
    journal_label = ctk.CTkLabel(journal_frame, text="Write down your thoughts and feelings:", font=("Arial", 16))
    journal_label.pack(pady=10)

    journal_textbox = ctk.CTkTextbox(journal_frame, height=400, width=750, fg_color="#D3D3D3")
    journal_textbox.pack(pady=10)

    # Save journal entry
    def save_journal():
        entry_text = journal_textbox.get("1.0", "end").strip()
        if entry_text:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("journal_entries.txt", "a") as file:
                file.write(f"{timestamp}\n{entry_text}\n\n")
            journal_textbox.delete("1.0", "end")
            messagebox.showinfo("Entry Saved", "Your personal notes have been saved.")
        else:
            messagebox.showwarning("Empty Entry", "Your journal is empty.")

    save_button = ctk.CTkButton(journal_frame, text="Save Entry", command=save_journal, fg_color="#FFC0CB")
    save_button.pack(pady=10)