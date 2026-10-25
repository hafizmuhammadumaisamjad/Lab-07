
# Add a GB conversion line to the storage estimator


UNITS = {
	"B": 1,
	"KB": 1_000,
	"MB": 1_000_000,
	"GB": 1_000_000_000,
	"TB": 1_000_000_000_000,
	"KIB": 1_024,
	"MIB": 1_048_576,
	"GIB": 1_073_741_824,
	"TIB": 1_099_511_627_776,
}


def read_number(prompt, minimum=0, allow_zero=False):
	"""Read a valid numeric value from the user."""
	while True:
		try:
			value = float(input(prompt))
			if value >= minimum and (allow_zero or value > minimum):
				return value
		except ValueError:
			pass
		comparison = "at least" if allow_zero else "greater than"
		print(f"Enter a number {comparison} {minimum}.")


def read_unit(prompt):
	"""Read a supported storage unit."""
	available = ", ".join(UNITS)
	while True:
		unit = input(f"{prompt} ({available}): ").strip().upper()
		if unit in UNITS:
			return unit
		print("Unsupported unit. Please choose one from the list.")


def format_size(byte_count):
	"""Format bytes using the largest suitable decimal unit."""
	for unit in ("TB", "GB", "MB", "KB"):
		if byte_count >= UNITS[unit]:
			return f"{byte_count / UNITS[unit]:,.2f} {unit}"
	return f"{byte_count:,.0f} B"


def main():
	print("Storage Estimator")
	print("Estimate the space needed for files and compare it with a drive.\n")

	while True:
		try:
			file_count = int(input("Number of files: "))
			if file_count > 0:
				break
		except ValueError:
			pass
		print("Enter a whole number greater than zero.")

	average_size = read_number("Average file size: ")
	file_unit = read_unit("File size unit")
	drive_size = read_number("Drive capacity: ")
	drive_unit = read_unit("Drive capacity unit")

	while True:
		reserve = read_number("Space to keep free (percent, 0-100): ", allow_zero=True)
		if reserve <= 100:
			break
		print("The reserve cannot exceed 100%.")

	required = file_count * average_size * UNITS[file_unit]
	capacity = drive_size * UNITS[drive_unit]
	usable = capacity * (1 - reserve / 100)
	difference = usable - required

	print("\nEstimate")
	print(f"  Files:             {file_count:,}")
	print(f"  Required storage:  {format_size(required)}")
	print(f"  Drive capacity:    {format_size(capacity)}")
	print(f"  Usable capacity:   {format_size(usable)}")
	if difference >= 0:
		print(f"  Space remaining:   {format_size(difference)}")
		print("  Result: The files should fit.")
	else:
		print(f"  Space shortfall:   {format_size(-difference)}")
		print("  Result: A larger drive or less data is needed.")


if __name__ == "__main__":
	main()
