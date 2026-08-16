-- Tree database
-- Version 1.1
-- Date 3/13/2026
-- Author Ezra Billings and Kieran Larrabee
DROP DATABASE IF EXISTS tree;
CREATE DATABASE tree;
USE tree;

CREATE TABLE species (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    mature_size VARCHAR(10),
    functional_type VARCHAR(100),
    PRIMARY KEY (id),
    CONSTRAINT uc_name UNIQUE (name)
);

CREATE TABLE neighborhood (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    CONSTRAINT uc_name UNIQUE (name),
    PRIMARY KEY (id)
); 

CREATE TABLE address (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    street_address VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    state CHAR(2),
    zip VARCHAR(5),
    neighborhood_id INT UNSIGNED,
    PRIMARY KEY (id),
    FOREIGN KEY (neighborhood_id) REFERENCES neighborhood(id),
    CONSTRAINT uc_address UNIQUE (street_address, city, state, zip)
); 

CREATE TABLE site_description (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    site_type VARCHAR(50),
    site_size VARCHAR(50),
    site_width DOUBLE,
    wires VARCHAR(50),
    improvement VARCHAR(50),
    PRIMARY KEY (id),
    CONSTRAINT uc_site_description UNIQUE (site_type, site_size, site_width, wires, improvement)
);
        
CREATE TABLE bird_species (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    common_name VARCHAR(50),
    scientific_name VARCHAR(50),
    PRIMARY KEY (id),
    CONSTRAINT uc_common_name UNIQUE (common_name)
);

CREATE TABLE tree (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    x_coord DOUBLE NOT NULL,
    y_coord DOUBLE NOT NULL,
    diameter DOUBLE,
    date_inventoried DATETIME,
    tree_condition VARCHAR(50),
    address_id INT UNSIGNED,
    species_id INT UNSIGNED,
    site_description_id INT UNSIGNED,
    PRIMARY KEY (id),
    FOREIGN KEY (address_id) REFERENCES address(id),
    FOREIGN KEY (species_id) REFERENCES species(id),
    FOREIGN KEY (site_description_id) REFERENCES site_description(id)
);

CREATE TABLE bird_tree_xref (
    bird_species_id INT UNSIGNED NOT NULL,
    tree_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (bird_species_id, tree_id),
    FOREIGN KEY (bird_species_id) REFERENCES bird_species(id),
    FOREIGN KEY (tree_id) REFERENCES tree(id)
);


