class RunnerGenerator:

  def generate(self, configs, aggregate=False):
    if system_name == "apple_ii":
      from .apple_ii import AppleII
      system_using = AppleII()
    else:
      raise Exception("Unknown system type...")
    return system_using.register_systems(aggregate)

