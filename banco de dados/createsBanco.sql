CREATE DATABASE dados_criminais;
USE dados_criminais;


CREATE TABLE Departamento (
    PK_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nome_departamento VARCHAR(100) NOT NULL
);

CREATE TABLE Seccional (
    PK_seccional INT AUTO_INCREMENT PRIMARY KEY,
    nome_seccional VARCHAR(100) NOT NULL,
    FK_departamento INT,
    FOREIGN KEY (FK_departamento) REFERENCES Departamento(PK_departamento)
);

CREATE TABLE Delegacia (
    PK_delegacia INT AUTO_INCREMENT PRIMARY KEY,
    nome_delegacia VARCHAR(100) NOT NULL,
    FK_seccional INT,
    FOREIGN KEY (FK_seccional) REFERENCES Seccional(PK_seccional)
);

CREATE TABLE Municipio (
    PK_municipio INT AUTO_INCREMENT PRIMARY KEY,
    nome_municipio VARCHAR(100) NOT NULL
);

CREATE TABLE Localizacao (
    PK_localizacao INT AUTO_INCREMENT PRIMARY KEY,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    FK_municipio INT,
    FOREIGN KEY (FK_municipio) REFERENCES Municipio(PK_municipio)
);

CREATE TABLE ocorrencias_criminais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_bo VARCHAR(20),
    ano_bo INT,
    data_registro DATE,
    data_ocorrencia DATE,
    hora_ocorrencia TIME,
    desc_periodo VARCHAR(50),
    nome_municipio VARCHAR(100),
    nome_departamento VARCHAR(100),
    nome_seccional VARCHAR(100),
    nome_delegacia VARCHAR(100),
    rubrica VARCHAR(255),
    natureza_apurada VARCHAR(255),
    descr_conduta TEXT,
    latitude DOUBLE,
    longitude DOUBLE,
    mes_estatistica INT,
    ano_estatistica INT,
    bairro VARCHAR(100),
    descr_subtipolocal VARCHAR(100),
    logradouro VARCHAR(150)
);

CREATE TABLE Natureza_Apurada (
    PK_natureza INT AUTO_INCREMENT PRIMARY KEY,
    descricao TEXT NOT NULL
);

CREATE TABLE Ocorrencia_Natureza (
    FK_ocorrencia INT,
    FK_natureza INT,
    PRIMARY KEY (FK_ocorrencia, FK_natureza),
    FOREIGN KEY (FK_ocorrencia) REFERENCES ocorrencias_criminais(id),
    FOREIGN KEY (FK_natureza) REFERENCES Natureza_Apurada(PK_natureza)
);

ALTER TABLE ocorrencias_criminais ADD COLUMN subtipo_local VARCHAR(100);

