-- Создаем таблицу Users
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(50) NOT NULL
);

-- Создаем таблицу Owners
CREATE TABLE Owners (
    owner_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    user_id INT REFERENCES Users(user_id),
    phone VARCHAR(20),
    email VARCHAR(255),
    address VARCHAR(255)
    
);

-- Создаем таблицу Animals
CREATE TABLE Animals (
    animal_id SERIAL PRIMARY KEY,
    owner_id INT NOT NULL REFERENCES Owners(owner_id),
    animal_type VARCHAR(255) NOT NULL,
    breed VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    birth_date DATE,
    special_needs TEXT
);

-- Создаем таблицу Services
CREATE TABLE Services (
    service_id SERIAL PRIMARY KEY,
    service_name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL
);

-- Создаем таблицу Employees
CREATE TABLE Employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    role VARCHAR(50) NOT null,
    description text,
    address VARCHAR(255),
    user_id INT references Users(user_id),
    verify INT
);

-- Создаем таблицу food
CREATE TABLE food (
    food_id SERIAL PRIMARY KEY,
    food_name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL
);

-- Создаем таблицу Bookings
CREATE TABLE Bookings (
    booking_id SERIAL PRIMARY KEY,
    animal_id INT NOT NULL REFERENCES Animals(animal_id),
    service_id INT NOT NULL REFERENCES Services(service_id),
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    employee_id INT REFERENCES Employees(employee_id),
    food_id INT REFERENCES food(food_id),
    price NUMERIC(10, 2) NOT NULL
);

CREATE OR REPLACE FUNCTION calculate_booking_price()
RETURNS TRIGGER AS $$
DECLARE
  days INT; -- Количество дней
  service_price NUMERIC(10, 2); -- Цена услуги
  food_price NUMERIC(10, 2); -- Цена корма
BEGIN
  -- Расчет количества дней
  days := (NEW.check_out_date - NEW.check_in_date + 1)::INT;

  -- Получение цены услуги
  SELECT price INTO service_price FROM Services WHERE service_id = NEW.service_id;

  -- Получение цены корма (обработка NULL food_id)
  SELECT COALESCE(price, 0) INTO food_price FROM food WHERE food_id = NEW.food_id;

  -- Расчет общей цены
  NEW.price := (service_price * days) + ((food_price / 30) * days);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_price_trigger
BEFORE INSERT ON Bookings
FOR EACH ROW
EXECUTE PROCEDURE calculate_booking_price();













