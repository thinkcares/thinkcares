SET NOCOUNT ON   SELECT  [id_grupo_flujo],REPLACE(REPLACE(REPLACE(REPLACE([desc_grupo_flujo],'|',''),'"',''),CHAR(13),''),CHAR(10),'') as desc_grupo_flujo,REPLACE(REPLACE(REPLACE(REPLACE([correo_empresa],'|',''),'"',''),CHAR(13),''),CHAR(10),'') as correo_empresa,REPLACE(REPLACE(REPLACE(REPLACE([remitente_correo],'|',''),'"',''),CHAR(13),''),CHAR(10),'') as remitente_correo,[nivel_autorizacion] FROM [sethdzqa].[dbo].[cat_grupo_flujo] WITH (NOLOCK)