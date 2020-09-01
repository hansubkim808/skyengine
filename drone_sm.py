from drone_state import State

class Init(State): 
    # Turn power on, turn telemetry on 
    def power_up(self): 
        return self 

    # Controller 
    def on_event(self, drone):
        if drone.target_state == 'idle':
            return Idle()
        elif drone.target_state == 'self_test':
            return Self_Test()
        elif drone.target_state == 'low_power':
            return LowPower()
        elif drone.target_state == 'safe':
            return Safe()
        elif drone.target_state == 'manual':
            return Manual()
        
        return self


class Idle(State):
    # Command setpoints for telemetry and power supply 
    def cmd_setpoints(self):
        return self 

    # Controller 
    def on_event(self, drone):
        if drone.target_state == 'self_test':
            return Self_Test()
        elif drone.target_state == 'low_power':
            return LowPower()
        elif drone.target_state == 'safe':
            return Safe()
        elif drone.target_state == 'manual':
            return Manual()

        return self 


class Safe(State):
    # Command everything off except telemetry logger 
    def safe_power(self):
        return self 
    
    # Controller 
    def on_event(self, drone):
        if drone.target_state == 'idle':
            return Idle()
        elif drone.target_state == 'low_power':
            return LowPower()
        elif drone.target_state == 'safe':
            return Safe()
        elif drone.target_state == 'manual':
            return Manual()
        elif drone.target_state == 'self_test':
            return Self_Test()


class LowPower(State):
    # If vehicle is in the air, reduce power and land. 
    def low_power_landing(self):
        return self 
    # If vehicle is on the ground, turn of all power except telemetry logger 
    def low_power_shutdown(self):
        return self 

    # Controller 
    def on_event(self, drone):
        if drone.target_state == 'idle':
            return Idle()
        elif drone.target_state == 'safe':
            return Safe()
        elif drone.target_state == 'manual':
            return Manual()


class Manual(State): 
    # Release all telemetry to RC controller 
    def manual_release(self):
        return self
    
    def on_event(self, drone):
        return self 

class Self_Test(State):
    # Start commanding current + voltage to different components, test that they work 
    def e_test(self):
        return self

    # Test propellers, ESCs, brushless motors, at different speeds and power
    def m_test(self):
        return self 
    
    def on_event(self, drone):
        if drone.target_state == 'safe':
            return Safe()
        elif drone.target_state == 'manual':
            return Manual()
        elif drone.target_state == 'low_power':
            return LowPower()
        elif drone.target_state == 'idle':
            return Idle() 
        elif drone.target_state == 'fly':
            return Fly()

class Fly(State):
    # Start vertical takeoff (move straight up before activating PID control at a certain height)
    def VTO(self):
        return self 

    # If sensors indicate blockage, active PID control immediately 
    def XTO(self):
        return self 

    def on_event(self, drone):
        

# Finite State Machine for simulated drone actions. 

# Init 

# Safe 

# Self_test 

# Fly (VTOL + Fly)

# FDIR (degraded hardware component) 

# Safe 

# Landing 

# Engine_shutdown

# Off 