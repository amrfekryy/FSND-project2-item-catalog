
create table categories (
	id serial primary key,
	name varchar(50) not null
);


create table items (
 	id serial primary key,
 	name varchar(50) not null,
 	description varchar(1000),
 	category_id references categories (id)
);
