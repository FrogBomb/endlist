import StringIO
import cloud

class FullPickler:
    @staticmethod
    def dump(value):
        f = StringIO.StringIO()
        pickler = cloud.serialization.cloudpickle.CloudPickler(f)
        pickler.dump(value)
        buf = f.getvalue()
        f.close()
        return buf

    @staticmethod
    def load(buf):
        f = StringIO.StringIO(buf)
        value = pickle.load(f)
        f.close()
        return value
