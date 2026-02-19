-- ============================================================
-- BASE DE DATOS: CAJA DE AHORRO UPTNM "LUDOVICO SILVA"
-- Versión: 2.0
-- Fecha: Febrero 2026
-- Motor: MySQL 8.x
-- ============================================================

-- Eliminar la base de datos si ya existe (solo para desarrollo)
DROP DATABASE IF EXISTS caja_ahorro;

-- Crear la base de datos
CREATE DATABASE caja_ahorro
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_spanish_ci;

USE caja_ahorro;

-- ============================================================
-- TABLA 1: usuario
-- Usuarios del sistema (administradora/secretaria)
-- ============================================================
CREATE TABLE usuario (
  id_usuario    INT AUTO_INCREMENT PRIMARY KEY,
  cedula        VARCHAR(20) NOT NULL UNIQUE,
  nombre        VARCHAR(100) NOT NULL,
  apellido      VARCHAR(100) NOT NULL,
  correo        VARCHAR(100),
  clave_hash    VARCHAR(255) NOT NULL,
  rol           ENUM('admin', 'operador', 'consulta') NOT NULL DEFAULT 'operador',
  activo        BOOLEAN NOT NULL DEFAULT TRUE,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- TABLA 2: sueldo_base (rangos/cargos docentes)
-- Catálogo de rangos con su salario base
-- Al modificar el monto, se actualiza para todos los afiliados
-- con ese rango automáticamente
-- ============================================================
CREATE TABLE sueldo_base (
  id_sueldo     INT AUTO_INCREMENT PRIMARY KEY,
  descripcion   VARCHAR(100) NOT NULL UNIQUE,  -- Ej: Instructor, Asistente, Agregado, Asociado, Titular
  monto         DECIMAL(12,2) NOT NULL,         -- Salario base en Bs.
  activo        BOOLEAN NOT NULL DEFAULT TRUE,
  fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- TABLA 3: afiliados
-- Docentes asociados a la caja de ahorro
-- ============================================================
CREATE TABLE afiliados (
  id_afiliado   INT AUTO_INCREMENT PRIMARY KEY,
  cedula        VARCHAR(20) NOT NULL UNIQUE,
  nombre        VARCHAR(100) NOT NULL,
  apellido      VARCHAR(100) NOT NULL,
  telefono      VARCHAR(20),
  correo        VARCHAR(100),
  condicion     ENUM('ordinario', 'contratado', 'jubilado') NOT NULL DEFAULT 'ordinario',
  id_sueldo     INT NOT NULL,                   -- FK → sueldo_base (rango actual)
  fecha_ingreso DATE NOT NULL,                   -- Fecha de ingreso a la caja de ahorro
  activo        BOOLEAN NOT NULL DEFAULT TRUE,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_afiliado_sueldo
    FOREIGN KEY (id_sueldo) REFERENCES sueldo_base(id_sueldo)
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- TABLA 4: tasa
-- Catálogo de tasas de interés (actualmente 8% fija)
-- Se mantiene historicidad por si cambia en el futuro
-- ============================================================
CREATE TABLE tasa (
  id_tasa       INT AUTO_INCREMENT PRIMARY KEY,
  tasa          DECIMAL(5,2) NOT NULL,           -- Ej: 8.00
  descripcion   VARCHAR(100),                    -- Ej: "Tasa fija anual 2026"
  fecha_vigencia DATE NOT NULL,                  -- Desde cuándo aplica
  activa        BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

-- ============================================================
-- TABLA 5: prestamo
-- Registro de cada préstamo otorgado
-- Las cuotas se calculan UNA SOLA VEZ al aprobar
-- No hay recálculos nunca
-- ============================================================
CREATE TABLE prestamo (
  id_prestamo       INT AUTO_INCREMENT PRIMARY KEY,
  id_afiliado       INT NOT NULL,
  monto_solicitado  DECIMAL(12,2) NOT NULL,       -- Lo que pidió el docente
  monto_aprobado    DECIMAL(12,2) NOT NULL,       -- Lo que se le aprobó
  fecha_solicitud   DATE NOT NULL,
  fecha_inicio_pago DATE NOT NULL,                -- Cuándo empieza a pagar
  fecha_finalizacion DATE NOT NULL,               -- Cuándo termina de pagar
  num_cuotas        INT NOT NULL,                 -- Cantidad total de cuotas
  monto_cuota       DECIMAL(12,2) NOT NULL,       -- Monto fijo de cada cuota
  periodicidad      ENUM('mensual', 'quincenal') NOT NULL DEFAULT 'mensual',
  id_tasa           INT NOT NULL,                 -- Tasa vigente al momento de aprobar
  estado            ENUM('activo', 'pagado', 'cancelado') NOT NULL DEFAULT 'activo',
  fecha_registro    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_prestamo_afiliado
    FOREIGN KEY (id_afiliado) REFERENCES afiliados(id_afiliado),

  CONSTRAINT fk_prestamo_tasa
    FOREIGN KEY (id_tasa) REFERENCES tasa(id_tasa)
) ENGINE=InnoDB;

-- ============================================================
-- TABLA 6: plan_pago
-- Tabla de amortización generada automáticamente al aprobar
-- Cada fila = 1 cuota con desglose de capital + interés
-- El saldo de la última cuota SIEMPRE es 0.00
-- ============================================================
CREATE TABLE plan_pago (
  id_plan_pago      INT AUTO_INCREMENT PRIMARY KEY,
  id_prestamo       INT NOT NULL,
  num_cuota         INT NOT NULL,                 -- Número de cuota: 1, 2, 3...
  fecha_vencimiento DATE NOT NULL,                -- Cuándo vence esta cuota
  monto_capital     DECIMAL(12,2) NOT NULL,       -- Porción que va a capital
  monto_interes     DECIMAL(12,2) NOT NULL,       -- Porción que va a interés
  monto_cuota       DECIMAL(12,2) NOT NULL,       -- Capital + Interés
  saldo_restante    DECIMAL(12,2) NOT NULL,       -- Saldo después de esta cuota
  pagada            BOOLEAN NOT NULL DEFAULT FALSE,

  CONSTRAINT fk_plan_prestamo
    FOREIGN KEY (id_prestamo) REFERENCES prestamo(id_prestamo)
    ON DELETE CASCADE,

  -- No puede haber dos cuotas con el mismo número para el mismo préstamo
  UNIQUE KEY uk_prestamo_cuota (id_prestamo, num_cuota)
) ENGINE=InnoDB;

-- ============================================================
-- TABLA 7: detalles_prestamo (pagos/abonos reales)
-- Registro de cada pago realizado
-- ============================================================
CREATE TABLE detalles_prestamo (
  id_detalles_prestamo INT AUTO_INCREMENT PRIMARY KEY,
  id_prestamo          INT NOT NULL,
  id_plan_pago         INT,                       -- A qué cuota corresponde (NULL si es abono extra)
  fecha_pago           DATE NOT NULL,
  monto_abonado        DECIMAL(12,2) NOT NULL,
  tipo_pago            ENUM('cuota', 'abono_extra', 'nomina') NOT NULL DEFAULT 'nomina',
  observacion          TEXT,
  fecha_registro       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_detalle_prestamo
    FOREIGN KEY (id_prestamo) REFERENCES prestamo(id_prestamo),

  CONSTRAINT fk_detalle_plan
    FOREIGN KEY (id_plan_pago) REFERENCES plan_pago(id_plan_pago)
) ENGINE=InnoDB;

-- ============================================================
-- TABLA 8: aportes
-- Aportes mensuales de ahorro de cada afiliado
-- Es el corazón de la caja de ahorro
-- Se usa para reparto de fin de año y balances trimestrales
-- ============================================================
CREATE TABLE aportes (
  id_aporte     INT AUTO_INCREMENT PRIMARY KEY,
  id_afiliado   INT NOT NULL,
  anio          INT NOT NULL,                     -- Ej: 2026
  mes           INT NOT NULL,                     -- 1-12
  monto         DECIMAL(12,2) NOT NULL,
  fecha_registro DATE NOT NULL,

  CONSTRAINT fk_aporte_afiliado
    FOREIGN KEY (id_afiliado) REFERENCES afiliados(id_afiliado),

  -- Un afiliado no puede tener dos aportes en el mismo mes/año
  UNIQUE KEY uk_aporte_mes (id_afiliado, anio, mes)
) ENGINE=InnoDB;

-- ============================================================
-- TABLA 9: haberes
-- Registro mensual de haberes del afiliado
-- Se usa para verificar capacidad de pago
-- ============================================================
CREATE TABLE haberes (
  id_haberes    INT AUTO_INCREMENT PRIMARY KEY,
  id_afiliado   INT NOT NULL,
  anio          INT NOT NULL,
  mes           INT NOT NULL,                     -- 1-12
  monto         DECIMAL(12,2) NOT NULL,

  CONSTRAINT fk_haberes_afiliado
    FOREIGN KEY (id_afiliado) REFERENCES afiliados(id_afiliado),

  UNIQUE KEY uk_haberes_mes (id_afiliado, anio, mes)
) ENGINE=InnoDB;


-- ============================================================
-- DATOS INICIALES
-- ============================================================

-- Usuario administrador por defecto
-- Contraseña: admin123 (hash SHA256)
INSERT INTO usuario (cedula, nombre, apellido, correo, clave_hash, rol) VALUES
('V-00.000.001', 'Administrador', 'Sistema', 'admin@cajaahorro.edu.ve',
 SHA2('admin123', 256), 'admin');

-- Tasa de interés vigente (8%)
INSERT INTO tasa (tasa, descripcion, fecha_vigencia, activa) VALUES
(8.00, 'Tasa fija anual 2026', '2026-01-01', TRUE);

-- Rangos docentes iniciales (los montos son de ejemplo, la secretaria los ajustará)
INSERT INTO sueldo_base (descripcion, monto) VALUES
('Instructor', 2500.00),
('Asistente', 3200.00),
('Agregado', 4000.00),
('Asociado', 5000.00),
('Titular', 6500.00);


-- ============================================================
-- VISTAS ÚTILES
-- ============================================================

-- Vista: afiliados con su rango y salario actual
CREATE VIEW v_afiliados_completo AS
SELECT
  a.id_afiliado,
  a.cedula,
  a.nombre,
  a.apellido,
  a.telefono,
  a.correo,
  a.condicion,
  s.descripcion AS rango,
  s.monto AS sueldo_base,
  ROUND(s.monto * 0.3333, 2) AS max_cuota_permitida,
  a.fecha_ingreso,
  a.activo
FROM afiliados a
INNER JOIN sueldo_base s ON a.id_sueldo = s.id_sueldo;

-- Vista: préstamos con datos del afiliado
CREATE VIEW v_prestamos_completo AS
SELECT
  p.id_prestamo,
  a.cedula,
  CONCAT(a.nombre, ' ', a.apellido) AS afiliado,
  s.descripcion AS rango,
  p.monto_solicitado,
  p.monto_aprobado,
  p.num_cuotas,
  p.monto_cuota,
  p.periodicidad,
  t.tasa AS tasa_interes,
  p.fecha_solicitud,
  p.fecha_inicio_pago,
  p.fecha_finalizacion,
  p.estado,
  -- Cuotas pagadas
  (SELECT COUNT(*) FROM plan_pago pp WHERE pp.id_prestamo = p.id_prestamo AND pp.pagada = TRUE) AS cuotas_pagadas,
  -- Saldo pendiente
  (SELECT COALESCE(SUM(pp.monto_cuota), 0) FROM plan_pago pp WHERE pp.id_prestamo = p.id_prestamo AND pp.pagada = FALSE) AS saldo_pendiente
FROM prestamo p
INNER JOIN afiliados a ON p.id_afiliado = a.id_afiliado
INNER JOIN sueldo_base s ON a.id_sueldo = s.id_sueldo
INNER JOIN tasa t ON p.id_tasa = t.id_tasa;

-- Vista: resumen de préstamos por mes (para reporte general)
CREATE VIEW v_prestamos_por_mes AS
SELECT
  YEAR(p.fecha_solicitud) AS anio,
  MONTH(p.fecha_solicitud) AS mes,
  COUNT(*) AS total_prestamos,
  SUM(p.monto_aprobado) AS monto_total_prestado,
  AVG(p.monto_aprobado) AS monto_promedio,
  COUNT(DISTINCT p.id_afiliado) AS afiliados_distintos
FROM prestamo p
GROUP BY YEAR(p.fecha_solicitud), MONTH(p.fecha_solicitud);


-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================
-- Para ejecutar:
-- 1. Abrir MySQL Workbench o terminal MySQL
-- 2. Copiar y pegar todo este script
-- 3. Ejecutar (F5 o botón de rayo)
-- 4. Verificar: SHOW TABLES;
-- ============================================================
