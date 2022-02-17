import time
import tkinter

class window_main(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen Shot")
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
    def screen_shot(self):
        self.withdraw()
        self.sub_app = window_full_screen(self)
        self.sub_app.mainloop()
    def event_exit(self):
        self.destroy()

class window_full_screen(tkinter.Tk):
    def __init__(self, window_main = tkinter.Tk):
        super().__init__()
        self.window_main = window_main
        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.25)
        self.create_canvas()
        self.bind("<Escape>", self.event_exit)
        self.bind("<B1-Motion>", self.event_create_rectangle)
        self.bind("<ButtonRelease-1>", self.event_save_rectangle)
        self.rec_exist = False
    def create_canvas(self):
        self.canvas = tkinter.Canvas(self,
                                     width = self.winfo_screenwidth(),
                                     height = self.winfo_screenheight())
        self.canvas.place(x = 0, y = 0)
    def event_exit(self, event):
        self.window_main.deiconify()
        self.destroy()
    def event_create_rectangle(self, event):
        if not self.rec_exist:
            self.x1 = event.x
            self.y1 = event.y
            self.canvas.create_rectangle(self.x1, self.y1, self.x1, self.y1,
                                         fill = "", outline = "red", tag = "rec")
        self.rec_exist = True
        self.canvas.delete("rec")
        self.x2 = event.x
        self.y2 = event.y
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                     fill = "", outline = "red", tag = "rec")
    def event_save_rectangle(self, event):
        self.rec_exist = False

app = window_main()
app.mainloop()