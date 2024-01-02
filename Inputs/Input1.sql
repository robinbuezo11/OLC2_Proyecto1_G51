-- lo del bit son puntos extras

-- CREATE FUNCTION fn_regresatasa (@idproducto int)
-- RETURN decimal
-- AS
-- BEGIN
-- 	DECLARE @TASA as decimal; 
-- 	set @TASA = (select tasa from tbproducto where idproducto = @idproducto and idestado = 1);

-- 	RETURN @TASA;	
-- END;

CREATE FUNCTION fn_retornanombre(@primerNombre as nvarchar, @segundoNombre nvarchar, @apellido_ nvarchar)
RETURNS nvarchar
AS
BEGIN
    DECLARE @nombres nvarchar(100);
	DECLARE @apellidos nvarchar(100);
	DECLARE @nombrecompleto nvarchar(100);

    SET @nombres = CONCATENAR(@primerNombre, @segundoNombre);
    SET @apellidos = @apellido_;
    RETURN CONCATENAR(@nombres, @apellidos);
END;

SELECT fn_retornanombre('Brandon', 'Andy', 'Tejaxun');

-- select fn_retornanombre(identificacion,primernombre,segundonombre)
-- from tbidentificacion 
-- where idestado = 1;

CREATE PROCEDURE sp_actualizatasa(@aumento int, @fecha date)
AS
BEGIN
		IF (@aumento > 0)
		BEGIN
            SELECT 'Aumento';
		END 
		ELSE 
		BEGIN
            select 'Disminucion';
		END; 
END;

sp_actualizatasa (0, '2021-01-01');