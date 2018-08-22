from connexion.apps.flask_app import FlaskJSONEncoder
from swagger_server.models.base_model_ import Model
import six

class ServiceJSONEncoder(FlaskJSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None:
                    continue
                if isinstance(value, Model):
                    value = self.default(value)
                elif isinstance(value, list):
                    for i in range(len(value)):
                        if isinstance(value[i], Model):
                            value[i] = self.default(value[i])
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return FlaskJSONEncoder.default(self, o)


