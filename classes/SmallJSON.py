# DADSA - Assignment 1
# Reece Benson

import json

class SmallJSON(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(SmallJSON, self).__init__(*args, **kwargs)
        self.current_indent = 0
        self.current_indent_str = ""

    def encode(self, o):
        # Special process for list
        #  SRC: https://stackoverflow.com/a/26512016
        # EDIT: Edited to stop checking for primitives containing dicts, and edited what happens when dictionaries are within lists
        if isinstance(o, (list, tuple)):
            primitives_only = True
            for item in o:
                if isinstance(item, (list, tuple)):
                    primitives_only = False
                    break
            output = []
            if primitives_only:
                ## Modificaiton Processed Here for dictionaries within lists
                self.current_indent += self.indent
                self.current_indent_str = (" " * self.current_indent)
                for item in o:
                    output.append(self.current_indent_str + json.dumps(item))
                self.current_indent -= self.indent
                self.current_indent_str = (" " * self.current_indent)
                return "[ \n" + (",\n".join(output)) + "\n" + self.current_indent_str + "]"
            else:
                self.current_indent += self.indent
                self.current_indent_str = "".join( [ " " for x in range(self.current_indent) ])
                for item in o:
                    output.append(self.current_indent_str + self.encode(item))
                self.current_indent -= self.indent
                self.current_indent_str = "".join( [ " " for x in range(self.current_indent) ])
                return "[\n" + ",\n".join(output) + "\n" + self.current_indent_str + "]"
        elif isinstance(o, dict):
            output = []
            self.current_indent += self.indent
            self.current_indent_str = "".join( [ " " for x in range(self.current_indent) ])
            for key, value in o.items():
                output.append(self.current_indent_str + json.dumps(key) + ": " + self.encode(value))
            self.current_indent -= self.indent
            self.current_indent_str = "".join( [ " " for x in range(self.current_indent) ])
            return "{\n" + ",\n".join(output) + "\n" + self.current_indent_str + "}"
        else:
            return json.dumps(o)