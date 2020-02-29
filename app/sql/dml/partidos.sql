with 
stg as (
    select 
        dados->>'id' as id, 
        dados->>'nome' as nm_partido, 
        dados->>'sigla' as nm_sigla, 
        dados->>'uri' as url_base,
        dados->'status' as status,
        '{ds}' as dt_evento
    from tbl_partidos_{ds_nodash}_stg
)

INSERT INTO tbl_partidos_{ds_nodash}
select 
    id,
    url_base,
    nm_partido,
    nm_sigla,
    regexp_replace(status->'lider'->>'uri', 'https://dadosabertos.camara.leg.br/api/v2/deputados/', '') as id_lider,
    (status->>'situacao') as st_partido,
    (status->>'totalPosse') as qt_posse,
    (status->>'totalMembros') as qt_membros,
    (status->>'idLegislatura') as id_legislatura,
    dt_evento
from stg
;