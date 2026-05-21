-- ============================================================
-- BASE DE DATOS: AQUINIELATOR
-- Proyecto TFG DAW
-- Backend: FastAPI
-- SGBD: MySQL
-- ============================================================

DROP DATABASE IF EXISTS aquinielator_db;
CREATE DATABASE aquinielator_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE aquinielator_db;

-- ============================================================
-- TABLA: roles
-- Guarda los roles de la aplicación.
-- Ejemplos: USER, ADMIN
-- ============================================================

CREATE TABLE roles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA: users
-- Guarda los usuarios registrados en la aplicación.
-- La contraseña se guardará cifrada desde FastAPI.
-- ============================================================

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    role_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_users_roles
        FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Índices para mejorar búsquedas frecuentes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role_id ON users(role_id);

-- ============================================================
-- TABLA: teams
-- Guarda equipos de fútbol usados en las predicciones.
-- Puede rellenarse desde JSON/CSV o manualmente.
-- ============================================================

CREATE TABLE teams (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    stats_name VARCHAR(120) NOT NULL,
    csv_name VARCHAR(120) NOT NULL,
    short_name VARCHAR(20),
    league VARCHAR(100) DEFAULT 'LaLiga',
    country VARCHAR(100) DEFAULT 'España',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_teams_name ON teams(name);
CREATE INDEX idx_teams_stats_name ON teams(stats_name);
CREATE INDEX idx_teams_csv_name ON teams(csv_name);
CREATE INDEX idx_teams_league ON teams(league);

-- ============================================================
-- TABLA: predictions
-- Guarda una quiniela/predicción generada por un usuario.
-- Una predicción puede tener varios partidos asociados.
-- ============================================================

CREATE TABLE predictions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(150) NOT NULL DEFAULT 'Predicción de quiniela',
    model_used VARCHAR(80) NOT NULL DEFAULT 'ensemble',
    global_confidence DECIMAL(5,2),
    ai_explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_predictions_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT chk_predictions_confidence
        CHECK (global_confidence IS NULL OR (global_confidence >= 0 AND global_confidence <= 100))
);

CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
CREATE INDEX idx_predictions_model_used ON predictions(model_used);

-- ============================================================
-- TABLA: prediction_matches
-- Guarda los partidos concretos que forman parte de una predicción.
-- Cada registro representa un partido de una quiniela.
-- ============================================================

CREATE TABLE prediction_matches (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    prediction_id BIGINT NOT NULL,
    home_team VARCHAR(120) NOT NULL,
    away_team VARCHAR(120) NOT NULL,
    predicted_result ENUM('1', 'X', '2') NOT NULL,
    home_win_probability DECIMAL(5,2),
    draw_probability DECIMAL(5,2),
    away_win_probability DECIMAL(5,2),
    confidence DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prediction_matches_predictions
        FOREIGN KEY (prediction_id)
        REFERENCES predictions(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT chk_home_probability
        CHECK (home_win_probability IS NULL OR (home_win_probability >= 0 AND home_win_probability <= 100)),

    CONSTRAINT chk_draw_probability
        CHECK (draw_probability IS NULL OR (draw_probability >= 0 AND draw_probability <= 100)),

    CONSTRAINT chk_away_probability
        CHECK (away_win_probability IS NULL OR (away_win_probability >= 0 AND away_win_probability <= 100)),

    CONSTRAINT chk_match_confidence
        CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 100))
);

CREATE INDEX idx_prediction_matches_prediction_id ON prediction_matches(prediction_id);
CREATE INDEX idx_prediction_matches_home_team ON prediction_matches(home_team);
CREATE INDEX idx_prediction_matches_away_team ON prediction_matches(away_team);
CREATE INDEX idx_prediction_matches_result ON prediction_matches(predicted_result);

-- ============================================================
-- TABLA: favorites
-- Permite que un usuario marque predicciones como favoritas.
-- ============================================================

CREATE TABLE favorites (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    prediction_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_favorites_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_favorites_predictions
        FOREIGN KEY (prediction_id)
        REFERENCES predictions(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT uq_favorites_user_prediction
        UNIQUE (user_id, prediction_id)
);

CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_prediction_id ON favorites(prediction_id);

-- ============================================================
-- TABLA: login_audit
-- Guarda registros de inicio de sesión.
-- Nos sirve como auditoría básica.
-- ============================================================

CREATE TABLE login_audit (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    email VARCHAR(120) NOT NULL,
    success BOOLEAN NOT NULL,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_login_audit_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE INDEX idx_login_audit_user_id ON login_audit(user_id);
CREATE INDEX idx_login_audit_email ON login_audit(email);
CREATE INDEX idx_login_audit_created_at ON login_audit(created_at);

-- ============================================================
-- TABLA: prediction_audit
-- Guarda auditoría automática cuando se crea una predicción.
-- Se rellena mediante trigger.
-- ============================================================

CREATE TABLE prediction_audit (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    prediction_id BIGINT,
    user_id BIGINT,
    action VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prediction_audit_predictions
        FOREIGN KEY (prediction_id)
        REFERENCES predictions(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_prediction_audit_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE INDEX idx_prediction_audit_prediction_id ON prediction_audit(prediction_id);
CREATE INDEX idx_prediction_audit_user_id ON prediction_audit(user_id);
CREATE INDEX idx_prediction_audit_created_at ON prediction_audit(created_at);

-- ============================================================
-- INSERTS INICIALES
-- ============================================================

INSERT INTO roles (name, description) VALUES
('USER', 'Usuario normal de la aplicación'),
('ADMIN', 'Usuario administrador con permisos avanzados');

INSERT INTO teams (name, stats_name, csv_name, short_name, league, country) VALUES
('Real Madrid', 'Real Madrid', 'Real Madrid', 'RMA', 'LaLiga', 'España'),
('FC Barcelona', 'FC Barcelona', 'Barcelona', 'BAR', 'LaLiga', 'España'),
('Atlético de Madrid', 'Atlético de Madrid', 'Ath Madrid', 'ATM', 'LaLiga', 'España'),
('Sevilla', 'Sevilla FC', 'Sevilla', 'SEV', 'LaLiga', 'España'),
('Betis', 'Real Betis', 'Betis', 'BET', 'LaLiga', 'España'),
('Real Sociedad', 'Real Sociedad', 'Sociedad', 'RSO', 'LaLiga', 'España'),
('Villarreal', 'Villarreal CF', 'Villarreal', 'VIL', 'LaLiga', 'España'),
('Athletic Club', 'Athletic Club', 'Ath Bilbao', 'ATH', 'LaLiga', 'España'),
('Valencia', 'Valencia CF', 'Valencia', 'VAL', 'LaLiga', 'España'),
('Osasuna', 'CA Osasuna', 'Osasuna', 'OSA', 'LaLiga', 'España'),
('Celta de Vigo', 'Celta', 'Celta', 'CEL', 'LaLiga', 'España'),
('Rayo Vallecano', 'Rayo Vallecano', 'Vallecano', 'RAY', 'LaLiga', 'España'),
('Alavés', 'Deportivo Alavés', 'Alaves', 'ALA', 'LaLiga', 'España'),
('RCD Espanyol', 'RCD Espanyol de Barcelona', 'Espanol', 'ESP', 'LaLiga', 'España'),
('Elche', 'Elche CF', 'Elche', 'ELC', 'LaLiga', 'España'),
('Getafe', 'Getafe CF', 'Getafe', 'GET', 'LaLiga', 'España'),
('Mallorca', 'RCD Mallorca', 'Mallorca', 'MLL', 'LaLiga', 'España'),
('Levante UD', 'Levante UD', 'Levante', 'LEV', 'LaLiga', 'España'),
('Real Oviedo', 'Real Oviedo', 'Oviedo', 'OVI', 'LaLiga', 'España'),
('Girona', 'Girona FC', 'Girona', 'GIR', 'LaLiga', 'España');

-- ============================================================
-- TRIGGER 1:
-- Actualiza automáticamente updated_at en users.
-- ============================================================

DELIMITER //

CREATE TRIGGER trg_users_before_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

DELIMITER ;

-- ============================================================
-- TRIGGER 2:
-- Actualiza automáticamente updated_at en predictions.
-- ============================================================

DELIMITER //

CREATE TRIGGER trg_predictions_before_update
BEFORE UPDATE ON predictions
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

DELIMITER ;

-- ============================================================
-- TRIGGER 3:
-- Crea una auditoría automáticamente al insertar una predicción.
-- ============================================================

DELIMITER //

CREATE TRIGGER trg_predictions_after_insert
AFTER INSERT ON predictions
FOR EACH ROW
BEGIN
    INSERT INTO prediction_audit (
        prediction_id,
        user_id,
        action,
        description
    )
    VALUES (
        NEW.id,
        NEW.user_id,
        'CREATE',
        CONCAT('Predicción creada con el modelo ', NEW.model_used)
    );
END//

DELIMITER ;

-- ============================================================
-- FUNCIÓN:
-- Devuelve el número de predicciones creadas por un usuario.
-- ============================================================

DELIMITER //

CREATE FUNCTION fn_count_user_predictions(p_user_id BIGINT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_predictions INT;

    SELECT COUNT(*)
    INTO total_predictions
    FROM predictions
    WHERE user_id = p_user_id;

    RETURN total_predictions;
END//

DELIMITER ;

-- ============================================================
-- PROCEDIMIENTO:
-- Elimina predicciones antiguas de un usuario.
-- Sirve como ejemplo de mantenimiento de datos.
-- ============================================================

DELIMITER //

CREATE PROCEDURE sp_delete_old_predictions(
    IN p_user_id BIGINT,
    IN p_days INT
)
BEGIN
    DELETE FROM predictions
    WHERE user_id = p_user_id
    AND created_at < DATE_SUB(NOW(), INTERVAL p_days DAY);
END//

DELIMITER ;

-- ============================================================
-- VISTA:
-- Resumen de predicciones por usuario.
-- Nos puede servir para panel de usuario o administración.
-- ============================================================

CREATE VIEW vw_user_prediction_summary AS
SELECT
    u.id AS user_id,
    u.username,
    u.email,
    COUNT(p.id) AS total_predictions,
    MAX(p.created_at) AS last_prediction_date
FROM users u
LEFT JOIN predictions p ON u.id = p.user_id
GROUP BY u.id, u.username, u.email;

-- ============================================================
-- CONSULTAS DE COMPROBACIÓN
-- ============================================================

SELECT 'Base de datos aquinielator_db creada correctamente' AS message;
SELECT * FROM roles;
SELECT * FROM teams;