def format_float(float):
    return f"{float:.2f}"
    
def print_results(m):
    print()
    print("Results")
    
    print('\n\n ------------- Final Bank   ---------')
    print('CO2 temp in = ',
          format_float(value(m.fs.FBNK.control_volume.properties_in[0].temperature)), 'K')
    print('CO2 temp out = ',
          format_float(value(m.fs.FBNK.control_volume.properties_out[0].temperature)), 'K')   
    print('CO2 pressure in = ',
          format_float(value(m.fs.FBNK.control_volume.properties_in[0].pressure / 1e6)), 'MPa')
    print('CO2 pressure out = ',
          format_float(value(m.fs.FBNK.control_volume.properties_out[0].pressure / 1e6)), 'MPa')
    print('Enthalpy in = ', 
          format_float(value(m.fs.FBNK.control_volume.properties_in[0].enth_mol)), 'J / mol ?')
    print('Heat Duty =format_float ',
          format_float(value(m.fs.FBNK.heat_duty[0] / 1e6)), 'MW')
    
    print('\n\n ------------- Boiler Water Wall ---------')
    print('CO2 temp in = ',
          format_float(value(m.fs.WW.control_volume.properties_in[0].temperature)), 'K')
    print('CO2 temp out = ',
          format_float(value(m.fs.WW.control_volume.properties_out[0].temperature)), 'K')   
    print('CO2 pressure in = ',
          format_float(value(m.fs.WW.control_volume.properties_in[0].pressure / 1e6)), 'MPa')
    print('CO2 pressure out = ',
          format_float(value(m.fs.WW.control_volume.properties_out[0].pressure / 1e6)), 'MPa')
    print('Enthalpy in = ', 
          format_float(value(m.fs.WW.control_volume.properties_in[0].enth_mol)), 'J / mol ?')
    print('Heat Duty = ',
          format_float(value(m.fs.WW.heat_duty[0] / 1e6)), 'MW')
    
    print('\n\n ------------- Second Internal Bank ---------')
    print('CO2 temp in = ',
          format_float(value(m.fs.SIBNK.control_volume.properties_in[0].temperature)), 'K')
    print('CO2 temp out = ',
          format_float(value(m.fs.SIBNK.control_volume.properties_out[0].temperature)), 'K')   
    print('CO2 pressure in = ',
          format_float(value(m.fs.SIBNK.control_volume.properties_in[0].pressure / 1e6)), 'MPa')
    print('CO2 pressure out = ',
          format_float(value(m.fs.SIBNK.control_volume.properties_out[0].pressure / 1e6)), 'MPa')
    print('Enthalpy format_float = ', 
          format_float(value(m.fs.SIBNK.control_volume.properties_in[0].enth_mol)), 'J / mol ?')
    print('Heat Duformat_floatty = ',
          format_float(value(m.fs.SIBNK.heat_duty[0] / 1e6)), 'MW')
    
    print('\n\n ------------- Pendant Bank ---------')
    print('CO2 temp in = ',
          format_float(value(m.fs.PBNK.control_volume.properties_in[0].temperature)), 'K')
    print('CO2 temp out = ',
          format_float(value(m.fs.PBNK.control_volume.properties_out[0].temperature)), 'K')   
    print('CO2 pressure in = ',
          format_float(value(m.fs.PBNK.control_volume.properties_in[0].pressure / 1e6)), 'MPa')
    print('CO2 pressure out = ',
          format_float(value(m.fs.PBNK.control_volume.properties_out[0].pressure / 1e6)), 'MPa')
    print('Enthalpy in = ', 
          format_float(value(m.fs.PBNK.control_volume.properties_in[0].enth_mol)), 'J / mol ?')
    print('Heat Duty = ',
          format_float(value(m.fs.PBNK.heat_duty[0] / 1e6)), 'MW')    
    
    print('\n\n ------------- First Internal Bank ---------')
    print('CO2 temp in = ',
          format_float(value(m.fs.FIBNK.control_volume.properties_in[0].temperature)), 'K')
    print('CO2 temp out = ',
          format_float(value(m.fs.FIBNK.control_volume.properties_out[0].temperature)), 'K')   
    print('CO2 pressure in = ',
          format_float(value(m.fs.FIBNK.control_volume.properties_in[0].pressure / 1e6)), 'MPa')
    print('CO2 pressure out = ',
          format_float(value(m.fs.FIBNK.control_volume.properties_out[0].pressure / 1e6)), 'MPa')
    print('Enthalpy in = ', 
          format_float(value(m.fs.FIBNK.control_volume.properties_in[0].enth_mol)), 'J / mol ?')
    print('Heat Duty = ',
          format_float(value(m.fs.FIBNK.heat_duty[0] / 1e6)), 'MW')    
