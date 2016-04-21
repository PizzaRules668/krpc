import unittest
import testingtools
import krpc
from mathtools import dot

class TestParts(testingtools.TestCase):

    @classmethod
    def setUpClass(cls):
        if testingtools.connect().space_center.active_vessel.name != 'Parts':
            testingtools.new_save()
            testingtools.launch_vessel_from_vab('Parts')
            testingtools.remove_other_vessels()
        cls.conn = testingtools.connect(name='TestParts')
        cls.vessel = cls.conn.space_center.active_vessel
        cls.parts = cls.vessel.parts

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_all_parts(self):
        parts = self.parts.all
        part_titles = sorted(p.title for p in parts)
        self.assertEqual(
            part_titles,
            ['\'Drill-O-Matic Junior\' Mining Excavator',
             'AE-FF1 Airstream Protective Shell (1.25m)',
             'Adjustable Ramp Intake (Radial)',
             'Advanced Reaction Wheel Module, Large',
             'Aerodynamic Nose Cone',
             'Aerodynamic Nose Cone',
             'Aerodynamic Nose Cone',
             'Clamp-O-Tron Docking Port',
             'Clamp-O-Tron Docking Port Jr.',
             'Communotron 16',
             'Convert-O-Tron 250',
             'Delta-Deluxe Winglet',
             'EAS-4 Strut Connector',
             'EAS-4 Strut Connector',
             'EAS-4 Strut Connector',
             'FL-R1 RCS Fuel Tank',
             'GRAVMAX Negative Gravioli Detector',
             'Gigantor XL Solar Array',
             'Illuminator Mk1',
             'Illuminator Mk1',
             'Illuminator Mk1',
             'LT-1 Landing Struts',
             'LT-1 Landing Struts',
             'LT-1 Landing Struts',
             'LY-10 Small Landing Gear',
             'Mk1-2 Command Pod',
             'Mk2-R Radial-Mount Parachute',
             'Mk2-R Radial-Mount Parachute',
             'Mk2-R Radial-Mount Parachute',
             u'Mystery Goo\u2122 Containment Unit',
             u'Mystery Goo\u2122 Containment Unit',
             u'Mystery Goo\u2122 Containment Unit',
             'OX-STAT Photovoltaic Panels',
             'PresMat Barometer',
             'RE-I5 "Skipper" Liquid Fuel Engine',
             'RE-L10 "Poodle" Liquid Fuel Engine',
             'RE-M3 "Mainsail" Liquid Fuel Engine',
             'RV-105 RCS Thruster Block',
             'Rockomax Jumbo-64 Fuel Tank',
             'Rockomax X200-32 Fuel Tank',
             'Rockomax X200-8 Fuel Tank',
             'S1 SRB-KD25k "Kickback" Solid Fuel Booster',
             'S1 SRB-KD25k "Kickback" Solid Fuel Booster',
             'S1 SRB-KD25k "Kickback" Solid Fuel Booster',
             'SP-L 1x6 Photovoltaic Panels',
             'SP-L 1x6 Photovoltaic Panels',
             'Service Bay (2.5m)',
             'TR-XL Stack Separator',
             'TR-XL Stack Separator',
             'TR-XL Stack Separator',
             'TT-70 Radial Decoupler',
             'TT-70 Radial Decoupler',
             'TT-70 Radial Decoupler',
             'TT18-A Launch Stability Enhancer',
             'TT18-A Launch Stability Enhancer',
             'TT18-A Launch Stability Enhancer',
             'TT18-A Launch Stability Enhancer',
             'TT18-A Launch Stability Enhancer',
             'TT18-A Launch Stability Enhancer',
             'Thermal Control System (small)',
             'XM-G50 Radial Air Intake',
             'Z-400 Rechargeable Battery'
         ])

    def test_root_part(self):
        root = self.parts.root
        self.assertEqual('Mark1-2Pod', root.name)
        self.assertEqual('Mk1-2 Command Pod', root.title)
        self.assertEqual(self.vessel, root.vessel)
        self.assertEqual(None, root.parent)
        self.assertGreater(len(root.children), 0)

    def test_controlling(self):
        commandpod = self.parts.root
        dockingport = self.parts.docking_ports[0].part
        part = self.parts.with_title('Z-400 Rechargeable Battery')[0]
        self.assertNotEqual(commandpod, dockingport)
        self.assertNotEqual(commandpod, part)

        self.assertEqual(commandpod, self.parts.controlling)
        self.parts.controlling = dockingport
        self.assertEqual(dockingport, self.parts.controlling)
        self.parts.controlling = part
        self.assertEqual(part, self.parts.controlling)
        self.parts.controlling = commandpod
        self.assertEqual(commandpod, self.parts.controlling)

    def test_controlling_orientation(self):
        ref = self.vessel.orbit.body.reference_frame
        root = self.parts.root
        port = self.parts.with_title('Clamp-O-Tron Docking Port')[0]

        # Check vessel direction is in direction of root part
        # and perpendicular to the docking port
        vessel_dir = self.vessel.direction(ref)
        root_dir = root.direction(ref)
        port_dir = port.direction(ref)
        self.assertClose(vessel_dir, root_dir)
        self.assertClose(0, dot(vessel_dir, port_dir))

        # Control from the docking port
        self.parts.controlling = port

        # Check vessel direction is now the direction of the docking port
        vessel_dir = self.vessel.direction(ref)
        self.assertClose(0, dot(vessel_dir, root_dir))
        self.assertClose(vessel_dir, port_dir)

        # Control from the root part
        self.parts.controlling = root

        # Check vessel direction is now the direction of the root part
        vessel_dir = self.vessel.direction(ref)
        self.assertClose(vessel_dir, root_dir)
        self.assertClose(0, dot(vessel_dir, port_dir))

    def test_parts_with_name(self):
        parts = self.parts.with_name('spotLight1')
        self.assertEqual(['spotLight1']*3, [p.name for p in parts])
        parts = self.parts.with_name('doesntExist')
        self.assertEqual(len(parts), 0)

    def test_parts_with_title(self):
        parts = self.parts.with_title('Illuminator Mk1')
        self.assertEqual(['Illuminator Mk1']*3, [p.title for p in parts])
        parts = self.parts.with_title('Doesn\'t Exist')
        self.assertEqual(len(parts), 0)

    def test_parts_with_module(self):
        parts = self.parts.with_module('ModuleLight')
        self.assertEqual(['spotLight1']*3 + ['SmallGearBay'], [p.name for p in parts])
        parts = self.parts.with_module('DoesntExist')
        self.assertEqual(len(parts), 0)

    def test_parts_in_stage(self):
        def part_titles_in_stage(s):
            return sorted([p.title for p in self.parts.in_stage(s)])
        self.assertEqual(
            ['\'Drill-O-Matic Junior\' Mining Excavator',
             'Adjustable Ramp Intake (Radial)',
             'Advanced Reaction Wheel Module, Large',
             'Aerodynamic Nose Cone',
             'Aerodynamic Nose Cone',
             'Aerodynamic Nose Cone',
             'Communotron 16',
             'Convert-O-Tron 250',
             'Delta-Deluxe Winglet',
             'EAS-4 Strut Connector',
             'EAS-4 Strut Connector',
             'EAS-4 Strut Connector',
             'FL-R1 RCS Fuel Tank',
             'GRAVMAX Negative Gravioli Detector',
             'Gigantor XL Solar Array',
             'Illuminator Mk1',
             'Illuminator Mk1',
             'Illuminator Mk1',
             'LT-1 Landing Struts',
             'LT-1 Landing Struts',
             'LT-1 Landing Struts',
             'LY-10 Small Landing Gear',
             'Mk1-2 Command Pod',
             u'Mystery Goo\u2122 Containment Unit',
             u'Mystery Goo\u2122 Containment Unit',
             u'Mystery Goo\u2122 Containment Unit',
             'OX-STAT Photovoltaic Panels',
             'PresMat Barometer',
             'RV-105 RCS Thruster Block',
             'Rockomax Jumbo-64 Fuel Tank',
             'Rockomax X200-32 Fuel Tank',
             'Rockomax X200-8 Fuel Tank',
             'SP-L 1x6 Photovoltaic Panels',
             'SP-L 1x6 Photovoltaic Panels',
             'Service Bay (2.5m)',
             'Thermal Control System (small)',
             'XM-G50 Radial Air Intake',
             'Z-400 Rechargeable Battery'],
            part_titles_in_stage(-1))
        self.assertEqual(
            ['AE-FF1 Airstream Protective Shell (1.25m)'],
            part_titles_in_stage(0))
        self.assertEqual(
            ['TR-XL Stack Separator'],
            part_titles_in_stage(1))
        self.assertEqual(
            ['Mk2-R Radial-Mount Parachute']*3,
            part_titles_in_stage(2))
        self.assertEqual(
            ['RE-L10 "Poodle" Liquid Fuel Engine',
             'TR-XL Stack Separator'],
            part_titles_in_stage(3))
        self.assertEqual(
            #TODO: why are docking ports activated in a stage?
            [u'Clamp-O-Tron Docking Port',
             u'Clamp-O-Tron Docking Port Jr.',
             'RE-I5 "Skipper" Liquid Fuel Engine',
             'TR-XL Stack Separator'],
            part_titles_in_stage(4))
        self.assertEqual(
            ['TT-70 Radial Decoupler']*3,
            part_titles_in_stage(5))
        self.assertEqual(
            ['RE-M3 "Mainsail" Liquid Fuel Engine'] + \
            ['S1 SRB-KD25k "Kickback" Solid Fuel Booster']*3 + \
            ['TT18-A Launch Stability Enhancer']*6,
            part_titles_in_stage(6))
        self.assertEqual([], part_titles_in_stage(7))

    def test_parts_in_decouple_stage(self):
        def part_titles_in_decouple_stage(s):
            return sorted([p.title for p in self.parts.in_decouple_stage(s)])
        self.assertEqual(
            ['AE-FF1 Airstream Protective Shell (1.25m)'] + \
            ['LT-1 Landing Struts']*3 + \
            ['LY-10 Small Landing Gear',
             'Mk1-2 Command Pod'],
            part_titles_in_decouple_stage(-1))
        self.assertEqual([], part_titles_in_decouple_stage(0))
        self.assertEqual(
            ['RE-M3 "Mainsail" Liquid Fuel Engine',
             'Rockomax Jumbo-64 Fuel Tank',
             'TR-XL Stack Separator'],
            part_titles_in_decouple_stage(4))
        self.assertEqual(
            ['Aerodynamic Nose Cone']*3 + \
            ['Illuminator Mk1']*3 + \
            ['S1 SRB-KD25k "Kickback" Solid Fuel Booster']*3 + \
            ['TT-70 Radial Decoupler']*3,
            part_titles_in_decouple_stage(5))
        self.assertEqual(
            ['TT18-A Launch Stability Enhancer']*6,
            part_titles_in_decouple_stage(6))
        self.assertEqual([], part_titles_in_decouple_stage(7))

    def test_modules_with_name(self):
        modules = self.parts.modules_with_name('ModuleLight')
        self.assertEqual(['ModuleLight']*4, [m.name for m in modules])
        modules = self.parts.modules_with_name('DoesntExist')
        self.assertEqual(len(modules), 0)

    def test_cargo_bays(self):
        self.assertEqual(['Service Bay (2.5m)'], sorted(x.part.title for x in self.parts.cargo_bays))

    def test_control_surfaces(self):
        self.assertEqual(['Delta-Deluxe Winglet'], sorted(x.part.title for x in self.parts.control_surfaces))

    def test_decouplers(self):
        self.assertEqual(
            ['TR-XL Stack Separator', 'TR-XL Stack Separator', 'TR-XL Stack Separator',
             'TT-70 Radial Decoupler', 'TT-70 Radial Decoupler', 'TT-70 Radial Decoupler'],
            sorted(x.part.title for x in self.parts.decouplers))

    def test_docking_ports(self):
        self.assertEqual(
            ['Clamp-O-Tron Docking Port', 'Clamp-O-Tron Docking Port Jr.'],
            sorted(x.part.title for x in self.parts.docking_ports))

    def test_docking_port_with_name(self):
        port = self.parts.docking_ports[0]
        if 'ModuleDockingNodeNamed' not in set(x.name for x in port.part.modules):
            # Docking Port Alignment Indicator mod not installed
            return
        # FIXME: unicode -> str bug
        name = str(port.name)
        self.assertEqual(port, self.parts.docking_port_with_name(name))
        self.assertEqual(None, self.parts.docking_port_with_name('Not the name'))
        port.name = 'Jeb\'s port'
        self.assertEqual(port, self.parts.docking_port_with_name('Jeb\'s port'))
        self.assertEqual(None, self.parts.docking_port_with_name(name))
        self.assertEqual(None, self.parts.docking_port_with_name('Not the name'))
        port.name = name

    def test_engines(self):
        self.assertEqual(
            ['RE-I5 "Skipper" Liquid Fuel Engine', 'RE-L10 "Poodle" Liquid Fuel Engine',
             'RE-M3 "Mainsail" Liquid Fuel Engine', 'S1 SRB-KD25k "Kickback" Solid Fuel Booster',
             'S1 SRB-KD25k "Kickback" Solid Fuel Booster', 'S1 SRB-KD25k "Kickback" Solid Fuel Booster'],
            sorted(x.part.title for x in self.parts.engines))

    def test_fairings(self):
        self.assertEqual(['AE-FF1 Airstream Protective Shell (1.25m)'], sorted(x.part.title for x in self.parts.fairings))

    def test_intakes(self):
        self.assertEqual(['Adjustable Ramp Intake (Radial)', 'XM-G50 Radial Air Intake'], sorted(x.part.title for x in self.parts.intakes))

    def test_landing_gear(self):
        self.assertEqual(['LY-10 Small Landing Gear'], sorted(x.part.title for x in self.parts.landing_gear))

    def test_landing_legs(self):
        self.assertEqual(['LT-1 Landing Struts']*3, sorted(x.part.title for x in self.parts.landing_legs))

    def test_launch_clamps(self):
        self.assertEqual(['TT18-A Launch Stability Enhancer']*6, sorted(x.part.title for x in self.parts.launch_clamps))

    def test_lights(self):
        self.assertEqual(['Illuminator Mk1']*3 + ['LY-10 Small Landing Gear'], sorted(x.part.title for x in self.parts.lights))

    def test_parachutes(self):
        self.assertEqual(
            ['Mk2-R Radial-Mount Parachute']*3,
            sorted(x.part.title for x in self.parts.parachutes))

    def test_radiators(self):
        self.assertEqual(
            ['Thermal Control System (small)'],
            sorted(x.part.title for x in self.parts.radiators))

    def test_rcs(self):
        self.assertEqual(['RV-105 RCS Thruster Block'], sorted(x.part.title for x in self.parts.rcs))

    def test_reaction_wheels(self):
        self.assertEqual(
            ['Advanced Reaction Wheel Module, Large', 'Mk1-2 Command Pod'],
            sorted(x.part.title for x in self.parts.reaction_wheels))

    def test_resource_converters(self):
        self.assertEqual(
            ['Convert-O-Tron 250'],
            sorted(x.part.title for x in self.parts.resource_converters))

    def test_resource_harvesters(self):
        self.assertEqual(
            ['\'Drill-O-Matic Junior\' Mining Excavator'],
            sorted(x.part.title for x in self.parts.resource_harvesters))

    def test_sensors(self):
        self.assertEqual(
            ['GRAVMAX Negative Gravioli Detector', 'PresMat Barometer'],
            sorted(x.part.title for x in self.parts.sensors))

    def test_solar_panels(self):
        self.assertEqual(
            ['Gigantor XL Solar Array', 'OX-STAT Photovoltaic Panels',
             'SP-L 1x6 Photovoltaic Panels', 'SP-L 1x6 Photovoltaic Panels'],
            sorted(x.part.title for x in self.parts.solar_panels))

if __name__ == "__main__":
    unittest.main()