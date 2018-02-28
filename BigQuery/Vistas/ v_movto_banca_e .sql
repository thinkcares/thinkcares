select *,'movto_banca_e'as KxTblSource
from `mx-herdez-analytics.sethdzqa.movto_banca_e`
union all
select * ,'hist_movto_banca_e' as KxTblSource
from `mx-herdez-analytics.sethdzqa.hist_movto_banca_e`