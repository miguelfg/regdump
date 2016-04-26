USE 'panama_registry';
CREATE TABLE sociedades (
  nombre VARCHAR(100),
  ficha INTEGER NOT NULL,
  capital FLOAT NOT NULL,
  moneda VARCHAR(30),
  agente VARCHAR(50),
  notaria VARCHAR(50),
  fecha_registro DATE,
  capital_text VARCHAR(1000),
  representante_text VARCHAR(1000),
  status VARCHAR(30),
  duracion VARCHAR(10) NOT NULL,
  provincia VARCHAR(20),
  visited INTEGER NOT NULL,
  html VARCHAR(32),
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (ficha)
);

CREATE TABLE personas (
  id INTEGER NOT NULL,
  nombre VARCHAR(50),
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE personas (
  id INTEGER NOT NULL,
  nombre VARCHAR(50),
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);

CREATE TABLE asociaciones (
  persona_id INTEGER NOT NULL,
  sociedad_id INTEGER NOT NULL,
  rol VARCHAR(25) NOT NULL,
  PRIMARY KEY (persona_id, sociedad_id, rol),
  FOREIGN KEY(persona_id) REFERENCES personas (id),
  FOREIGN KEY(sociedad_id) REFERENCES sociedades (ficha)
);

CREATE TABLE asociaciones (
  persona_id INTEGER NOT NULL,
  sociedad_id INTEGER NOT NULL,
  rol VARCHAR(25) NOT NULL,
  FOREIGN KEY(sociedad_id) REFERENCES sociedades (ficha)
);

CREATE TABLE fundaciones (
  nombre VARCHAR(100),
  ficha INTEGER NOT NULL,
  documento INTEGER,
  escritura INTEGER,
  patrimonio FLOAT,
  moneda VARCHAR(30),
  agente VARCHAR(50),
  notaria VARCHAR(50),
  fecha_registro DATE,
  patrimonio_text TEXT,
  firmante_text TEXT,
  status VARCHAR(30),
  duracion VARCHAR(10) NOT NULL,
  provincia VARCHAR(20),
  html VARCHAR(32),
  created_at DATETIME,
  updated_at DATETIME,
  PRIMARY KEY (ficha),
  UNIQUE (nombre)
);

CREATE TABLE fundacion_personas (
  persona_id INTEGER NOT NULL,
  fundacion_id INTEGER NOT NULL,
  rol VARCHAR(25) NOT NULL,
  PRIMARY KEY (persona_id, fundacion_id, rol),
  FOREIGN KEY(fundacion_id) REFERENCES fundaciones (ficha)
);
