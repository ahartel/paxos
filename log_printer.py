import copy


class LogPrinter:
    def __init__(self, raw_log, num_endpoints, column_width=None):
        self.raw_log = raw_log
        self.num_endpoints = num_endpoints
        self.column_width = column_width
        self.max_column_widths = [0 for _ in range(self.num_endpoints)]

    def adjust_max_column_widths(self, message, endpoint_index):
        if len(message) > self.max_column_widths[endpoint_index]:
            self.max_column_widths[endpoint_index] = len(message)

    def prepare_rows_and_times(self):
        rows = []
        row = ["" for _ in range(self.num_endpoints)]
        current_time = self.raw_log[0][0]
        times = [current_time]
        for time, message, endpoint_index in self.raw_log:
            if time == current_time and row[endpoint_index] == "":
                row[endpoint_index] = message
            else:
                current_time = time
                times.append(current_time)
                rows.append(row)
                row = ["" for _ in range(self.num_endpoints)]
                row[endpoint_index] = message
            self.adjust_max_column_widths(message, endpoint_index)
        if not all(col == "" for col in row):
            rows.append(row)
        return times, rows

    def adjust_column_widths(self, rows):
        new_rows = []
        for row in rows:
            new_row = copy.copy(row)
            for index, col in enumerate(row):
                for _ in range(self.max_column_widths[index] - len(col)):
                    new_row[index] += " "
            new_rows.append(new_row)
        return new_rows

    def print_header(self, max_time_width):
        string = ' ' * (max_time_width+2)
        delimiter = ' ' * (max_time_width+2)
        for ep_index, width in enumerate(self.max_column_widths):
            number = str(ep_index)
            string += number
            string += ' ' * (width + 1 - len(number))
            delimiter += '=' * (width + 1)
        print(string)
        print(delimiter)

    def do_print(self, times, rows):
        max_time_width = len(str(times[-1]))
        self.print_header(max_time_width)
        for time, row in zip(times, rows):
            row_string = " ".join(row)
            time_string = str(time)
            for _ in range(max_time_width-len(time_string)):
                time_string += " "
            print("{}: {}".format(time_string, row_string))

    def print(self):
        times, rows = self.prepare_rows_and_times()
        rows = self.adjust_column_widths(rows)
        self.do_print(times, rows)

