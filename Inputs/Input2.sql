-----lo del bit son puntos extras

CREATE FUNCTION fn_regresatasa (@idproducto as int)
RETURNS decimal
BEGIN
	DECLARE @TASA decimal; 
	set @TASA = (select tasa from tbproducto where idproducto = @idproducto and idestado = 1);

	RETURN @TASA;
END;