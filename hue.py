import requests
import json


class HueException(Exception):
    pass


class Hue(object):
    def __init__(self, **kwargs):
        self.url = kwargs.pop('url', None)
        self.api_key = kwargs.pop('api_key', None)

    def process_errors(self, resp):
        errors = [m['error']['description'] for m in resp if 'error' in m]
        if errors:
            raise HueException("\n".join(errors))

    def get_light_id(self, **kwargs):
        light_found = False
        light_name = kwargs.pop('light_name', None)
        url = "%s/api/%s/lights" % (self.url, self.api_key)
        r = requests.get(url)
        if r.status_code != 200:
            raise HueException(
                "Recieved %s status code from url %s ") % (r.status_code, url)
        self.process_errors(json.loads(r.text))
        lights = json.loads(r.text)
        for light in lights:
            name = lights[light].get('name')
            if name == light_name:
                light_found = True
                return light
        if not light_found:
            raise HueException('light not found')

    def change_state(self, **kwargs):
        light_id = kwargs.pop('light_id', None)
        on = kwargs.pop('on', False)
        url = "%s/api/%s/lights/%s/state" % (self.url, self.api_key, light_id)
        payload = {"on": on}
        r = requests.put(url, data=json.dumps(payload))
        if r.status_code != 200:
            raise HueException(
                "Recieved %s status code from url %s ") % (r.status_code, url)
        self.process_errors(json.loads(r.text))
        success = [s['success'] for s in json.loads(r.text) if 'success' in s]
        return success

    def off(self, **kwargs):
        light_id = kwargs.pop('light_id', None)
        if not light_id:
            light_name = kwargs.pop('light_name', None)
            light_id = self.get_light_id(light_name=light_name)
        self.change_state(on=False, light_id=light_id)

    def on(self, **kwargs):
        light_id = kwargs.pop('light_id', None)
        if not light_id:
            light_name = kwargs.pop('light_name', None)
            light_id = self.get_light_id(light_name=light_name)
        self.change_state(on=True, light_id=light_id)
