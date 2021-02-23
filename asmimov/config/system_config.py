from os.path import sep as path_sep, expanduser, exists
import json, pathlib

class SystemConfig:

  def __init__(self):
    self.using_user_config = False
    config_dir = path_sep + "config_files"
    self.abspath = str(pathlib.Path(__file__).parent.absolute())
    self.base_config_dir = self.abspath + path_sep + config_dir

    homedir = expanduser("~")
    user_config_dir = homedir + path_sep + ".asmimov"

    if exists(user_config_dir):
      self.config_dir = user_config_dir
      self.using_user_config = True
    else:
      self.config_dir = self.base_config_dir

    
    main_config_file = self.config_dir + path_sep + "system_config.json"
    print("LOADING MAIN CONFIG FILE " + main_config_file)
    with open(main_config_file, 'r') as mcf:
      main_config = json.load(mcf)

    self.machine = main_config["machine"]
    self.mode = main_config["mode"]
    self.aggregate = main_config["aggregate"]
    machine_config = self._process_machine_config()
    self.cpu = machine_config["cpu"]
    self.systems = machine_config["systems"]

  def _get_machine_config_filename(self, config_dir):
    return config_dir + path_sep + self.machine + "_config.json"

  def _process_machine_config(self):
    machine_config_file = self._get_machine_config_filename(self.config_dir)
    print("LOADING MACHINE CONFIG FILE " + machine_config_file)
    if not exists(machine_config_file) and self.using_user_config:
      machine_config_file = self._get_machine_config_filename(self.base_config_dir)
    with open(machine_config_file, 'r') as mcf:
      return json.load(mcf)







