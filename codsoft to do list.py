import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # Import ttk for Combobox

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")
        master.geometry("500x650") # Increased width and height for new features
        master.resizable(True, True)
        master.config(bg="#f0f0f0")

        self.tasks = []
        self.current_filter = "All"

        self.title_label = tk.Label(master, text="My To-Do List", font=("Arial", 28, "bold"), bg="#f0f0f0", fg="#333333")
        self.title_label.pack(pady=20)

        self.input_frame = tk.Frame(master, bg="#f0f0f0")
        self.input_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.input_frame, width=30, font=("Arial", 14), bd=2, relief="groove")
        self.task_entry.pack(side=tk.LEFT, padx=10)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = tk.Button(self.input_frame, text="Add Task", font=("Arial", 12, "bold"),
                                    bg="#28a745", fg="white", activebackground="#218838",
                                    command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.tasks_frame = tk.Frame(master, bg="#f0f0f0")
        self.tasks_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(self.tasks_frame, width=45, height=15, font=("Arial", 14),
                                        bd=2, relief="sunken", selectbackground="#cce5ff", selectforeground="#000000",
                                        activestyle="none")
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        self.scrollbar = tk.Scrollbar(self.tasks_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.button_frame = tk.Frame(master, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        self.complete_button = tk.Button(self.button_frame, text="Mark Complete", font=("Arial", 12),
                                         bg="#007bff", fg="white", activebackground="#0056b3",
                                         command=self.mark_complete)
        self.complete_button.grid(row=0, column=0, padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit Task", font=("Arial", 12),
                                      bg="#ffc107", fg="black", activebackground="#e0a800",
                                      command=self.edit_task_popup)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Selected", font=("Arial", 12),
                                       bg="#dc3545", fg="white", activebackground="#c82333",
                                       command=self.delete_task)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.move_frame = tk.Frame(master, bg="#f0f0f0")
        self.move_frame.pack(pady=5)

        self.move_up_button = tk.Button(self.move_frame, text="Move Up", font=("Arial", 10),
                                        bg="#17a2b8", fg="white", activebackground="#138496",
                                        command=self.move_task_up)
        self.move_up_button.grid(row=0, column=0, padx=5)

        self.move_down_button = tk.Button(self.move_frame, text="Move Down", font=("Arial", 10),
                                          bg="#17a2b8", fg="white", activebackground="#138496",
                                          command=self.move_task_down)
        self.move_down_button.grid(row=0, column=1, padx=5)

        self.filter_frame = tk.Frame(master, bg="#f0f0f0")
        self.filter_frame.pack(pady=10)

        tk.Label(self.filter_frame, text="Show:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.filter_combobox = ttk.Combobox(self.filter_frame, values=["All", "Active", "Completed"],
                                            font=("Arial", 12), width=10, state="readonly")
        self.filter_combobox.set("All")
        self.filter_combobox.pack(side=tk.LEFT, padx=5)
        self.filter_combobox.bind("<<ComboboxSelected>>", self.apply_filter)

        self.clear_all_button = tk.Button(master, text="Clear All Tasks", font=("Arial", 12),
                                          bg="#6c757d", fg="white", activebackground="#545b62",
                                          command=self.clear_all_tasks)
        self.clear_all_button.pack(pady=10)

        self.load_tasks()
        self.update_listbox()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append((task, False))
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            # Convert listbox index back to actual task list index
            actual_index = self._get_actual_index(selected_index)
            if actual_index is not None:
                del self.tasks[actual_index]
                self.save_tasks()
                self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def mark_complete(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            actual_index = self._get_actual_index(selected_index)
            if actual_index is not None:
                task_text, is_completed = self.tasks[actual_index]
                self.tasks[actual_index] = (task_text, not is_completed) # Toggle completion status
                self.save_tasks()
                self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark complete/incomplete.")

    def edit_task_popup(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            actual_index = self._get_actual_index(selected_index)
            if actual_index is None:
                raise IndexError

            current_task_text, is_completed = self.tasks[actual_index]

            edit_window = tk.Toplevel(self.master)
            edit_window.title("Edit Task")
            edit_window.geometry("350x150")
            edit_window.resizable(False, False)
            edit_window.transient(self.master)
            edit_window.grab_set()

            tk.Label(edit_window, text="Edit Task Description:", font=("Arial", 12)).pack(pady=10)

            edit_entry = tk.Entry(edit_window, width=40, font=("Arial", 12))
            edit_entry.pack(pady=5)
            edit_entry.insert(0, current_task_text)
            edit_entry.focus_set()

            save_button = tk.Button(edit_window, text="Save Changes", font=("Arial", 10),
                                    bg="#28a745", fg="white", activebackground="#218838",
                                    command=lambda: self._save_edited_task(actual_index, edit_entry, edit_window))
            save_button.pack(pady=10)

            edit_window.protocol("WM_DELETE_WINDOW", edit_window.destroy)

            self.master.update_idletasks()
            x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (edit_window.winfo_width() // 2)
            y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (edit_window.winfo_height() // 2)
            edit_window.geometry(f"+{x}+{y}")

        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit.")

    def _save_edited_task(self, actual_index, entry_widget, popup_window):
        new_task_text = entry_widget.get().strip()
        if new_task_text:
            _, is_completed = self.tasks[actual_index]
            self.tasks[actual_index] = (new_task_text, is_completed)
            self.save_tasks()
            self.update_listbox()
            popup_window.destroy()
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty!", parent=popup_window)

    def move_task_up(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            actual_index = self._get_actual_index(selected_index)
            if actual_index is not None and actual_index > 0:
                self.tasks[actual_index], self.tasks[actual_index - 1] = \
                    self.tasks[actual_index - 1], self.tasks[actual_index]
                self.save_tasks()
                self.update_listbox()
                self.task_listbox.selection_set(selected_index - 1)
                self.task_listbox.activate(selected_index - 1)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to move.")

    def move_task_down(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            actual_index = self._get_actual_index(selected_index)
            if actual_index is not None and actual_index < len(self.tasks) - 1:
                self.tasks[actual_index], self.tasks[actual_index + 1] = \
                    self.tasks[actual_index + 1], self.tasks[actual_index]
                self.save_tasks()
                self.update_listbox()
                self.task_listbox.selection_set(selected_index + 1)
                self.task_listbox.activate(selected_index + 1)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to move.")

    def apply_filter(self, event=None):
        self.current_filter = self.filter_combobox.get()
        self.update_listbox()

    def _get_actual_index(self, listbox_index):
        visible_tasks = self._get_filtered_tasks()
        if listbox_index < len(visible_tasks):
            listbox_task_text = self.task_listbox.get(listbox_index)
            # Find the original index of this task in the main self.tasks list
            for i, (task_text, is_completed) in enumerate(self.tasks):
                if task_text == listbox_task_text and (i, task_text, is_completed) in self._get_original_filtered_tuples(visible_tasks):
                    return i
        return None

    def _get_original_filtered_tuples(self, filtered_tasks_display):
        original_tuples = []
        for task_display in filtered_tasks_display:
            for i, (task_text, is_completed) in enumerate(self.tasks):
                if task_text == task_display[0] and is_completed == task_display[1]:
                    original_tuples.append((i, task_text, is_completed))
                    break
        return original_tuples


    def clear_all_tasks(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?"):
            self.tasks = []
            self.save_tasks()
            self.update_listbox()

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        filtered_tasks = self._get_filtered_tasks()

        for i, (task_text, is_completed) in enumerate(filtered_tasks):
            self.task_listbox.insert(tk.END, task_text)
            if is_completed:
                self.task_listbox.itemconfig(i, fg="grey", selectforeground="grey")
            else:
                self.task_listbox.itemconfig(i, fg="black", selectforeground="black")

    def _get_filtered_tasks(self):
        if self.current_filter == "All":
            return self.tasks
        elif self.current_filter == "Active":
            return [task for task in self.tasks if not task[1]]
        elif self.current_filter == "Completed":
            return [task for task in self.tasks if task[1]]
        return []

    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            for task_text, is_completed in self.tasks:
                f.write(f"{task_text},{is_completed}\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(',', 1)
                    if len(parts) == 2:
                        task_text = parts[0]
                        is_completed = parts[1].lower() == 'true'
                        self.tasks.append((task_text, is_completed))
                    elif len(parts) == 1:
                        self.tasks.append((parts[0], False))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
