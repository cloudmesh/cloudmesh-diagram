import json
import subprocess
import textwrap

from jinja2 import Template

from cloudmesh.common.util import path_expand


class Rack(object):
    def __init__(self, servers):
        self.template_string = None
        self.servers = servers
        self.diag = None
        self.data = None

    def set_template(self, template):

        if template is None:
            self.template_string = "rackdiag {" + '''
              // Change order of rack-number as ascending
              ascending;

              // define height of rack
              20U;

              // define description of rack
              description = "Cloudmesh Cluster Diagram";

              // define rack units
              1: UPS [2U];   // define height of unit
              3: Network [color=green]
              {% for x in range (0, 10) %}
              {{x+4}}: Server [''' + " ".join([
                '{{server[x]["label"]}}',
                '{{server[x]["numbered"]}}',
                '{{server[x]["fontsize"]}}',
                '{{server[x]["shape"]}}',
                '{{server[x]["textcolor"]}}',
                '{{server[x]["color"]}}'
            ]) + "]" + '''{% endfor %}''' + "\n}"
        else:
            self.template_string = template
        self.generate_rack(self.servers)

    def generate_rack(self, servers):
        empty = {
            "color": 'color="white" ',
            "label": "",
            "numbered": "",
            "fontsize": "",
            "shape": "",
            "textcolor": "",
        }
        self.data = []
        for server in range(0, servers):
            self.data.append(dict(empty))

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def dump(self):
        content = self.diag
        result = []
        counter = 1
        for line in content.splitlines():
            result.append("{0:>5}: {1}".format(counter, line))
            counter += 1
        return '\n'.join(result)

    def set(self, server, **kwargs):
        for attribute in kwargs:
            comma = ' '
            if attribute != 'color':
                comma = ', '
            value = kwargs[attribute]
            self.data[server - 1][attribute] = f'{attribute}="{value}"{comma}'

    def set_color(self, server, color):
        self.set(server, color=color)

    def set_label(self, server, label):
        self.set(server, label=label)

    def set_numbering(self, server, numbering):
        self.set(server, numbering=numbering)

    def set_fontsize(self, server, fontsize):
        self.set(server, fontsize=fontsize)

    def set_textcolorl(self, server, textcolorl):
        self.set(server, textcolorl=textcolorl)

    def set_shape(self, server, shape):
        self.set(server, shape=shape)

    def render(self):
        template = Template(textwrap.dedent(self.template_string))
        self.diag = template.render(server=self.data)
        return self.diag

    def diagram(self, name):
        filename = path_expand(name)
        with open(f'{name}.diag', 'w') as f:
            f.write(self.diag)

    def svg(self, name):
        filename = path_expand(name)
        self.diagram(filename)
        cmd = ['rackdiag', "-T", "svg", f"{filename}.diag"]
        subprocess.Popen(cmd).wait()

    def view(self, name):
        filename = path_expand(name)
        cmd = ['open', f"{filename}.svg"]
        subprocess.Popen(cmd)


if __name__ == "__main__":
    rack = Rack(10)
    rack.set_template(None)
    rack.set(10, color="blue")
    rack.set(9, color="green")
    rack.set(8, textcolor="red")
    rack.set(7, textsize="24")
    rack.set(7, shape="cloud")
    rack.set(6, numbered="1")
    rack.set_label(5, "red01\nabc")

    result = rack.render()
    # print rack.dump()

    name = "~/.cloudmesh/h"
    rack.svg(name)
    rack.view(name)

