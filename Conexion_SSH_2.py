import paramiko
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("500x400")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.ip_label = tk.Label(self, text="IP:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(self)
        self.ip_entry.pack()

        self.user_label = tk.Label(self, text="User:")
        self.user_label.pack()
        self.user_entry = tk.Entry(self)
        self.user_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.connect_button = tk.Button(self, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.command_label = tk.Label(self, text="Command:")
        self.command_label.pack()
        self.command_entry = tk.Entry(self)
        self.command_entry.pack()

        self.execute_button = tk.Button(self, text="Execute", command=self.execute_command)
        self.execute_button.pack()

        self.response_label = tk.Label(self, text="")
        self.response_label.pack()

        self.master.protocol("WM_DELETE_WINDOW", self.quit)

    def connect(self):
        ip = self.ip_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(ip, username=user, password=password)
        except Exception as e:
            self.response_label.configure(text="Error connecting: " + str(e))
            return

        self.client = client
        self.response_label.configure(text="Connected to " + ip)

    def execute_command(self):
        command = self.command_entry.get()

        if not hasattr(self, 'client'):
            self.response_label.configure(text="Not connected to any server.")
            return

        stdin, stdout, stderr = self.client.exec_command(command)
        response = stdout.read().decode()

        self.response_label.configure(text=response)

    def quit(self):
        if hasattr(self, 'client'):
            self.client.close()
        self.master.destroy()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
