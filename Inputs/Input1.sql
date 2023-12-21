CREATE DATA BASE tbbanco;  
-- USE tbbanco;
CREATE TABLE tbestado (
idestado int PRIMARY KEY,
estado nvarchar(50) NOT NULL
);

CREATE TABLE tbidentificaciontipo (
ididentificaciontipo int PRIMARY KEY,
identificaciontipo nvarchar(15) not null
);

CREATE TABLE tbcliente (
codigocliente nvarchar(15) PRIMARY KEY,
primer_nombre nvarchar(50) not null,
segundo_nombre nvarchar(50),
primer_apellido nvarchar(50) not null,
segundo_apellido nvarchar(50),
fecha_nacimiento date not null, 
genero nvarchar(1),
idestado int not null /*REFERENCE tbestado (idestado)*/
);

CREATE TABLE tbidentificacion (
ididentificacion int PRIMARY KEY,
codigocliente nvarchar(15) PRIMARY KEY, /*REFERENCE tbcliente (codigocliente)*/
identificacion nvarchar(20) NOT NULL,
ididentificaciontipo int /*REFERENCE tbidentificaciontipo (ididentificaciontipo)*/
);

INSERT INTO tbidentificaciontipo (ididentificaciontipo,identificaciontipo) VALUES(1,"DPI");
INSERT INTO tbidentificaciontipo (ididentificaciontipo,identificaciontipo) VALUES(2,"NIT");
INSERT INTO tbidentificaciontipo (ididentificaciontipo,identificaciontipo) VALUES(3,"PASAPORTE");

INSERT INTO tbestado (idestado,estado) VALUES(1,"Activo");
INSERT INTO tbestado (idestado,estado) VALUES(2,"Inactivo");
INSERT INTO tbestado (idestado,estado) VALUES(3,"Eliminado");

INSERT INTO tbcliente (codigocliente,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,fecha_nacimiento,genero,idestado)
VALUES ("GT-0001","PETER","JUAN","PARKER","SEGUNDO","1990-01-01","M",1);
INSERT INTO tbcliente (codigocliente,primer_nombre,primer_apellido,segundo_apellido,fecha_nacimiento,idestado)
VALUES ("GT-0002","JULIO","PEREZ","LOPEZ","1995-12-01",1);
INSERT INTO tbidentificacion (ididentificacion,codigocliente,identificacion,ididentificaciontipo)
VALUES (1,"GT-0001","45784560101",1);
INSERT INTO tbidentificacion (ididentificacion,codigocliente,identificacion,ididentificaciontipo)
VALUES (2,"GT-0001","94675057",2);
INSERT INTO tbidentificacion (ididentificacion,codigocliente,identificacion,ididentificaciontipo)
VALUES (3,"GT-0002","4854560101",1);

CREATE TABLE tbproducto (idproducto int primary key,
producto nvarchar(100) not null,
idestado int not null);

INSERT INTO tbproducto (idproducto,producto,idestado) VALUES(1,"Credito Fiduiciario",1);
INSERT INTO tbproducto (idproducto,producto,idestado) VALUES(2,"Credito Hipotecario",1);
INSERT INTO tbproducto (idproducto,producto,idestado) VALUES(3,"Tarjeta de Credito Oro",1);

-- ALTER TABLE tbproducto ADD COLUMN tasa decimal;

CREATE TABLE tbcredito (
credito int PRIMARY KEY,
nocuenta nvarchar(20) not null,
idcliente int not null,
fechaultimocorte date not null,
idproducto int /*REFERENCE tbproducto (idproducto)*/
);

CREATE TABLE tbobligaciontipo (
idobligaciontipo int PRIMARY KEY,
obligaciontipo nvarchar(30)
);

INSERT INTO tbobligaciontipo (idobligaciontipo,obligaciontipo) VALUES (1,"DIRECTO");
INSERT INTO tbobligaciontipo (idobligaciontipo,obligaciontipo) VALUES (2,"INDIRECTO");

CREATE TABLE tbcreditoobligacion (
codigocliente nvarchar(15) PRIMARY KEY, 
credito int PRIMARY KEY,
idobligaciontipo int /*REFERENCE tbobligaciontipo (idobligaciontipo)*/
);

INSERT INTO tbcredito (credito,nocuenta,idcliente,fechaultimocorte,idproducto) VALUES (1,"45-5454",1,"2023-11-30",1);
INSERT INTO tbcredito (credito,nocuenta,idcliente,fechaultimocorte,idproducto) VALUES (2,"AF4545D",3,"2023-11-30",1);
INSERT INTO tbcreditoobligacion (codigocliente,Credito,idobligaciontipo) VALUES ("GT-0001",1,1);
INSERT INTO tbcreditoobligacion  (codigocliente,Credito,idobligaciontipo) VALUES("GT-0002",2,1);

CREATE TABLE tbcreditoSaldo (
credito int PRIMARY KEY, 
fechacorte date PRIMARY KEY, 
idmoneda int PRIMARY KEY,
idcreditoestado int PRIMARY KEY, 
SaldoActual decimal, 
SaldoMora decimal,
ValorCuota decimal,
DiasMora int,
alturamora int not null,
limite decimal not null,
idcalificacion int not null
);

insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-01-31",1,1,05,0,600,0,0,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-02-28",1,1,4400,0,600,0,0,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-03-31",1,1,3800,0,600,0,0,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-04-30",1,1,3200,0,600,0,0,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-05-31",1,1,2600,0,600,0,0,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-06-30",1,1,2600,600,600,30,1,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-07-31",1,1,3150,1200.25,600,60,2,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-08-30",1,1,3760,1700,600,90,3,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-09-30",1,2,4275,2300,600,120,4,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-10-31",1,2,4275,2900,600,120,4,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-11-30",1,2,4275,3500,700,120,4,5000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (1,"2023-12-31",1,2,3575,3575,600,120,4,5000,1);

insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-01-31",1,1,15000,0,1250.25,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-02-28",1,1,14249.75,0,1250.25,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-03-31",1,1,12999.50,0,1250.25,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-04-30",1,1,11748.75,0,1250.75,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-05-31",1,1,10498,0,1250.75,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-06-30",1,1,9247.25,0,1250.75,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-07-31",1,1,7996.50,0,1250.75,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-08-30",1,1,6745.75,0,1250.75,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-09-30",1,2,5495,0,1250.75,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-10-31",1,2,4244.25,0,1250.75,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-11-30",1,2,2993.50,0,1250.75,0,0,15000,1);
insert into tbcreditoSaldo (credito,fechacorte,idmoneda,idcreditoestado,SaldoActual,SaldoMora,ValorCuota,DiasMora,
alturamora,limite,idcalificacion) values (2,"2023-12-31",1,2,1742.75,0,1250.75,0,0,15000,1);

-- SELECT tbcliente.codigocliente,CONCATENA(tbcliente.primer_nombre,tbcliente.primer_apellido),
-- tbidentificacion.identificacion,tbidentificaciontipo.identificaciontipo
-- FROM tbcliente,tbidentificacion ,tbidentificaciontipo 
-- where tbcliente.codigocliente = tbidentificacion.codigocliente 
-- && tbcliente.identificaciontipo = tbidentificacion.identificaciontipo;

-- SELECT tbcredito.credito,tbcredito.fechaultimocorte,tbcredito.nocuenta,fechaultimocorte,tbproducto.producto,
-- idmoneda,SaldoActual,SaldoMora,ValorCuota,DiasMora,alturamora,limite,idcalificacion
-- FROM tbcredito,tbcreditoobligacion,tbcreditoSaldo,tbcliente,tbproducto 
-- where tbcredito.credito = tbcreditoobligacion.credito 
-- && tbcreditoobligacion.Credito = tbcreditoSaldo.credito 
-- && tbcliente.codigocliente = tbcreditoobligacion.codigocliente
-- && tbproducto.idproducto = tbcredito.idproducto

-- select CONTAR(*) FROM tbcredito;
-- SELECT SUMA(SaldoActual) from tbcreditoSaldo;
-- SELECT HOY();

-- SELECT HOY(),SUBSTRAER(primer_nombre,1,5)
-- from tbcliente;