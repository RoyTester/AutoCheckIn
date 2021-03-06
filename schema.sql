DROP TABLE IF EXISTS titles;
DROP TABLE IF EXISTS ywzs;

CREATE TABLE titles (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) UNIQUE NOT NULL,
  url TEXT  NOT NULL
);
CREATE TABLE ywzs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title_id INT NOT NULL,
  title TEXT NOT NULL,
  ywz_text TEXT NOT NULL,
  ywz TEXT NOT NULL,
  FOREIGN KEY ywzs(title_id) REFERENCES titles(id)
)