import RFSignalGenerators
import BPMDevice
import Gate_Source
import ProgrammableAttenuator
import Latex_Report
import Tests

RF = RFSignalGenerators.Rigol3030DSG_RFSigGen(
    ipaddress="172.23.252.51",
    port=5555,
    timeout=1,
    limit=-40)

GS = Gate_Source.Rigol3030DSG_GateSource(
    ipaddress="172.23.252.51",
    port=5555,
    timeout=1)

ProgAtten = ProgrammableAttenuator.MC_RC4DAT6G95_Prog_Atten(
    ipaddress="172.23.244.105",
    port=23,
    timeout=1)

BPM = BPMDevice.SparkERXR_EPICS_BPMDevice(
    database="libera",
    daq_type="fa")

report = Latex_Report.Tex_Report("BPMTestReport")

dls_RF_frequency = 499.6817682
dls_bunch = 1.87319
subdirectory = "./Results/"
settling_time = 2

Tests.Beam_position_equidistant_grid_raster_scan_test(
    RFObject=RF,
    BPMObject=BPM,
    ProgAttenObject=ProgAtten,
    rf_frequency=dls_RF_frequency,
    rf_power=-40,
    nominal_attenuation=10,
    x_points=3,
    y_points=3,
    settling_time=settling_time,
    ReportObject=report,
    sub_directory=subdirectory)

Tests.Beam_position_attenuation_permutation_test(
    RFObject=RF,
    BPMObject=BPM,
    ProgAttenObject=ProgAtten,
    rf_frequency=dls_RF_frequency,
    rf_power=-40,
    attenuator_max=50,
    attenuator_min=10,
    attenuator_steps=2,
    settling_time=settling_time,
    ReportObject=report,
    sub_directory=subdirectory)

ProgAtten.set_global_attenuation(0)

Tests.Beam_Power_Dependance(
    RFObject=RF,
    BPMObject=BPM,
    frequency=dls_RF_frequency,
    start_power=-100,
    end_power=-40,
    samples=10,
    settling_time=settling_time,
    ReportObject=report,
    sub_directory=subdirectory)

Tests.Fixed_voltage_amplitude_fill_pattern_test(
    RFObject=RF,
    BPMObject=BPM,
    GateSourceObject=GS,
    frequency=dls_RF_frequency,
    power=-40,
    samples=10,
    pulse_period=dls_bunch,
    settling_time=settling_time,
    ReportObject=report,
    sub_directory=subdirectory)

Tests.Scaled_voltage_amplitude_fill_pattern_test(
    RFObject=RF,
    BPMObject=BPM,
    GateSourceObject=GS,
    frequency=dls_RF_frequency,
    desired_power=-70,
    samples=10,
    pulse_period=dls_bunch,
    settling_time=settling_time,
    ReportObject=report,
    sub_directory=subdirectory)

report.create_report()

