from postgis_module import pg
import nazo
import glob, time, csv

class pg(pg):
    def __init__(self, dbname='gistest'):
        super(pg, self).__init__(dbname=dbname)
        self.pg.execute("select version()")
        for x in self.pg:
            print(x)

    def chk_srid(self, tbname='tokyo_syogyo'):
        self.pg.execute('select ST_SRID(geom) from {} limit 1'.format(tbname))
        for x in self.pg:
            print(x)

    def dwithin(self, lon='139.777254', lat='35.713768', kyori='1000.0'):
        debug = False
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
        ls = []
        ls_kouri = []
        uriage = 0
        for x in pg:
            ls_kouri.append('{}:{}'.format(x[0], x[3]))
            if debug is True:
                print(x)
            ls.append(round(x[2]))
            try:
                uriage = uriage + x[3]
            except TypeError:
                pass
        if debug is True:
            print(ls, uriage)
        return uriage, ls_kouri

    def nazo01(self, ls=None, kyori=None):
        rl = []
        for x in ls:
            i, ls_kouri = self.dwithin(lon=x[1], lat=x[2], kyori=kyori)
            rl.append(x + [i] + ls_kouri)
        return rl

if __name__ == '__main__':
    nazo = nazo.nazo()
    pg = pg(dbname='gistest')
    pg.chk_srid()
    #lon, lat = [139.69861500000002,35.68843]
    rls = []
    for x in glob.glob('stationdata\\tokyo\\*.csv'):
        ls = nazo.rcsv(x)
        rl = pg.nazo01(ls, kyori=1000)
        print(x)
        rls = rls + rl
    nazo.wcsv('stadata_tokyo_003.csv', rls)
