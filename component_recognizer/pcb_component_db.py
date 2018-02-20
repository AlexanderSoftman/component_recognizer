import logging
import csv
LOG = logging.getLogger(__name__)


# class get pcb file from kicad
# convert in to list of components component_description_list
class PCBComponentDB():

    component_description_list = []
    # dict describe position of parameters in format description:
    kicad_dot_pos_format_description = {
        "reference": 0,
        "value": 1,
        "package": 2,
        "pos_x": 3,
        "pos_y": 4,
        "rotation": 5,
        "side": 6
    }
    kicad_comment_symbol = "#"

    # input value - pcb_file_path
    def __init__(self, pcb_file_path):
        if self.check_kicad_name(pcb_file_path):
            self.parse_kicad_file(pcb_file_path)

    def parse_kicad_file(self, pcb_file_path):
        with open(pcb_file_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for component_line in spamreader:
                # generate new list
                # input: get list of elements
                # return empty elements
                # example:
                # input : ['D14', '', 'Green', '', 'LED_0603_1608Metric']
                # output: ['D14', 'Green', 'LED_0603_1608Metric']
                component_line_filtered = (
                    [x for x in component_line if x != ''])
                if (-1 == component_line_filtered[0].find(
                        self.kicad_comment_symbol)):
                    self.component_description_list.append(
                        component_line_filtered)

    # check that kicad file name have .pos postfix
    def check_kicad_name(self, pcb_file_path):
        # split one time by dot delimiter
        parts = pcb_file_path.rsplit('.', maxsplit=1)
        if parts[-1] == "pos":
            return True
        else:
            return False

