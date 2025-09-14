import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
import csv
import os

class InputFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Input", padding=(8, 6))
        self.bowler_name_var = tk.StringVar()
        self.bowler_type_var = tk.StringVar(value="Fast")
        self.pitching_var = tk.StringVar(value="20.12")
        self.start_frame_var = tk.StringVar()
        self.end_frame_var = tk.StringVar()
        self.fps_var = tk.StringVar(value="30")

        ttk.Label(self, text="Bowler's Name:").grid(row=0, column=0, sticky="e", pady=3, padx=3)
        ttk.Entry(self, textvariable=self.bowler_name_var, width=12, justify="center").grid(row=0, column=1, pady=3)

        # Add combobox for bowler type
        ttk.Label(self, text="Bowler Type:").grid(row=1, column=0, sticky="e", pady=3, padx=3)
        self.bowler_type_cb = ttk.Combobox(
            self, textvariable=self.bowler_type_var, width=12, state="readonly",
            values=["Fast", "Medium-Fast", "Spinner"]
        )
        self.bowler_type_cb.grid(row=1, column=1, pady=3)

        ttk.Label(self, text="Pitching length (m):").grid(row=2, column=0, sticky="e", pady=3, padx=3)
        ttk.Entry(self, textvariable=self.pitching_var, width=12, justify="center").grid(row=2, column=1, pady=3)

        ttk.Label(self, text="Start-frame:").grid(row=3, column=0, sticky="e", pady=3, padx=3)
        ttk.Entry(self, textvariable=self.start_frame_var, width=12, justify="center").grid(row=3, column=1, pady=3)

        ttk.Label(self, text="End-frame:").grid(row=4, column=0, sticky="e", pady=3, padx=3)
        ttk.Entry(self, textvariable=self.end_frame_var, width=12, justify="center").grid(row=4, column=1, pady=3)

        ttk.Label(self, text="FPS:").grid(row=5, column=0, sticky="e", pady=3, padx=3)
        ttk.Entry(self, textvariable=self.fps_var, width=12, justify="center").grid(row=5, column=1, pady=3)


class OperationFrame(ttk.LabelFrame):
    def __init__(self, parent, on_calc, on_reset, on_exit, on_save):
        super().__init__(parent, text="Operation", padding=(8, 6))
        ttk.Button(self, text="Calc", command=on_calc).grid(row=0, column=0, pady=4, padx=2, sticky="ew")
        ttk.Button(self, text="Save", command=on_save).grid(row=0, column=1, pady=4, padx=2, sticky="ew")
        ttk.Button(self, text="Reset", command=on_reset).grid(row=1, column=0, columnspan=2, pady=4, padx=2, sticky="ew")
        ttk.Button(self, text="Exit", command=on_exit).grid(row=2, column=0, columnspan=2, pady=4, padx=2, sticky="ew")


class ResultFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Result", padding=(8, 6))
        self.diff_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.ms_var = tk.StringVar()
        self.kmh_var = tk.StringVar()
        self.mph_var = tk.StringVar()

        rows = [
            ("Δ-frame:", self.diff_var),
            ("Time (s):", self.time_var),
            ("Speed (mph):", self.mph_var),
            ("Speed (km/h):", self.kmh_var),
        ]
        for i, (lbl, var) in enumerate(rows):
            ttk.Label(self, text=lbl).grid(row=i, column=0, sticky="e", padx=10, pady=3)
            ttk.Entry(self, textvariable=var, width=15, foreground="darkblue", justify="center", state="readonly",).grid(row=i, column=1, padx=10, pady=3)


class BowlingSpeedCalculator:
    def __init__(self, root):
        self.root = root
        # self.root.iconbitmap('icon.ico')
        self.root.title("Cricket Bowling Speed Calculator")
        self.root.geometry("480x410")
        self.root.minsize(480, 410)
        self.root.resizable(True, True)

        # theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 9))
        style.configure("TEntry", font=("Segoe UI", 9), padding=(4, 2))
        style.configure("TButton", font=("Segoe UI", 9), padding=(4, 2))
        style.configure("TLabelframe", font=("Segoe UI", 9, "bold"), padding=(8, 6))
        style.configure("TLabelframe.Label", font=("Segoe UI", 9, "bold"))

        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # container
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # two coulmns layout
        content_frame.grid_columnconfigure(0, weight=1, uniform="content")
        content_frame.grid_columnconfigure(1, weight=1, uniform="content")

        # input section
        self.input_section = InputFrame(content_frame)
        self.input_section.grid(row=0, column=0, padx=(0, 8), pady=(0, 8), sticky="nsew")

        # operation section
        self.operation_section = OperationFrame(
            content_frame, self.calculate, self.reset, root.destroy, self.save_results
        )
        self.operation_section.grid(row=0, column=1, padx=(8, 0), pady=(0, 8), sticky="nsew")

        # result section
        self.result_frame = ResultFrame(content_frame)
        self.result_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        content_frame.grid_rowconfigure(1, weight=1)

        # error label
        self.error_label = ttk.Label(main_frame, text="", foreground="red", font=("Segoe UI", 9))
        self.error_label.grid(row=1, column=0, pady=(8, 0), sticky="w")

    def calculate(self):
        try:
            pitching = float(self.input_section.pitching_var.get())
            start_frame = int(self.input_section.start_frame_var.get())
            end_frame = int(self.input_section.end_frame_var.get())
            fps = float(self.input_section.fps_var.get())

            if end_frame <= start_frame:
                raise ValueError("End frame must be greater than start frame.")
            if fps <= 0:
                raise ValueError("Frame rate must be positive.")

            delta_frames = end_frame - start_frame
            time_sec = delta_frames / fps
            speed_ms = pitching / time_sec
            speed_kmh = speed_ms * 3.6
            speed_mph = speed_kmh * 0.621371

            self.result_frame.diff_var.set(f"{delta_frames}")
            self.result_frame.time_var.set(f"{time_sec:.3f}")
            self.result_frame.mph_var.set(f"{speed_mph:.2f}")
            self.result_frame.kmh_var.set(f"{speed_kmh:.2f}")
            self.result_frame.ms_var.set("")
            self.error_label.config(text="")
        except ValueError as e:
            self.error_label.config(text=f"Error: {e}")

    def reset(self):
        self.input_section.bowler_type_var.set("Fast")
        self.input_section.pitching_var.set("20.12")
        self.input_section.start_frame_var.set("")
        self.input_section.end_frame_var.set("")
        self.input_section.fps_var.set("30")
        self.result_frame.diff_var.set("")
        self.result_frame.time_var.set("")
        self.result_frame.mph_var.set("")
        self.result_frame.kmh_var.set("")
        self.result_frame.ms_var.set("")
        self.error_label.config(text="")

    def save_results(self):
        now = datetime.now()
        data = {
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%I:%M:%S %p"),
            "Bowler's Name": self.input_section.bowler_name_var.get(),
            "Bowler Type": self.input_section.bowler_type_var.get(),
            "Pitching length (m)": self.input_section.pitching_var.get(),
            "Start-frame": self.input_section.start_frame_var.get(),
            "End-frame": self.input_section.end_frame_var.get(),
            "FPS": self.input_section.fps_var.get(),
            "Δ-frame": self.result_frame.diff_var.get(),
            "Time (s)": self.result_frame.time_var.get(),
            "Speed (mph)": self.result_frame.mph_var.get(),
            "Speed (km/h)": self.result_frame.kmh_var.get(),
        }
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*")]
        )
        if file_path:
            try:
                write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
                with open(file_path, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if write_header:
                        writer.writerow(data.keys())
                    writer.writerow(data.values())
                self.error_label.config(text=f"Saved successfully. Time: {now.strftime('%I:%M:%S %p')}", foreground="green")
            except Exception as e:
                self.error_label.config(text=f"Save error: {e}", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = BowlingSpeedCalculator(root)
    root.mainloop()
