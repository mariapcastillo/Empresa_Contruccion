-- (Opcional) crea y usa la BD
CREATE DATABASE IF NOT EXISTS empresa_construccion DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;

USE empresa_construccion;

-- =========================
-- 1) USERS
-- =========================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NULL,
    last_name VARCHAR(100) NULL,
    rol ENUM('admin', 'operario') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- =========================
-- 2) OPERARIOS
-- =========================

CREATE TABLE operarios (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NOT NULL,
    especialidad  VARCHAR(100) NOT NULL,
    estado        ENUM('disponible', 'ocupado') NOT NULL,
    localizacion  VARCHAR(255) NOT NULL,
    telefono      VARCHAR(15) NOT NULL,

CONSTRAINT fk_operarios_user
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

-- Si quieres reflejar "un user tiene (a lo sumo) un operario"
CONSTRAINT uq_operarios_user UNIQUE (user_id) ) ENGINE=InnoDB;

-- =========================
-- 3) OBRAS
-- =========================
CREATE TABLE obras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    localizacion VARCHAR(200) NOT NULL,
    operario_id INT NULL,
    estado ENUM(
        'pendiente',
        'en progreso',
        'completada'
    ) NOT NULL,
    foto TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_inicio TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_obras_operario FOREIGN KEY (operario_id) REFERENCES operarios (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB;

-- =========================
-- 4) NOTIFICACIONES
-- =========================
CREATE TABLE notificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    obra_id INT NOT NULL,
    tipo ENUM(
        'incidencia',
        'avance',
        'material'
    ) NOT NULL,
    mensaje TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_notif_obra FOREIGN KEY (obra_id) REFERENCES obras (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- Índices recomendados para consultas típicas
CREATE INDEX idx_obras_operario ON obras (operario_id);

CREATE INDEX idx_notif_user_read ON notificaciones (user_id, is_read);

CREATE INDEX idx_notif_obra ON notificaciones (obra_id);

CREATE INDEX idx_notif_created_at ON notificaciones (created_at);  