"""
app.py
Punto de entrada principal del sistema.
Controla la transición entre Login y Dashboard.

EJECUTAR ESTE ARCHIVO:  python app.py
"""

import sys
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


def _instalar_manejador_excepciones():
    """Evita que excepciones en callbacks de Qt se pierdan en silencio."""

    def _excepthook(exc_type, exc_value, exc_tb):
        print("[APP ERROR] Excepción no controlada:")
        traceback.print_exception(exc_type, exc_value, exc_tb)

    sys.excepthook = _excepthook


def main():
    # Configurar DPI alto
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    # NO cerrar la app cuando se oculta una ventana
    app.setQuitOnLastWindowClosed(False)

    _instalar_manejador_excepciones()

    # Importar módulos
    from login import LoginWindow
    from main_principal import CajaAhorroDashboard

    # Variables para mantener las ventanas vivas
    ventanas = {'login': None, 'dashboard': None}

    def mostrar_login():
        """Muestra la ventana de login."""
        # Cerrar dashboard si existe
        if ventanas['dashboard']:
            ventanas['dashboard'].close()
            ventanas['dashboard'] = None

        # Crear login
        ventanas['login'] = LoginWindow()

        def on_login_exitoso(usuario):
            """Abre el dashboard cuando el login valida credenciales."""
            try:
                print(f"[APP] Usuario validado: {usuario['nombre']} {usuario['apellido']}")

                # Cerrar el dashboard previo si existe (sesiones repetidas)
                if ventanas['dashboard']:
                    ventanas['dashboard'].close()

                ventanas['dashboard'] = CajaAhorroDashboard(usuario=usuario)
                ventanas['dashboard'].senal_cerrar_sesion.connect(on_cerrar_sesion)

                ventanas['dashboard'].show()
                print("[APP] Dashboard mostrado")

                ventanas['login'].hide()
                print("[APP] Login ocultado")
            except Exception:
                print("[APP ERROR] Falló la apertura del dashboard")
                traceback.print_exc()

        # Conectar la señal real que emite login.py
        ventanas['login'].login_exitoso.connect(on_login_exitoso)
        ventanas['login'].show()
        print("[APP] Login mostrado")

    def on_cerrar_sesion():
        """Cuando se cierra sesión en el dashboard."""
        print("[APP] Cerrando sesión, volviendo al login...")
        mostrar_login()

    # Iniciar con login
    mostrar_login()

    # Manejar cierre limpio
    app.aboutToQuit.connect(lambda: print("[APP] Aplicación cerrada"))

    sys.exit(app.exec_())


if __name__ == "__main__":
   main()
