USE ecommerce;

INSERT INTO customers (name, email, state, city) VALUES
    ('Alice Silva', 'alice@email.com', 'SP', 'São Paulo'),
    ('Bob Santos', 'bob@email.com', 'RJ', 'Rio de Janeiro'),
    ('Carol Souza', 'carol@email.com', 'SP', 'Campinas'),
    ('David Lima', 'david@email.com', 'MG', 'Belo Horizonte'),
    ('Eve Costa', 'eve@email.com', 'RJ', 'Niterói');

INSERT INTO products (name, category, price) VALUES
    ('Notebook Dell', 'Eletrônicos', 3500.00),
    ('Mouse Logitech', 'Acessórios', 120.00),
    ('Teclado Mecânico', 'Acessórios', 350.00),
    ('Monitor LG 27"', 'Eletrônicos', 1500.00),
    ('Webcam HD', 'Acessórios', 250.00);

INSERT INTO orders (customer_id, product_id, quantity, order_status) VALUES
    (1, 1, 1, 'completed'),
    (1, 2, 2, 'completed'),
    (2, 4, 1, 'completed'),
    (3, 3, 1, 'pending'),
    (4, 5, 3, 'completed'),
    (5, 1, 1, 'cancelled'),
    (2, 2, 1, 'completed'),
    (3, 4, 2, 'pending');