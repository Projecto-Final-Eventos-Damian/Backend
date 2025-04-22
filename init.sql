CREATE DATABASE IF NOT EXISTS eventos_db;
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON eventos_db.* TO 'admin'@'%';
FLUSH PRIVILEGES;

USE eventos_db;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'organizer', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT NOT NULL,
    organizer_id INT NOT NULL,
    capacity INT NOT NULL,
    start_date_time DATETIME NOT NULL,
    end_date_time DATETIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (organizer_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reservations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    tickets_number INT NOT NULL,
    reserved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS ticket_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tickets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    ticket_type_id INT NOT NULL,
    ticket_code VARCHAR(50) UNIQUE NOT NULL,
    status ENUM('valid', 'used', 'cancelled') DEFAULT 'valid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_type_id) REFERENCES ticket_types(id),
    FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_ratings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    rating TINYINT UNSIGNED NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    payment_method ENUM('credit_card', 'paypal', 'stripe'),
    transaction_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id)
);

CREATE TABLE IF NOT EXISTS user_followers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    organizer_id INT NOT NULL,
    followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, organizer_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (organizer_id) REFERENCES users(id)
);

-- Usuarios
INSERT INTO users (id, name, email, password_hash, role) VALUES
(1, 'Organizador1', 'org1@example.com', '$2b$12$R6AgBSkyZT03C9XAxX.LoeRtCQYNZEnzYaltcFrbB89qEDCJXRM8C', 'organizer'),
(2, 'Organizador2', 'org2@example.com', '$2b$12$gl0tt4nhct5XH.MftrwlwOYzYpWpIPFQwSXSc.cE1mCz/7ZzPyDrK', 'organizer'),
(4, 'User1', 'user1@example.com', '$2b$12$uf.ayV1TqhW.cvsY0Ih.JuLsW8ToFqvmsIVfhtlX7yOOYHdP5kjJ.', 'user'),
(5, 'User2', 'user2@example.com', '$2b$12$GpJMy37Sxpo6byuL6KrNre2TME7JP/bB3PwUp7GFlucYYF52kMLPO', 'user'),
(6, 'User3', 'user3@example.com', '$2b$12$Q.xHuhU.4WPf1B0xTMw/LODe8cLHnAT1KKnii5goeSe12LY8YYozy', 'user');

-- Categorías
INSERT INTO categories (id, name, description) VALUES
(1, 'Fiesta', NULL),
(2, 'Deporte', 'ejercicios al aire libre');

-- Evento
INSERT INTO events (
    title, description, category_id, organizer_id, capacity,
    start_date_time, end_date_time, location, image_url
) VALUES (
    'Fiesta en Alcoy',
    'Fiesta temática en Alcoy sobre moros y cristianos',
    1,
    1,
    100,
    '2025-04-04 16:22:22',
    '2025-04-04 23:22:22',
    'Alcoy',
    'https://example.com/'
);