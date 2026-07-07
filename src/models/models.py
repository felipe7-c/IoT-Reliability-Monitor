from pydantic import BaseModel

class IoTData(BaseModel):
    udi : int
    product_ID : str
    type : str
    air_temperature : float
    process_temperature : float
    rotational_speed : float
    torque : float
    tool_wear : int
    machine_failure : bool
    TWF : bool
    HDF : bool
    PWF : bool
    OSF : bool
    RNF : bool
