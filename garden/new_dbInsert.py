import mysql
import mysql.connector

def mariadbInsert(airResults, soilResults, lightResults):
    
    #global Host
    #global SQLUser
    #global SQLPw
    #global CoolingOn
    
    Host = 'localhost'
    SQLUser = 'lakehal'
    SQLPw = 'imagod'
   
    db = mysql.connector.connect(
      host=Host,
      user=SQLUser,
      password=SQLPw,
      database="Sensorenmesswerte")
    cursor = db.cursor()
    sql = ("INSERT INTO messwert (lux, air_temp, air_hum, pressure, gas_resist, soil_temp, soil_hum, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")
    values = (lightResults['lux'], airResults['air_temp'], airResults['air_hum'], airResults['pressure'], airResults['gas_resist'], soilResults['soil_temp'], soilResults['soil_hum'])
   
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    
    
    # soll jede 15 min wiederholt werden
def main():
    # call start_measures from messwert_lesen.py 
    results = []
    mariadbInsert(results['airResults'],results['soilResults'],results['lightResults'])
    print('geschaft')
  
if __name__ == "__main__":
    main()
