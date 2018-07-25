# Voltage labels

VLABELS="REF1 REF2 4V0_A 3V3_A 6V0_A VIN 1V8_D 3V3_D 1V35 VCCPINT -6V0_A -3V3_A N/A N/A N/A N/A"

TARGET_VOLTAGES="0.239 0.461 N/A 3.30 6.00 5.00 1.80 3.30 1.35 1.00 -6.00 -3.30 N/A N/A N/A N/A"

# Board Off - Voltage Ranges
BOARD_OFF_VMIN="N/A N/A N/A N/A N/A -0.10 N/A N/A N/A N/A N/A N/A N/A N/A N/A N/A"
BOARD_OFF_VMAX="N/A N/A N/A N/A N/A 0.50 N/A N/A N/A N/A N/A N/A N/A N/A N/A N/A"

# Board On - Voltage Ranges
BOARD_ON_VMIN="0.235 0.456 N/A 3.20 5.90 4.50 1.70 3.20 1.30 0.95 -6.10 -3.40 N/A N/A N/A N/A"
BOARD_ON_VMAX="0.244 0.466 N/A 3.45 6.10 5.50 1.90 3.40 1.40 1.05 -5.90 -3.20 N/A N/A N/A N/A"

pre_measure() {
	toggle_pins GPIO_EXP1 pin6 pin4
}

post_measure() {
	toggle_pins GPIO_EXP1 pin4
}
