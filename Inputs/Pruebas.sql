create table products(
    ID int not null primary key,
    PrimerNombre nvarchar(3) not null,
    rol nvarchar(150),
    identificacion int,
    foreing key (identificacion) reference indentificaciones(identificacion)
);

insert into products(id, primernombre, rol, identificacion) values(1, "Miguel Alcubierre", "Escritor", 11);
insert into products(id, primernombre, rol, identificacion) values(2, "Isaac Asimov", "Escritor", 12);
insert into products(id, primernombre, rol, identificacion) values(3, "Marie Curie", "Escritor", 13);
insert into products(id, primernombre, rol, identificacion) values(4, "Stephen Hawking", "Escritor", 14);
insert into products(id, primernombre, rol, identificacion) values(5, "Susana Arrechea", "Escritor", 15);

update products set rol = "Investigador" where ID = 5;
-- truncate table products;
-- delete from products where rol = "Escritor";
-- drop table products;

select identificacion
from products
where ID > 0 && ID < 4;