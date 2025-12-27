
class TxtStorage:

    def read_day(self, filename, date):
        notes = []
        printing = False

        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.rstrip("\n")
                if line.startswith("===") and printing:
                    break
                if line == date:
                    printing = True
                if printing:
                    notes.append(line)

        return notes

    def create_new_day(self, filename, date):
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"=== {date[0]}-{int(date[1]):02d}-{int(date[2]):02d} ===\n")
            file.write("==================\n")

    def read_all_file(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            all_file = file.readlines()
            return all_file

    def write_all_lines(self, filename, all_file):
        with open(filename, "w", encoding="utf-8") as file:
            file.writelines(all_file)