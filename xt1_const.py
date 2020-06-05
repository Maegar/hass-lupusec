import const as GENERAL

ACTION_SENSOR_LIST_GET = 'sensorListGet'
ACTION_PANEL_CONDITION_GET = 'panelCondGet'

MODES = {'ARM': GENERAL.Mode.ARM, 
         'HOME': GENERAL.Mode.HOME, 
         'DISARM': GENERAL.Mode.DISARM}

STATUS = {'': GENERAL.Status.CLOSED, 
          'Geschlossen': GENERAL.Status.CLOSED, 
          'Offen': GENERAL.Status.OPEN}

TYPES = {'Fensterkontakt': GENERAL.Device.TYPE_WINDOW_SENSOR,
         'Türkontakt': GENERAL.Device.TYPE_DOOR_SENSOR,
         'Keypad': GENERAL.Device.TYPE_KEY_PAD, 
         'Steckdose': GENERAL.Device.TYPE_POWER_SWITCH,
         'Bewegungsmelder': GENERAL.Device.TYPE_MOTION_DETECTOR, 
         'Rauchmelder': GENERAL.Device.TYPE_SMOKE_DETECOR, 
         'Wassermelder': GENERAL.Device.TYPE_WATER_DETECTOR}
