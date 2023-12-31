/*hanoi(3, "A", "C", "B");

create procedure hanoi(
    @n AS int,
    @origen AS nvarchar,
    @destino AS nvarchar,
    @medio AS nvarchar
)
begin
    if @n == 1 then
        select "Mover disco: 1, desde: "+ @origen+ " hasta: "+ @destino;
        return;
    end if;
    hanoi(@n - 1, @origen, @medio, @destino);
    select "Mover disco: "+ cast(@n as nvarchar) + ", desde: "+ @origen+ " hasta: "+ @destino;
    hanoi(@n - 1, @medio, @destino, @origen);
end;*/

select 12;
select 3.14;
select 15;
select 'Hola';