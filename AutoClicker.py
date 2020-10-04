import rumps
from pynput import mouse, keyboard

class AutoClicker(rumps.App):
    def __init__(self):
        

        super().__init__(name="AutoClicker", icon="mouselogo.icns")
            
        default_value = 0.0
        self.cps_value = AutoClicker.map_slider_to_cps(default_value)
        self.click_timer = rumps.Timer(lambda _ : self.mouse.click(mouse.Button.left), 1/self.cps_value)

        def timer_start(_):
            print(rumps.timers())
            self.click_timer.start()

        self.menu = [
            rumps.MenuItem("Start", timer_start),
            "Stop key: esc",
            None,
            "cps_value",
            rumps.SliderMenuItem(dimensions=(180,15), callback=self.change_cps, min_value = -1, max_value=5, value=default_value),
            None
        ]
        
        self.menu["cps_value"].title = f"CPS: {self.cps_value}"

        self.mouse = mouse.Controller()

        self.check_keys()

        
        
    
    @staticmethod
    def map_slider_to_cps(slide_val):
        base = 2
        if base**slide_val > 10:
            return int(base**slide_val)

        return round(base**slide_val, 2)

    def change_cps(self, slider):
        # map slider.value non-linearly to cps_value
        self.cps_value = AutoClicker.map_slider_to_cps(slider.value)
        self.menu["cps_value"].title = f"CPS: {self.cps_value}"

        self.click_timer.interval = 1/self.cps_value

    def check_keys(self):
        def on_press(key):
            if key == keyboard.Key.esc:
                print("stop")
                for t in rumps.timers(): # just in case things get out of sync
                    t.stop()
                

        self.listener = keyboard.Listener(
            on_press = on_press
        )
        self.listener.start()

AutoClicker().run()