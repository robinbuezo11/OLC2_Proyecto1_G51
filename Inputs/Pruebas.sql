-- create procedure hanoi(
--     @n AS int,
--     @origen AS nvarchar,
--     @destino AS nvarchar,
--     @medio AS nvarchar
-- )
-- begin
--     if @n == 1 then
--         select 'Mover disco: 1, desde: '+ @origen+ ' hasta: '+ @destino;
--         return;
--     end if;
--     hanoi(@n - 1, @origen, @medio, @destino);
--     select 'Mover disco: '+ @n + ', desde: '+ @origen+ ' hasta: '+ @destino;
--     hanoi(@n - 1, @medio, @destino, @origen);
-- end;

-- hanoi(3, 'A', 'C', 'B');

create procedure factorial(@n AS int) begin
    DECLARE @FACTORIAL INT;
    SET @FACTORIAL = 1;
    WHILE @N >= 1 begin
        SET @FACTORIAL = @FACTORIAL * @N;
        SET @N = @N - 1;
    END;
    SELECT @FACTORIAL;
end;

factorial(2);

-- declare @nota int;
-- set @nota = 62;

-- if @nota >= 61 && @nota <= 63 then
--     select 'Aprobado';
-- else
--     select 'Reprobado';
-- end if;