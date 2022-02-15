import re
import time
import tkinter
import win32con
import win32gui

class window_main():
    def __init__(self):
        self.window = tkinter.Tk()
        self.set_window_title("Screen Shot")
        self.create_widgets()
        self.wind_hwnd = int()
        self.window.mainloop()
    def set_window_title(self, title):
        self.window.title(title)
    def set_window_geometry(self, height, width):
        window_geometry = str(height) + "x" + str(height)
        self.window.geometry(window_geometry)
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
    def get_hwnd(self, hwnd, window_hwnd):
        if win32gui.IsWindow(hwnd) \
            and win32gui.IsWindowEnabled(hwnd) \
            and win32gui.IsWindowVisible(hwnd):
            window_hwnd.append(hwnd)
    def hwnd_find_by_title(self, pattern):
        window_hwnd = []
        win32gui.EnumWindows(self.get_hwnd, window_hwnd)
        window_detail = []
        for i in range(len(window_hwnd)):
            txt_class = win32gui.GetClassName(window_hwnd[i])
            txt_window = win32gui.GetWindowText(window_hwnd[i])
            txt_pattern = re.findall(pattern, txt_window)
            if len(txt_pattern) > 0:
                window_detail.append([window_hwnd[i], txt_class, txt_window])
        return window_detail
    def wind_hide(self):
        self.wind_hwnd = self.hwnd_find_by_title(self.button_st["text"])[0][0]
        win32gui.ShowWindow(self.wind_hwnd, win32con.SW_HIDE)
    def wind_show(self):
        win32gui.ShowWindow(self.wind_hwnd, win32con.SW_NORMAL)
    def screen_shot(self):
        self.wind_hide()
        time.sleep(2)
        self.wind_show()
    def event_exit(self):
        self.window.destroy()

app = window_main()
