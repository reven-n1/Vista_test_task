create table contacts(id int NOT NULL AUTO_INCREMENT, user_id int NOT NULL ,full_name varchar(256) NOT NULL, phone varchar(256) NOT NULL, births_date date NOT NULL, PRIMARY KEY (id), UNIQUE KEY unique_record (user_id, full_name, phone, births_date), CONSTRAINT contacts_to_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE);

create table users(id int NOT NULL AUTO_INCREMENT, email varchar(256) NOT NULL, password varchar(256) NOT NULL, births_date date NOT NULL, PRIMARY KEY (id), UNIQUE KEY unique_users (email));

