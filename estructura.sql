-- Estructura MySQL para bolprexSRL
CREATE DATABASE IF NOT EXISTS bolprex DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bolprex;

-- Tabla usuarios
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(256) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'cliente',
  city VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Usuario administrador de ejemplo
INSERT INTO usuarios (name, email, password_hash, role, city)
VALUES ('Administrador General', 'admin@bolprex.com', '$2b$12$yG1w9z7e3k0hQ9vP6g7uSeQJxH2h2ZlqOeV0R3qE.5fOa6wXwV4hC', 'admin', 'Cochabamba');
-- La contraseña del admin es: admin123  (hash bcrypt de ejemplo arriba)

-- Tabla envios
DROP TABLE IF EXISTS envios;
CREATE TABLE envios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tracking_code VARCHAR(20) NOT NULL UNIQUE,
  numero_guia VARCHAR(50) NOT NULL UNIQUE,
  sender_name VARCHAR(120) NOT NULL,
  recipient_name VARCHAR(120) NOT NULL,
  origin_city VARCHAR(50) NOT NULL,
  destination_city VARCHAR(50) NOT NULL,
  address VARCHAR(200) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
  notes VARCHAR(300),
  delivered_photo VARCHAR(300),
  delivered_at DATETIME NULL,
  client_id INT NULL,
  messenger_id INT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_envios_numero_guia (numero_guia)
) ENGINE=InnoDB;

-- Envío de prueba
INSERT INTO shipment (tracking_code, numero_guia, sender_name, recipient_name, origin_city, destination_city, address, status, created_at)
VALUES ('TRACK12345', 'GUIA98765', 'Empresa Ejemplo', 'Juan Pérez', 'La Paz', 'Cochabamba', 'Av. América #123', 'En tránsito', NOW());
