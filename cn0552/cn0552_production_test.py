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

def main(COMPORT_number, dev_name):
    try:
        import adi
        dev_ad7746 = adi.ad7746(uri="serial:" + COMPORT_number + ",115200,8n1", device_name=dev_name)
        print("Connected with CN0552 context at %s" % (COMPORT_number))
    except:
        print("No Device Found. Please make sure that your COM PORT number is correct.")
        sys.exit()

    def cap_channels(dev_channel, channel_name):
        try:
            raw_val = dev_ad7746.channel[dev_channel].raw
        except Exception as e:
            print("Device Error: " + str(e))
            sys.exit()

        try:
            scale_val = dev_ad7746.channel[dev_channel].scale
        except Exception as e:
            print("Device Error: " + str(e))
            sys.exit()

        meas_cap = float(raw_val) * float(scale_val)
        print("\tMeasured Capacitance: " + str(meas_cap) + " pF")

        # I'd set the range from 2pF to 3pF, the pin headers contribute to the measured capacitance around 0.5pF
        if (2.0 < meas_cap < 3.0):
            print("\n\t" + channel_name + " is GOOD!\n")
        else:
            print("\n\t" + channel_name + " FAILS!\n")
            failed_tests.append(channel_name + " out of range")


    input("\nStarting Production Test! Verify test jig is connected properly! Press enter to continue...")
    failed_tests = []

    # Normal Range Test
    print("\nStarting Normal Range Test...\n")

    # Channel 1 - CIN1(+) and EXCA pins 
    print("Channel 1\n")
    cap_channels("capacitance0", "Channel 1")

    # Channel 2 - CIN2(+) and EXCB pins 
    print("Channel 2\n")
    cap_channels("capacitance1", "Channel 2")

    # Extended Range Test
    input("Starting Extended Range Test! Measure the voltage at P14 then press enter to continue \n")
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

    COMPORT_number = "COM5" #Change this according to your device COM PORT number
    dev_name = "ad7746"

    main(COMPORT_number, dev_name)
