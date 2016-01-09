# hue
python module for interacting with the phillips hue lighting system

# Usage

```python
from hue import Hue

url = 'http://1.2.3.4' # IP address of your HUE base station
api_key = '82022f5631d9435084b0417ead31412a' # user key obtained after registering (http://www.developers.meethue.com/documentation/getting-started)

# create Hue object
h = Hue(url=url, api_key=api_key)

# turn light off/on by name
h.off(light_name='Living room 1')
h.on(light_name='Living room 1')

# turn light off/on by id 
h.off(light_id=1)
h.on(light_id=1)

# get a lights id
h.get_light_id(light_name='Living room 1')

```
