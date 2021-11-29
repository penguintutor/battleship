import pygame.joystick

class Controller:

    def __init__ (self):
        # Initialize the joysticks.
        pygame.joystick.init()
        # does not save any values - recalculate each time
        
    # returns list of all joysticks as a list of dict
    # each entry in list has jid (joystick number) name and gid
    def get_controllers (self):
        joystick_count = pygame.joystick.get_count()
        joystick_list = []
        
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            
            joystick_info = {}
            
            try:
                jid = joystick.get_instance_id()
                joystick_info['jid']=jid
            except AttributeError:
                # get_instance_id() is an SDL2 method
                jid = joystick.get_id()
                joystick_info['jid']=jid
            
            try:
                guid = joystick.get_guid()
                joystick_info['guid']=guid
            except AttributeError:
                # get_guid() is an SDL2 method
                pass
            
            # get name of joystick
            try:
                name = joystick.get_name()
                joystick_info['name']=name
            except AttributeError:
                pass
            
            joystick_list.append(joystick_info)
        return joystick_list
        
        
        
    # Gets all axis for a specific joystick
    def get_axis (self, jid):
        pass
        
        
