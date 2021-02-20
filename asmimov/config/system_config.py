from os.path import sep as path_sep, expanduser, exists
import json

class SystemConfig:

  def __init__(self):
    self.using_user_config = False
    config_dir = "." + path_sep + "config_files"
    self.base_config_dir = config_dir = "." + path_sep + "config_files"

    homedir = expanduser("~")
    user_config_dir = homedir + path_sep + ".asmimov"

    if exists(user_config_dir):
      self.config_dir = user_config_dir
      self.using_user_config = True
    else:
      self.config_dir = self.base_config_dir

    main_config_file = self.config_dir + path_sep + "system_config.json"
    main_config = json.loads(main_config_file)

    self.machine = main_config["machine"]
    self.mode = main_config["mode"]
    machine_config = self._process_machine_config()
    self.cpu = machine_config["cpu"]
    self.systems = machine_config["systems"]

  def _get_machine_config_filename(self, config_dir):
    return config_dir + path_sep + self.machine + "_config.json"

  def _process_machine_config(self):
    machine_config_file = self.get_machine_config_filename(self.config_dir)
    if not exists(machine_config_file) and self.using_user_config:
      machine_config_file = self.get_machine_config_filename(self.base_config_dir)
    return json.loads(machine_config_file)







