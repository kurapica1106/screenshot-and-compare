import time
import tkinter

class window_main(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen Shot")
        self.bind("<Escape>", self.event_show)
        self.create_widgets()
    def create_widgets(self):
        self.button_st = tkinter.Button(self)
        self.button_st["text"] = "Screen Shot"
        self.button_st["height"] = 2
        self.button_st["width"] = 13
        self.button_st["command"] = self.screen_shot
        self.button_st.grid(row = 0, column = 0,
                            padx = 5, pady = 5)
        self.button_exit = tkinter.Button(self)
        self.button_exit["text"] = "Exit"
        self.button_exit["height"] = 2
        self.button_exit["width"] = 13
        self.button_exit["command"] = self.event_exit
        self.button_exit.grid(row = 1, column = 0,
                              padx = 5, pady = 5)
    def wind_hide(self):
        self.withdraw()
    def wind_show(self):
        self.deiconify()
    def event_hide(self):
        self.attributes("-alpha", 0)
    def event_show(self, event):
        self.attributes("-alpha", 1)
    def screen_shot(self):
        self.event_hide()
        self.sub_app = window_full_screen()
        self.sub_app.mainloop()
    def event_exit(self):
        self.destroy()

class window_full_screen(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.25)
        self.create_canvas()
        self.bind("<Escape>", self.event_exit)
    def create_canvas(self):
        self.canvas = tkinter.Canvas(self,
                                     width = self.winfo_screenwidth(),
                                     height = self.winfo_screenheight())
        self.canvas.place(x = 0, y = 0)
        self.canvas.create_line(0, 0, 1440, 900)
    def event_exit(self, event):
        self.destroy()

app = window_main()
app.mainloop()