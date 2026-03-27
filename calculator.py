import math
from fractions import Fraction
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.clock import Clock

# iPhone用に画面とscaleを調整
scale = 2.5  # 画面に合わせて調整
Window.size = (320*scale, 480*scale)

WHITE = (1,1,1)
GRAY = (0.86,0.86,0.86)
DARK = (0.23,0.23,0.23)
ORANGE = (1,0.55,0)

class ButtonRect:
    def __init__(self, x, y, w, h, text, color):
        self.rect = (x, y, w, h)
        self.text = text
        self.color = color

class CalculatorWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expression = ""
        self.buttons = []
        self.create_buttons()
        self.bind(on_touch_down=self.on_touch)
        Clock.schedule_interval(lambda dt: self.canvas.clear() or self.draw(), 1/60)

    def create_buttons(self):
        labels = [
            ["√","^","(",")"],
            ["7","8","9","/"],
            ["4","5","6","×"],
            ["1","2","3","-"],
            ["0",".","C","+"],
            ["a/b","%","BS","="]
        ]
        for i, row in enumerate(labels):
            for j, text in enumerate(row):
                x = j*80
                y = 480 - ((i+1)*60 + 120)
                color = ORANGE if text in ["+","-","×","/","="] else DARK
                self.buttons.append(ButtonRect(x, y, 80, 60, text, color))

    def draw(self):
        with self.canvas:
            # 背景
            Color(*WHITE)
            Rectangle(pos=(0,0), size=Window.size)
            # 表示欄
            Color(*GRAY)
            Rectangle(pos=(0, 480-120), size=(320, 120))
            # 上の文字
            display_text = self.expression[-18:] if self.expression else ""
            label = CoreLabel(text=display_text, font_size=32*scale)
            label.refresh()
            texture = label.texture
            self.canvas.add(Color(0,0,0))
            self.canvas.add(Rectangle(texture=texture, pos=(10*scale, 480-80*scale), size=texture.size))
            # ボタン描画
            for btn in self.buttons:
                Color(*btn.color)
                Rectangle(pos=(btn.rect[0]*scale, btn.rect[1]*scale), size=(btn.rect[2]*scale, btn.rect[3]*scale))
                label = CoreLabel(text=btn.text, font_size=28*scale)
                label.refresh()
                texture = label.texture
                self.canvas.add(Color(1,1,1))
                self.canvas.add(Rectangle(texture=texture, pos=(btn.rect[0]*scale+20*scale, btn.rect[1]*scale+15*scale), size=texture.size))

    def on_touch(self, touch):
        for btn in self.buttons:
            x, y, w, h = [v*scale for v in btn.rect]
            if x <= touch.x <= x+w and y <= touch.y <= y+h:
                self.handle_button(btn.text)

    def handle_button(self, text):
        if text == "C":
            self.expression = ""
        elif text == "BS":
            self.expression = self.expression[:-1]
        elif text == "=":
            self.expression = self.safe_eval(self.expression)
        elif text == "√":
            self.expression += "√("
        elif text == "^":
            self.expression += "^"
        elif text == "a/b":
            self.expression += "/"
        else:
            self.expression += text

    def safe_eval(self, expr):
        try:
            expr = expr.replace("^", "**")
            expr = expr.replace("√", "math.sqrt")
            expr = expr.replace("×", "*")
            expr = expr.replace("%", "/100")

            if "a/b" in expr:
                parts = expr.split("/")
                if len(parts) == 2:
                    result = float(Fraction(int(parts[0]), int(parts[1])))
            else:
                result = eval(expr, {"__builtins__": None}, {"math": math, "Fraction": Fraction})

            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            return str(result)
        except:
            return "Error"

class CalculatorApp(App):
    def build(self):
        return CalculatorWidget()

if __name__ == "__main__":
    CalculatorApp().run()