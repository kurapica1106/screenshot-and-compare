import PIL
import tkinter

class window_main():
    def __init__(self):
        self.window = tkinter.Tk()
        self.set_window_title("Screen Shot")
        self.create_widgets()
        self.window.mainloop()
    def set_window_title(self, title):
        self.window.title(title)
    def set_window_geometry(self, height, width):
        window_geometry = str(height) + "x" + str(height)
        self.window.geometry(window_geometry)
    def create_widgets(self):
        self.button_st = tkinter.Button(self.window)
        self.button_st["text"] = "Screen shot"
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
        pass
    def wind_show(self):
        pass
    def screen_shot(self):
        pass
    def event_exit(self):
        self.window.destroy()

app = window_main()