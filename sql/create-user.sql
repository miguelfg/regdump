CREATE USER 'panama_scraper'@'%' IDENTIFIED BY 'multi-server-scraper';
GRANT ALL PRIVILEGES ON panama_registry.* TO 'panama_scraper'@'%';
FLUSH PRIVILEGES;
