
INSERT INTO Departamento (nome_departamento)
SELECT DISTINCT oc.nome_departamento
FROM ocorrencias_criminais oc
WHERE NOT EXISTS (
    SELECT 1 
    FROM Departamento d 
    WHERE d.nome_departamento = oc.nome_departamento
);

INSERT INTO Seccional (nome_seccional, FK_departamento)
SELECT DISTINCT oc.nome_seccional, d.PK_departamento
FROM ocorrencias_criminais oc
JOIN Departamento d ON d.nome_departamento = oc.nome_departamento
WHERE NOT EXISTS (
    SELECT 1 
    FROM Seccional s
    WHERE s.nome_seccional = oc.nome_seccional
);

INSERT INTO Delegacia (nome_delegacia, FK_seccional)
SELECT DISTINCT oc.nome_delegacia, s.PK_seccional
FROM ocorrencias_criminais oc
JOIN Seccional s ON s.nome_seccional = oc.nome_seccional
WHERE NOT EXISTS (
    SELECT 1 
    FROM Delegacia d
    WHERE d.nome_delegacia = oc.nome_delegacia
);

INSERT INTO Municipio (nome_municipio)
SELECT DISTINCT oc.nome_municipio
FROM ocorrencias_criminais oc
WHERE NOT EXISTS (
    SELECT 1
    FROM Municipio m
    WHERE m.nome_municipio = oc.nome_municipio
);

INSERT INTO Localizacao (latitude, longitude, FK_municipio)
SELECT DISTINCT
    CAST(oc.latitude AS DECIMAL(10,8)) AS latitude,
    CAST(oc.longitude AS DECIMAL(11,8)) AS longitude,
    m.PK_municipio
FROM ocorrencias_criminais oc
JOIN Municipio m ON m.nome_municipio = oc.nome_municipio
WHERE oc.latitude REGEXP '^-?[0-9]+\\.[0-9]+'
  AND oc.longitude REGEXP '^-?[0-9]+\\.[0-9]+'
  AND NOT EXISTS (
      SELECT 1
      FROM Localizacao l
      WHERE l.latitude = CAST(oc.latitude AS DECIMAL(10,8))
        AND l.longitude = CAST(oc.longitude AS DECIMAL(11,8))
  );

INSERT INTO Natureza_Apurada (descricao)
SELECT DISTINCT oc.NATUREZA_APURADA
FROM ocorrencias_criminais oc
WHERE oc.NATUREZA_APURADA IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM Natureza_Apurada na
      WHERE na.descricao = oc.NATUREZA_APURADA
  );

INSERT INTO Ocorrencia_Natureza (FK_ocorrencia, FK_natureza)
SELECT DISTINCT oc.id, na.PK_natureza
FROM ocorrencias_criminais oc
JOIN Natureza_Apurada na ON na.descricao = oc.NATUREZA_APURADA
WHERE oc.NATUREZA_APURADA IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM Ocorrencia_Natureza onat
      WHERE onat.FK_ocorrencia = oc.id
        AND onat.FK_natureza = na.PK_natureza
  );
