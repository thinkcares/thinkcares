 SET NOCOUNT ON   SELECT  [id_forma_pago],REPLACE(REPLACE(REPLACE(REPLACE([desc_forma_pago],'|',''),'"',''),CHAR(13),''),CHAR(10),'') as desc_forma_pago FROM [sethdzqa].[dbo].[cat_forma_pago] WITH (NOLOCK)