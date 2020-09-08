from drone_state import State
from mavsdk import System
from mavsdk.camera import (CameraError, Mode)
import asyncio

class Init(State): 
    # Turn power on, turn telemetry on 
    async def power_up(self): 
        drone = System()
        await drone.connect(system_address="udp://:14540") # Connects to FCPU (Raspberry Pi)
        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered with UUID {state.uuid}")
                break

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

    # Set camera #1/2 (peripheral) to video recording mode, camera #3/4 (front) to photo mode.
    # Video frame breakdown from cameras 1/2 (with OpenCV) will be used as data augmentation images for
    # the object detection neural net. 
    async def camera_config(self):
        for i in range(2): # "drones.connections.cameras" is not defined yet, simply represents the collection of cameras hooked up to rPi
            try:
                camera = drone.connections.camera[i]
                await drone.camera.set_mode(Mode.VIDEO)
            except CameraError as error:
                print(f"Failed to configure camera {} for video with error code: {error._result.result}".format(i))

        for i in range(3, 5):
            try:
                camera = drone.connections.camera[i]
                await drone.camera.set_mode(Mode.PHOTO)
            except CameraError as error:
                print(f"Failed to configure camera {} for photo with error code: {error._result.result}".format(i))

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
    # Calibrate all components 
    async def calibrate(self):

        print("-- Starting gyroscope calibration")
        async for progress_data in drone.calibration.calibrate_gyro():
            print(progress_data)
        print("-- Gyroscope calibration finished")

        print("-- Starting accelerometer calibration")
        async for progress_data in drone.calibration.calibrate_accelerometer():
            print(progress_data)
        print("-- Accelerometer calibration finished")

        print("-- Starting magnetometer calibration")
        async for progress_data in drone.calibration.calibrate_magnetometer():
            print(progress_data)
        print("-- Magnetometer calibration finished")

        print("-- Starting board level horizon calibration")
        async for progress_data in drone.calibration.calibrate_level_horizon():
            print(progress_data)
        print("-- Board level calibration finished")
    
    # Stress test sensitive components to catch potential issues 
    async def test_components(self):
        return self

    # Switch-wait:
    def on_event(self, drone):
        if drone.target_state == 'safe':
            return Safe()
        elif drone.target_state == 'manual':
            return Manual()
        elif drone.target_state == 'low_power':
            return LowPower()
        elif drone.target_state == 'idle':
            return Idle() 
        elif drone.target_state == 'arm':
            return Arm()

class Arm(State):

    # Load mission plan manually 
    def Mission_set(self):
        mission_items = []
        mission_items.append(MissionItem(34.05221010100,
                                     118.24371010100,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))
        mission_items.append(MissionItem(34.05221010150,
                                     118.24371010150,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))
        mission_items.append(MissionItem(34.05221020000,
                                     118.24371010090,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))

        mission_plan = MissionPlan(mission_items)
        
        await drone.mission.set_return_to_launch_after_mission(True)

        print("-- Uploading mission")
        await drone.mission.upload_mission(mission_plan)

    # Load .seq or .txt file containing mission data (lat/long, etc), parses it down into MavSDK friendly format 
    def Mission_parse(self):
        return self 

    def arm(self):
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
    
    # Start recording video (or snapping pics at short, regular intervals, whichever one is better)
    async def video(self):
        return self

    def on_event(self, drone):
        return self 
        

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