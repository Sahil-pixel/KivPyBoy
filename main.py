import numpy as np

from pyboy import PyBoy
from pyboy.utils import WindowEvent

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.utils import platform
#For desktop we can use pygame to play audio for android pygame mixer also work but we dont need to add one more module 
#android media is enough 
if platform =='android':
    
    print("android")

else:
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()




ROM_PATH = "Metal Gear Solid (USA).gbc"#"Legend of Zelda, The - Link's Awakening DX (U) (V1.2) [C][!].gbc"
#




class AudioBridge:

    def __init__(self):

        self.android = (platform == "android")

        self.bridge = None

        if self.android:
            try:
                from jnius import autoclass

                JavaBridge = autoclass("org.test.pyboytest.AudioBridge")
                self.bridge = JavaBridge()

                print("AudioBridge ready")

            except Exception as e:
                print("AudioBridge init failed:", e)
        else:
            self.audio_channel = pygame.mixer.Channel(0)
            print("not android ")

    def play(self, audio):

        if not self.android:
            try:
                sound = pygame.sndarray.make_sound(audio)

                if not self.audio_channel.get_busy():
                    self.audio_channel.play(sound)

            except Exception as e:
                print("Audio error:", e)
                return  # desktop fallback (no-op or pygame if you want)

        if self.bridge:
            self.bridge.sendAudio(audio.tobytes())


class GBEmulator:

    def __init__(self, rom):
        self.pyboy = PyBoy(rom, window="null")

    def tick(self):
        self.pyboy.tick()

        frame = self.pyboy.screen.ndarray

        if frame.shape[2] == 4:
            frame = frame[:, :, :3]

        return frame

    def audio(self):
        try:
            return self.pyboy.sound.ndarray
        except:
            return None

    def press(self, event):
        self.pyboy.send_input(event)

    def release(self, event):
        self.pyboy.send_input(event)


#button map 
BUTTON_MAP = {
    "LEFT": (WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT),
    "RIGHT": (WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT),
    "UP": (WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP),
    "DOWN": (WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN),
    "A": (WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A),
    "B": (WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B),
    "START": (WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START),
    "SELECT": (WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT),
}



class GameBoyWidget(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.gb = GBEmulator(ROM_PATH)

        frame = self.gb.tick()
        h, w, _ = frame.shape

        self.texture = Texture.create(size=(w, h), colorfmt="rgb")
        self.texture.mag_filter = "nearest"
        self.texture.min_filter = "nearest"

        with self.canvas:
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.update_texture(frame)

        # UI
        self.build_buttons()

        # resize listener
        Window.bind(size=self.on_window_resize)

        # keyboard input
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)
        #if platform=='android':
        self.audio_backend = AudioBridge()
    



        # game loop
        Clock.schedule_interval(self.update, 1 / 60.0)

    
    def update_rect(self, *args):

        screen_ratio = 160 / 144

        w, h = self.width, self.height

        if w / h > screen_ratio:
            draw_h = h
            draw_w = h * screen_ratio
        else:
            draw_w = w
            draw_h = w / screen_ratio

        self.rect.size = (draw_w, draw_h)
        self.rect.pos = (self.x + (w - draw_w) / 2, self.y + (h - draw_h) / 2)

    def update_texture(self, frame):

        frame = np.flipud(frame)

        self.texture.blit_buffer(
            frame.tobytes(),
            colorfmt="rgb",
            bufferfmt="ubyte"
        )

        self.rect.texture = self.texture


    def update_audio(self):

        audio = self.gb.audio()
        #print(audio.dtype)
        #print(audio.min(), audio.max())
        if audio is None or audio.size == 0:
            return

        audio = np.asarray(audio)

     
        
        #audio = np.clip(audio, -1.0, 1.0)
        audio = audio.astype(np.int16) * 256

        audio = audio.astype(np.int16)

        #  mono to stereo
        if audio.ndim == 1:
            audio = np.column_stack((audio, audio))

        # 4. ensure memory layout is correct
        audio = np.ascontiguousarray(audio)

        # 
        self.audio_backend.play(audio)

    def _update_audio(self):

        audio = self.gb.audio()
        if audio is None or audio.size == 0:
            return

        audio = np.asarray(audio).astype(np.int16)

        # stereo fix
        if audio.ndim == 1:
            audio = np.column_stack((audio, audio))

        self.audio_backend.play(audio.tobytes())


    # def update_audio(self):

    #     audio = self.gb.audio()
    #     if audio is None:
    #         return

    #     audio = np.asarray(audio)

    #     # SAFE FIX (no overflow)
    #     audio = audio.astype(np.int16)
    #     audio = audio * 128

    #     # stereo conversion
    #     if audio.ndim == 1:
    #         audio = np.column_stack((audio, audio))

    #     try:
    #         sound = pygame.sndarray.make_sound(audio)

    #         if not self.audio_channel.get_busy():
    #             self.audio_channel.play(sound)

    #     except Exception as e:
    #         print("Audio error:", e)

    def update(self, dt):
        frame = self.gb.tick()
        if frame is not None:
            self.update_texture(frame)
            self.update_audio()

 
    def press_btn(self, key):
        self.gb.press(BUTTON_MAP[key][0])

    def release_btn(self, key):
        self.gb.release(BUTTON_MAP[key][1])

    def make_btn(self, text, key):

        btn = Button(
            text=text,
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            font_size=sp(14),
            background_color=(1, 1, 1, 0.25)
        )

        btn.bind(on_press=lambda *_: self.press_btn(key))
        btn.bind(on_release=lambda *_: self.release_btn(key))

        self.add_widget(btn)
        return btn

    def build_buttons(self):

        self.left_btn = self.make_btn("<", "LEFT")
        self.right_btn = self.make_btn(">", "RIGHT")
        self.up_btn = self.make_btn("^", "UP")
        self.down_btn = self.make_btn("v", "DOWN")

        self.a_btn = self.make_btn("A", "A")
        self.b_btn = self.make_btn("B", "B")

        self.start_btn = self.make_btn("START", "START")
        self.select_btn = self.make_btn("SELECT", "SELECT")

        self.update_controls_layout()


    def update_controls_layout(self):

        w, h = Window.width, Window.height

        btn = dp(70)
        pad = dp(20)
        gap = dp(10)

        # D-PAD (left bottom)
        self.left_btn.pos = (pad, h * 0.2 + btn + gap)
        self.right_btn.pos = (pad + btn * 2 + gap, h * 0.2 + btn + gap)

        self.up_btn.pos = (pad + btn + gap, h * 0.2 + btn * 2 + gap * 2)
        self.down_btn.pos = (pad + btn + gap, h * 0.2)

        # ACTION (right bottom)
        self.a_btn.pos = (w - pad - btn, h * 0.2 + btn + gap)
        self.b_btn.pos = (w - pad - btn * 2 - gap, h * 0.2 + btn + gap)

        # SYSTEM (bottom center)
        self.select_btn.pos = (w / 2 - btn * 2, dp(40))
        self.start_btn.pos = (w / 2 + btn, dp(40))

    def on_window_resize(self, *args):
        self.update_controls_layout()

  
    def on_key_down(self, window, key, scancode, codepoint, modifiers):

        mapping = {
            273: "UP",
            274: "DOWN",
            276: "LEFT",
            275: "RIGHT",
            ord("z"): "A",
            ord("x"): "B",
            13: "START",
            32: "SELECT",
        }

        if key in mapping:
            self.press_btn(mapping[key])

    def on_key_up(self, window, key, scancode):

        mapping = {
            273: "UP",
            274: "DOWN",
            276: "LEFT",
            275: "RIGHT",
            ord("z"): "A",
            ord("x"): "B",
            13: "START",
            32: "SELECT",
        }

        if key in mapping:
            self.release_btn(mapping[key])

class GameBoyApp(App):

    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        return GameBoyWidget()


if __name__ == "__main__":
    GameBoyApp().run()