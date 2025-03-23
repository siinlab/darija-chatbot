"""This module replaces numbers in a string with their alphabetic representation."""

import re

from lgg import logger


def number_to_darija(n: int) -> str:  # noqa: C901, PLR0912
	"""Transform number from digits to Darija wording.

	Args:
		n (int): The number to be transformed.

	Returns:
		str: The alphabet-representation of the number.
	"""
	numbers = {
		0: "زيرو",
		1: "واحد",
		2: "جوج",
		3: "تلاتة",
		4: "ربعة",
		5: "خمسة",
		6: "ستة",
		7: "سبعة",
		8: "تمانية",
		9: "تسعة",
		10: "عشرة",
		11: "حداش",
		12: "تناش",
		13: "تلتاش",
		14: "ربعطاش",
		15: "خمسطاش",
		16: "سطاش",
		17: "سبعطاش",
		18: "ثمانطاش",
		19: "تسعطاش",
		20: "عشرين",
		21: "واحد و عشرين",
		22: "اتنين و عشرين",
		23: "تلاتة و عشرين",
		24: "ربعة و عشرين",
		25: "خمسة و عشرين",
		26: "ستة و عشرين",
		27: "سبعة و عشرين",
		28: "تمانية و عشرين",
		29: "تسعة و عشرين",
		30: "تلاتين",
		31: "واحد و تلاتين",
		32: "اتنين و تلاتين",
		33: "تلاتة و تلاتين",
		34: "ربعة و تلاتين",
		35: "خمسة و تلاتين",
		36: "ستة و تلاتين",
		37: "سبعة و تلاتين",
		38: "تمانية و تلاتين",
		39: "تسعة و تلاتين",
		40: "ربعين",
		41: "واحد و ربعين",
		42: "اتنين و ربعين",
		43: "تلاتة و ربعين",
		44: "ربعة و ربعين",
		45: "خمسة و ربعين",
		46: "ستة و ربعين",
		47: "سبعة و ربعين",
		48: "تمانية و ربعين",
		49: "تسعة و ربعين",
		50: "خمسين",
		51: "واحد و خمسين",
		52: "اتنين و خمسين",
		53: "تلاتة و خمسين",
		54: "ربعة و خمسين",
		55: "خمسة و خمسين",
		56: "ستة و خمسين",
		57: "سبعة و خمسين",
		58: "تمانية و خمسين",
		59: "تسعة و خمسين",
		60: "ستين",
		61: "واحد و ستين",
		62: "اتنين و ستين",
		63: "تلاتة و ستين",
		64: "ربعة و ستين",
		65: "خمسة و ستين",
		66: "ستة و ستين",
		67: "سبعة و ستين",
		68: "تمانية و ستين",
		69: "تسعة و ستين",
		70: "سبعين",
		71: "واحد و سبعين",
		72: "اتنين و سبعين",
		73: "تلاتة و سبعين",
		74: "ربعة و سبعين",
		75: "خمسة و سبعين",
		76: "ستة و سبعين",
		77: "سبعة و سبعين",
		78: "تمانية و سبعين",
		79: "تسعة و سبعين",
		80: "تمانين",
		81: "واحد و تمانين",
		82: "اتنين و تمانين",
		83: "تلاتة و تمانين",
		84: "ربعة و تمانين",
		85: "خمسة و تمانين",
		86: "ستة و تمانين",
		87: "سبعة و تمانين",
		88: "تمانية و تمانين",
		89: "تسعة و تمانين",
		90: "تسعين",
		91: "واحد و تسعين",
		92: "اتنين و تسعين",
		93: "تلاتة و تسعين",
		94: "ربعة و تسعين",
		95: "خمسة و تسعين",
		96: "ستة و تسعين",
		97: "سبعة و تسعين",
		98: "تمانية و تسعين",
		99: "تسعة و تسعين",
		100: "مية",
	}

	if n in numbers:
		return numbers[n]

	if n == 1_000_000_000:  # noqa: PLR2004
		return "مليار"
	if n > 1_000_000_000:  # noqa: PLR2004
		msg = "Number is too large to handle"
		raise ValueError(msg)

	parts = []

	# Handle millions
	if n >= 1_000_000:  # noqa: PLR2004
		millions_part = n // 1_000_000
		if millions_part == 1:
			parts.append("مليون")
		elif millions_part == 2:  # noqa: PLR2004
			parts.append("جوج ملاين")
		elif 3 <= millions_part <= 10:  # noqa: PLR2004
			parts.append(f"{number_to_darija(millions_part)} ملاين")
		else:
			parts.append(f"{number_to_darija(millions_part)} مليون")
		n %= 1_000_000

	# Handle thousands
	if n >= 1000:  # noqa: PLR2004
		thousands_part = n // 1000
		if thousands_part == 1:
			parts.append("ألف")
		elif thousands_part == 2:  # noqa: PLR2004
			parts.append("ألفين")
		elif 3 <= thousands_part <= 10:  # noqa: PLR2004
			parts.append(f"{number_to_darija(thousands_part)} آلاف")
		else:
			parts.append(f"{number_to_darija(thousands_part)} ألف")
		n %= 1000

	# Handle hundreds
	if n >= 100:  # noqa: PLR2004
		hundreds_part = n // 100
		if hundreds_part == 1:
			parts.append("مية")
		elif hundreds_part == 2:  # noqa: PLR2004
			parts.append("ميتين")
		else:
			parts.append(f"{number_to_darija(hundreds_part)} مية")
		n %= 100

	# Handle 1-99 using hardcoded values
	if n != 0:
		parts.append(numbers[n])

	return " و ".join(parts)


def transform_number_to_darija(text: str) -> str:
	"""Transform all numbers in a text from digits to Darija wording.

	Args:
		text (str): string potentially containing numbers.

	Returns:
		str: String where numbers are written using letters.
	"""
	try:
		numbers = re.findall(r"\d+", text)
		numbers = sorted(numbers, key=lambda x: len(x), reverse=True)
		for number in numbers:
			darija_number = number_to_darija(int(number))
			darija_number = f" {darija_number} "
			text = text.replace(number, darija_number)
	except Exception as e:  # noqa: BLE001
		logger.error(f"Failed to transform numbers to darija letters due to: {e}")
	return text
