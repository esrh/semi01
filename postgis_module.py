import configparser
import psycopg2,psycopg2.extras
import os,os.path

class pg:
    def __init__(self, dbname='postgis_24_sample'):
        inifile = os.path.expanduser('~') + r'/important/password/postgres.ini'
        print("setting information:    {}\ndbname:    {}".format(inifile, dbname))
        conf = configparser.SafeConfigParser()
        conf.read(inifile)
        host = conf.get('postgres', 'host')
        port = conf.get('postgres', 'port')
        user = conf.get('postgres', 'user')
        password = conf.get('postgres', 'password')
        self.connection = psycopg2.connect("host={} port={} dbname={} user={} password={}".format(host,port,dbname,user,password))
        #dbnameは任意に設定して下さい。ここではPostGISをインストールしたときに生成されたものにしています。
        self.pg = self.connection.cursor()
        self.connection.autocommit = True
    
    def version(self):
        pg = self.pg
        pg.execute("select version()")
        for x in pg:
            print(x)
              
    def sql(self,str):
        self.pg.execute(str)
        return self.pg
        
    def geodistance(self, lon1, lat1, lon2, lat2):#keido,ido
        lon1, lat1, lon2, lat2 = float(lon1), float(lat1), float(lon2), float(lat2)
        sql = "SELECT ST_Distance(" + \
        "ST_GeographyFromText('POINT({} {})'),".format(lon1,lat1) + \
        "ST_GeographyFromText('POINT({} {})')".format(lon2,lat2) + \
        ");"
        print(sql)
        for x in self.sql(sql):
            for xx in x:
                print(xx)
                return xx
        

if __name__ == '__main__':
    p = pg(dbname='gistest')
    p.version()
    p.geodistance(0.0, 0.0, 180.0, 0.0)
    p.pg.close()
    p.connection.close()    
    
