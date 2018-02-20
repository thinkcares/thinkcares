declare @dataset_name nvarchar(100)
set @dataset_name='PRISM.';


with data as (
SELECT 
  TABLE_NAME,
  TABLE_SCHEMA,TABLE_CATALOG
, REPLACE(REPLACE(COLUMN_NAME,'$',''),'#','_')  +':' +
 case 
	when DATA_TYPE='varchar' then 'STRING'
	when DATA_TYPE='nvarchar' then 'STRING'
	when DATA_TYPE='nchar' then 'STRING'
	when DATA_TYPE='char' then 'STRING'
	when DATA_TYPE='int' then 'INTEGER'
	when DATA_TYPE='smallint' then 'INTEGER'
	when DATA_TYPE='bigint' then 'INTEGER'
	when DATA_TYPE='decimal' then 'FLOAT'
	when DATA_TYPE='numeric' then 'FLOAT'
	when DATA_TYPE='float' then 'FLOAT'
	when DATA_TYPE='datetime' then 'TIMESTAMP'
	when DATA_TYPE='date' then 'TIMESTAMP'
END  value2
,ORDINAL_POSITION
--select * 
FROM INFORMATION_SCHEMA.COLUMNS
where TABLE_CATALOG='PRISM'  
    )
SELECT 'bq mk -t '+ @dataset_name +p1.TABLE_SCHEMA+'_'+p1.table_name+' '+
       ( SELECT value2 + ',' 
           FROM data p2
          WHERE p2.table_name = p1.table_name
          ORDER BY ORDINAL_POSITION,value2
            FOR XML PATH('') ) AS Products
FROM data p1
      GROUP BY table_name,p1.TABLE_SCHEMA,p1.TABLE_CATALOG ;
      
     
