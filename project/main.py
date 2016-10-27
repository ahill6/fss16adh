from maxwalksat import mws
from simulatedannealer import annealer
from de import diffevolve
from particleswarm import pso
import sys


def prettyprint(self):
    if not isinstance(self, (list ,tuple)):
        show = [':%s %s' % (k, self.has()[k])
                for k in sorted(self.has().keys())
                if k[0] is not "_"]
        txt = ' '.join(show)
        if len(txt) > 60:
            show = map(lambda x: '\t' + x + '\n', show)
        return '{' + ' '.join(show) + '}'
    else:
        return str(self)

results = {}
file = ['specialization.xml']
method = [mws, annealer, diffevolve, pso]
out = open('output.txt', 'w')
for f in file:
    for m in method:
        out.write(str(f) + " using " + str(m) + "\n")
        print("running " + f)
        #results[str(m)+str(f)] = m(f)
        out.write(prettyprint(m(f)))
        out.write("\n")
print results
out.close()