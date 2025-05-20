from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._ret= DAO.getRet()
        self._idMap = {}
        for n in self._ret:
            self._idMap[n.Retailer_code]= n

    def buildGraph(self,country,anno):
        self.addNodi(country)
        self.addEdges(country,anno)

    def addNodi(self,country):
        ret= DAO.getRetailerCountry(country)
        for n in ret:
            self._grafo.add_node(n)

    def addEdges(self,country,anno):
        archi = DAO.getArchi(country,country,anno,self._idMap)
        for a in archi:
            self._grafo.add_edge(a[0],a[1],weight=a[2])


    def Anni(self):
        anni = DAO.getAnno()
        return anni

    def Nazioni(self):
        nazioni = DAO.getCountry()
        return nazioni

    def RetailerC(self,country):
        ret = DAO.getRetailerCountry(country)
        return ret

    def getVolume(self):
        list = []
        for n in self._grafo.nodes:
            vol = 0
            for n2 in self._grafo.neighbors(n):
                vol += self._grafo[n][n2]["weight"]
            list.append((n,vol))

        ord = sorted(list, key= lambda x:x[1], reverse=True)

        return ord

    def trova_ciclo_massimo(self,N):
        G = self._grafo
        best_path = []
        best_weight = 0

        def backtrack(current, start, path, visited, weight):
            nonlocal best_path, best_weight

            if len(path) == N:
                if G.has_edge(current, start):  # ciclo chiuso
                    total_weight = weight + G[current][start]['weight']
                    if total_weight > best_weight:
                        best_weight = total_weight
                        best_path = path + [start]
                return

            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    edge_weight = G[current][neighbor]['weight']
                    visited.add(neighbor)
                    backtrack(neighbor, start, path + [neighbor], visited, weight + edge_weight)
                    visited.remove(neighbor)

        for node in G.nodes():
            backtrack(node, node, [node], set([node]), 0)

        return best_path, best_weight
