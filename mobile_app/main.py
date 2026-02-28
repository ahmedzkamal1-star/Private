from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from auth_manager import AuthManager
from security_logic import SecurityShield
from kivy.core.text import LabelBase
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from kivy.properties import StringProperty
import os
import platform
import logging
import requests
import json

# Register Arabic font globally
if platform.system() == 'Windows':
    arial_path = 'C:\\Windows\\Fonts\\arial.ttf'
    if os.path.exists(arial_path):
        LabelBase.register(name='Roboto', 
                           fn_regular=arial_path,
                           fn_bold='C:\\Windows\\Fonts\\arialbd.ttf')
        LabelBase.register(name='Arabic', fn_regular=arial_path)

# Translations Dictionary
TRANSLATIONS = {
    'ar': {
        'login_title': 'تسجيل الدخول',
        'login_subtitle': 'الرجاء إدخال بياناتك للوصول للمواد',
        'student_code': 'كود الطالب',
        'footer_version': 'الإصدار 1.0.6 - منصة الداحي',
        'dashboard_title': 'لوحة التحكم',
        'welcome_msg': 'مرحباً بك يا بطل!',
        'welcome_sub': 'الداحي معاك خطوة بخطوة',
        'welcome': 'مرحباً بك في منصة الداحي التعليمية',
        'login_btn': 'الدخول الان',
        'user_code': 'الكود الجامعي',
        'password': 'كلمة المرور',
        'courses_header': 'المواد الدراسية',
        'menu_lang_en': 'English Language',
        'menu_lang_ar': 'اللغة العربية',
        'menu_theme_dark': 'الوضع المظلم',
        'menu_theme_light': 'الوضع السماوي (الافتراضي)',
        'logout': 'تسجيل خروج',
        'back_btn': 'رجوع',
        'lessons_header': 'دروس المادة',
        'no_courses': 'لا توجد مواد مسجلة',
        'no_lessons': 'لا توجد دروس في هذه المادة',
        'security_alert': 'تحذير أمني!',
        'violation_msg': 'تم رصد مخالفة أمنية! سيتم إغلاق التطبيق.',
        'exit': 'خروج'
    },
    'en': {
        'login_title': 'Student Login',
        'login_subtitle': 'Please enter your credentials',
        'student_code': 'Student ID',
        'footer_version': 'Version 1.0.6 - El-Dahih',
        'dashboard_title': 'Dashboard',
        'welcome_msg': 'Welcome Hero!',
        'welcome_sub': 'Ready to study today?',
        'welcome': 'Welcome to El-Dahih Platform',
        'login_btn': 'Login Now',
        'user_code': 'Student Code',
        'password': 'Password',
        'courses_header': 'Your Courses',
        'menu_lang_en': 'English Language',
        'menu_lang_ar': 'اللغة العربية',
        'menu_theme_dark': 'Dark Mode',
        'menu_theme_light': 'Sky Blue Mode (Default)',
        'logout': 'Logout',
        'back_btn': 'Back',
        'lessons_header': 'Course Lessons',
        'no_courses': 'No courses found',
        'no_lessons': 'No lessons in this course',
        'security_alert': 'Security Alert!',
        'violation_msg': 'Security violation detected! App will close.',
        'exit': 'Exit'
    }
}

def f_ar(text):
    """Reshapes and reorders Arabic text for Kivy labels."""
    if not text: return ""
    reshaped_text = reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

Window.size = (360, 640)

class LoginScreen(Screen):
    def on_enter(self, *args):
        try:
            shield = SecurityShield()
            if shield.check_root():
                self.show_fatal_error(f_ar("عذراً، لا يمكن تشغيل التطبيق على أجهزة تحتوي على صلاحيات الروت لضمان الأمان."))
            elif shield.is_emulator():
                self.show_fatal_error(f_ar("عذراً، يمنع استخدام المحاكيات. يرجى استخدام هاتف حقيقي."))
        except Exception as e:
            logging.error(f"Startup check bypass: {e}")

    def do_login(self, code, password):
        if not code or not password:
            self.show_error(f_ar("يرجى إدخال البيانات كاملة"))
            return
            
        auth = AuthManager()
        success, message = auth.login(code, password)
        
        if success:
            MDApp.get_running_app().root.current = 'dashboard'
        else:
            self.ids.user_code.error = True
            self.ids.password.error = True
            self.show_error(f_ar(message))

    def show_error(self, text):
        self.dialog = MDDialog(
            title=f_ar("خطأ"),
            text=text,
            buttons=[MDFlatButton(text=f_ar("حسناً"), theme_text_color="Custom", text_color=MDApp.get_running_app().theme_cls.primary_color, on_release=lambda x: self.dialog.dismiss())],
        )
        self.dialog.open()
        
    def show_fatal_error(self, text):
        self.dialog = MDDialog(
            text=text,
            title=f_ar("تحذير!"),
            buttons=[MDFlatButton(text=f_ar("خروج"), on_release=lambda x: os._exit(0))],
        )
        self.dialog.auto_dismiss = False
        self.dialog.open()

class DashboardScreen(Screen):
    def on_enter(self, *args):
        self.load_courses()
        Clock.schedule_once(self.monitor_security, 10)

    def load_courses(self):
        auth = AuthManager()
        app = MDApp.get_running_app()
        try:
            url = f"{AuthManager.base_url()}/api/courses"
            headers = auth.get_headers()
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                courses = response.json()
                self.ids.courses_list.clear_widgets()
                
                if not courses:
                    self.ids.courses_list.add_widget(MDLabel(text=app.get_text('no_courses'), halign="center", theme_text_color="Hint"))
                    return

                for course in courses:
                    from kivymd.uix.card import MDCard
                    from kivymd.uix.boxlayout import MDBoxLayout
                    card = MDCard(size_hint_y=None, height="80dp", padding="10dp", radius="12dp", elevation=1, on_release=lambda x, c=course: self.show_lessons(c['id'], c['name']))
                    layout = MDBoxLayout(orientation='horizontal')
                    icon = MDIcon(icon="book-open-page-variant", theme_text_color="Custom", text_color=get_color_from_hex("#00B4D8"), pos_hint={"center_y": .5})
                    label = MDLabel(text=app.f_ar(course['name']), font_name="Arabic", halign="right" if app.current_lang == 'ar' else "left", pos_hint={"center_y": .5})
                    layout.add_widget(icon)
                    layout.add_widget(label)
                    card.add_widget(layout)
                    self.ids.courses_list.add_widget(card)
        except Exception as e:
            logging.error(f"Error loading courses: {e}")

    def show_lessons(self, course_id, course_name):
        auth = AuthManager()
        app = MDApp.get_running_app()
        try:
            url = f"{AuthManager.base_url()}/api/lessons/{course_id}"
            headers = auth.get_headers()
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                lessons = response.json()
                self.ids.courses_list.clear_widgets()
                self.ids.section_title.text = app.f_ar(course_name)
                
                self.ids.courses_list.add_widget(MDRectangleFlatIconButton(text=app.get_text('back_btn'), icon="arrow-left" if app.current_lang == 'en' else "arrow-right", on_release=lambda x: self.load_courses(), font_name="Arabic"))

                if not lessons:
                    self.ids.courses_list.add_widget(MDLabel(text=app.get_text('no_lessons'), halign="center"))
                    return

                for lesson in lessons:
                    from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
                    item = OneLineIconListItem(text=app.f_ar(lesson['title']), on_release=lambda x, l=lesson: self.open_lesson(l['id'], l['title']))
                    item.add_widget(IconLeftWidget(icon="file-pdf-box" if lesson['content_type'] == 'pdf' else "video"))
                    self.ids.courses_list.add_widget(item)
        except Exception as e:
            logging.error(f"Error loading lessons: {e}")

    def open_lesson(self, lesson_id, title):
        auth = AuthManager()
        app = MDApp.get_running_app()
        try:
            url = f"{AuthManager.base_url()}/api/secure_content/lesson/{lesson_id}"
            headers = auth.get_headers()
            response = requests.get(url, headers=headers, timeout=60, stream=True)
            
            if response.status_code == 200:
                Snackbar(text=app.f_ar(f"تم تحميل '{title}' بنجاح وجارِ العرض..."), font_name="Arabic").open()
            else:
                app.root.get_screen('login').show_error(app.f_ar("عذراً، الرابط غير متاح."))
        except Exception as e:
            logging.error(f"Download error: {e}")

    def monitor_security(self, dt):
        shield = SecurityShield()
        if shield.check_vpn() or shield.check_root() or shield.check_recording():
            os._exit(0)
        Clock.schedule_once(self.monitor_security, 30)

class SecurePlatformApp(MDApp):
    current_lang = StringProperty('ar')
    
    def get_text(self, key):
        text = TRANSLATIONS[self.current_lang][key]
        return f_ar(text) if self.current_lang == 'ar' else text

    def f_ar(self, text):
        return f_ar(text)

    def change_language(self, lang):
        self.current_lang = lang
        if hasattr(self, 'menu'): self.menu.dismiss()
        self.root.get_screen('dashboard').load_courses()

    def set_theme(self, theme):
        self.theme_cls.theme_style = theme
        if hasattr(self, 'menu'): self.menu.dismiss()

    def show_settings_menu(self, button):
        menu_items = [
            {"text": self.get_text('menu_lang_en'), "viewclass": "OneLineListItem", "on_release": lambda x="en": self.change_language(x)},
            {"text": self.get_text('menu_lang_ar'), "viewclass": "OneLineListItem", "on_release": lambda x="ar": self.change_language(x)},
            {"text": self.get_text('menu_theme_dark'), "viewclass": "OneLineListItem", "on_release": lambda x="Dark": self.set_theme(x)},
            {"text": self.get_text('menu_theme_light'), "viewclass": "OneLineListItem", "on_release": lambda x="Light": self.set_theme(x)}
        ]
        self.menu = MDDropdownMenu(caller=button, items=menu_items, width_mult=4)
        self.menu.open()

    def build(self):
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        
        try:
            SecurityShield.enable_screenshot_protection()
        except: pass
            
        try:
            import certifi
            os.environ['SSL_CERT_FILE'] = certifi.where()
        except: pass

        Builder.load_file('app_ui.kv')
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    SecurePlatformApp().run()
