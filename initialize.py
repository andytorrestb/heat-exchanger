import pyomo.environ as pe # Pyomo environment
from pyomo.environ import ConcreteModel, SolverFactory, value, \
    TransformationFactory, units as pyunits
from pyomo.network import Arc

from idaes.core import FlowsheetBlock, StateBlock
from idaes.core.util.model_statistics import degrees_of_freedom

from idaes.power_generation.unit_models.boiler_heat_exchanger import BoilerHeatExchanger, TubeArrangement, \
    DeltaTMethod
from idaes.generic_models.properties import swco2

from idaes.power_generation.properties import FlueGasParameterBlock

from pyomo.environ import units as pyunits

def initialize_FIBNK(m):
    # FIRST INTERNAL BANK
    
    hp_fibnk_in = swco2.htpx((572.7 + 273.15) * pyunits.K, 24.51e6 * pyunits.Pa)
    m.fs.FIBNK.side_1_inlet[:].enth_mol.fix(hp_fibnk_in)
    m.fs.FIBNK.side_1_inlet[:].pressure.fix(24.51e6)
    
    hp_fibnk_out = swco2.htpx((593.0 + 273.15) * pyunits.K, 24.28e6 * pyunits.Pa)
    m.fs.FIBNK.side_1_outlet[:].pressure.fix(24.28e6)
    m.fs.FIBNK.side_1_outlet[:].enth_mol.fix(hp_fibnk_out)
    
#     m.fs.FIBNK.side_1_outlet.flow_mol[0].fix(1074792.897)
        
    # m_dot_fg = 96.7 kg /s ~= 5089 mol / s
    FGrate = 5089  # mol/s
    # Use FG molar composition to set component flow rates (baseline report)
    m.fs.FIBNK.side_2_inlet.flow_mol_comp[0, "H2O"].fix(FGrate*8.69/100)
    m.fs.FIBNK.side_2_inlet.flow_mol_comp[0, "CO2"].fix(FGrate*14.49/100)
    m.fs.FIBNK.side_2_inlet.flow_mol_comp[0, "N2"].fix(FGrate*74.34/100)
    m.fs.FIBNK.side_2_inlet.flow_mol_comp[0, "O2"].fix(FGrate*2.47/100)
    m.fs.FIBNK.side_2_inlet.flow_mol_comp[0, "NO"].fix(FGrate*0.0006)
    m.fs.FIBNK.side_2_inlet.flow_mol_comp[0, "SO2"].fix(FGrate*0.002)
    m.fs.FIBNK.side_2_inlet.pressure[0].fix(100145)
    
    m.fs.FIBNK.side_2_inlet.temperature[0].fix(823.4 + 273.15)

    # FIBNKomizer design variables and parameters
    ITM = 0.0254  # inch to meter conversion
    # Based on NETL Baseline Report Rev3
    m.fs.FIBNK.tube_di.fix((2-2*0.188)*ITM)  # calc inner diameter
    #                                   (2 = outer diameter, thickness = 0.188)
#     m.fs.FIBNK.tube_thickness.fix(0.188*ITM)  # tube thickness
    m.fs.FIBNK.pitch_x.fix(3.5*ITM)
    # pitch_y = (54.5) gas path transverse width /columns
    m.fs.FIBNK.pitch_y.fix(6.03*ITM)
    m.fs.FIBNK.tube_length.fix(103.41*12*ITM)  # use tube length (53.41 ft)
    m.fs.FIBNK.tube_nrow.fix(4*2)
    m.fs.FIBNK.tube_ncol.fix(70)
    m.fs.FIBNK.nrow_inlet.fix(2)
    m.fs.FIBNK.delta_elevation.fix(50)
    # parameters
    # heat transfer resistance due to tube side fouling (water scales)
    m.fs.FIBNK.tube_r_fouling = 0.000176
    # heat transfer resistance due to tube shell fouling (ash deposition)
    m.fs.FIBNK.shell_r_fouling = 0.00088
    
    if m.fs.FIBNK.config.has_radiation is True:
        m.fs.FIBNK.emissivity_wall.fix(0.7)  # wall emissivity
    # correction factor for overall heat transfer coefficient
    m.fs.FIBNK.fcorrection_htc.fix(1.5)
    # correction factor for pressure drop calc tube side
    m.fs.FIBNK.fcorrection_dp_tube.fix(1.0)
    # correction factor for pressure drop calc shell side
    m.fs.FIBNK.fcorrection_dp_shell.fix(1.0)

def initialize_PBNK(m):
    # PENDANT BANK
    hp_PBNK_in = swco2.htpx((531.6 + 273.15) * pyunits.K, 25.09e6 * pyunits.Pa)
    m.fs.PBNK.side_1_inlet[:].enth_mol.fix(hp_PBNK_in)
    m.fs.PBNK.side_1_inlet[:].pressure.fix(25.09e6)
    
    hp_PBNK_out = swco2.htpx((572.7 + 273.15) * pyunits.K, 24.55e6 * pyunits.Pa)
    m.fs.PBNK.side_1_outlet[:].enth_mol.fix(hp_PBNK_out)
    m.fs.PBNK.side_1_outlet[:].pressure.fix(24.28e6)

    
#     m.fs.PBNK.side_1_outlet.flow_mol[0].fix(1074792.897)
        
    # m_dot_fg = 96.7 kg /s ~= 5089 mol / s
    FGrate = 5089  # mol/s
    # Use FG molar composition to set component flow rates (baseline report)
#     m.fs.PBNK.side_2_inlet.flow_mol_comp[0, "H2O"].fix(FGrate*8.69/100)
#     m.fs.PBNK.side_2_inlet.flow_mol_comp[0, "CO2"].fix(FGrate*14.49/100)
#     m.fs.PBNK.side_2_inlet.flow_mol_comp[0, "N2"].fix(FGrate*74.34/100)
#     m.fs.PBNK.side_2_inlet.flow_mol_comp[0, "O2"].fix(FGrate*2.47/100)
#     m.fs.PBNK.side_2_inlet.flow_mol_comp[0, "NO"].fix(FGrate*0.0006)
#     m.fs.PBNK.side_2_inlet.flow_mol_comp[0, "SO2"].fix(FGrate*0.002)
#     m.fs.PBNK.side_2_inlet.pressure[0].fix(100145)
    
#     m.fs.PBNK.side_2_inlet.temperature[0].fix(823.4 + 273.15)

    # PBNKomizer design variables and parameters
    ITM = 0.0254  # inch to meter conversion
    # Based on NETL Baseline Report Rev3
    m.fs.PBNK.tube_di.fix((2-2*0.188)*ITM)  # calc inner diameter
    #                                   (2 = outer diameter, thickness = 0.188)
#     m.fs.PBNK.tube_thickness.fix(0.188*ITM)  # tube thickness
    m.fs.PBNK.pitch_x.fix(3.5*ITM)
    # pitch_y = (54.5) gas path transverse width /columns
    m.fs.PBNK.pitch_y.fix(6.03*ITM)
    m.fs.PBNK.tube_length.fix(103.41*12*ITM)  # use tube length (53.41 ft)
#     m.fs.PBNK.tube_nrow.fix(4*2)         # use to match baseline performance
#     m.fs.PBNK.tube_ncol.fix(70)            # 130 from NETL
#     m.fs.PBNK.nrow_inlet.fix(2)
    m.fs.PBNK.delta_elevation.fix(50)
    # parameters
    # heat transfer resistance due to tube side fouling (water scales)
    m.fs.PBNK.tube_r_fouling = 0.000176
    # heat transfer resistance due to tube shell fouling (ash deposition)
    m.fs.PBNK.shell_r_fouling = 0.00088
    
    if m.fs.PBNK.config.has_radiation is True:
        m.fs.PBNK.emissivity_wall.fix(0.7)  # wall emissivity
    # correction factor for overall heat transfer coefficient
    m.fs.PBNK.fcorrection_htc.fix(1.5)
    # correction factor for pressure drop calc tube side
    m.fs.PBNK.fcorrection_dp_tube.fix(1.0)
    # correction factor for pressure drop calc shell side
    m.fs.PBNK.fcorrection_dp_shell.fix(1.0)

    
def initialize_SIBNK(m):
    # Second I BANK
    hp_SIBNK_in = swco2.htpx((520.8 + 273.15) * pyunits.K, 25.33e6 * pyunits.Pa)
    m.fs.SIBNK.side_1_inlet[:].enth_mol.fix(hp_SIBNK_in)
    m.fs.SIBNK.side_1_inlet[:].pressure.fix(25.33e6)
    
    hp_SIBNK_out = swco2.htpx((531.6 + 273.15) * pyunits.K, 25.12e6 * pyunits.Pa)
    m.fs.SIBNK.side_1_outlet[:].pressure.fix(25.12e6)
    m.fs.SIBNK.side_1_outlet[:].enth_mol.fix(hp_SIBNK_out)
    
#     m.fs.SIBNK.side_1_outlet.flow_mol[0].fix(1074792.897)

    # m_dot_fg = 96.7 kg /s ~= 5089 mol / s
    FGrate = 5089  # mol/s
    # Use FG molar composition to set component flow rates (baseline report)
    m.fs.SIBNK.side_2_inlet.flow_mol_comp[0, "H2O"].fix(FGrate*8.69/100)
    m.fs.SIBNK.side_2_inlet.flow_mol_comp[0, "CO2"].fix(FGrate*14.49/100)
    m.fs.SIBNK.side_2_inlet.flow_mol_comp[0, "N2"].fix(FGrate*74.34/100)
    m.fs.SIBNK.side_2_inlet.flow_mol_comp[0, "O2"].fix(FGrate*2.47/100)
    m.fs.SIBNK.side_2_inlet.flow_mol_comp[0, "NO"].fix(FGrate*0.0006)
    m.fs.SIBNK.side_2_inlet.flow_mol_comp[0, "SO2"].fix(FGrate*0.002)
    m.fs.SIBNK.side_2_inlet.pressure[0].fix(100145)
    
    m.fs.SIBNK.side_2_inlet.temperature[0].fix(823.4 + 273.15)

    # SIBNKomizer design variables and parameters
    ITM = 0.0254  # inch to meter conversion
    # Based on NETL Baseline Report Rev3
    m.fs.SIBNK.tube_di.fix((2-2*0.188)*ITM)  # calc inner diameter
    #                                   (2 = outer diameter, thickness = 0.188)
#     m.fs.SIBNK.tube_thickness.fix(0.188*ITM)  # tube thickness
    m.fs.SIBNK.pitch_x.fix(3.5*ITM)
    # pitch_y = (54.5) gas path transverse width /columns
    m.fs.SIBNK.pitch_y.fix(6.03*ITM)
#     m.fs.SIBNK.tube_length.fix(103.41*12*ITM)  # use tube length (53.41 ft)
#     m.fs.SIBNK.tube_nrow.fix(4*2)         # use to match baseline performance
#     m.fs.SIBNK.tube_ncol.fix(70)            # 130 from NETL
    m.fs.SIBNK.nrow_inlet.fix(2)
    m.fs.SIBNK.delta_elevation.fix(50)
    # parameters
    # heat transfer resistance due to tube side fouling (water scales)
    m.fs.SIBNK.tube_r_fouling = 0.000176
    # heat transfer resistance due to tube shell fouling (ash deposition)
    m.fs.SIBNK.shell_r_fouling = 0.00088
    
    if m.fs.SIBNK.config.has_radiation is True:
        m.fs.SIBNK.emissivity_wall.fix(0.7)  # wall emissivity
    # correction factor for overall heat transfer coefficient
    m.fs.SIBNK.fcorrection_htc.fix(1.5)
    # correction factor for pressure drop calc tube side
    m.fs.SIBNK.fcorrection_dp_tube.fix(1.0)
    # correction factor for pressure drop calc shell side
    m.fs.SIBNK.fcorrection_dp_shell.fix(1.0)

def initialize_WW(m):
    # Second Internal Bank
    hp_WW_in = swco2.htpx((416.8 + 273.15) * pyunits.K, 25.91e6 * pyunits.Pa)
    m.fs.WW.side_1_inlet[:].pressure.fix(25.91e6)
    m.fs.WW.side_1_inlet[:].enth_mol.fix(hp_WW_in)
    
    hp_WW_out = swco2.htpx((520.8 + 273.15) * pyunits.K, 25.39e6 * pyunits.Pa)
    m.fs.WW.side_1_outlet[:].pressure.fix(25.39e6)
    m.fs.WW.side_1_outlet[:].enth_mol.fix(hp_WW_out)
    
#     m.fs.WW.side_1_outlet.flow_mol[0].fix(1074792.897)
        
    # m_dot_fg = 96.7 kg /s ~= 5089 mol / s
    FGrate = 5089  # mol/s
    # Use FG molar composition to set component flow rates (baseline report)
#     m.fs.WW.side_2_inlet.flow_mol_comp[0, "H2O"].fix(FGrate*8.69/100)
#     m.fs.WW.side_2_inlet.flow_mol_comp[0, "CO2"].fix(FGrate*14.49/100)
#     m.fs.WW.side_2_inlet.flow_mol_comp[0, "N2"].fix(FGrate*74.34/100)
#     m.fs.WW.side_2_inlet.flow_mol_comp[0, "O2"].fix(FGrate*2.47/100)
#     m.fs.WW.side_2_inlet.flow_mol_comp[0, "NO"].fix(FGrate*0.0006)
#     m.fs.WW.side_2_inlet.flow_mol_comp[0, "SO2"].fix(FGrate*0.002)
#     m.fs.WW.side_2_inlet.pressure[0].fix(100145)
    
#     m.fs.WW.side_2_inlet.temperature[0].fix(823.4 + 273.15)

    # WWomizer design variables and parameters
    ITM = 0.0254  # inch to meter conversion
    # Based on NETL Baseline Report Rev3
    m.fs.WW.tube_di.fix((2-2*0.188)*ITM)  # calc inner diameter
    #                                   (2 = outer diameter, thickness = 0.188)
#     m.fs.WW.tube_thickness.fix(0.188*ITM)  # tube thickness
    m.fs.WW.pitch_x.fix(3.5*ITM)
    # pitch_y = (54.5) gas path transverse width /columns
    m.fs.WW.pitch_y.fix(6.03*ITM)
#     m.fs.WW.tube_length.fix(103.41*12*ITM)  # use tube length (53.41 ft)
#     m.fs.WW.tube_nrow.fix(4*2)         # use to match baseline performance
#     m.fs.WW.tube_ncol.fix(70)            # 130 from NETL
    m.fs.WW.nrow_inlet.fix(2)
    m.fs.WW.delta_elevation.fix(50)
    # parameters
    # heat transfer resistance due to tube side fouling (water scales)
    m.fs.WW.tube_r_fouling = 0.000176
    # heat transfer resistance due to tube shell fouling (ash deposition)
    m.fs.WW.shell_r_fouling = 0.00088
    
    if m.fs.WW.config.has_radiation is True:
        m.fs.WW.emissivity_wall.fix(0.7)  # wall emissivity
    # correction factor for overall heat transfer coefficient
    m.fs.WW.fcorrection_htc.fix(1.5)
    # correction factor for pressure drop calc tube side
    m.fs.WW.fcorrection_dp_tube.fix(1.0)
    # correction factor for pressure drop calc shell side
    m.fs.WW.fcorrection_dp_shell.fix(1.0)

def initialize_FBNK(m):
    # FINAL BANK
    
    # m_dot_co2 = 863 kg / s ~= 19609 mol / s 
    m.fs.FBNK.side_1_inlet.flow_mol[0].fix(19609.18)
    
    
    hp_FBNK_in = swco2.htpx((572.7 + 273.15) * pyunits.K, 24.51e6 * pyunits.Pa)
    m.fs.FBNK.side_1_inlet[:].enth_mol.fix(hp_FBNK_in)
    m.fs.FBNK.side_1_inlet[:].pressure.fix(24.51e6)
    
    hp_FBNK_out = swco2.htpx((593.0 + 273.15) * pyunits.K, 24.28e6 * pyunits.Pa)
    m.fs.FBNK.side_1_outlet[:].pressure.fix(24.28e6)
    m.fs.FBNK.side_1_outlet[:].enth_mol.fix(hp_FBNK_out)
    
#     m.fs.FBNK.side_1_outlet.flow_mol[0].fix(1074792.897)
        
    # m_dot_fg = 96.7 kg /s ~= 5089 mol / s
    FGrate = 5089  # mol/s
    # Use FG molar composition to set component flow rates (baseline report)
#     m.fs.FBNK.side_2_inlet.flow_mol_comp[0, "H2O"].fix(FGrate*8.69/100)
#     m.fs.FBNK.side_2_inlet.flow_mol_comp[0, "CO2"].fix(FGrate*14.49/100)
#     m.fs.FBNK.side_2_inlet.flow_mol_comp[0, "N2"].fix(FGrate*74.34/100)
#     m.fs.FBNK.side_2_inlet.flow_mol_comp[0, "O2"].fix(FGrate*2.47/100)
#     m.fs.FBNK.side_2_inlet.flow_mol_comp[0, "NO"].fix(FGrate*0.0006)
#     m.fs.FBNK.side_2_inlet.flow_mol_comp[0, "SO2"].fix(FGrate*0.002)
#     m.fs.FBNK.side_2_inlet.pressure[0].fix(100145)
    
#     m.fs.FBNK.side_2_inlet.temperature[0].fix(823.4 + 273.15)

    # FBNKomizer design variables and parameters
    ITM = 0.0254  # inch to meter conversion
    # Based on NETL Baseline Report Rev3
    m.fs.FBNK.tube_di.fix((2-2*0.188)*ITM)  # calc inner diameter
    #                                   (2 = outer diameter, thickness = 0.188)
#     m.fs.FBNK.tube_thickness.fix(0.188*ITM)  # tube thickness
    m.fs.FBNK.pitch_x.fix(3.5*ITM)
    # pitch_y = (54.5) gas path transverse width /columns
    m.fs.FBNK.pitch_y.fix(6.03*ITM)
#     m.fs.FBNK.tube_length.fix(103.41*12*ITM)  # use tube length (53.41 ft)
#     m.fs.FBNK.tube_nrow.fix(4*2)         # use to match baseline performance
#     m.fs.FBNK.tube_ncol.fix(70)            # 130 from NETL
    m.fs.FBNK.nrow_inlet.fix(2)
    m.fs.FBNK.delta_elevation.fix(50)
    # parameters
    # heat transfer resistance due to tube side fouling (water scales)
    m.fs.FBNK.tube_r_fouling = 0.000176
    # heat transfer resistance due to tube shell fouling (ash deposition)
    m.fs.FBNK.shell_r_fouling = 0.00088
    
    if m.fs.FBNK.config.has_radiation is True:
        m.fs.FBNK.emissivity_wall.fix(0.7)  # wall emissivity
    # correction factor for overall heat transfer coefficient
    m.fs.FBNK.fcorrection_htc.fix(1.5)
    # correction factor for pressure drop calc tube side
    m.fs.FBNK.fcorrection_dp_tube.fix(1.0)
    # correction factor for pressure drop calc shell side
    m.fs.FBNK.fcorrection_dp_shell.fix(1.0)



def initialize(m):
        initialize_FIBNK(m)
        initialize_PBNK(m)
        initialize_SIBNK(m)
        initialize_WW(m)
        initialize_FBNK(m)
        