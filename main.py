from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import platform

try:
    from plyer import gps, notification, call
except ImportError:
    gps = notification = call = None


class SecurityBikerLayout(BoxLayout):
    status_text = StringProperty("Sistema activo y protegido")
    location_text = StringProperty("Ubicacion: esperando senal GPS...")
    gps_text = StringProperty("GPS: solicitando permiso")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_location = None
        self.gps_started = False
        Clock.schedule_once(self.start_location, 0.5)

    def start_location(self, _dt):
        if platform == "android":
            from android.permissions import Permission, request_permissions
            request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION])

        if gps is None:
            self.gps_text = "GPS: instala plyer para activarlo"
            return

        try:
            gps.configure(on_location=self.on_location, on_status=self.on_gps_status)
            gps.start(minTime=1000, minDistance=1)
            self.gps_started = True
            self.gps_text = "GPS: activo"
        except Exception as error:
            self.gps_text = "GPS: no disponible"
            self.location_text = f"Ubicacion no disponible ({error})"

    def on_location(self, **kwargs):
        latitude = kwargs.get("lat")
        longitude = kwargs.get("lon")
        if latitude is None or longitude is None:
            return
        self.current_location = (latitude, longitude)
        self.location_text = f"Ubicacion: {latitude:.6f}, {longitude:.6f}"
        self.gps_text = "GPS: senal recibida"

    def on_gps_status(self, status, message):
        if status == "provider-enabled":
            self.gps_text = "GPS: activo"
        elif message:
            self.gps_text = f"GPS: {message}"

    def show_location(self):
        if self.current_location:
            latitude, longitude = self.current_location
            self.show_message("Ubicacion actual", f"Latitud: {latitude:.6f}\nLongitud: {longitude:.6f}")
        else:
            self.show_message("GPS", "Aun no se ha recibido una senal GPS.")

    def simulate_accident(self):
        self.status_text = "Accidente detectado: alerta preparada"
        self.show_message("Alerta de accidente", "Se ha detectado un posible accidente. Revisa tu estado y contacta a emergencias si es necesario.")
        if notification:
            try:
                notification.notify(title="Security Biker", message="Accidente detectado. Alerta preparada.")
            except Exception:
                pass

    def send_sos(self):
        self.status_text = "SOS activado: solicita ayuda inmediata"
        if notification:
            try:
                notification.notify(title="Security Biker SOS", message="Solicitud de emergencia activada.")
            except Exception:
                pass
        if call:
            try:
                call.makecall("112")
                return
            except Exception:
                pass
        self.show_message("SOS", "SOS activado. No fue posible abrir el marcador automaticamente.")

    def show_message(self, title, message):
        Popup(
            title=title,
            content=Label(text=message, halign="center", valign="middle"),
            size_hint=(0.86, 0.32),
        ).open()


class SecurityBikerApp(App):
    title = "Security Biker"

    def build(self):
        return SecurityBikerLayout(orientation="vertical", padding=dp(20), spacing=dp(14))

    def on_stop(self):
        if gps and self.root and self.root.gps_started:
            try:
                gps.stop()
            except Exception:
                pass


if __name__ == "__main__":
    SecurityBikerApp().run()
