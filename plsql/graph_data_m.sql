DROP FUNCTION graph_data_m;
CREATE FUNCTION graph_data_m (
	p_id integer,
	base_date date
)
RETURNS TABLE (
    WAKING integer,
    STAMP_YMD text,
    STAMP_HMS text
) AS $$
BEGIN
	RETURN QUERY
	select
	    stamp.WAKING,
	    TO_CHAR(stamp.TIME, 'YYYY-MM-DD'),
	    TO_CHAR(stamp.TIME, 'HH24:MI:SS')
	from
	    stamp
	where
	    stamp.ID = p_id AND
	    stamp.TIME BETWEEN
	    	base_date - interval '1 month' + interval '1 day' AND
	    	base_date + interval '1 day'
	order by
	    stamp.TIME asc;
END;
$$ LANGUAGE plpgsql;