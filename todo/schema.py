instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS TODO;',
    'DROP TABLE IF EXISTS USER;',
    'SET FOREIGN_KEY_CHECKS=1;',

    """
    CREATE TABLE USER(
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    )
    """,
    """
    CREATE TABLE TODO(
        id INT PRIMARY KEY AUTO_INCREMENT,
        created_by INT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL,
        FOREIGN KEY (created_by) REFERENCES USER (id)
    )
    """

]