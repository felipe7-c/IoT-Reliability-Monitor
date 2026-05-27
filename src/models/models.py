from pydantic import BaseModel

class IoTData(BaseModel):
    log_id : int
    farm_id : int
    farm_region : str
    sensor_id : int
    device_type : str
    failure_category: str
    failure_timestamp : str 
    downtime_hours : float
    resolution_action : str
    temperature_celsius : float
    humidity_percent : float
    weather_condition : str
    soil_moisture_percent : float
    maintenance_team : str
    resolved : bool
    estimated_loss_usd : float
