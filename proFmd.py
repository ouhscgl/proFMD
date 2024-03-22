# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 20:58:58 2024

@author: zalka
"""

import tkinter as tk
import time
import pyautogui
import json
import sys
from pynput import keyboard

class medicabg_TimerApp:
    def __init__(self, master):
        
        #TEST
        self.set_file = 'settings.json'
        
        # Initialize basic variables
        self.master = master
        self.st_time = None
        self.running = True
        
        # Initialize label
        self.timer_label = tk.Label(master,text="00:00.0")
        self.timer_label.pack()
        
        # Import setup variables
        try:
            with open(self.set_file, 'r') as f:
                self.sd = json.load(f)
        except FileNotFoundError:
            self.sd = {"x_offset": 200,
                       "y_offset": 100,
                       "timer"   : 30,
                       "x_mouse" : 200,
                       "y_mouse" : 100,
                       "input_char"   :'\x03'}
            with open('settings.json', 'w') as j:
                json.dump(self.sd, j, indent=4)
        
        # Set window to foreground, permanently
        master.attributes("-topmost", True)
        
        # Set window location
        width_screen, height_screen = pyautogui.size()
        x_offset = self.sd["x_offset"]
        y_offset = self.sd["y_offset"]
        master.geometry(f"+{width_screen - x_offset}+{height_screen - y_offset}")
        
        # Trigger
        self.listener = keyboard.Listener(on_press = self.on_press)
        self.listener.start()
    
    def on_press(self,key):
        if key == keyboard.KeyCode(char=self.sd["input_char"]):
            self.listener.stop()
            self.start_timer()
        
    def start_timer(self):
        if self.st_time is None:
            self.st_time = time.time()
            self.update_timer()
    
    def update_timer(self):
        if self.running == True:
            # Update timer value
            cu_time = time.time() - self.st_time
        
            mi = int(cu_time / 60)      
            se = int(cu_time % 60)
            de = int((cu_time % 1) * 10)
        
            self.timer_label.config(text="{:02d}:{:02d}.{}".format(mi, se, de))
        
            # Trigger event
            if cu_time > self.sd["timer"]:
                self.execute_command()
        
            # Sleep for 100ms, then update_timer()
            self.master.after(100, self.update_timer)
    
    # Perform the 'click' action
    def execute_command(self):
        pyautogui.click(self.sd["x_mouse"], self.sd["y_mouse"])
        self.running = False
    
def main():
    root = tk.Tk()
    root.title("Simple Timer")
    app = medicabg_TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    
#     if __name__ == "__main__":
#         if len(sys.argv) != 4:
#             print("Incorrect parameters. For more information, add -h argument.")

#         # runfile('ntpsync.py', args='time.google.com setup.json log.csv')
#         # https://yash7.medium.com/how-to-turn-your-python-script-into-an-executable-file-d64edb13c2d4

#         srv_locs = sys.argv[1]
#         set_file = sys.argv[2]
#         log_file = sys.argv[3]

#         listener = InputListener(srv_locs, set_file, log_file)
#         listener_thread = threading.Thread(target=listener.start)

#         try:
#             listener_thread.start()
#             listener_thread.join()
#         except KeyboardInterrupt:
#             listener.quitp()
#             listener_thread.join()
#         finally:
#             listener_thread.join()
