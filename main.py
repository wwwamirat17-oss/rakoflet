from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import threading
import time
import requests
from bs4 import BeautifulSoup

TOKEN = "8304126927:AAGKnXke0AY-T-YVxMJJonCs1q26nCbrRPo"
CHAT_ID = "8309958339"
URL_SITE = "https://minha.anem.dz/pre_inscription"

running = False

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_loop():
    global running
    while running:
        try:
            r = requests.get(URL_SITE, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            if "لا توجد مواعيد" not in soup.text:
                send_telegram_message("✅ يوجد موعد متاح الآن!")
            time.sleep(30)
        except:
            time.sleep(30)

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        self.status_label = Label(text="اضغط لبدء المراقبة")
        start_btn = Button(text="بدء المراقبة", on_press=self.start_check)
        stop_btn = Button(text="إيقاف المراقبة", on_press=self.stop_check)
        layout.add_widget(self.status_label)
        layout.add_widget(start_btn)
        layout.add_widget(stop_btn)
        return layout

    def start_check(self, instance):
        global running
        if not running:
            running = True
            threading.Thread(target=check_loop, daemon=True).start()
            self.status_label.text = "📡 المراقبة بدأت..."

    def stop_check(self, instance):
        global running
        running = False
        self.status_label.text = "⏹ تم إيقاف المراقبة"

if __name__ == "__main__":
    MainApp().run()
