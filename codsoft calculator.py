import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Mobile Calculator")
        master.geometry("320x500")
        master.resizable(False, False)

        # Color and style
        self.bg_color = "#1e1e1e"
        self.button_color = "#2e2e2e"
        self.operator_color = "#f7af68"
        self.clear_del_color = "#666666"
        self.equals_color = "#6a8ff5"
        self.text_color = "#ffffff"
        self.hover_color = "#444444"
        self.active_color = "#888888"
        self.font_family = "Segoe UI"

        self.master.configure(bg=self.bg_color)

        self.current_expression = ""
        self.history_expression = ""
        self.input_text = tk.StringVar()
        self.history_text = tk.StringVar()

        # Display History
        self.history_label = tk.Label(
            master, textvariable=self.history_text, anchor="e",
            font=(self.font_family, 14), bg=self.bg_color,
            fg="#aaaaaa", padx=10
        )
        self.history_label.grid(row=0, column=0, columnspan=4, sticky="we", pady=(15, 0))

        # Display Input
        self.display = tk.Entry(
            master, textvariable=self.input_text, font=(self.font_family, 26, "bold"),
            bg=self.bg_color, fg=self.text_color, bd=0,
            justify='right', insertwidth=2, relief="flat"
        )
        self.display.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        self.display.bind("<Key>", self.key_press)
        self.display.focus_set()

        # Grid Configuration
        for i in range(6):
            master.grid_rowconfigure(i+2, weight=1)
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)

        # Button config
        buttons_config = [
            ('C', 2, 0, self.clear_del_color), ('DEL', 2, 1, self.clear_del_color),
            ('(', 2, 2, self.operator_color), (')', 2, 3, self.operator_color),
            ('7', 3, 0, self.button_color), ('8', 3, 1, self.button_color), ('9', 3, 2, self.button_color), ('/', 3, 3, self.operator_color),
            ('4', 4, 0, self.button_color), ('5', 4, 1, self.button_color), ('6', 4, 2, self.button_color), ('*', 4, 3, self.operator_color),
            ('1', 5, 0, self.button_color), ('2', 5, 1, self.button_color), ('3', 5, 2, self.button_color), ('-', 5, 3, self.operator_color),
            ('0', 6, 0, self.button_color), ('.', 6, 1, self.button_color), ('=', 6, 2, self.equals_color), ('+', 6, 3, self.operator_color)
        ]

        for (text, row, col, color) in buttons_config:
            button = tk.Button(
                master, text=text, bg=color, fg=self.text_color,
                font=(self.font_family, 18, "bold"), bd=0,
                activebackground=self.active_color, relief="flat",
                command=lambda t=text: self.on_button_press(t)
            )
            button.grid(row=row+1, column=col, padx=5, pady=5, sticky="nsew")
            button.bind("<Enter>", lambda e, b=button: b.config(bg=self.hover_color))
            button.bind("<Leave>", lambda e, b=button, c=color: b.config(bg=c))

    def on_button_press(self, char):
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.clear_expression()
        elif char == 'DEL':
            self.delete_last_char()
        else:
            if char in "+-*/" and self.current_expression.endswith(char):
                return  # Prevent duplicate operators
            self.current_expression += str(char)
            self.input_text.set(self.current_expression)

    def clear_expression(self):
        self.current_expression = ""
        self.input_text.set("")
        self.history_text.set("")

    def delete_last_char(self):
        self.current_expression = self.current_expression[:-1]
        self.input_text.set(self.current_expression)

    def calculate(self):
        try:
            result = str(eval(self.current_expression))
            self.history_text.set(self.current_expression + " =")
            self.input_text.set(result)
            self.current_expression = result
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero.")
            self.clear_expression()
        except Exception:
            messagebox.showerror("Error", "Invalid expression.")
            self.clear_expression()

    def key_press(self, event):
        valid_keys = "0123456789+-*/()."
        if event.char in valid_keys:
            self.current_expression += event.char
            self.input_text.set(self.current_expression)
        elif event.keysym == 'Return':
            self.calculate()
        elif event.keysym == 'BackSpace':
            self.delete_last_char()
        elif event.keysym == 'Escape':
            self.clear_expression()
        return "break"  # Prevent text insertion into Entry

# Launch App
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
