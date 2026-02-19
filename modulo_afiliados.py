"""
modulo_afiliados.py
Módulo de gestión de afiliados (listar, buscar, agregar, editar y desactivar)
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QWidget,
    QComboBox, QDateEdit, QHeaderView, QFrame, QGridLayout, QStyleFactory
)
from PyQt5.QtCore import Qt, QDate

from conexion_bd import ejecutar_consulta, ejecutar_accion


class GestionAfiliadosDialog(QDialog):
    """Ventana de gestión de afiliados con estilo inspirado en prototipo HTML."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.afiliado_id_edicion = None
        self._configurar_ventana()
        self._crear_ui()
        self._aplicar_estilos()
        self._cargar_rangos()
        self._cargar_afiliados()

    def _configurar_ventana(self):
        self.setWindowTitle("Gestionar Afiliados")
        self.setMinimumSize(1220, 760)
        self.setModal(True)
        self.setStyle(QStyleFactory.create("Fusion"))

    def _crear_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(14)

        # Encabezado
        self.lbl_titulo = QLabel("Gestionar Afiliados")
        self.lbl_titulo.setObjectName("tituloModulo")
        self.lbl_subtitulo = QLabel("Administrar docentes asociados a la Caja de Ahorro")
        self.lbl_subtitulo.setObjectName("subtituloModulo")
        root.addWidget(self.lbl_titulo)
        root.addWidget(self.lbl_subtitulo)

        # Barra superior
        top = QHBoxLayout()
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("🔎 Buscar por cédula o nombre...")
        self.txt_buscar.textChanged.connect(self._filtrar_tabla)

        self.btn_recargar = QPushButton("Recargar")
        self.btn_recargar.setObjectName("btnOutline")
        self.btn_recargar.clicked.connect(self._cargar_afiliados)

        self.btn_nuevo = QPushButton("+ Nuevo afiliado")
        self.btn_nuevo.setObjectName("btnBlue")
        self.btn_nuevo.clicked.connect(self._limpiar_form)

        top.addWidget(self.txt_buscar, 1)
        top.addWidget(self.btn_recargar)
        top.addWidget(self.btn_nuevo)
        root.addLayout(top)

        # Tarjeta lista
        self.card_lista = QFrame()
        self.card_lista.setObjectName("card")
        lista_layout = QVBoxLayout(self.card_lista)
        lista_layout.setContentsMargins(0, 0, 0, 0)
        lista_layout.setSpacing(0)

        self.lbl_lista = QLabel("  Afiliados registrados")
        self.lbl_lista.setObjectName("cardHeader")
        lista_layout.addWidget(self.lbl_lista)

        self.tabla = QTableWidget(0, 8)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Cédula", "Nombre", "Apellido", "Teléfono", "Correo", "Condición", "Estado"
        ])
        self.tabla.setAlternatingRowColors(False)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.horizontalHeader().setStretchLastSection(False)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        lista_layout.addWidget(self.tabla)
        root.addWidget(self.card_lista, 2)

        # Tarjeta formulario
        self.card_form = QFrame()
        self.card_form.setObjectName("card")
        form_wrap = QVBoxLayout(self.card_form)
        form_wrap.setContentsMargins(0, 0, 0, 0)
        form_wrap.setSpacing(0)

        self.lbl_form = QLabel("  Registrar / editar afiliado")
        self.lbl_form.setObjectName("cardHeader")
        form_wrap.addWidget(self.lbl_form)

        form_body = QWidget()
        body_layout = QVBoxLayout(form_body)
        body_layout.setContentsMargins(16, 16, 16, 16)
        body_layout.setSpacing(12)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(10)

        self.txt_cedula = QLineEdit()
        self.txt_cedula.setPlaceholderText("V-00.000.000")
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre del docente")
        self.txt_apellido = QLineEdit()
        self.txt_apellido.setPlaceholderText("Apellido del docente")
        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("0414-0000000")
        self.txt_correo = QLineEdit()
        self.txt_correo.setPlaceholderText("correo@ejemplo.com")

        self.cmb_condicion = QComboBox()
        self.cmb_condicion.addItems(["ordinario", "contratado", "jubilado"])

        self.cmb_rango = QComboBox()

        self.fecha_ingreso = QDateEdit()
        self.fecha_ingreso.setCalendarPopup(True)
        self.fecha_ingreso.setDate(QDate.currentDate())

        campos = [
            ("Cédula *", self.txt_cedula, 0, 0),
            ("Nombre *", self.txt_nombre, 0, 1),
            ("Apellido *", self.txt_apellido, 1, 0),
            ("Teléfono", self.txt_telefono, 1, 1),
            ("Correo", self.txt_correo, 2, 0),
            ("Condición", self.cmb_condicion, 2, 1),
            ("Rango/Cargo *", self.cmb_rango, 3, 0),
            ("Fecha de ingreso *", self.fecha_ingreso, 3, 1),
        ]

        for texto, widget, fila, col in campos:
            lbl = QLabel(texto)
            lbl.setObjectName("labelCampo")
            cont = QVBoxLayout()
            cont.setContentsMargins(0, 0, 0, 0)
            cont.setSpacing(6)
            cont.addWidget(lbl)
            cont.addWidget(widget)
            panel = QWidget()
            panel.setLayout(cont)
            grid.addWidget(panel, fila, col)

        body_layout.addLayout(grid)

        fila_botones = QHBoxLayout()
        self.btn_cargar = QPushButton("Cargar selección")
        self.btn_cargar.setObjectName("btnBlue")
        self.btn_cargar.clicked.connect(self._cargar_seleccion_en_form)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setObjectName("btnGreen")
        self.btn_guardar.clicked.connect(self._guardar_afiliado)

        self.btn_desactivar = QPushButton("Desactivar")
        self.btn_desactivar.setObjectName("btnRed")
        self.btn_desactivar.clicked.connect(self._desactivar_afiliado)

        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.setObjectName("btnOutline")
        self.btn_cerrar.clicked.connect(self.close)

        fila_botones.addWidget(self.btn_cargar)
        fila_botones.addWidget(self.btn_guardar)
        fila_botones.addWidget(self.btn_desactivar)
        fila_botones.addStretch()
        fila_botones.addWidget(self.btn_cerrar)

        body_layout.addLayout(fila_botones)
        form_wrap.addWidget(form_body)
        root.addWidget(self.card_form, 1)

    def _aplicar_estilos(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #050b1b;
                color: #dbe7ff;
                font-family: 'Segoe UI';
            }

            QLabel {
                background: transparent;
                color: #dbe7ff;
            }

            QLabel#tituloModulo {
                font-size: 46px;
                font-weight: 800;
                color: #e6eeff;
            }

            QLabel#subtituloModulo {
                font-size: 14px;
                color: #7f95b8;
                margin-bottom: 4px;
            }

            QFrame#card {
                background-color: #0c1730;
                border: 1px solid #1b2c4e;
                border-radius: 16px;
            }

            QLabel#cardHeader {
                border-bottom: 1px solid #1b2c4e;
                font-size: 30px;
                font-weight: 700;
                color: #e8eeff;
                padding: 12px 14px;
            }

            QLabel#labelCampo {
                font-size: 13px;
                font-weight: 600;
                color: #8ea5c9;
                padding-left: 2px;
            }

            QLineEdit, QComboBox, QDateEdit {
                background-color: #0a1530;
                border: 1px solid #1f335a;
                border-radius: 10px;
                padding: 10px 12px;
                color: #dbe7ff;
                font-size: 13px;
                min-height: 20px;
            }

            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #3b82f6;
            }

            QLineEdit::placeholder {
                color: #5f7398;
            }

            QComboBox::drop-down, QDateEdit::drop-down {
                border: none;
                width: 20px;
            }

            QTableWidget {
                border: none;
                background-color: #0c1730;
                color: #d0ddf7;
                gridline-color: #182949;
                selection-background-color: rgba(59, 130, 246, 0.20);
                selection-color: #ffffff;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #0a1530;
                color: #8ea5c9;
                border: none;
                border-right: 1px solid #1b2c4e;
                border-bottom: 1px solid #1b2c4e;
                padding: 9px;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            QPushButton {
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 12px;
                font-weight: 700;
                min-height: 20px;
            }

            QPushButton#btnOutline {
                background-color: transparent;
                color: #8ea5c9;
                border: 1px solid #2a3e66;
            }

            QPushButton#btnOutline:hover {
                color: #dbe7ff;
                border-color: #3c5d93;
            }

            QPushButton#btnBlue {
                background-color: #3b82f6;
                color: #ffffff;
                border: 1px solid #2563eb;
            }

            QPushButton#btnBlue:hover { background-color: #2563eb; }

            QPushButton#btnGreen {
                background-color: #10b981;
                color: #052e16;
                border: 1px solid #059669;
            }

            QPushButton#btnGreen:hover { background-color: #22c55e; }

            QPushButton#btnRed {
                background-color: rgba(239, 68, 68, 0.16);
                color: #f87171;
                border: 1px solid rgba(239, 68, 68, 0.28);
            }

            QPushButton#btnRed:hover { background-color: rgba(239, 68, 68, 0.24); }
        """)

    def _cargar_rangos(self):
        self.cmb_rango.clear()
        filas = ejecutar_consulta("SELECT id_sueldo, descripcion, monto FROM sueldo_base ORDER BY descripcion")
        if not filas:
            return
        for r in filas:
            texto = f"{r['descripcion']} — Bs. {r['monto']:,.2f}"
            self.cmb_rango.addItem(texto, r['id_sueldo'])

    def _cargar_afiliados(self):
        query = """
            SELECT id_afiliado, cedula, nombre, apellido, telefono, correo, condicion, activo
            FROM afiliados
            ORDER BY activo DESC, apellido, nombre
        """
        filas = ejecutar_consulta(query) or []

        self.tabla.setRowCount(len(filas))
        for i, row in enumerate(filas):
            estado = "Activo" if row['activo'] else "Inactivo"
            valores = [
                row['id_afiliado'], row['cedula'], row['nombre'], row['apellido'],
                row['telefono'] or "", row['correo'] or "", row['condicion'].capitalize(), estado
            ]
            for j, val in enumerate(valores):
                item = QTableWidgetItem(str(val))
                if not row['activo']:
                    item.setForeground(Qt.gray)
                self.tabla.setItem(i, j, item)

        self._filtrar_tabla()

    def _filtrar_tabla(self):
        texto = self.txt_buscar.text().strip().lower()
        for i in range(self.tabla.rowCount()):
            ced = self.tabla.item(i, 1).text().lower()
            nom = self.tabla.item(i, 2).text().lower()
            ape = self.tabla.item(i, 3).text().lower()
            mostrar = (texto in ced) or (texto in nom) or (texto in ape)
            self.tabla.setRowHidden(i, not mostrar)

    def _fila_seleccionada_id(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            return None
        return int(self.tabla.item(fila, 0).text())

    def _cargar_seleccion_en_form(self):
        afiliado_id = self._fila_seleccionada_id()
        if not afiliado_id:
            QMessageBox.warning(self, "Atención", "Seleccione un afiliado en la tabla.")
            return

        fila = ejecutar_consulta(
            """
            SELECT id_afiliado, cedula, nombre, apellido, telefono, correo, condicion, id_sueldo, fecha_ingreso
            FROM afiliados WHERE id_afiliado = %s
            """,
            (afiliado_id,),
            fetchone=True
        )
        if not fila:
            QMessageBox.warning(self, "Aviso", "No se encontró el afiliado.")
            return

        self.afiliado_id_edicion = fila['id_afiliado']
        self.txt_cedula.setText(fila['cedula'])
        self.txt_nombre.setText(fila['nombre'])
        self.txt_apellido.setText(fila['apellido'])
        self.txt_telefono.setText(fila['telefono'] or "")
        self.txt_correo.setText(fila['correo'] or "")
        self.cmb_condicion.setCurrentText(fila['condicion'])

        idx_rango = self.cmb_rango.findData(fila['id_sueldo'])
        if idx_rango >= 0:
            self.cmb_rango.setCurrentIndex(idx_rango)

        fecha = fila['fecha_ingreso']
        self.fecha_ingreso.setDate(QDate(fecha.year, fecha.month, fecha.day))

    def _validar_form(self):
        ced = self.txt_cedula.text().strip()
        nom = self.txt_nombre.text().strip()
        ape = self.txt_apellido.text().strip()

        if not ced or not nom or not ape:
            QMessageBox.warning(self, "Validación", "Cédula, nombre y apellido son obligatorios.")
            return False

        if len(ced) < 6:
            QMessageBox.warning(self, "Validación", "La cédula parece inválida.")
            return False

        correo = self.txt_correo.text().strip()
        if correo and "@" not in correo:
            QMessageBox.warning(self, "Validación", "Correo inválido.")
            return False

        return True

    def _guardar_afiliado(self):
        if not self._validar_form():
            return

        datos = (
            self.txt_cedula.text().strip(),
            self.txt_nombre.text().strip(),
            self.txt_apellido.text().strip(),
            self.txt_telefono.text().strip() or None,
            self.txt_correo.text().strip() or None,
            self.cmb_condicion.currentText(),
            self.cmb_rango.currentData(),
            self.fecha_ingreso.date().toString("yyyy-MM-dd"),
        )

        if self.afiliado_id_edicion is None:
            ok = ejecutar_accion(
                """
                INSERT INTO afiliados (cedula, nombre, apellido, telefono, correo, condicion, id_sueldo, fecha_ingreso, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)
                """,
                datos,
            )
            if ok:
                QMessageBox.information(self, "Éxito", "Afiliado agregado correctamente.")
        else:
            ok = ejecutar_accion(
                """
                UPDATE afiliados
                SET cedula=%s, nombre=%s, apellido=%s, telefono=%s, correo=%s,
                    condicion=%s, id_sueldo=%s, fecha_ingreso=%s
                WHERE id_afiliado=%s
                """,
                datos + (self.afiliado_id_edicion,),
            )
            if ok:
                QMessageBox.information(self, "Éxito", "Afiliado actualizado correctamente.")

        if ok:
            self._limpiar_form()
            self._cargar_afiliados()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar. Verifique si la cédula ya existe.")

    def _desactivar_afiliado(self):
        afiliado_id = self._fila_seleccionada_id()
        if not afiliado_id:
            QMessageBox.warning(self, "Atención", "Seleccione un afiliado para desactivar.")
            return

        resp = QMessageBox.question(
            self,
            "Desactivar afiliado",
            "¿Desea marcar este afiliado como INACTIVO?\n\n(Se conserva historial)",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if resp != QMessageBox.Yes:
            return

        ok = ejecutar_accion("UPDATE afiliados SET activo = FALSE WHERE id_afiliado = %s", (afiliado_id,))
        if ok:
            QMessageBox.information(self, "Éxito", "Afiliado desactivado correctamente.")
            self._cargar_afiliados()
            self._limpiar_form()
        else:
            QMessageBox.critical(self, "Error", "No se pudo desactivar el afiliado.")

    def _limpiar_form(self):
        self.afiliado_id_edicion = None
        self.txt_cedula.clear()
        self.txt_nombre.clear()
        self.txt_apellido.clear()
        self.txt_telefono.clear()
        self.txt_correo.clear()
        self.cmb_condicion.setCurrentIndex(0)
        if self.cmb_rango.count():
            self.cmb_rango.setCurrentIndex(0)
        self.fecha_ingreso.setDate(QDate.currentDate())
        self.txt_cedula.setFocus()
