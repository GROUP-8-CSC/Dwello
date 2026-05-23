CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE properties (
    property_id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    region VARCHAR(50) NOT NULL,
    neighborhood VARCHAR(100) NOT NULL,
    price BIGINT NOT NULL,
    description TEXT,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE saved_properties (
    saved_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    property_id INT REFERENCES properties(property_id) ON DELETE CASCADE,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO properties
(title, region, neighborhood, price, description, image_path)
VALUES

(
    '3 Bedroom Duplex',
    'Mainland',
    'Ikeja',
    35000000,
    'Spacious duplex with modern finishing and parking space.',
    'assets/images/ikeja_duplex.jpg'
),

(
    'Modern Mini Flat',
    'Mainland',
    'Yaba',
    18000000,
    'Affordable apartment close to tech hubs and transport routes.',
    'assets/images/yaba_flat.jpg'
),

(
    'Luxury Apartment',
    'Mainland',
    'Surulere',
    42000000,
    'Elegant apartment with premium interiors and balcony.',
    'assets/images/surulere_apartment.jpg'
),

(
    'Executive Family House',
    'Mainland',
    'Maryland',
    55000000,
    'Large family house in a peaceful neighborhood.',
    'assets/images/maryland_house.jpg'
),

(
    'Contemporary Flat',
    'Mainland',
    'Gbagada',
    28000000,
    'Modern flat with excellent road accessibility.',
    'assets/images/gbagada_flat.jpg'
),

(
    'Luxury Penthouse',
    'Island',
    'Lekki',
    120000000,
    'Premium penthouse with ocean-facing balcony.',
    'assets/images/lekki_penthouse.jpg'
),

(
    'Beachfront Apartment',
    'Island',
    'Victoria Island',
    95000000,
    'Stylish apartment close to commercial districts and beaches.',
    'assets/images/vi_apartment.jpg'
),

(
    'Smart Home Duplex',
    'Island',
    'Ikoyi',
    150000000,
    'Fully automated smart duplex with premium security systems.',
    'assets/images/ikoyi_duplex.jpg'
),

(
    'Modern Apartment',
    'Island',
    'Ajah',
    45000000,
    'Contemporary apartment in a rapidly developing area.',
    'assets/images/ajah_apartment.jpg'
),

(
    'Luxury Terrace',
    'Island',
    'Chevron',
    70000000,
    'Modern terrace property with upscale amenities.',
    'assets/images/chevron_terrace.jpg'
);