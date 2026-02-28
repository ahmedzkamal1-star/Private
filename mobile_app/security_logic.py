import os
import platform
from kivy.utils import platform as kivy_platform

def is_android():
    return kivy_platform == 'android'

class SecurityShield:
    @staticmethod
    def enable_screenshot_protection():
        """Enables FLAG_SECURE on Android to prevent screenshots and screen recording."""
        if is_android():
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                currentActivity = PythonActivity.mActivity
                WindowManager = autoclass('android.view.WindowManager$LayoutParams')
                
                def run_on_main_thread():
                    window = currentActivity.getWindow()
                    window.addFlags(WindowManager.FLAG_SECURE)
                
                # In Kivy, some Android UI changes must happen on the main thread
                from android.runnable import run_on_ui_thread
                run_on_ui_thread(run_on_main_thread)()
                print("Screenshot protection ENABLED")
                return True
            except Exception as e:
                print(f"Failed to enable screenshot protection: {e}")
                return False
        else:
            print("Screenshot protection skipped (Not Android)")
            return True

    @staticmethod
    def check_root():
        """Checks for common root indicators (su binary, busybox, etc)."""
        if not is_android():
            return False
            
        try:
            paths = [
                '/system/app/Superuser.apk',
                '/sbin/su',
                '/system/bin/su',
                '/system/xbin/su',
                '/data/local/xbin/su',
                '/data/local/bin/su',
                '/system/sd/xbin/su',
                '/working/bin/su',
                '/system/bin/failsafe/su',
                '/data/local/su'
            ]
            for path in paths:
                if os.path.exists(path):
                    return True
            
            # Additional check via which
            import subprocess
            try:
                result = subprocess.run(['which', 'su'], capture_output=True, text=True, timeout=1)
                if result.returncode == 0:
                    return True
            except:
                pass
                
            return False
        except Exception as e:
            print(f"Error checking root: {e}")
            return False

    @staticmethod
    def is_emulator():
        """Detects if the app is running on an emulator."""
        if not is_android():
            return False
            
        try:
            from jnius import autoclass
            Build = autoclass('android.os.Build')
            model = Build.MODEL.lower()
            hardware = Build.HARDWARE.lower()
            fingerprint = Build.FINGERPRINT.lower()
            manufacturer = Build.MANUFACTURER.lower()
            
            is_emu = (
                "google_sdk" in model or 
                "emulator" in model or 
                "android sdk built for x86" in model or
                "goldfish" in hardware or
                "ranchu" in hardware or
                "vbox" in hardware or
                "sdk" in model or
                "genymotion" in manufacturer or
                fingerprint.startswith("generic")
            )
            return is_emu
        except Exception as e:
            print(f"Error detecting emulator: {e}")
            return False

    @staticmethod
    def check_vpn():
        """Detects if a VPN or Proxy is active."""
        if not is_android():
            return False
            
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = PythonActivity.mActivity
            ConnectivityManager = autoclass('android.net.ConnectivityManager')
            cm = Context.getSystemService(Context.CONNECTIVITY_SERVICE)
            networks = cm.getAllNetworks()
            for network in networks:
                caps = cm.getNetworkCapabilities(network)
                if caps and caps.hasTransport(4): # TRANSPORT_VPN = 4
                    return True
            return False
        except Exception as e:
            print(f"Error checking VPN: {e}")
            return False
