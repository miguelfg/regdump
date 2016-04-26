USE 'panama_registry';
CREATE TABLE sociedades (
  nombre VARCHAR,
  ficha INTEGER NOT NULL,
  capital FLOAT,
  moneda VARCHAR,
  agente VARCHAR,
  notaria VARCHAR,
  fecha_registro DATE,
  capital_text TEXT,
  representante_text TEXT,
  status VARCHAR,
  duracion VARCHAR,
  provincia VARCHAR,
  visited BOOLEAN,
  html TEXT,
  created_at DATETIME,
  updated_at DATETIME,
  PRIMARY KEY (ficha),
  UNIQUE (nombre),
  CHECK (visited IN (0, 1))
);
CREATE TABLE fundaciones (
  nombre VARCHAR,
  ficha INTEGER NOT NULL,
  documento INTEGER,
  escritura INTEGER,
  patrimonio FLOAT,
  moneda VARCHAR,
  agente VARCHAR,
  notaria VARCHAR,
  fecha_registro DATE,
  patrimonio_text TEXT,
  firmante_text TEXT,
  status VARCHAR,
  duracion VARCHAR,
  provincia VARCHAR,
  html TEXT,
  created_at DATETIME,
  updated_at DATETIME,
  PRIMARY KEY (ficha),
  UNIQUE (nombre)
);
CREATE TABLE personas (
  id INTEGER NOT NULL,
  nombre VARCHAR,
  created_at DATETIME,
  updated_at DATETIME,
  PRIMARY KEY (id),
  UNIQUE (nombre)
);
CREATE TABLE asociaciones (
  persona_id INTEGER NOT NULL,
  sociedad_id INTEGER NOT NULL,
  rol VARCHAR NOT NULL,
  PRIMARY KEY (persona_id, sociedad_id, rol),
  FOREIGN KEY(persona_id) REFERENCES personas (id),
  FOREIGN KEY(sociedad_id) REFERENCES sociedades (ficha)
);
CREATE TABLE fundacion_personas (
  persona_id INTEGER NOT NULL,
  fundacion_id INTEGER NOT NULL,
  rol VARCHAR NOT NULL,
  PRIMARY KEY (persona_id, fundacion_id, rol),
  FOREIGN KEY(persona_id) REFERENCES personas (id),
  FOREIGN KEY(fundacion_id) REFERENCES fundaciones (ficha)
);
