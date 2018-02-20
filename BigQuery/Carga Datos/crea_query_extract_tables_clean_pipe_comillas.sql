with data as (
SELECT 
  TABLE_NAME,  
  TABLE_SCHEMA,
 case 
	when DATA_TYPE='varchar'
	 or DATA_TYPE='nvarchar' 
	 or DATA_TYPE='nchar'
	 or DATA_TYPE='char'
	 then 'REPLACE(REPLACE(REPLACE(REPLACE('+'['+COLUMN_NAME+']'+',''|'',''''),''"'',''''),CHAR(13),''''),CHAR(10),'''') as '  + COLUMN_NAME
	else '['+COLUMN_NAME+']'
end value2
,ORDINAL_POSITION
FROM INFORMATION_SCHEMA.COLUMNS
where TABLE_CATALOG='PRISM' 

)
    
SELECT 'SELECT '+
       ( SELECT value2 + ',' 
           FROM data p2
          WHERE p2.table_name = p1.table_name
          ORDER BY ORDINAL_POSITION ,value2
            FOR XML PATH('') ) +' FROM  [' +p1.TABLE_SCHEMA+'].['+p1.table_name+'] WITH (NOLOCK)' AS Products
FROM data p1
      GROUP BY table_name,p1.TABLE_SCHEMA

