from connexion.apps.flask_app import FlaskJSONEncoder
from learner_inferences_server.models.base_model_ import Model
import six

class ServiceJSONEncoder(FlaskJSONEncoder):
    def __init__(self, include_nulls):
        self.include_nulls = include_nulls

    def default(self, o):
        if isinstance(o, Model):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
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


