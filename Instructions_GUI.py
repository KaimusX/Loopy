import tkinter as tk
from tkinter import Event

class InstructionsGUI:
    def create_gui(self):
        instructions = [
            "Space Bar - Pause/Play",
            "F - Full Screen Toggle",
            "Q - Quit Back To Home",
            "R - Restart Video",
            "J - Rewind 5 Seconds",
            "L - Fast Forward 5 Seconds",
            "H - Close Instructions Window (Select this window first)",
            "X - Open Instructions Window",
        ]

        root = tk.Tk()
        root.title("Player Instructions")

        text_widget = tk.Text(root, height=10, width=50, bg="black", fg="white")
        text_widget.pack()

        for instruction in instructions:
            text_widget.insert(tk.END, instruction + "\n")

        # Bind the 'H' key to the close_window method
        root.bind('h', self.close_window)

        root.mainloop()

    def close_window(self, event: Event):
        # Close the window
        event.widget.quit()

