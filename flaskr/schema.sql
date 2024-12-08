DROP TABLE IF EXISTS utenti;
DROP TABLE IF EXISTS eventi;
DROP TABLE IF EXISTS utenti_eventi;

CREATE TABLE utenti (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  nome TEXT UNIQUE NOT NULL,
  cognome TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE eventi (
  id INTEGER PRIMARY KEY AUTOINCREMENT,  
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  event_date DATE NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES utenti (id)
);

CREATE TABLE utenti_eventi (
  id_evento INTEGER NOT NULL,
  id_utente INTEGER NOT NULL,
  biglietti_prenotati INTEGER NOT NULL,
  FOREIGN KEY (id_evento) REFERENCES utenti (id),
  FOREIGN KEY (id_utente) REFERENCES eventi (id)
);