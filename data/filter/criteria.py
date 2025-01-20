"""This module defines the criteria for filtering data in the darija-tts project."""

CRITERIA = {
	"silence": {  # percentages
		"max": 80,
	},
	"duration": {  # seconds
		"min": 1,
		"max": 20,
	},
	"length": {  # characters
		"min": 2,
	},
	"snr": {  # decibels
		"min": -5,
	},
	"bias": {  # amplitude
		"min": 0.03,
	},
	"slope": {  # amplitude
		"min": -1e-6,
		"max": 1e-6,
	},
	"mean": {  # amplitude
	},
	"duration_length_ratio": {
		"min": 0.05,
		"max": 0.15,
	},
}
