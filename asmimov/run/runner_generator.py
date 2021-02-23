class RunnerGenerator:

  def generate(self, config):
    if config.machine == "apple_ii":
      from .apple_ii import AppleII
      system_using = AppleII()
    else:
      raise Exception("Unknown system type " + config.machine + "... ")
    return system_using.register_systems(config)

