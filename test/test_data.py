
smartctl_output_ssd_hdd = """
=== START OF INFORMATION SECTION ===
Model Family:     Seagate IronWolf 110 SATA SSD
Device Model:     ZA240NM10001
Serial Number:    ABCD1234
LU WWN Device Id: 5 000c50 A1B2C3D4
Firmware Version: SF44011J
User Capacity:    240,057,409,536 bytes [240 GB]
Sector Sizes:     512 bytes logical, 4096 bytes physical
Rotation Rate:    Solid State Device
TRIM Command:     Available, deterministic, zeroed
Device is:        In smartctl database 7.3/5319
ATA Version is:   ACS-4, ACS-2 T13/2015-D revision 3
SATA Version is:  SATA 3.3, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Sun Dec 31 02:13:22 2023 CET
SMART support is: Available - device has SMART capability.
SMART support is: Enabled

=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

General SMART Values:
Offline data collection status:  (0x02) Offline data collection activity
                                        was completed without error.
                                        Auto Offline Data Collection: Disabled.
Self-test execution status:      (   0) The previous self-test routine completed
                                        without error or no self-test has ever
                                        been run.
Total time to complete Offline
data collection:                (    0) seconds.
Offline data collection
capabilities:                    (0x59) SMART execute Offline immediate.
                                        No Auto Offline data collection support.
                                        Suspend Offline collection upon new
                                        command.
                                        Offline surface scan supported.
                                        Self-test supported.
                                        No Conveyance Self-test supported.
                                        Selective Self-test supported.
SMART capabilities:            (0x0003) Saves SMART data before entering
                                        power-saving mode.
                                        Supports SMART auto save timer.
Error logging capability:        (0x01) Error logging supported.
                                        General Purpose Logging supported.
Short self-test routine
recommended polling time:        (   1) minutes.
Extended self-test routine
recommended polling time:        (  30) minutes.
SCT capabilities:              (0x103d) SCT Status supported.
                                        SCT Error Recovery Control supported.
                                        SCT Feature Control supported.
                                        SCT Data Table supported.

SMART Attributes Data Structure revision number: 11
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x002f   100   100   090    Pre-fail  Always       -       0
  5 Reallocated_Sector_Ct   0x0032   100   100   000    Old_age   Always       -       0
  9 Power_On_Hours          0x0032   100   100   000    Old_age   Always       -       27773
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       129
100 Flash_GB_Erased         0x0032   100   100   000    Old_age   Always       -       85641
102 Lifetime_PS4_Entry_Ct   0x0032   100   100   000    Old_age   Always       -       2
103 Lifetime_PS3_Exit_Ct    0x0032   100   100   000    Old_age   Always       -       291
170 Grown_Bad_Block_Ct      0x0032   100   100   000    Old_age   Always       -       0
171 Program_Fail_Count      0x0032   100   100   000    Old_age   Always       -       0
172 Erase_Fail_Count        0x0032   100   100   000    Old_age   Always       -       0
173 Avg_Program/Erase_Ct    0x0032   093   093   000    Old_age   Always       -       534
174 Unexpected_Pwr_Loss_Ct  0x0032   100   100   000    Old_age   Always       -       54
177 Wear_Range_Delta        0x0023   098   098   089    Pre-fail  Always       -       0 0 2
183 SATA_Downshift_Count    0x0032   100   100   000    Old_age   Always       -       0x00000001000000
187 Uncorrectable_ECC_Ct    0x0032   100   100   000    Old_age   Always       -       0
194 Temperature_Celsius     0x0022   025   049   000    Old_age   Always       -       25 (Min/Max 18/49)
195 RAISE_ECC_Cor_Ct        0x0032   100   100   000    Old_age   Always       -       0
198 Uncor_Read_Error_Ct     0x0032   100   100   000    Old_age   Always       -       0
199 UDMA_CRC_Error_Count    0x0032   100   100   000    Old_age   Always       -       0
230 Drv_Life_Protect_Status 0x0023   100   100   091    Pre-fail  Always       -       100
231 SSD_Life_Left           0x0033   093   093   010    Pre-fail  Always       -       0x00000000645d00
232 Available_Reservd_Space 0x0027   100   100   003    Pre-fail  Always       -       0
233 Lifetime_Wts_To_Flsh_GB 0x0032   100   100   000    Old_age   Always       -       163817
241 Lifetime_Wts_Frm_Hst_GB 0x0032   100   100   000    Old_age   Always       -       141921
242 Lifetime_Rds_Frm_Hst_GB 0x0032   100   100   000    Old_age   Always       -       353372
243 Free_Space              0x0026   062   012   003    Old_age   Always       -       0x07189600027f85

SMART Error Log not supported

SMART Self-test log structure revision number 1
Num  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error
# 1  Extended offline    Completed without error       00%     27045         -
# 2  Extended offline    Completed without error       00%     26320         -
# 3  Extended offline    Completed without error       00%     25569         -
# 4  Extended offline    Completed without error       00%     24845         -
# 5  Extended offline    Completed without error       00%     24094         -
# 6  Extended offline    Completed without error       00%     23345         -
# 7  Extended offline    Completed without error       00%     22617         -
# 8  Extended offline    Completed without error       00%     21867         -
# 9  Extended offline    Completed without error       00%     21142         -
#10  Short offline       Completed without error       00%     20494         -
#11  Extended offline    Completed without error       00%     20398         -
#12  Short offline       Completed without error       00%     20325         -
#13  Short offline       Completed without error       00%     20156         -
#14  Short offline       Completed without error       00%     19988         -
#15  Short offline       Completed without error       00%     19817         -
#16  Extended offline    Completed without error       00%     19721         -
#17  Short offline       Completed without error       00%     19648         -
#18  Short offline       Completed without error       00%     19479         -
#19  Short offline       Completed without error       00%     19309         -

SMART Selective self-test log data structure revision number 1
 SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS
    1        0        0  Not_testing
    2        0        0  Not_testing
    3        0        0  Not_testing
    4        0        0  Not_testing
    5        0        0  Not_testing
Selective self-test flags (0x0):
  After scanning selected spans, do NOT read-scan remainder of disk.
If Selective self-test is pending on power-up, resume after 0 minute delay.
"""

smartctl_output_nvme = """
smartctl 7.3 2022-02-28 r5338 [x86_64-linux-6.1.63-production+truenas] (local build)
Copyright (C) 2002-22, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Number:                       WD Red SN700 500GB
Serial Number:                      A1B2C3D4E5F6
Firmware Version:                   111130WD
PCI Vendor/Subsystem ID:            0x15b7
IEEE OUI Identifier:                0x001b44
Total NVM Capacity:                 500,107,862,016 [500 GB]
Unallocated NVM Capacity:           0
Controller ID:                      8215
NVMe Version:                       1.3
Number of Namespaces:               1
Namespace 1 Size/Capacity:          500,107,862,016 [500 GB]
Namespace 1 Formatted LBA Size:     512
Namespace 1 IEEE EUI-64:            001b44 AABBCCDDEE
Local Time is:                      Sun Dec 31 02:57:33 2023 CET
Firmware Updates (0x14):            2 Slots, no Reset required
Optional Admin Commands (0x0017):   Security Format Frmw_DL Self_Test
Optional NVM Commands (0x005f):     Comp Wr_Unc DS_Mngmt Wr_Zero Sav/Sel_Feat Timestmp
Log Page Attributes (0x0e):         Cmd_Eff_Lg Ext_Get_Lg Telmtry_Lg
Maximum Data Transfer Size:         128 Pages
Warning  Comp. Temp. Threshold:     84 Celsius
Critical Comp. Temp. Threshold:     88 Celsius
Namespace 1 Features (0x02):        NA_Fields

Supported Power States
St Op     Max   Active     Idle   RL RT WL WT  Ent_Lat  Ex_Lat
 0 +     5.50W       -        -    0  0  0  0        0       0
 1 +     3.50W       -        -    1  1  1  1        0       0
 2 +     3.00W       -        -    2  2  2  2        0       0
 3 -   0.0700W       -        -    3  3  3  3     4000   10000
 4 -   0.0035W       -        -    4  4  4  4     4000   40000

Supported LBA Sizes (NSID 0x1)
Id Fmt  Data  Metadt  Rel_Perf
 0 +     512       0         2
 1 -    4096       0         1

=== START OF SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

SMART/Health Information (NVMe Log 0x02)
Critical Warning:                   0x00
Temperature:                        43 Celsius
Available Spare:                    100%
Available Spare Threshold:          10%
Percentage Used:                    111%
Data Units Read:                    1,053,595,599 [539 TB]
Data Units Written:                 1,902,011,793 [973 TB]
Host Read Commands:                 4,038,233,904
Host Write Commands:                6,130,585,377
Controller Busy Time:               20,611
Power Cycles:                       54
Power On Hours:                     14,527
Unsafe Shutdowns:                   10
Media and Data Integrity Errors:    0
Error Information Log Entries:      0
Warning  Comp. Temperature Time:    0
Critical Comp. Temperature Time:    0

Error Information (NVMe Log 0x01, 16 of 256 entries)
No Errors Logged
"""

# ipmitool sdr 2>/dev/null | grep -iE FAN[0-9A-Z]+
fan_sensor_list_bis = """
FAN1             | 1000 RPM          | ok
FAN2             | no reading        | ns
FAN3             | no reading        | ns
FAN4             | no reading        | ns
FAN5             | 800 RPM           | ok
FANA             | 600 RPM           | nc
FANB             | 700 RPM           | ok
"""

# ipmitool sensor list 2>/dev/null | grep -iE FAN[0-9A-Z]+
fan_sensor_list = """
FAN1             | 1000.000   | RPM        | ok    | 200.000   | 300.000   | 400.000   | 2500.000  | 2600.000  | 2700.000
FAN2             | na         |            | na    | na        | na        | na        | na        | na        | na
FAN3             | na         |            | na    | na        | na        | na        | na        | na        | na
FAN4             | na         |            | na    | na        | na        | na        | na        | na        | na
FAN5             | 700.000    | RPM        | ok    | 200.000   | 300.000   | 400.000   | 2400.000  | 2500.000  | 2600.000
FANA             | 600.000    | RPM        | nc    | 400.000   | 500.000   | 600.000   | 3300.000  | 3400.000  | 3500.000
FANB             | 700.000    | RPM        | ok    | 400.000   | 500.000   | 600.000   | 3300.000  | 3400.000  | 3500.000
"""

disk_info = [
    ('sda', 31, 'K4X9R2TQ'), ('sdb', 26, 'Q1Z3M8VW'), ('sdc', 31, 'B7F5X2L9J0H3'), ('sdd', 34, 'T6G1K7M3V2Z9'),
    ('sde', 33, 'M3P9H4ND'), ('sdf', 35, 'V7X1Q2LB'), ('sdg', 29, 'L5N3Z8AW'), ('sdh', 33, 'Y2W4K6MS'),
    ('sdi', 32, 'C8L7J3ZT'), ('sdj', 32, 'P9Q6M4BR'), ('sdk', 32, 'R3X7N8LQ'), ('nvme0n1', 43, 'Q7L9P2W6K3JD85')
]

sensors_json = """
{
   "k10temp-pci-00c3":{
      "Adapter": "PCI adapter",
      "Tctl":{
         "temp1_input": 27.250
      },
      "Tccd1":{
         "temp3_input": 26.000
      },
      "Tccd3":{
         "temp5_input": 26.000
      },
      "Tccd5":{
         "temp7_input": 26.500
      },
      "Tccd7":{
         "temp9_input": 25.250
      }
   },
   "nvme-pci-8400":{
      "Adapter": "PCI adapter",
      "Composite":{
         "temp1_input": 45.850,
         "temp1_max": 83.850,
         "temp1_min": -5.150,
         "temp1_crit": 87.850,
         "temp1_alarm": 0.000
      }
   },
   "cxgb4_0000:41:00.4-virtual-0":{
      "Adapter": "Virtual device",
      "temp1":{
         "temp1_input": 47.000
      }
   }
}
"""

disk_list_output = """
{
   "blockdevices": [
      {
         "name": "sda",
         "rota": true
      },{
         "name": "sdb",
         "rota": true
      },{
         "name": "sdc",
         "rota": true
      },{
         "name": "sdd",
         "rota": true
      },{
         "name": "sde",
         "rota": true
      },{
         "name": "sdf",
         "rota": true
      },{
         "name": "sdg",
         "rota": true
      },{
         "name": "sdh",
         "rota": true
      },{
         "name": "sdi",
         "rota": true
      },{
         "name": "sdj",
         "rota": true
      },{
         "name": "sdk",
         "rota": true
      },{
         "name": "sdl",
         "rota": true
      },{
         "name": "sdm",
         "rota": true
      },{
         "name": "sdn",
         "rota": true
      },{
         "name": "sdo",
         "rota": true
      },{
         "name": "sdp",
         "rota": false
      },{
         "name": "sdq",
         "rota": false
      },{
         "name": "sdr",
         "rota": false
      },{
         "name": "nvme0n1",
         "rota": false
      }
   ]
}
"""

# CPU TEMP

intel_cpu_temps = """
coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +80.0°C  (high = +100.0°C, crit = +100.0°C)
Core 0:        +80.0°C  (high = +100.0°C, crit = +100.0°C)
Core 1:        +46.0°C  (high = +100.0°C, crit = +100.0°C)
Core 2:        +53.0°C  (high = +100.0°C, crit = +100.0°C)
Core 3:        +48.0°C  (high = +100.0°C, crit = +100.0°C)
Core 4:        +46.0°C  (high = +100.0°C, crit = +100.0°C)
Core 5:        +47.0°C  (high = +100.0°C, crit = +100.0°C)
"""

amd_cpu_temps = """
k10temp-pci-00c3
Adapter: PCI adapter
Tctl:         +27.2°C
Tccd1:        +26.8°C
Tccd3:        +27.0°C
Tccd5:        +26.5°C
Tccd7:        +26.2°C
"""