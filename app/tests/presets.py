from app import app, db

from influxdb import InfluxDBClient
import types


class UseTestInfluxDB(object):
    default_influxDB_host = app.config['INFLUX_HOST']

    @classmethod
    def setUpClass(cls):
        """Sets up the influx InfluxDBClient and test database."""
        app.config['TESTING'] = True
        app.config['INFLUX_HOST'] = "localhost"

        cls.cli = InfluxDBClient(host=app.config['INFLUX_HOST'], port=app.config['INFLUX_PORT'],
                                 username=app.config['INFLUX_USER'], password=app.config['INFLUX_PASSWORD'])

        cls.cli.create_database('songs')
        cls.cli.switch_database('songs')

        if hasattr(cls, 'populate_influx_with'):
            if isinstance(cls.populate_influx_with, types.ModuleType):
                for var in dir(cls.populate_influx_with):
                    if not var.startswith("__"):
                        cls.cli.write_points(getattr(cls.populate_influx_with, var))
            else:
                cls.cli.write_points(cls.populate_influx_with)

    @classmethod
    def tearDownClass(cls):
        """Drops the influx database and closes the connection."""
        cls.cli.drop_database('test_db')
        app.config['INFLUX_HOST'] = cls.default_influxDB_host


class UseTestSqlDB(object):
    default_sqlDB_uri = app.config['SQLALCHEMY_DATABASE_URI']

    @classmethod
    def setUpClass(cls):
        """Create a new test sql database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['TESTING'] = True
        # Removes old session, if there was any.
        db.session.remove()
        db.create_all()

        if hasattr(cls, 'populate_sql_with'):
            if isinstance(cls.populate_sql_with, types.ModuleType):
                for var in dir(cls.populate_sql_with):
                    if not var.startswith("__"):
                        for item in getattr(cls.populate_sql_with, var):
                            db.session.add(item)
                            db.session.commit()
            else:
                for item in cls.populate_sql_with:
                    db.session.add(item)
                    db.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Remove and drop the sql database."""
        db.session.remove()

        app.config['SQLALCHEMY_DATABASE_URI'] = cls.default_sqlDB_uri
