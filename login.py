"""
login.py
Módulo de inicio de sesión
Sistema de Caja de Ahorro - UPTNM "Ludovico Silva"
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal


class LoginWindow(QWidget):
    """Ventana de inicio de sesión del sistema."""

    # Señal que se emite cuando el login es exitoso
    login_exitoso = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.usuario_actual = None
        self._configurar_ventana()
        self._crear_interfaz()
        print("[LOGIN] Ventana creada")

    def _configurar_ventana(self):
        self.setWindowTitle("Caja de Ahorro — UPTNM Ludovico Silva")
        self.setFixedSize(960, 620)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def _crear_interfaz(self):
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        panel = QFrame()
        panel.setObjectName("panelPrincipal")
        panel.setFixedSize(960, 620)
        panel.setStyleSheet("""
            #panelPrincipal {
                background-color: #f0f4f8;
                border-radius: 16px;
                border: 1px solid #d0d7de;
            }
        """)

        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(40)
        sombra.setXOffset(0)
        sombra.setYOffset(8)
        sombra.setColor(QColor(0, 0, 0, 60))
        panel.setGraphicsEffect(sombra)

        layout_panel = QHBoxLayout(panel)
        layout_panel.setContentsMargins(0, 0, 0, 0)
        layout_panel.setSpacing(0)

        layout_panel.addWidget(self._crear_panel_izquierdo())
        layout_panel.addWidget(self._crear_panel_derecho())

        layout_principal.addWidget(panel, alignment=Qt.AlignCenter)

    def _crear_panel_izquierdo(self):
        panel = QFrame()
        panel.setObjectName("panelIzq")
        panel.setFixedWidth(400)
        panel.setStyleSheet("""
            #panelIzq {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a56db, stop:0.5 #1e40af, stop:1 #1e3a8a
                );
                border-top-left-radius: 16px;
                border-bottom-left-radius: 16px;
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(40, 50, 40, 40)

        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_path = self._buscar_logo()
        if logo_path:
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("🏦")
            logo_label.setStyleSheet("font-size: 72px;")
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        layout.addSpacing(30)

        titulo = QLabel("Caja de Ahorro\nDocente")
        titulo.setStyleSheet("color: #ffffff; font-size: 26px; font-weight: bold; font-family: 'Segoe UI';")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setWordWrap(True)
        layout.addWidget(titulo)

        layout.addSpacing(16)

        desc = QLabel("Sistema automatizado para la gestión\nde préstamos, cuotas, intereses\ny aportes de la Caja de Ahorro\nde los Docentes.")
        desc.setStyleSheet("color: rgba(255,255,255,0.80); font-size: 13px; font-family: 'Segoe UI';")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()

        inst = QLabel("Universidad Politécnica Territorial\ndel Norte de Monagas\n\"Ludovico Silva\"")
        inst.setStyleSheet("color: rgba(255,255,255,0.60); font-size: 11px; font-family: 'Segoe UI';")
        inst.setAlignment(Qt.AlignCenter)
        layout.addWidget(inst)

        return panel

    def _crear_panel_derecho(self):
        panel = QFrame()
        panel.setObjectName("panelDer")
        panel.setStyleSheet("""
            #panelDer {
                background-color: #ffffff;
                border-top-right-radius: 16px;
                border-bottom-right-radius: 16px;
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(50, 60, 50, 40)

        layout.addStretch(2)

        titulo = QLabel("Iniciar Sesión")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #0f172a; font-family: 'Segoe UI';")
        layout.addWidget(titulo)

        subtitulo = QLabel("Ingrese sus credenciales para acceder al sistema")
        subtitulo.setStyleSheet("font-size: 13px; color: #64748b; font-family: 'Segoe UI';")
        layout.addWidget(subtitulo)

        layout.addSpacing(32)

        # Campo cédula
        lbl = QLabel("Cédula")
        lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #475569; font-family: 'Segoe UI';")
        layout.addWidget(lbl)
        layout.addSpacing(6)

        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("V-00.000.000")
        self.txt_usuario.setMinimumHeight(48)
        self.txt_usuario.setStyleSheet("""
            padding: 14px 18px; border: 2px solid #e2e8f0; border-radius: 10px;
            font-size: 14px; background-color: #f8fafc; color: #1e293b;
        """)
        self.txt_usuario.returnPressed.connect(lambda: self.txt_clave.setFocus())
        layout.addWidget(self.txt_usuario)

        layout.addSpacing(18)

        # Campo contraseña
        lbl2 = QLabel("Contraseña")
        lbl2.setStyleSheet("font-size: 13px; font-weight: bold; color: #475569; font-family: 'Segoe UI';")
        layout.addWidget(lbl2)
        layout.addSpacing(6)

        self.txt_clave = QLineEdit()
        self.txt_clave.setPlaceholderText("Ingrese su contraseña")
        self.txt_clave.setEchoMode(QLineEdit.Password)
        self.txt_clave.setMinimumHeight(48)
        self.txt_clave.setStyleSheet("""
            padding: 14px 18px; border: 2px solid #e2e8f0; border-radius: 10px;
            font-size: 14px; background-color: #f8fafc; color: #1e293b;
        """)
        self.txt_clave.returnPressed.connect(self.validar_login)
        layout.addWidget(self.txt_clave)

        layout.addSpacing(10)

        # Error label
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: #ef4444; font-size: 12px; padding: 4px 0;")
        self.lbl_error.setVisible(False)
        layout.addWidget(self.lbl_error)

        layout.addSpacing(12)

        # Botón login
        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setMinimumHeight(50)
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setStyleSheet("""
            QPushButton {
                padding: 14px; background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #2563eb, stop:1 #1d4ed8);
                color: white; border: none; border-radius: 10px; font-size: 15px;
                font-weight: bold; font-family: 'Segoe UI';
            }
            QPushButton:hover { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #1d4ed8, stop:1 #1e40af); }
            QPushButton:pressed { background-color: #1e3a8a; }
        """)
        btn_login.clicked.connect(self.validar_login)
        layout.addWidget(btn_login)

        layout.addStretch(3)

        # Footer
        layout_inf = QHBoxLayout()
        btn_salir = QPushButton("✕  Salir")
        btn_salir.setFixedSize(100, 38)
        btn_salir.setCursor(Qt.PointingHandCursor)
        btn_salir.setStyleSheet("""
            QPushButton { padding: 10px; background: transparent; color: #94a3b8;
                border: 1px solid #e2e8f0; border-radius: 8px; font-size: 12px; }
            QPushButton:hover { background: #fef2f2; color: #ef4444; border-color: #fecaca; }
        """)
        btn_salir.clicked.connect(lambda: QApplication.instance().quit())

        lbl_ver = QLabel("v2.0 — Febrero 2026")
        lbl_ver.setStyleSheet("color: #94a3b8; font-size: 11px;")
        lbl_ver.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout_inf.addWidget(btn_salir)
        layout_inf.addStretch()
        layout_inf.addWidget(lbl_ver)
        layout.addLayout(layout_inf)

        return panel

    # ================================================================
    # LÓGICA
    # ================================================================
    def _buscar_logo(self):
        nombres = ["logo-ludovico.png", "LUDOVICO-removebg-preview.png", "logo.png"]
        carpetas = [os.path.dirname(os.path.abspath(__file__)), os.getcwd()]
        for carpeta in carpetas:
            for nombre in nombres:
                ruta = os.path.join(carpeta, nombre)
                if os.path.exists(ruta):
                    return ruta
        return None

    def validar_login(self):
        """Valida las credenciales contra la base de datos."""
        print("[LOGIN] ========================================")
        print("[LOGIN] Botón INICIAR SESIÓN presionado")

        usuario = self.txt_usuario.text().strip()
        clave = self.txt_clave.text().strip()
        print(f"[LOGIN] Cédula ingresada: '{usuario}'")
        print(f"[LOGIN] Clave ingresada: {'*' * len(clave)} ({len(clave)} caracteres)")

        if not usuario or not clave:
            print("[LOGIN] Campos vacíos")
            self._mostrar_error("Por favor ingrese cédula y contraseña.")
            return

        # Importar conexión
        try:
            from conexion_bd import validar_usuario, probar_conexion
            print("[LOGIN] conexion_bd importado OK")
        except Exception as e:
            print(f"[LOGIN] ERROR importando: {e}")
            self._mostrar_error(f"Error: {e}")
            return

        # Probar conexión
        try:
            ok = probar_conexion()
            print(f"[LOGIN] Conexión BD: {ok}")
            if not ok:
                self._mostrar_error("No se pudo conectar a MySQL.")
                return
        except Exception as e:
            print(f"[LOGIN] ERROR conexión: {e}")
            self._mostrar_error(f"Error BD: {e}")
            return

        # Validar credenciales
        try:
            resultado = validar_usuario(usuario, clave)
            print(f"[LOGIN] Resultado: {resultado}")
        except Exception as e:
            print(f"[LOGIN] ERROR validación: {e}")
            self._mostrar_error(f"Error: {e}")
            return

        if resultado:
            self.usuario_actual = resultado
            self.lbl_error.setVisible(False)
            print(f"[LOGIN] ✅ ÉXITO: {resultado['nombre']} {resultado['apellido']}")
            print("[LOGIN] Emitiendo señal login_exitoso...")
            self.login_exitoso.emit(resultado)
            print("[LOGIN] Señal emitida")
        else:
            print("[LOGIN] ❌ Credenciales incorrectas")
            self._mostrar_error("Cédula o contraseña incorrectos.")
            self.txt_clave.clear()
            self.txt_clave.setFocus()

    def _mostrar_error(self, mensaje):
        self.lbl_error.setText(f"⚠  {mensaje}")
        self.lbl_error.setVisible(True)

    def limpiar(self):
        self.usuario_actual = None
        self.txt_usuario.clear()
        self.txt_clave.clear()
        self.lbl_error.setVisible(False)
        self.txt_usuario.setFocus()

    # ================================================================
    # EVENTOS
    # ================================================================
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.instance().quit()


# ============================================================
# EJECUCIÓN STANDALONE (python login.py)
# ============================================================
if __name__ == "__main__":
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setFont(QFont("Segoe UI", 10))

    login = LoginWindow()
    dashboard = None

    def on_login_ok(usuario):
        global dashboard
        print(f"[MAIN] Señal recibida, creando dashboard...")
        try:
            from main_principal import CajaAhorroDashboard
            dashboard = CajaAhorroDashboard(usuario=usuario)
            print("[MAIN] Dashboard creado, mostrando...")
            dashboard.show()
            print("[MAIN] Dashboard visible, ocultando login...")
            login.hide()
            print("[MAIN] Login ocultado. ¡TODO OK!")

            def volver_al_login():
                global dashboard
                if dashboard:
                    dashboard.close()
                    dashboard = None
                login.limpiar()
                login.show()

            dashboard.senal_cerrar_sesion.connect(volver_al_login)

        except Exception as e:
            import traceback
            print(f"[MAIN ERROR]\n{traceback.format_exc()}")
            QMessageBox.critical(login, "Error", f"Error abriendo dashboard:\n\n{e}")

    login.login_exitoso.connect(on_login_ok)
    login.show()
    print("[MAIN] Login mostrado, esperando interacción...")

    sys.exit(app.exec_())
