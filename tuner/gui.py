
from ast import Break
import tkinter as tk
from queue import Empty, Queue


class TunerGUI:
    def __init__(self, root, result_queue):
        self.root = root
        self.result_queue = result_queue

        self.root.title("Guitar Tuner")
        self.root.geometry("400x300")

        title = tk.Label(
            root,
            text="Guitar Tuner",
            font=("Arial", 20)
        )
        title.pack(pady=(20, 10))

        self.note_label = tk.Label(
            root,
            text="—",
            font=("Arial", 48, "bold")
        )
        self.note_label.pack(pady=5)

        self.frequency_label = tk.Label(
            root,
            text="Waiting for audio...",
            font=("Arial", 14)
        )
        self.frequency_label.pack(pady=5)

        self.status_label = tk.Label(
            root,
            text="",
            font=("Arial", 16)
        )
        self.status_label.pack(pady=10)

        # Check for new measurements every 50 milliseconds
        self.root.after(50, self.check_queue)

    def check_queue(self):
        latest_result = None

        # Use the newest available measurement
        while True:
            try:
                latest_result = self.result_queue.get_nowait()
            except Empty:
                break

        if latest_result is not None:
            note, frequency, cents = latest_result

            self.note_label.config(text=note)
            self.frequency_label.config(
                text=f"{frequency:.2f} Hz"
            )

            if abs(cents) < 5:
                status = "In tune"
            elif cents < 0:
                status = f"Flat ({cents:+.1f} cents)"
            else:
                status = f"Sharp ({cents:+.1f} cents)"

            self.status_label.config(text=status)

        # Schedule the next check
        self.root.after(50, self.check_queue)


# Allow us to test the GUI without starting the microphone
if __name__ == "__main__":
    root = tk.Tk()
    result_queue = Queue()
    gui = TunerGUI(root, result_queue)
    root.mainloop()
