from pydal import DAL, Field


def model(dbinfo="sqlite://storage.sqlite", dbfolder="./dados"):
    db = DAL(dbinfo, folder=dbfolder, pool_size=1)
    table(db)
    return db


def table(db):
    db.define_table("populacao_total",
                    Field("uf", type="string"),
                    Field("populacao", type="double")
                    )
                    
    db.define_table("uf_nome",
                    Field("uf", type="string"),
                    Field("nome", type="string")
                    )



DB = model()
