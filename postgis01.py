from postgis_module import pg
class pg(pg):
    def __init__(self, dbname='gistest'):
        super(pg, self).__init__(dbname=dbname)
        self.pg.execute("select version()")
        for x in self.pg:
            print(x)

    def chk_srid(self):
        self.pg.execute('select ST_SRID(geom) from tokyo_syogyo limit 1')
        for x in self.pg:
            print(x)

    def nazo01(self, lon='139.777254', lat='35.713768', kyori='1000.0'):
        pg = self.pg
        #ST_Distance('SRID=4612;POINT({0} {1})', geom) as dist
        a="""
        SELECT
            chome,
            ST_AsText(geom),
            ST_Distance(
                ST_GeomFromText('POINT({0} {1})', 4612)::GEOGRAPHY,
                geom
                ) as dist,
            uriage::Integer as uriage
        FROM tokyo_syogyo
        WHERE ST_DWithin(geom, ST_GeomFromText('POINT({0} {1})', 4612)::GEOGRAPHY, {2})
        ORDER BY dist;
        """.format(lon, lat, kyori).replace("\n        ", '\n')
        pg.execute(a)
        xx = []
        uriage = 0
        for x in pg:
            print(x)
            xx.append(round(x[2]))
            uriage = uriage + x[3]
        print(xx, uriage)
        

if __name__ == '__main__':
    pg = pg(dbname='gistest')
    pg.chk_srid()
    lon, lat = [139.69861500000002,35.68843]
    pg.nazo01(lon, lat, '1000')
