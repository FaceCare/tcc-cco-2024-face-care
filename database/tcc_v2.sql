-- TCC_V1

-- drop database if exists tcc;
create database if not exists tcc;

use tcc;

create table if not exists `tcc`.`photo` (
	id bigint primary key auto_increment,
	url text,
	date datetime,
	degree int(4)
);

create table if not exists `tcc`.`login` (
	id bigint primary key auto_increment,
	login varchar(60),
	passwd varchar(60)
);

create table  if not exists `tcc`.`user` (
	id bigint primary key auto_increment,
	first_name varchar(45),
	last_name varchar(45),
	email varchar(60) unique,
	cpf varchar(11) unique,
	phone_number varchar(11),
	fk_login bigint,
	fk_photo bigint,
	foreign key (fk_login) references login(id),
	foreign key (fk_photo) references photo(id)
);
