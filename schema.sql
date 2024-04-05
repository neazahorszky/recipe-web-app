CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    user_id INTEGER REFERENCES users(id),
    ingredients TEXT,
    instructions TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    rating INTEGER,
    comment TEXT
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE recipes_categorized (
    category_id INTEGER REFERENCES categories(id),
    recipe_id INTEGER REFERENCES recipes(id)
);