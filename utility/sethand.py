# boop's amazing config loader thingy
# utilizes yaml, non-async.

import ruamel.yaml
import os # We need this to check for file existence

# Default configuration
_DEFAULT_CONFIGS = [
    {
        "varname" : "fps-limit",
        "default" : 120,
        "comment" : "This value should be pretty straight-forward unless you're a caveman. Setting to `null` = No limit."
    },

    {
        "varname" : "fps-display",
        "default" : False,
        "comment" : "Shows a little FPS counter at the top of the screen, in case you're into that, ironically it lowers fps slightly."
    },

    {
        'varname' : 'ram-display',
        'default' : False,
        'comment' : "Shows how many MB of ram the python process is using."
    },

    {
        'varname' : 'disabled-extensions',
        'default' : [
            "here is an extension i dont want",
            "this is another extension i dont want",
            "this extension breaks my game!!",
            "example 4!"
        ],
        'comment' : 'A list of all of the disabled extensions, not to be loaded on startup.'
    },

    {
        'varname' : 'console-debug-logs',
        'default' : False,
        'comment' : 'When the console is open, this will show verbose information logs, usually only for development.'
    }
]

def dict_defaults():
    # Simply returns defaults as if they were not formatted in such a weird way
    return {i['varname'] : i['default'] for i in _DEFAULT_CONFIGS}

class boopSettingStructure(object):
    def __init__(self, config, *args, **kwargs):
        self.defaults = kwargs.get('defaults', None)
        self.config = config

    def fetch(self, key : str):

        # Does the key exist?
        if key not in self.config:
            # Checks to see if defaults are enabled
            if self.defaults is None:
                raise KeyError("No setting key found, and defaults are none")
            
            # If defaults are enabled, check them
            if key not in self.defaults:
                raise KeyError("Invalid Setting Key")

            return self.defaults[key]
        
        return self.config[key]
        

def create_settings_file(comments : bool = True):
    """
    Creates a new settings config.

    `comments` : If true, will add useful tips for every config option
    """
    yaml = ruamel.yaml.YAML()
    data = ruamel.yaml.comments.CommentedMap() # Empty Data
    
    for index, config_option in enumerate(_DEFAULT_CONFIGS, start=0):
        data.insert(
            index,
            config_option['varname'],
            config_option['default'],
            comment = config_option['comment'] if comments else None
        )

    with open('./config.yml', 'w+') as ymlfile:
        yaml.indent( # QOL Indenting <3
            offset = 2,
            mapping = 2,
            sequence= 4
        )
        yaml.dump(
            data, ymlfile
        )
    
    return load_settings_file(create_if_not_exists=False, include_defaults=False)


def load_settings_file(include_defaults : bool = True, create_if_not_exists : bool = False):
    """
    Loads the settings file from the __main__'s directory

    `include_defaults` : If true, it'll load _DEFAULT_CONFIG's vars on top 
    of the user-set configuration.
    """

    yaml = ruamel.yaml.YAML()

    if not os.path.exists('./config.yml'):
        return create_settings_file(comments = True)
    
    with open('./config.yml', 'r') as cf:
        conf = yaml.load(cf)
    
    return boopSettingStructure(
        conf,
        dict_defaults()
    )