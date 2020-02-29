INSERT INTO tbl_deputados_{ds_nodash}
select 
    dados->>'id' as id_deputado,
    dados->>'cpf' as nu_cpf,
    dados->>'uri' as url_base,
    dados->>'sexo' as sg_sexo,
    initcap(dados->>'nomeCivil') as nm_civil,
    dados->>'redeSocial' as ls_rede_social,
    dados->>'urlWebsite' as url_deputado,
    dados->>'escolaridade' as ds_escolaridade,
    dados->>'ufNascimento' as sg_uf_nascimento,
    dados->>'dataNascimento' as dt_nascimento,
    dados->>'dataFalecimento' as dt_falecimento,
    dados->>'municipioNascimento' as nm_municipio_nascimento,

    initcap(dados->'ultimoStatus'->>'nome') as nm_deputado,
    dados->'ultimoStatus'->>'email' as ds_email,
    dados->'ultimoStatus'->>'siglaUf' as sg_uf,
    dados->'ultimoStatus'->>'urlFoto' as url_foto,

    dados->'ultimoStatus'->'gabinete'->>'sala' as nu_sala,
    dados->'ultimoStatus'->'gabinete'->>'andar' as nu_andar,
    dados->'ultimoStatus'->'gabinete'->>'email' as ds_email_gabinete,
    dados->'ultimoStatus'->'gabinete'->>'predio' as nu_predio,
    dados->'ultimoStatus'->'gabinete'->>'telefone' as nu_telefone,

    dados->'ultimoStatus'->>'situacao' as ds_situacao,
    dados->'ultimoStatus'->>'siglaPartido' as sg_partido,
    dados->'ultimoStatus'->>'idLegislatura' as id_egislatura,
    initcap(dados->'ultimoStatus'->>'nomeEleitoral') as nm_eleitoral,
    dados->'ultimoStatus'->>'descricaoStatus' as ds_status,
    dados->'ultimoStatus'->>'condicaoEleitoral' as ds_condicao_leitoral,
    '{ds}' as dt_evento
from tbl_deputados_{ds_nodash}_stg
;