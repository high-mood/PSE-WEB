from app import app, db

from influxdb import InfluxDBClient
import influxdb
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

    def setUp(self):
        """Populate the influx database if set."""
        self.cli.create_database('songs')
        self.cli.switch_database('songs')

        if hasattr(self, 'populate_influx_with'):
            if isinstance(self.populate_influx_with, types.ModuleType):
                for var in dir(self.populate_influx_with):
                    if not var.startswith("__"):
                        self.populate(getattr(self.populate_influx_with, var))
            else:
                self.populate(self.populate_influx_with)

    def tearDown(self):
        """Drops the influx database and closes the connection."""
        self.cli.drop_database('test_db')
        app.config['INFLUX_HOST'] = self.default_influxDB_host

    def populate(self, points):
        """Populate the influx database with points."""
        self.cli.write_points(points)


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

    def setUp(self):
        """Populate the sql database if set."""
        if hasattr(self, 'populate_sql_with'):
            if isinstance(self.populate_sql_with, types.ModuleType):
                for var in dir(self.populate_sql_with):
                    if not var.startswith("__"):
                        self.populate(getattr(self.populate_sql_with, var))
            else:
                self.populate(self.populate_sql_with)

    @classmethod
    def tearDownClass(cls):
        """Remove and drop the sql database."""
        db.session.remove()

        app.config['SQLALCHEMY_DATABASE_URI'] = cls.default_sqlDB_uri

    def populate(self, *data):
        """Populate the sql database with data."""
        for item in data:
            db.session.add(item)
            db.session.commit()
