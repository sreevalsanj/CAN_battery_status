#!/usr/bin/env python

from tabulate import tabulate
import can
import struct
import curses
import subprocess
import time
import datetime


class Dataa:
    def __init__(self):
        self.bus=can.interface.Bus(bustype="socketcan",channel="can0",bitrate=250000)
        self.controllerstatus=0
        self.boot_up=False
        self.stopped=False
        self.operational=False
        self.canopenerror=0
        self.errorregistor=0
        self.faultcode=0
        self.batterydischargelimit=0
        self.batterychargelimit=0
        self.batterydischargestatus=0
        self.discharge=False
        self.chargeinterlockstate=0
        self.batteryMPEstatus=0
        self.readypower=0
        self.chargepower=0
        self.chargerhighestvoltage=0
        self.chargerhighestcurrent=0
        self.chargestatus=0
        self.chargermode=0
        self.chargeroutputvoltage=0
        self.chargeroutputcurrent=0
        self.chargerstatus=0
        self.chargertemperature=0
        self.batterycurrent=0
        self.batteryvoltage=0
        self.batterysoc=0
        self.batteryamphours=0
        self.batteryhighesttemperature=0
        self.highesttemperaturethermistorid=0
        self.batterylowesttemperature=0
        self.highestlowestthermistorid=0
        self.batteryaveragetemperature=0
        self.bmstemperature=0
        self.batteryadaptivesoc=0
        self.batteryadaptiveamphours=0
        self.auxilarybatteryvoltage=0
        self.bpfailsafestatus=0
        self.dtcstatus1=0
        self.dtcstatus2=0
        self.currentlimitstatus=0
        self.j1772currentlimit=0
        self.j1772plugstate=0
        self.batteryadaptivetotalcapacity=0
        self.batterytotalcycles=0
        self.batterysoh=0
        self.celldata=0

      
    def twos_comp(self, val, bits):
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val 

    def to_little(self,val):
        little_hex = bytearray.fromhex(val)
        little_hex.reverse()
        # print("Byte array format:", little_hex)
        str_little = ''.join(format(x, '02x') for x in little_hex)
        return str_little
        
    def can_data(self):
       #Every Can id except '0x292' is  little endian and swap to get correct value.
       #for '0x292' not in little endian, so no need to swap.
        self.message=self.bus.recv()
        
        # if self.message.arbitration_id==0x701:
        #     self.a=bytearray(self.message.data)
        #     self.he=self.a.hex() #converting bytearray to hex format

        #     aa=self.to_little(self.he[0:2])
        #     self.controllerstatus=int(aa,16)
        #     if self.controllerstatus==0:
        #         self.controllerstatus="Boot up"
        #     elif self.controllerstatus==4:
        #         self.ControllerStatus="Stopped"
        #     elif self.controllerstatus==5:
        #         self.ControllerStatus="Operational"        

        # elif self.message.arbitration_id==0x081:    
        #     self.a=bytearray(self.message.data)
        #     self.he= self.a.hex()

        #     ab = self.to_little(self.he[0:4]) #Not little endian. No need to swap
        #     self.canopenerror= int(ab,16)
            
        #     ac = self.to_little(self.he[4:6]) #Not little endian. No need to swap
        #     self.errorregistor= int(ac,16)

        #     ad =self.to_little(self.he[6:10]) #Not little endian. No need to swap
        #     self.faultcode= int(ad,16)
        
        # elif self.message.arbitration_id==0x181:
        #     self.a=bytearray(self.message.data)
        #     self.he=self.a.hex() #converting bytearray to hex format

        #     ae= self.to_little(self.he[0:4])
        #     self.batterydischargelimit=int(ae,16)
        #     self.batterydischargelimit= self.twos_comp(self.batterydischargelimit,16)*1
            
        #     af= self.to_little(self.he[4:8])
        #     self.batterychargelimit=int(af,16)
        #     self.batterychargelimit= self.twos_comp(self.batterychargelimit,16)*1

        #     ag= self.to_little(self.he[8:10])
        #     self.batterydischargestatus=int(ag,16)
        #     if self.batterydischargestatus==0:
        #         self.batterydischargestatus="OFF"
        #     else:
        #         if self.batterydischargestatus==255:
        #             self.batterydischargestatus="ON"

        #     ah= self.to_little(self.he[10:12])
        #     self.chargeinterlockstate=int(ah,16) 
        #     if self.chargeinterlockstate==0:
        #         if self.chargeinterlockstate==0:
        #             self.chargeinterlockstate="OFF"                
        #         elif self.chargeinterlockstate==1:
        #             self.chargeinterlockstate="ON"  

        #     self.batteryMPEstatus=int(ah,16)      
        #     if self.batteryMPEstatus==1:
        #         if self.batteryMPEstatus==0:
        #             self.batteryMPEstatus="OFF"
        #         elif self.batteryMPEstatus==1:
        #             self.batteryMPEstatus="On"
            
        #     self.readypower=int(ah,16)
        #     if self.readypower==2:
        #         if self.readypower==0:
        #             self.readypower="OFF"
        #         elif self.readypower==1:
        #             self.readypower="ON"

        #     self.chargepower=int(ah,16)
        #     if self.chargepower==3:
        #         if self.chargepower==0:
        #             self.chargepower="OFF"
        #         elif self.chargepower==1:
        #             self.chargepower="ON"


        # elif self.message.arbitration_id==0x1806E5F4:
        #     self.a=bytearray(self.message.data)
        #     self.he=self.a.hex() #converting bytearray to hex format

        #     ai=self.to_little(self.he[0:4])
        #     self.chargerhighestvoltage=int(ai,16)*0.1
            

        #     aj=self.to_little(self.he[4:8])
        #     self.chargerhighestcurrent=int(aj,16)*0.1
            
        #     ak=self.to_little(self.he[8:10])
        #     self.chargestatus=int(ak,16)
        #     if self.chargestatus==0:
        #         self.chargestatus="Charge"
        #     elif self.chargerstatus==1:
        #         self.chargestatus="STOP Charge"    

        #     al=self.to_little(self.he[10:12])    
        #     self.chargermode=int(al,16)


        # elif self.message.arbitration_id==0x18FF50E5:
        #     self.a=bytearray(self.message.data)
        #     self.he=self.a.hex() #converting bytearray to hex format

        #     am=self.to_little(self.he[0:4])
        #     self.chargeroutputvoltage=int(am,16)*0.1
            
        #     an=self.to_little(self.he[4:8])
        #     self.chargeroutputcurrent=int(an,16)*0.1

        #     ao=self.to_little(self.he[8:10])
        #     self.chargerstatus=int(ao,16)
        #     if self.chargerstatus==0:
        #         self.chargerstatus="Hardware Status"
        #     elif self.chargerstatus==1:
        #         self.chargerstatus="Thermal Status"
        #     elif self.chargerstatus==2:
        #         self.chargerstatus="Input Voltage Status"    
        #     elif self.chargerstatus==3:
        #         self.chargerstatus="Start Status"
        #     elif self.chargerstatus==4:
        #         self.chargerstatus="Communication Status"    

        #     ap=self.to_little(self.he[12:14])        
        #     self.chargertemperature=int(ap,16)


        if self.message.arbitration_id==0x182:
            self.a=bytearray(self.message.data)
            self.he=self.a.hex() #converting bytearray to hex format

            aq= self.to_little(self.he[0:4])
            self.batterycurrent=int(aq,16)
            self.batterycurrent= self.twos_comp(self.batterycurrent,16)*0.1
            
            ar= self.to_little(self.he[4:8])
            self.batteryvoltage=int(ar,16)*0.1

        elif self.message.arbitration_id==0x183:
            self.a=bytearray(self.message.data)
            self.he=self.a.hex() #converting bytearray to hex format

            _as= self.to_little(self.he[0:2])
            self.batterysoc=int(_as,16)*0.5
        
            at= self.to_little(self.he[2:6])
            self.batteryamphours=int(at,16)*0.1

            au= self.to_little(self.he[6:8])
            self.batteryhighesttemperature=int(au,16)
            self.batteryhighesttemperature=self.twos_comp(self.batteryhighesttemperature,8)*1

            av=self.to_little(self.he[8:10])
            self.highesttemperaturethermistorid=int(av,16)*1
            
            aw=self.to_little(self.he[10:12])
            self.batterylowesttemperature=int(aw,16)
            self.batterylowesttemperature=self.twos_comp(self.batterylowesttemperature,8)*1

            ax=self.to_little(self.he[12:14])
            self.highestlowestthermistorid=int(ax,16)*1

            ay=self.to_little(self.he[14:16])
            self.batteryaveragetemperature=int(ay,16)
            self.batteryaveragetemperature=self.twos_comp(self.batteryaveragetemperature,8)*1

        elif self.message.arbitration_id==0x184:
            self.a=bytearray(self.message.data)
            self.he=self.a.hex()

            az= self.to_little(self.he[0:2])   
            self.bmstemperature=int(az,16)
            self.bmstemperature=self.twos_comp(self.bmstemperature,8)*1

            ba= self.to_little(self.he[2:4])
            self.batteryadaptivesoc=int(ba,16)*0.5

            bb=self.to_little(self.he[4:8])
            self.batteryadaptiveamphours=int(bb,16)*0.1

            bc=self.to_little(self.he[8:12])
            self.auxilarybatteryvoltage=int(bc,16)*0.1


        # elif self.message.arbitration_id==0x185:
        #     self.a=bytearray(self.message.data)
        #     self.he=self.a.hex()

        #     bd =self.to_little(self.he[0:2])
        #     self.bpfailsafestatus=int(bd,16)
        #     if self.bpfailsafestatus==0:
        #         self.bpfailsafestatus="Voltage failsafe active"

        #     elif self.bpfailsafestatus==1:
        #         self.bpfailsafestatus="Current failsafe Active"

        #     elif self.bpfailsafestatus==2:
        #         self.bpfailsafestatus="Relay failsafe Active"    

        #     elif self.bpfailsafestatus==3:
        #         self.bpfailsafestatus="Cell balancing Active"    

        #     elif self.bpfailsafestatus==4:
        #         self.bpfailsafestatus="Charge interlock failsafe Active"    

        #     elif self.bpfailsafestatus==5:
        #         self.bpfailsafestatus="Thermistor B-value table invalid"    

        #     elif self.bpfailsafestatus==6:
        #         self.bpfailsafestatus="Input power supply faisafe Active"

        #     elif self.bpfailsafestatus==7:
        #         self.bpfailsafestatus="RESERVED"    

            # bdd =self.to_little(self.he[2:4])
            # self.bpfailsafestatus=int(bdd,16)
            # self.bpfailsafestatus="RESERVED"

            # be=self.to_little(self.he[4:6])
            # self.dtcstatus1=int(be,16)
            # if self.dtcstatus1==0:
            #     self.dtcstatus1="0A07(Discharge Limit Enforcement Fault)"

            # elif self.dtcstatus1==1:
            #     self.dtcstatus1="P0A08(Charger Safety Relay Fault)"    

            # elif self.dtcstatus1==2:
            #     self.dtcstatus1="P0A09(Internal Hardware Fault)"    

            # elif self.dtcstatus1==3:
            #     self.dtcstatus1="P0A0A(Internal Heatsink Thermistor Fault)"    

            # elif self.dtcstatus1==4:
            #     self.dtcstatus1="P0A0B(Internal Software Fault)"    

            # elif self.dtcstatus1==5:
            #     self.dtcstatus1="P0A0C(Highest Cell Voltage Too High Fault)"

            # elif self.dtcstatus1==6:
            #     self.dtcstatus1="P0A0E(Lowest Cell Voltage Too Low Fault)"

            # elif self.dtcstatus1==7:
            #     self.dtcstatus1="P0A10 (Pack Too Hot Fault)"

            # bee=self.to_little(self.he[6:8])
            # self.dtcstatus1=int(bee,16)
            # self.dtcstatus1="RESERVED"

        #     bf=self.to_little(self.he[8:10])
        #     self.dtcstatus2=int(bf,16)

        #     if self.dtcstatus2==0:
        #         self.dtcstatus2="P0A1F (Internal Communication Fault)"

        #     elif self.dtcstatus2==1:
        #         self.dtcstatus2="P0A12 (Cell Balancing Stuck Off Fault)"    

        #     elif self.dtcstatus2==2:
        #         self.dtcstatus2="P0A80 (Weak Cell Fault)"    

        #     elif self.dtcstatus2==3:
        #         self.dtcstatus2="P0AFA (Low Cell Voltage Fault)"    

        #     elif self.dtcstatus2==4:
        #         self.dtcstatus2="P0A04 (Open Wiring Fault)"    

        #     elif self.dtcstatus2==5:
        #         self.dtcstatus2="P0AC0 (Current Sensor Fault)"

        #     elif self.dtcstatus2==6:
        #         self.dtcstatus2="P0A0D (Highest Cell Voltage Over 5V Fault)"

        #     elif self.dtcstatus2==7:
        #         self.dtcstatus2="P0A0F (Cell ASIC Fault)"

        #     bff=self.to_little(self.he[10:12])
        #     self.dtcstatus2=int(bff,16)

        #     if self.dtcstatus2==0:
        #         self.dtcstatus2="P0A02 (Weak Pack Fault)"

        #     elif self.dtcstatus2==1:
        #         self.dtcstatus2="P0A81 (Fan Monitor Fault)"    

        #     elif self.dtcstatus2==2:
        #         self.dtcstatus2="P0A9C (Thermistor Fault)"    

        #     elif self.dtcstatus2==3:
        #         self.dtcstatus2="U0100 (External Communication Fault)"    

        #     elif self.dtcstatus2==4:
        #         self.dtcstatus2="P0560 (Redundant Power Supply Fault)"    

        #     elif self.dtcstatus2==5:
        #         self.dtcstatus2="P0AA6 (High Voltage Isolation Fault)"

        #     elif self.dtcstatus2==6:
        #         self.dtcstatus2="P0A05 (Input Power Supply Fault)"

        #     elif self.dtcstatus2==7:
        #         self.dtcstatus2="P0A06 (Charge Limit Enforcement Fault)"

            
        #     bg=self.to_little(self.he[12:14])
        #     self.currentlimitstatus=int(bg,16)

        #     if self.currentlimitstatus==0:
        #         self.currentlimitstatus="DCL Reduced Due To Low SOC"

        #     elif self.currentlimitstatus==1:
        #         self.currentlimitstatus="DCL Reduced Due To High Cell Resistance"    

        #     elif self.currentlimitstatus==2:
        #         self.currentlimitstatus="DCL Reduced Due To Temperature"    

        #     elif self.currentlimitstatus==3:
        #         self.currentlimitstatus="DCL Reduced Due To Low Cell Voltage"    

        #     elif self.currentlimitstatus==4:
        #         self.currentlimitstatus="DCL Reduced Due To Low Pack Voltage"    

        #     elif self.currentlimitstatus==5:
        #         self.currentlimitstatus="RESERVED"

        #     elif self.currentlimitstatus==6:
        #         self.currentlimitstatus="DCL and CCL Reduced Due To Voltage Failsafe"

        #     elif self.currentlimitstatus==7:
        #         self.currentlimitstatus="Bit 7: DCL and CCL Reduced Due To Communication Failsafe"

        #     bgg=self.to_little(self.he[14:16])
        #     self.currentlimitstatus=int(bgg,16)

        #     if self.currentlimitstatus==0:
        #         self.currentlimitstatus="RESERVED"

        #     elif self.currentlimitstatus==1:
        #         self.currentlimitstatus="CCL Reduced Due To High SOC"    

        #     elif self.currentlimitstatus==2:
        #         self.currentlimitstatus="CCL Reduced Due To High Cell Resistance"    

        #     elif self.currentlimitstatus==3:
        #         self.currentlimitstatus="CCL Reduced Due To Temperature"    

        #     elif self.currentlimitstatus==4:
        #         self.currentlimitstatus="CCL Reduced Due To High Cell Voltage"    

        #     elif self.currentlimitstatus==5:
        #         self.currentlimitstatus="CCL Reduced Due To High Pack Voltage"

        #     elif self.currentlimitstatus==6:
        #         self.currentlimitstatus="CCL Reduced Due To Charger Latch"

        #     elif self.currentlimitstatus==7:
        #         self.currentlimitstatus="CCL Reduced Due To Alternate Current Limit [MPI]"

        # elif self.message.arbitration_id==0x186:
        #     self.a=bytearray(self.message.data)
        #     self.he=self.a.hex()

        #     bh=self.to_little(self.he[0:4])
        #     self.j1772currentlimit=int(bh,16)*1

        #     bi=self.to_little(self.he[4:6])
        #     self.j1772plugstate=int(bi,16)
        #     if self.j1772plugstate==0:
        #         self.j1772plugstate="Invalid State"

        #     elif self.j1772plugstate==1:
        #         self.j1772plugstate="Disconnected State"    

        #     elif self.j1772plugstate==2:
        #         self.j1772plugstate="Abort State"

        #     elif self.j1772plugstate==3:
        #         self.j1772plugstate="Ready State"

        #     elif self.j1772plugstate==4:
        #         self.j1772plugstate="Charging State"

        #     bj=self.to_little(self.he[6:10])
        #     self.batteryadaptivetotalcapacity=int(bj,16)*0.1

        #     bk=self.to_little(self.he[10:14])
        #     self.batterytotalcycles=int(bk,16)*1

        #     bl=self.to_little(self.he[14:16])
        #     self.batterysoh=int(bl,16)*1




    def table1(self):
        while True:
            self.can_data()
            file= open("mytext.txt","w")
            self.table=[["Name", "Value"],["Controller Status", self.controllerstatus],["CANopen error", self.canopenerror],["Error Registor", self.errorregistor],["FaultCode",self.faultcode],["Battery Discharge Limit", self.batterydischargelimit],["BatteryChargeLimit", self.batterychargelimit],["BatteryDischargeStatus", self.batterydischargestatus],["ChargeInterlockState",self.chargeinterlockstate],["BatteryMPEStatus",self.batteryMPEstatus],["Ready Power",self.readypower],["Charge Power",self.chargepower],["ChargerHighestVoltage",self.chargerhighestvoltage],["ChargerHighestCurrent", self.chargerhighestcurrent],["ChargeStatus",self.chargestatus],["Charger Mode",self.chargermode],["ChargerOutputVoltage",self.chargeroutputvoltage],["ChargerOutputCurrent",self.chargeroutputcurrent],["Charger Status",self.chargerstatus],["ChargerTemperature",self.chargertemperature],["BatteryCurrent",self.batterycurrent],["BatteryVoltage",self.batteryvoltage],["BatterySOC",self.batterysoc],["BatteryAmphours",self.batteryamphours],["BatteryHighestTemperature",self.batteryhighesttemperature],["HighestTemperatureThermistorID",self.highesttemperaturethermistorid],["BatteryLowestTemperature",self.batterylowesttemperature],["HighestLowestThermistorID",self.highestlowestthermistorid],["BatteryAverageTemperature",self.batteryaveragetemperature],["BMSTemperature",self.bmstemperature],["BatteryAdaptiveSOC",self.batteryadaptivesoc],["BatteryAdaptiveAmphours",self.batteryadaptiveamphours],["AuxilaryBatteryVoltage",self.auxilarybatteryvoltage],["BP Failsafe status",self.bpfailsafestatus],["DTC Status 1",self.dtcstatus1],["DTC Status 2",self.dtcstatus2],["Current Limit Status",self.currentlimitstatus],["J1772CurrentLimit",self.j1772currentlimit],["J1772PlugState",self.j1772plugstate],["BatteryAdaptiveTotalCapacity",self.batteryadaptivetotalcapacity],["BatteryTotalCycles",self.batterytotalcycles], ["BatterySOH",self.batterysoh]]
            a=tabulate(self.table, headers="firstrow", tablefmt="pretty")
            file.write(str(a))
            file.close()
            # b=str(a)
            # print(b)
            return a

    def valuess(self):
        # while True:
        self.can_data()
        
        self.values_to_add= ["Controller Status", self.controllerstatus],["CANopen error", self.canopenerror],["Error Registor", self.errorregistor],["FaultCode",self.faultcode],["Battery Discharge Limit", self.batterydischargelimit],["BatteryChargeLimit", self.batterychargelimit],["BatteryDischargeStatus", self.batterydischargestatus],["ChargeInterlockState",self.chargeinterlockstate],["BatteryMPEStatus",self.batteryMPEstatus],["Ready Power",self.readypower],["Charge Power",self.chargepower],["ChargerHighestVoltage",self.chargerhighestvoltage],["ChargerHighestCurrent", self.chargerhighestcurrent],["ChargeStatus",self.chargestatus],["Charger Mode",self.chargermode],["ChargerOutputVoltage",self.chargeroutputvoltage],["ChargerOutputCurrent",self.chargeroutputcurrent],["Charger Status",self.chargerstatus],["ChargerTemperature",self.chargertemperature],["BatteryCurrent",self.batterycurrent],["BatteryVoltage",self.batteryvoltage],["BatterySOC",self.batterysoc],["BatteryAmphours",self.batteryamphours],["BatteryHighestTemperature",self.batteryhighesttemperature],["HighestTemperatureThermistorID",self.highesttemperaturethermistorid],["BatteryLowestTemperature",self.batterylowesttemperature],["HighestLowestThermistorID",self.highestlowestthermistorid],["BatteryAverageTemperature",self.batteryaveragetemperature],["BMSTemperature",self.bmstemperature],["BatteryAdaptiveSOC",self.batteryadaptivesoc],["BatteryAdaptiveAmphours",self.batteryadaptiveamphours],["AuxilaryBatteryVoltage",self.auxilarybatteryvoltage],["BP Failsafe status",self.bpfailsafestatus],["DTC Status 1",self.dtcstatus1],["DTC Status 2",self.dtcstatus2],["Current Limit Status",self.currentlimitstatus],["J1772CurrentLimit",self.j1772currentlimit],["J1772PlugState",self.j1772plugstate],["BatteryAdaptiveTotalCapacity",self.batteryadaptivetotalcapacity],["BatteryTotalCycles",self.batterytotalcycles], ["BatterySOH",self.batterysoh]
        
        return self.values_to_add
        

    def valuess1(self):
        # while True:
        self.can_data()
        # self.values_to_add= [self.controllerstatus, self.canopenerror, self.errorregistor,self.faultcode, self.batterydischargelimit, self.batterychargelimit,self.batterydischargestatus,self.chargeinterlockstate,self.batteryMPEstatus,self.readypower,self.chargepower,self.chargerhighestvoltage, self.chargerhighestcurrent,self.chargestatus,self.chargermode,self.chargeroutputvoltage,self.chargeroutputcurrent,self.chargerstatus,self.chargertemperature,self.batterycurrent,self.batteryvoltage,self.batterysoc,self.batteryamphours,self.batteryhighesttemperature,self.highesttemperaturethermistorid,self.batterylowesttemperature,self.highestlowestthermistorid,self.batteryaveragetemperature,self.bmstemperature,self.batteryadaptivesoc,self.batteryadaptiveamphours,self.auxilarybatteryvoltage,self.bpfailsafestatus,self.dtcstatus1,self.dtcstatus2,self.currentlimitstatus,self.j1772currentlimit,self.j1772plugstate,self.batteryadaptivetotalcapacity,self.batterytotalcycles,self.batterysoh]
        self.values_to_add= [self.batterycurrent,self.batteryvoltage,self.batterysoc,self.batteryamphours,self.batteryhighesttemperature,self.highesttemperaturethermistorid,self.batterylowesttemperature,self.highestlowestthermistorid,self.batteryaveragetemperature,self.bmstemperature,self.batteryadaptivesoc,self.batteryadaptiveamphours,self.auxilarybatteryvoltage]
        return self.values_to_add    


# A= Dataa()
# A.valuess1() 
# A.valuess()  
# A.terminal_update()
# while True:
#     a=A.valuess()

#     print(a)
# A.spe() 
# while True:
#     A.table1()
