"""
main_principal.py
Dashboard principal del sistema
Sistema de Caja de Ahorro - UPTNM "Ludovico Silva"
"""

import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QMessageBox, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QCursor, QIcon, QPixmap

from conexion_bd import ejecutar_consulta


# ============================================================
# COLORES DEL SISTEMA
# ============================================================
class Colores:
    # Sidebar
    SIDEBAR_BG = "#0f172a"
    SIDEBAR_HOVER = "rgba(255, 255, 255, 0.06)"
    SIDEBAR_ACTIVE = "rgba(59, 130, 246, 0.12)"
    SIDEBAR_ACTIVE_BORDER = "#3b82f6"

    # Contenido
    FONDO = "#f1f5f9"
    BLANCO = "#ffffff"

    # Texto
    TEXTO_OSCURO = "#0f172a"
    TEXTO_GRIS = "#475569"
    TEXTO_CLARO = "#94a3b8"

    # Acentos
    AZUL = "#3b82f6"
    AZUL_OSCURO = "#1e40af"
    VERDE = "#10b981"
    NARANJA = "#f59e0b"
    ROJO = "#ef4444"
    MORADO = "#8b5cf6"

    # Bordes
    BORDE = "#e2e8f0"


# ============================================================
# WIDGET: TARJETA DE MÓDULO
# ============================================================
class TarjetaModulo(QFrame):
    """Tarjeta interactiva para los módulos del dashboard."""

    clicked = pyqtSignal(str)

    def __init__(self, titulo, descripcion, icono, color_icono,
                 color_fondo_icono, identificador, parent=None):
        super().__init__(parent)
        self.identificador = identificador
        self.setObjectName("tarjetaModulo")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(140)
        self._crear_ui(titulo, descripcion, icono, color_icono, color_fondo_icono)
        self._aplicar_estilo()

    def _crear_ui(self, titulo, descripcion, icono, color_icono, color_fondo_icono):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(20)

        # Icono
        icono_label = QLabel(icono)
        icono_label.setFixedSize(60, 60)
        icono_label.setAlignment(Qt.AlignCenter)
        icono_label.setStyleSheet(f"""
            background-color: transparent;
            border: 1px solid {color_fondo_icono};
            border-radius: 14px;
            font-size: 16px;
            font-weight: 700;
            color: {color_icono};
            font-family: 'Segoe UI', sans-serif;
        """)
        layout.addWidget(icono_label)

        # Texto
        texto_layout = QVBoxLayout()
        texto_layout.setSpacing(4)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet(f"""
            font-size: 17px;
            font-weight: bold;
            color: {Colores.TEXTO_OSCURO};
            font-family: 'Segoe UI', sans-serif;
        """)

        lbl_desc = QLabel(descripcion)
        lbl_desc.setStyleSheet(f"""
            font-size: 12px;
            color: {Colores.TEXTO_CLARO};
            font-family: 'Segoe UI', sans-serif;
            line-height: 1.4;
        """)
        lbl_desc.setWordWrap(True)

        texto_layout.addWidget(lbl_titulo)
        texto_layout.addWidget(lbl_desc)
        texto_layout.addStretch()

        layout.addLayout(texto_layout, 1)

        # Flecha
        flecha = QLabel("→")
        flecha.setStyleSheet(f"""
            font-size: 20px;
            color: {Colores.TEXTO_CLARO};
            font-weight: bold;
        """)
        layout.addWidget(flecha, alignment=Qt.AlignVCenter)

    def _aplicar_estilo(self):
        self.setStyleSheet(f"""
            #tarjetaModulo {{
                background-color: {Colores.BLANCO};
                border: 1px solid {Colores.BORDE};
                border-radius: 14px;
            }}
            #tarjetaModulo:hover {{
                border-color: {Colores.AZUL};
                background-color: #f8faff;
            }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.identificador)


# ============================================================
# WIDGET: TARJETA DE ESTADÍSTICA
# ============================================================
class TarjetaEstadistica(QFrame):
    """Tarjeta con un número y etiqueta para las estadísticas."""

    def __init__(self, valor, etiqueta, icono, color_fondo_icono, parent=None):
        super().__init__(parent)
        self.setObjectName("tarjetaStat")
        self._crear_ui(valor, etiqueta, icono, color_fondo_icono)

    def _crear_ui(self, valor, etiqueta, icono, color_fondo_icono):
        self.setStyleSheet(f"""
            #tarjetaStat {{
                background-color: {Colores.BLANCO};
                border: 1px solid {Colores.BORDE};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        # Icono
        icono_label = QLabel(icono)
        icono_label.setFixedSize(42, 42)
        icono_label.setAlignment(Qt.AlignCenter)
        icono_label.setStyleSheet(f"""
            background-color: transparent;
            border: 1px solid {color_fondo_icono};
            border-radius: 10px;
            font-size: 14px;
            font-weight: 700;
            color: {Colores.TEXTO_GRIS};
            font-family: 'Segoe UI', sans-serif;
        """)
        layout.addWidget(icono_label)

        # Valor
        self.lbl_valor = QLabel(str(valor))
        self.lbl_valor.setStyleSheet(f"""
            font-size: 30px;
            font-weight: bold;
            color: {Colores.TEXTO_OSCURO};
            font-family: 'Segoe UI', sans-serif;
        """)
        layout.addWidget(self.lbl_valor)

        # Etiqueta
        lbl_etiqueta = QLabel(etiqueta)
        lbl_etiqueta.setStyleSheet(f"""
            font-size: 12px;
            color: {Colores.TEXTO_CLARO};
            font-family: 'Segoe UI', sans-serif;
        """)
        layout.addWidget(lbl_etiqueta)

    def actualizar_valor(self, valor):
        self.lbl_valor.setText(str(valor))


# ============================================================
# WIDGET: BOTÓN SIDEBAR
# ============================================================
class BotonSidebar(QPushButton):
    """Botón personalizado para el menú lateral."""

    def __init__(self, texto, icono, identificador, parent=None):
        super().__init__(parent)
        self.identificador = identificador
        self.activo = False
        self.setText(f"  {icono}   {texto}")
        self.setFixedHeight(48)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._aplicar_estilo(False)

    def set_activo(self, activo):
        self.activo = activo
        self._aplicar_estilo(activo)

    def _aplicar_estilo(self, activo):
        if activo:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colores.SIDEBAR_ACTIVE};
                    color: {Colores.AZUL};
                    border: none;
                    border-left: 3px solid {Colores.AZUL};
                    text-align: left;
                    padding-left: 20px;
                    font-size: 13px;
                    font-weight: bold;
                    font-family: 'Segoe UI', sans-serif;
                    border-radius: 0px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Colores.TEXTO_CLARO};
                    border: none;
                    border-left: 3px solid transparent;
                    text-align: left;
                    padding-left: 20px;
                    font-size: 13px;
                    font-weight: 500;
                    font-family: 'Segoe UI', sans-serif;
                    border-radius: 0px;
                }}
                QPushButton:hover {{
                    background-color: {Colores.SIDEBAR_HOVER};
                    color: #e2e8f0;
                }}
            """)


# ============================================================
# VENTANA PRINCIPAL: DASHBOARD
# ============================================================
class CajaAhorroDashboard(QMainWindow):
    """Dashboard principal del sistema de Caja de Ahorro."""

    senal_cerrar_sesion = pyqtSignal()

    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario or {
            'nombre': 'Admin',
            'apellido': 'Sistema',
            'rol': 'admin'
        }
        self.botones_sidebar = []
        self._stats_tarjetas = []
        self._tarjetas_modulos = []
        self.tarjeta_rangos = None
        self.stats_grid = None
        self.modulos_grid = None
        self._modo_responsivo = None
        self._dialogos = {}
        self._configurar_ventana()
        self._crear_interfaz()
        self._cargar_estadisticas()

    # ================================================================
    # CONFIGURACIÓN
    # ================================================================
    def _configurar_ventana(self):
        self.setWindowTitle("Caja de Ahorro — Dashboard")
        self.setMinimumSize(1280, 780)
        self.setStyleSheet(f"background-color: {Colores.FONDO};")

    # ================================================================
    # INTERFAZ
    # ================================================================
    def _crear_interfaz(self):
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setStretch(0, 0)
        layout.setStretch(1, 1)

        # Sidebar + Contenido
        layout.addWidget(self._crear_sidebar())
        layout.addWidget(self._crear_area_contenido(), 1)

    def _crear_sidebar(self):
        """Crea el menú lateral izquierdo."""
        sidebar = QFrame()
        sidebar.setMinimumWidth(250)
        sidebar.setMaximumWidth(330)
        sidebar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sidebar.setStyleSheet(f"""
            background-color: {Colores.SIDEBAR_BG};
            border-right: 1px solid #1e293b;
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ---- Encabezado del sidebar ----
        header = QFrame()
        header.setFixedHeight(92)
        header.setStyleSheet("border-bottom: 1px solid #1e293b; padding: 0 20px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(14, 0, 14, 0)

        logo_icon = QLabel()
        logo_icon.setFixedSize(44, 44)
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_ruta = self._buscar_logo_sidebar()
        if logo_ruta:
            pixmap = QPixmap(logo_ruta).scaled(34, 34, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_icon.setPixmap(pixmap)
            logo_icon.setStyleSheet("""
                background: transparent;
                border: 1px solid #1e293b;
                border-radius: 10px;
            """)
        else:
            logo_icon.setText("CA")
            logo_icon.setStyleSheet("""
                font-size: 14px;
                font-weight: 700;
                color: #e2e8f0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b82f6, stop:1 #8b5cf6);
                border-radius: 10px;
                font-family: 'Segoe UI', sans-serif;
            """)

        logo_texto = QLabel("Caja de Ahorro")
        logo_texto.setStyleSheet("""
            color: #e2e8f0;
            font-size: 14px;
            font-weight: 700;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: 0.2px;
        """)
        logo_texto.setMinimumWidth(170)

        header_layout.addWidget(logo_icon)
        header_layout.addSpacing(10)
        header_layout.addWidget(logo_texto)
        header_layout.addStretch()

        layout.addWidget(header)
        layout.addSpacing(12)

        # ---- Sección: Principal ----
        layout.addWidget(self._crear_label_seccion("PRINCIPAL"))

        btn_dashboard = BotonSidebar("Dashboard", "▦", "dashboard")
        btn_dashboard.set_activo(True)
        btn_dashboard.clicked.connect(lambda: self._on_sidebar_click("dashboard"))
        self.botones_sidebar.append(btn_dashboard)
        layout.addWidget(btn_dashboard)

        layout.addSpacing(8)

        # ---- Sección: Gestión ----
        layout.addWidget(self._crear_label_seccion("GESTIÓN"))

        menu_items = [
            ("Gestionar Afiliados", "AF", "afiliados"),
            ("Gestionar Préstamos", "PR", "prestamos"),
            ("Gestionar Abonos", "AB", "abonos"),
        ]

        for texto, icono, ident in menu_items:
            btn = BotonSidebar(texto, icono, ident)
            btn.clicked.connect(lambda checked, i=ident: self._on_sidebar_click(i))
            self.botones_sidebar.append(btn)
            layout.addWidget(btn)

        layout.addSpacing(8)

        # ---- Sección: Reportes ----
        layout.addWidget(self._crear_label_seccion("REPORTES"))

        btn_reportes = BotonSidebar("Reportes PDF", "RP", "reportes")
        btn_reportes.clicked.connect(lambda: self._on_sidebar_click("reportes"))
        self.botones_sidebar.append(btn_reportes)
        layout.addWidget(btn_reportes)

        layout.addSpacing(8)

        # ---- Sección: Administración ----
        layout.addWidget(self._crear_label_seccion("ADMINISTRACIÓN"))

        btn_rangos = BotonSidebar("Administrar Rangos", "RG", "rangos")
        btn_rangos.clicked.connect(lambda: self._on_sidebar_click("rangos"))
        self.botones_sidebar.append(btn_rangos)
        layout.addWidget(btn_rangos)

        layout.addStretch()

        # ---- Usuario actual y cerrar sesión ----
        footer = QFrame()
        footer.setStyleSheet("border-top: 1px solid #1e293b;")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(20, 12, 20, 16)
        footer_layout.setSpacing(8)

        nombre_completo = f"{self.usuario['nombre']} {self.usuario['apellido']}"
        lbl_user = QLabel(f"👤  {nombre_completo}")
        lbl_user.setStyleSheet("""
            color: #e2e8f0;
            font-size: 12px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        """)

        lbl_rol = QLabel(f"     {self.usuario['rol'].upper()}")
        lbl_rol.setStyleSheet("""
            color: #64748b;
            font-size: 10px;
            font-family: 'Segoe UI', sans-serif;
        """)

        btn_logout = QPushButton("🚪  Cerrar Sesión")
        btn_logout.setCursor(QCursor(Qt.PointingHandCursor))
        btn_logout.setFixedHeight(40)
        btn_logout.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(239, 68, 68, 0.08);
                color: #f87171;
                border: 1px solid rgba(239, 68, 68, 0.15);
                border-radius: 8px;
                font-size: 12px;
                font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{
                background-color: rgba(239, 68, 68, 0.15);
                border-color: rgba(239, 68, 68, 0.3);
            }}
        """)
        btn_logout.clicked.connect(self._on_cerrar_sesion)

        footer_layout.addWidget(lbl_user)
        footer_layout.addWidget(lbl_rol)
        footer_layout.addWidget(btn_logout)

        layout.addWidget(footer)

        return sidebar

    def _crear_label_seccion(self, texto):
        """Crea una etiqueta de sección para el sidebar."""
        label = QLabel(f"  {texto}")
        label.setFixedHeight(32)
        label.setStyleSheet("""
            color: #475569;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.2px;
            font-family: 'Segoe UI', sans-serif;
            padding-left: 20px;
        """)
        return label

    def _crear_area_contenido(self):
        """Crea el área de contenido principal (scroll)."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 4px;
                min-height: 30px;
            }
        """)

        contenido = QWidget()
        contenido.setStyleSheet(f"background-color: {Colores.FONDO};")
        self.layout_contenido = QVBoxLayout(contenido)
        self.layout_contenido.setContentsMargins(36, 28, 36, 40)
        self.layout_contenido.setSpacing(0)

        # Header de bienvenida
        nombre = self.usuario['nombre']
        lbl_bienvenida = QLabel(f"Bienvenida, {nombre}")
        lbl_bienvenida.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {Colores.TEXTO_OSCURO};
            font-family: 'Segoe UI', sans-serif;
        """)
        self.layout_contenido.addWidget(lbl_bienvenida)

        lbl_subtitulo = QLabel("Panel de control — Caja de Ahorro Docente UPTNM")
        lbl_subtitulo.setStyleSheet(f"""
            font-size: 13px;
            color: {Colores.TEXTO_CLARO};
            font-family: 'Segoe UI', sans-serif;
            margin-bottom: 8px;
        """)
        self.layout_contenido.addWidget(lbl_subtitulo)
        self.layout_contenido.addSpacing(24)

        # ---- Tarjetas de estadísticas ----
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(16)

        self.stat_afiliados = TarjetaEstadistica(
            "0", "Afiliados activos", "AF", "rgba(59, 130, 246, 0.10)"
        )
        self.stat_prestamos = TarjetaEstadistica(
            "0", "Préstamos activos", "PR", "rgba(16, 185, 129, 0.10)"
        )
        self.stat_monto = TarjetaEstadistica(
            "0", "Bs. prestados (mes)", "Bs", "rgba(245, 158, 11, 0.10)"
        )
        self.stat_pagados = TarjetaEstadistica(
            "0", "Préstamos pagados", "OK", "rgba(139, 92, 246, 0.10)"
        )

        self._stats_tarjetas = [
            self.stat_afiliados,
            self.stat_prestamos,
            self.stat_monto,
            self.stat_pagados,
        ]

        self.layout_contenido.addLayout(self.stats_grid)
        self.layout_contenido.addSpacing(28)

        # ---- Título de módulos ----
        lbl_modulos = QLabel("Módulos del sistema")
        lbl_modulos.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {Colores.TEXTO_OSCURO};
            font-family: 'Segoe UI', sans-serif;
        """)
        self.layout_contenido.addWidget(lbl_modulos)
        self.layout_contenido.addSpacing(14)

        # ---- Grid de módulos (2x2 + 1) ----
        self.modulos_grid = QGridLayout()
        self.modulos_grid.setSpacing(16)

        tarjetas = [
            ("Gestionar Afiliados",
             "Agregar, editar y consultar docentes.\nCambiar condición y asignar rangos.",
             "AF", Colores.AZUL, "rgba(59, 130, 246, 0.10)", "afiliados"),

            ("Gestionar Préstamos",
             "Otorgar préstamos, calcular cuotas.\nValidar capacidad de pago (33,33%).",
             "PR", Colores.VERDE, "rgba(16, 185, 129, 0.10)", "prestamos"),

            ("Gestionar Abonos",
             "Registrar pagos de cuotas y abonos.\nControl de saldo por préstamo.",
             "AB", Colores.NARANJA, "rgba(245, 158, 11, 0.10)", "abonos"),

            ("Reportes PDF",
             "Exportar reportes personales o generales.\nBalance mensual de préstamos.",
             "RP", Colores.MORADO, "rgba(139, 92, 246, 0.10)", "reportes"),
        ]

        for i, (titulo, desc, icono, color, fondo, ident) in enumerate(tarjetas):
            tarjeta = TarjetaModulo(titulo, desc, icono, color, fondo, ident)
            tarjeta.clicked.connect(self._on_modulo_click)
            self._tarjetas_modulos.append(tarjeta)

        # Tarjeta extra: Administrar Rangos (ancho completo)
        self.tarjeta_rangos = TarjetaModulo(
            "Administrar Rangos y Salarios",
            "Crear, editar y eliminar rangos docentes. Al modificar un salario, se actualiza automáticamente para todos los afiliados.",
            "RG", Colores.TEXTO_GRIS, "rgba(100, 116, 139, 0.10)", "rangos"
        )
        self.tarjeta_rangos.clicked.connect(self._on_modulo_click)

        self.layout_contenido.addLayout(self.modulos_grid)
        self.layout_contenido.addStretch()

        self._actualizar_layout_responsivo(force=True)

        scroll.setWidget(contenido)
        return scroll

    def _buscar_logo_sidebar(self):
        """Busca un logo local para el encabezado del sidebar."""
        base = os.path.dirname(os.path.abspath(__file__))
        candidatos = [
            os.path.join(base, "logo-ludovico.png"),
            os.path.join(base, "LUDOVICO-removebg-preview.png"),
            os.path.join(base, "logo.png"),
        ]
        for ruta in candidatos:
            if os.path.exists(ruta):
                return ruta
        return None

    def _limpiar_grid(self, grid):
        """Quita todos los widgets de un QGridLayout."""
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def _actualizar_layout_responsivo(self, force=False):
        """Reordena tarjetas según el ancho actual de la ventana."""
        ancho = self.width()

        # Modo ancho: 4 stats en una fila y módulos en 2 columnas.
        # Modo compacto: 2 stats por fila y módulos en 1 columna.
        modo = 'ancho' if ancho >= 1500 else 'compacto'
        if not force and modo == self._modo_responsivo:
            return
        self._modo_responsivo = modo

        stats_cols = 4 if modo == 'ancho' else 2
        mod_cols = 2 if modo == 'ancho' else 1

        # Reordenar estadísticas
        self._limpiar_grid(self.stats_grid)
        for i, tarjeta in enumerate(self._stats_tarjetas):
            fila, col = divmod(i, stats_cols)
            self.stats_grid.addWidget(tarjeta, fila, col)
        for col in range(stats_cols):
            self.stats_grid.setColumnStretch(col, 1)

        # Reordenar módulos
        self._limpiar_grid(self.modulos_grid)
        for i, tarjeta in enumerate(self._tarjetas_modulos):
            fila, col = divmod(i, mod_cols)
            self.modulos_grid.addWidget(tarjeta, fila, col)

        fila_rangos = (len(self._tarjetas_modulos) + mod_cols - 1) // mod_cols
        self.modulos_grid.addWidget(self.tarjeta_rangos, fila_rangos, 0, 1, mod_cols)
        for col in range(mod_cols):
            self.modulos_grid.setColumnStretch(col, 1)

    # ================================================================
    # LÓGICA
    # ================================================================
    def _cargar_estadisticas(self):
        """Carga las estadísticas desde la base de datos."""
        try:
            # Afiliados activos
            result = ejecutar_consulta(
                "SELECT COUNT(*) as total FROM afiliados WHERE activo = TRUE",
                fetchone=True
            )
            if result:
                self.stat_afiliados.actualizar_valor(result['total'])

            # Préstamos activos
            result = ejecutar_consulta(
                "SELECT COUNT(*) as total FROM prestamo WHERE estado = 'activo'",
                fetchone=True
            )
            if result:
                self.stat_prestamos.actualizar_valor(result['total'])

            # Monto prestado este mes
            result = ejecutar_consulta("""
                SELECT COALESCE(SUM(monto_aprobado), 0) as total
                FROM prestamo
                WHERE MONTH(fecha_solicitud) = MONTH(CURRENT_DATE())
                AND YEAR(fecha_solicitud) = YEAR(CURRENT_DATE())
            """, fetchone=True)
            if result:
                monto = f"{result['total']:,.2f}"
                self.stat_monto.actualizar_valor(monto)

            # Préstamos pagados
            result = ejecutar_consulta(
                "SELECT COUNT(*) as total FROM prestamo WHERE estado = 'pagado'",
                fetchone=True
            )
            if result:
                self.stat_pagados.actualizar_valor(result['total'])

        except Exception as e:
            print(f"[AVISO] No se pudieron cargar estadísticas: {e}")
            # No es crítico, el dashboard funciona igual con valores en 0

    def _on_sidebar_click(self, identificador):
        """Maneja click en los botones del sidebar."""
        # Actualizar estado visual
        for btn in self.botones_sidebar:
            btn.set_activo(btn.identificador == identificador)

        # Abrir módulo
        self._abrir_modulo(identificador)

    def _on_modulo_click(self, identificador):
        """Maneja click en las tarjetas de módulos."""
        # Actualizar sidebar
        for btn in self.botones_sidebar:
            btn.set_activo(btn.identificador == identificador)

        # Abrir módulo
        self._abrir_modulo(identificador)

    def _abrir_modulo(self, identificador):
        """Abre el módulo correspondiente."""
        modulos = {
            'dashboard': 'Dashboard',
            'afiliados': 'Gestionar Afiliados',
            'prestamos': 'Gestionar Préstamos',
            'abonos': 'Gestionar Abonos',
            'reportes': 'Reportes PDF',
            'rangos': 'Administrar Rangos',
        }

        nombre = modulos.get(identificador, identificador)

        if identificador == 'dashboard':
            self._cargar_estadisticas()
            return

        if identificador == 'afiliados':
            self._abrir_gestion_afiliados()
            return

        # TODO: Aquí se abrirán las ventanas de cada módulo
        # Por ahora muestra un mensaje informativo
        QMessageBox.information(
            self,
            nombre,
            f"El módulo \"{nombre}\" se implementará en el siguiente sprint.\n\n"
            f"Módulos pendientes:\n"
            f"  • Administrar Rangos\n"
            f"  • Gestionar Préstamos\n"
            f"  • Gestionar Abonos\n"
            f"  • Reportes PDF"
        )


    def _abrir_gestion_afiliados(self):
        """Abre la ventana de gestión de afiliados."""
        try:
            from modulo_afiliados import GestionAfiliadosDialog

            dlg = GestionAfiliadosDialog(self)
            self._dialogos['afiliados'] = dlg
            dlg.exec_()
            self._cargar_estadisticas()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el módulo de afiliados:\n\n{e}")

    def _on_cerrar_sesion(self):
        """Cierra sesión y vuelve al login."""
        respuesta = QMessageBox.question(
            self,
            "Cerrar Sesión",
            "¿Está segura que desea cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            self._cerrando_sesion = True
            self.senal_cerrar_sesion.emit()
            self.close()

    def closeEvent(self, event):
        """Maneja el cierre de la ventana."""
        event.accept()
        # Solo cerrar la app si NO se está volviendo al login
        if not getattr(self, '_cerrando_sesion', False):
            QApplication.instance().quit()

    def resizeEvent(self, event):
        """Ajusta distribución responsiva al cambiar el tamaño de ventana."""
        super().resizeEvent(event)
        self._actualizar_layout_responsivo()


# ============================================================
# PUNTO DE ENTRADA (para pruebas independientes)
# ============================================================
def main():
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    ventana = CajaAhorroDashboard()
    ventana.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
