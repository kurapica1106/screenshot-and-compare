import tkinter

class window_test():
    def __init__(self):
        self.window = tkinter.Tk()
        self.create_widgets()
        self.window.mainloop()
    def create_widgets(self):
        self.button_exit = tkinter.Button(self.window)
        self.button_exit["text"] = "Exit"
        self.button_exit["command"] = self.event_exit
        self.button_exit.grid(row = 0, column = 0)
    def event_exit(self):
        self.window.destroy()

app = window_test()