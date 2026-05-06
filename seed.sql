CREATE TABLE characters (
    char_id INT PRIMARY KEY AUTO_INCREMENT,
    char_name VARCHAR(100),
    char_category VARCHAR(100)
);

CREATE TABLE quotes (
    quote_id INT PRIMARY KEY AUTO_INCREMENT,
    character_id INT,
    quote TEXT,
    quote_jp TEXT,
    FOREIGN KEY (character_id)
        REFERENCES characters(char_id)
);