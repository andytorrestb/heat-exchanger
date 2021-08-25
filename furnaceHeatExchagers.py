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

from results import print_results
from initialize import initialize

def main():
    """
    Make the flowsheet object, fix some variables, and solve the problem
    """
    # Create a Concrete Model as the top level object
    m = ConcreteModel()

    # Add a flowsheet object to the model
    m.fs = FlowsheetBlock(default={"dynamic": False})

    m.fs.prop_swco2 = swco2.SWCO2ParameterBlock()
    m.fs.prop_fluegas = FlueGasParameterBlock()
    
    build_boiler(m.fs)

    TransformationFactory("network.expand_arcs").apply_to(m)

    # Create a solver
    solver = SolverFactory('ipopt')
    return(m, solver)

def build_boiler(fs):
    # Pendant Bank
    fs.PBNK = BoilerHeatExchanger(default=
                          {"side_1_property_package": fs.prop_swco2,
                           "side_2_property_package": fs.prop_fluegas,
                           "has_pressure_change": True,
                           "has_holdup": False,
                           "delta_T_method": DeltaTMethod.counterCurrent,
                           "tube_arrangement": TubeArrangement.inLine,
                           "side_1_water_phase": "Liq",
                           "has_radiation": True})

    # First Internal Bank
    fs.FIBNK =  BoilerHeatExchanger(default=
                          {"side_1_property_package": fs.prop_swco2,
                           "side_2_property_package": fs.prop_fluegas,
                           "has_pressure_change": True,
                           "has_holdup": False,
                           "delta_T_method": DeltaTMethod.counterCurrent,
                           "tube_arrangement": TubeArrangement.inLine,
                           "side_1_water_phase": "Liq",
                           "has_radiation": True})
    
    # Second Internal Bank
    fs.SIBNK =  BoilerHeatExchanger(default=
                          {"side_1_property_package": fs.prop_swco2,
                           "side_2_property_package": fs.prop_fluegas,
                           "has_pressure_change": True,
                           "has_holdup": False,
                           "delta_T_method": DeltaTMethod.counterCurrent,
                           "tube_arrangement": TubeArrangement.inLine,
                           "side_1_water_phase": "Liq",
                           "has_radiation": True})
    
    # Water Wall
    fs.WW =  BoilerHeatExchanger(default=
                          {"side_1_property_package": fs.prop_swco2,
                           "side_2_property_package": fs.prop_fluegas,
                           "has_pressure_change": True,
                           "has_holdup": False,
                           "delta_T_method": DeltaTMethod.counterCurrent,
                           "tube_arrangement": TubeArrangement.inLine,
                           "side_1_water_phase": "Liq",
                           "has_radiation": True})
    
        
    # Final Bank
    fs.FBNK =  BoilerHeatExchanger(default=
                          {"side_1_property_package": fs.prop_swco2,
                           "side_2_property_package": fs.prop_fluegas,
                           "has_pressure_change": True,
                           "has_holdup": False,
                           "delta_T_method": DeltaTMethod.counterCurrent,
                           "tube_arrangement": TubeArrangement.inLine,
                           "side_1_water_phase": "Liq",
                           "has_radiation": True})

    # Add CO2 connections
    fs.pbnk_2_fibnk = Arc(source = fs.PBNK.side_1_outlet,
                        destination = fs.FIBNK.side_1_inlet)
    
    fs.sibnk_2_pbnk = Arc(source = fs.SIBNK.side_1_outlet,
                        destination = fs.PBNK.side_1_inlet)
    
    fs.ww_2_sibnk = Arc(source = fs.WW.side_1_outlet,
                        destination = fs.SIBNK.side_1_inlet)
            
    fs.fbnk_2_ww = Arc(source = fs.FBNK.side_1_outlet,
                        destination = fs.WW.side_1_inlet)
                
    # Add flue gas connections
    fs.pbnk_2_fibnk_fg = Arc(source = fs.PBNK.side_2_outlet,
                          destination = fs.FIBNK.side_2_inlet)
    
    fs.fibnk_2_sibnk_fg = Arc(source = fs.FIBNK.side_2_outlet,
                              destination = fs.SIBNK.side_2_outlet)
    
    fs.sibnk_2_fbnk_fg = Arc(source = fs.SIBNK.side_2_outlet,
                              destination = fs.FIBNK.side_2_outlet)
   
    
if __name__ == "__main__":
    m, solver = main()

    solver.options = {"tol": 1e-6,
                      "linear_solver": "ma27",
                      "max_iter": 100,
                      "halt_on_ampl_error": 'yes'}
    # initialize each unit at the time
    initialize(m)
    print('flowsheet degrees of freedom = ' + str(degrees_of_freedom(m)))
#     results = solver.solve(m, tee=True, symbolic_solver_labels=True)
#     print_results(m)
#     m.pprint()

