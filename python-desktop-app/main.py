import tkinter as tk

from calculator import Calculator

# ── Constants ──────────────────────────────────────────────────────────────────
BG = "#1e1e2e"
BTN_BG = "#2a2a3d"
BTN_FG = "#cdd6f4"
ACC_BG = "#cba6f7"  # operator buttons
ACC_FG = "#1e1e2e"
EQ_BG = "#a6e3a1"  # equals button
EQ_FG = "#1e1e2e"
CLR_BG = "#f38ba8"  # clear button
CLR_FG = "#1e1e2e"
DISP_FG = "#cdd6f4"
FONT_MAIN = ("Courier", 32, "bold")
FONT_BTN = ("Courier", 18)


# ── UI ─────────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.calc = Calculator()
        self._build()

    def _build(self):
        # Display
        self.display_var = tk.StringVar(value="0")
        display = tk.Label(
            self,
            textvariable=self.display_var,
            font=FONT_MAIN,
            bg=BG,
            fg=DISP_FG,
            anchor="e",
            padx=16,
            pady=20,
            width=12,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="ew")

        # Button layout: (label, row, col, style, colspan)
        buttons = [
            ("C", 1, 0, "clr", 1),
            ("⌫", 1, 1, "acc", 1),
            ("%", 1, 2, "acc", 1),
            ("/", 1, 3, "acc", 1),  # noqa: E501
            ("7", 2, 0, "num", 1),
            ("8", 2, 1, "num", 1),
            ("9", 2, 2, "num", 1),
            ("*", 2, 3, "acc", 1),  # noqa: E501
            ("4", 3, 0, "num", 1),
            ("5", 3, 1, "num", 1),
            ("6", 3, 2, "num", 1),
            ("-", 3, 3, "acc", 1),  # noqa: E501
            ("1", 4, 0, "num", 1),
            ("2", 4, 1, "num", 1),
            ("3", 4, 2, "num", 1),
            ("+", 4, 3, "acc", 1),  # noqa: E501
            ("0", 5, 0, "num", 2),
            (".", 5, 2, "num", 1),
            ("=", 5, 3, "eq", 1),  # noqa: E501
        ]

        for label, row, col, style, colspan in buttons:
            bg, fg = self._style(style)
            btn = tk.Button(
                self,
                text=label,
                font=FONT_BTN,
                bg=bg,
                fg=fg,
                activebackground=fg,
                activeforeground=bg,
                relief="flat",
                bd=0,
                padx=8,
                pady=18,
                command=lambda lbl=label: self._on_click(lbl),
            )
            btn.grid(
                row=row,
                column=col,
                columnspan=colspan,
                sticky="nsew",
                padx=3,
                pady=3,
            )

        # Make grid cells expand evenly
        for i in range(4):
            self.columnconfigure(i, weight=1)
        for i in range(6):
            self.rowconfigure(i, weight=1)

        # Keyboard support
        self.bind("<Key>", self._on_key)

    def _style(self, style: str):
        return {
            "num": (BTN_BG, BTN_FG),
            "acc": (ACC_BG, ACC_FG),
            "eq": (EQ_BG, EQ_FG),
            "clr": (CLR_BG, CLR_FG),
        }[style]

    def _on_click(self, label: str):
        if label == "=":
            self.display_var.set(self.calc.evaluate())
        elif label == "C":
            self.display_var.set(self.calc.clear())
        elif label == "⌫":
            self.display_var.set(self.calc.backspace())
        else:
            self.display_var.set(self.calc.append(label))

    def _on_key(self, event: tk.Event):
        key = event.char
        if key in "0123456789.+-*/%":
            self._on_click(key)
        elif key in ("\r", "\n", "="):
            self._on_click("=")
        elif event.keysym == "BackSpace":
            self._on_click("⌫")
        elif key.lower() == "c":
            self._on_click("C")


if __name__ == "__main__":
    app = App()
    app.mainloop()
