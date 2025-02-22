DROP FUNCTION totalling;
CREATE FUNCTION totalling(
	p_id integer
)
RETURNS TABLE (
	ID integer,
    WAKING integer,
    STAMP_TIME text,
    DELTA interval
) AS $$
BEGIN
    RETURN QUERY
	select
		STARTt.ID,
		STARTt.WAKING,
		TO_CHAR(STARTt.TIME, 'YYYY-MM-DD HH24:MI:SS'),
		ENDt.TIME - STARTt.TIME
	from (
		select
			stamp.ID,
			stamp.WAKING,
			TO_CHAR(stamp.TIME, 'YYYY-MM-DD HH24:MI:SS'),
			stamp.TIME,
			ROW_NUMBER() OVER(order by TIME desc) as row
		from
			stamp
		where
			stamp.ID = p_id
		order by stamp.TIME desc
	) as STARTt
	left outer join (
		select
			stamp.ID,
			stamp.WAKING,
			TO_CHAR(stamp.TIME, 'YYYY-MM-DD HH24:MI:SS'),
			stamp.TIME,
			ROW_NUMBER() OVER(order by TIME desc) as row
		from
			stamp
		where
			stamp.ID = p_id
		order by stamp.TIME desc
	) as ENDt on STARTt.row - 1 = ENDt.row;
END;
$$ LANGUAGE plpgsql;