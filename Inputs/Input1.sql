CREATE FUNCTION fn_retornaalturamora (@diasmora int)
RETURNS nvarchar
AS
BEGIN
	DECLARE @alturamora nvarchar(100);
		if (@diasmora > 0 && @diasmora < 30) 
		BEGIN
			SET @alturamora = 'Al dia';
		END;
	
		IF (@diasmora >= 30 && @diasmora < 60) 
		BEGIN 
			SET @alturamora = 'Altura Mora 2';	
		END;
	
		IF (@diasmora >= 30 && @diasmora < 60) 
		BEGIN 
			SET @alturamora = 'Altura Mora 3';				
		END;

		IF (@diasmora >= 60 && @diasmora < 90) 
		BEGIN 
			SET @alturamora = 'Altura Mora 4';		
		END;
	
		IF (@diasmora >= 90 && @diasmora < 120) 
		BEGIN 
			SET @alturamora = 'Altura Mora 5';				
		END;
	RETURN @alturamora;
END;