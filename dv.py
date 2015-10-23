''' Delta-V calc for nanosat launcher.
'''

from __future__ import division
import math


class Stage(object):    

    def __init__(self, diameter, propellant_mass, non_tank_mass, specific_impulse):
        # Stage diameter [meter]
        self.r = diameter / 2
        # Propellant mass [kilogram]
        self.m_prop = propellant_mass
        # The non-tank inert mass of the stage [kilogram]
        self.m_non_tank = non_tank_mass
        # Specific impulse [second]
        self.isp = specific_impulse

        # Propellant density [kilogram meter**-3]
        self.rho_prop = 800
        # Tank pressure [pascal]
        self.p_tank = 5e6
        # Tank wall material max tensile stress [pascal]
        self.stress_max = 200e6
        # Tank wall material density [kilogram meter**-3]
        self.rho_tank_wall = 3000

        # Gravity for Isp calc [meter second**-2]
        self.g = 9.81
    

    def get_tank_length(self):
        '''Get the axial length of the stage's propellant tank.

        Returns:
            real: The length of the tank [meter].
        '''
        volume = self.m_prop / self.rho_prop
        length = volume / (math.pi * (self.r)**2)
        return length


    def get_tank_thickness(self):
        '''Calculate the required tank wall thickness.

        Returns:
            real: thickness [meter].
        '''
        thick = self.p_tank * self.r / self.stress_max
        return thick


    def get_tank_mass(self):
        '''Calculate the dry mass of the propellant tank.

        Returns:
            real: mass [kilogram].
        '''    
        L = self.get_tank_length()
        surface_area = (L * 2 * math.pi * self.r) \
            +  3/2 * (4 * math.pi * self.r**2)
        wall_volume = surface_area * self.get_tank_thickness()
        wall_mass = wall_volume * self.rho_tank_wall
        return wall_mass


    def get_delta_v(self, payload_mass):
        '''Calculate the delta-v of the stage.

        Arguements:
            payload_mass (real): Mass of stage payload [kilogram].

        Returns:
            real: the change in velocity from burning the stage's
                propellant [meter second**-1].
        '''
        m_inert = self.m_non_tank + self.get_tank_mass() + payload_mass
        m_0 = m_inert + self.m_prop
        m_1 = m_inert
        # Tsiolkovsky rocket equation.
        delta_v = self.isp * self.g * math.log(m_0 / m_1)
        return delta_v

    def get_total_mass(self):
        ''' Get the total (tank, propellant and non-tank) mass of the stage.

        Returns:
            real: The total mass [kilogram].
        '''
        return self.get_tank_mass() +self.m_non_tank + self.m_prop


class MultiStageRocket(object):
    def __init__(self, stages, payload_mass):
        ''' Create a new MultiStageRocket.

        Arguments:
            stages (list of Stage objects): The stages of the rocket.
                Element zero is the first stage to burn.
            payload_mass (real): The mass of the payload on the top stage [kilogram].
        '''
        self.stages = stages
        self.m_payload = payload_mass

    def get_stage_delta_v(self):
        ''' Get the delta-v of each stage in the rocket.

        The delta-v contributed is calculated for a stage by counting all the
        stages above as that stage's payload mass.

        Returns:
            real: The delta-v that each stage provides to the stages above it [meter second**-1].
        '''
        m_stages = [stage.get_total_mass() for stage in self.stages]
        stage_delta_vs = []
        for i in xrange(len(self.stages)-1):
            stage_delta_vs.append(
                self.stages[i].get_delta_v(sum(m_stages[i + 1 :]) + self.m_payload))
        stage_delta_vs.append(self.stages[-1].get_delta_v(self.m_payload))
        return stage_delta_vs

    def display_stages(self):
        ''' Print the performance of each stage.
        '''
        stage_delta_vs = self.get_stage_delta_v()
        for i in xrange(len(self.stages)):
            print 'Stage %d:' % (i + 1)
            print '\tTotal mass = %.1f kg' % (self.stages[i].get_total_mass())
            print '\tProp  mass = %.1f kg' % (self.stages[i].m_prop)
            print '\tPropellant mass fraction = %.2f' % (self.stages[i].m_prop / self.stages[i].get_total_mass())
            print '\tLength x diameter = %.1f x %.1f m' % (self.stages[i].get_tank_length(), self.stages[i].r * 2)
            print '\tI_sp = %.0f s' % (self.stages[i].isp)
            print '\tDelta-v = %.0f m/s' % (stage_delta_vs[i])
        print '\n'
        print 'Total delta-v = %.0f m/s' % (sum(stage_delta_vs))
        print 'Total mass on pad = %.0f kg' % (sum([s.get_total_mass() for s in self.stages]))



if __name__ == '__main__':
    solid_booster = Stage(diameter=0.8,
        propellant_mass=1.5e3,
        non_tank_mass=100,
        specific_impulse=230)
    # Solid propellant is dense
    solid_booster.rho_prop = 1200
    # Composite motor casing
    solid_booster.stress_max = 400e6
    solid_booster.rho_tank_wall = 2000

    solid_sustainer = Stage(diameter=0.5,
        propellant_mass=750,
        non_tank_mass=50,
        specific_impulse=230)
    # Solid propellant is dense
    solid_sustainer.rho_prop = 1200
    # Composite motor casing
    solid_sustainer.stress_max = 400e6
    solid_sustainer.rho_tank_wall = 2000

    solid_sustainer_2 = Stage(diameter=0.5,
        propellant_mass=500,
        non_tank_mass=25,
        specific_impulse=230)
    # Solid propellant is dense
    solid_sustainer_2.rho_prop = 1200
    # Composite motor casing
    solid_sustainer_2.stress_max = 400e6
    solid_sustainer_2.rho_tank_wall = 2000

    liquid_upper = Stage(diameter=0.5,
        propellant_mass=200,
        non_tank_mass=20,
        specific_impulse=320)
    # Ti alloy tanks
    liquid_upper.stress_max = 600e6
    liquid_upper.rho_tank_wall = 4500

    rocket = MultiStageRocket(
        [solid_booster, solid_sustainer, solid_sustainer_2, liquid_upper],
        payload_mass=10)
    rocket.display_stages()
