from abc import ABCMeta, abstractmethod

class Generic_Prog_Atten():

    __metaclass__ = ABCMeta  # Allows for abstract methods to be created.
    
    @abstractmethod
    def get_device_ID(self):
        pass

    @abstractmethod
    def set_global_attenuation(self, attenuation):
        pass

    @abstractmethod
    def get_global_attenuation(self):
        pass

    @abstractmethod
    def set_channel_attenuation(self, channel, attenuation):
        pass

    @abstractmethod
    def get_channel_attenuation(self, channel):
        pass
