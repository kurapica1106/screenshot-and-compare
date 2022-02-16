import time
import tkinter

class window_main():
    def __init__(self):
        self.window = tkinter.Tk()
        self.set_window_title("Screen Shot")
        self.create_widgets()
        self.window.mainloop()
    def set_window_title(self, title):
        self.window.title(title)
    def create_widgets(self):
        self.button_st = tkinter.Button(self.window)
        self.button_st["text"] = "Screen Shot"
        self.button_st["height"] = 2
        self.button_st["width"] = 13
        self.button_st["command"] = self.screen_shot
        self.button_st.grid(row = 0, column = 0,
                            padx = 5, pady = 5)
        self.button_exit = tkinter.Button(self.window)
        self.button_exit["text"] = "Exit"
        self.button_exit["height"] = 2
        self.button_exit["width"] = 13
        self.button_exit["command"] = self.event_exit
        self.button_exit.grid(row = 1, column = 0,
                              padx = 5, pady = 5)
    def wind_hide(self):
        self.window.withdraw()
    def wind_show(self):
        self.window.deiconify()
    def screen_shot(self):
        self.sub_app = window_full_screen()
    def event_exit(self):
        self.window.destroy()

class window_full_screen():
    def __init__(self):
        self.window_exist = True
        self.window = tkinter.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-alpha", 0.25)
        self.create_canvas()
        self.window.bind("<Escape>", self.event_exit)
        self.window.mainloop()
    def create_canvas(self):
        self.canvas = tkinter.Canvas(self.window,
                                     width = self.window.winfo_screenwidth(),
                                     height = self.window.winfo_screenheight())
        self.canvas.place(x = 0, y = 0)
        self.canvas.create_line(0, 0, 1440, 900)
    def event_exit(self, event):
        self.window_exist = False
        self.window.destroy()

app = window_main()
