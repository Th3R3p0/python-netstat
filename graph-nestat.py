import networkx as nx
import matplotlib.pyplot as plt
import netstat
import re

# note: this will graph origin/destination incorrectly if the listening port is no longer listening on the local address
conns = netstat.netstat()

ip = re.compile(r"[^:]*")

G = nx.DiGraph()


lports = []
for i in netstat.only_listening():
  source = re.findall(ip, i[3])
  try:
    if not (source[0] == '127.0.0.1' or source[0] == '127.0.1.1'):
      lports.append(source[2])
  except:
    pass

for i in conns:
  if i[5] == 'ESTABLISHED':
    src = re.findall(ip, i[3])
    dst = re.findall(ip, i[4])
    if not (src[0] == '127.0.0.1' or dst[0] == '127.0.0.1'):
      if src[2] in lports:
        G.add_edge(dst[0], src[0])
      else: 
        G.add_edge(src[0], dst[0])
nx.draw(G, with_labels=True)
plt.savefig('netstat.png')
