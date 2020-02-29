CREATE TABLE IF NOT EXISTS tbl_deputados (
    id_deputado text not null,
    nu_cpf text,
    url_base text,
    sg_sexo text,
    nm_civil text,
    ls_rede_social text,
    url_deputado text,
    ds_escolaridade text,
    sg_uf_nascimento text,
    dt_nascimento text,
    dt_falecimento text,
    nm_municipio_nascimento text, 

    nm_deputado text,
    ds_email text,
    sg_uf text,
    url_foto text, 

    nu_sala text,
    nu_andar text,
    ds_email_gabinete text,
    nu_predio text,
    nu_telefone text, 

    ds_situacao text,
    sg_partido text,
    id_egislatura text,
    nm_eleitoral text,
    ds_status text,
    ds_condicao_leitoral text,
    dt_evento text
);