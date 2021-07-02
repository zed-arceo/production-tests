# Copyright (C) 2021 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys

def main(ser_add, dev_name):
    try:
        import adi
        dev_ad7746 = adi.ad7746(uri=ser_add, device_name=dev_name)
        print("AD7746")
    except:
        print("No Device Found")
        sys.exit()

    # Normal Range Test
    input("\nStarting Production Test! Make sure the setup is done! \nPress enter to continue...")
    failed_tests = []
    print("\nNormal Range Test")

    # Channel 1 - CIN1(+) and EXCA pins 
    print("Channel 1\n")

    try:
        raw_val = dev_ad7746.channel["capacitance0"].raw
        print("\tRaw: " + str(raw_val))
    except Exception as e:
        print("Device Error: " + str(e))
        sys.exit()

    try:
         scale_val = dev_ad7746.channel["capacitance0"].scale
         print("\tScale: " + str(scale_val))
    except Exception as e:
         print("Device Error: " + str(e))
         sys.exit()

    meas_cap = raw_val * scale_val
    print("\tMeasured Capacitance: " + str(meas_cap) + " pF")

    # I'd set the range from 2pF to 3pF, the pin headers contribute to the measured capacitance around 0.5pF
    if (2.0 < meas_cap < 3.0):
         print("\n\tChannel 1 is GOOD!\n")
    else:
        print("\n\tChannel 1 FAILS!\n")
        failed_tests.append("Channel 1 out of range")

    # Channel 2 - CIN2(+) and EXCB pins 
    print("Channel 2\n")

    try:
        raw_val = dev_ad7746.channel["capacitance1"].raw
        print("\tRaw: " + str(raw_val))
    except Exception as e:
        print("Device Error: " + str(e))
        sys.exit()

    try:
        scale_val = dev_ad7746.channel["capacitance1"].scale
        print("\tScale: " + str(scale_val))
    except Exception as e:
        print("Device Error: " + str(e))
        sys.exit()

    meas_cap = raw_val * scale_val
    print("\tMeasured Capacitance: " + str(meas_cap) + " pF")

    # I'd set the range from 2pF to 3pF, the pin headers contribute to the measured capacitance around 0.5pF
    if (2.0 < meas_cap < 3.0):
        print("\n\tChannel 2 is GOOD!\n")
    else:
        print("\n\tChannel 2 FAILS!\n")
        failed_tests.append("Channel 2 out of range")

    # Extended Range Test
    input("Starting Extended Range Test! Measure the voltage at P14 the press enter to continue \n")
    input("The measured voltage must be around 3.1volts, once done measuring, press enter.\n")

    print("\nExtended Range Test\n")

    #write a value of 0x1B to register address 0x9
    try:
        reg_access = dev_ad7746._ctrl.debug_attrs["direct_reg_access"].value = "0x9 0x1B"
    except Exception as e:
        print("Device Error: " + str(e))
        sys.exit()

    input("\nMeasure the voltage at P14 again! Then press enter to continue.")
    print("If the measured voltage was around 1.7 volts, enter P. Otherwise, enter F.\n")
    x = input("")
    if (x == "P"):
        print("\nExtended Range Test GOOD!\n")
    else:
        print("\nExtended Range Test Failed\n")
        failed_tests.append("Extended Range Test Failed")

    if len(failed_tests) == 0:
        print("Board PASSES")
    else:
        print("Board Failed the following test:")
        for fails in failed_tests:
            print(fails)

if __name__ == '__main__':

    ser_add = "serial:COM5,115200,8n1"
    dev_name = "ad7746"

    main(ser_add, dev_name)
