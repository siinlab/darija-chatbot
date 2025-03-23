"""This module defines the criteria for filtering data in the darija-tts project."""

CRITERIA = {
	"silence": {  # percentages
		"max": 70,
	},
	"duration": {  # seconds
		"min": 1,
		"max": 29,
	},
	"length": {  # characters
		"max": 1000,
	},
	"snr": {  # decibels
		"min": -11,
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
	"duration_length_ratio": {  # seconds/character
		"min": 0.05,
		"max": 0.25,
	},
	"digits": {  # number of digits
		"max": 0,
	},
	"non_arabic": {  # number of non-Arabic characters
		"max": 0,
	},
}
