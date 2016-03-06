'''
Created on 3 de mar. de 2016

@author: fiutten
'''
import networkx as nx
import matplotlib.pyplot as plt

class semantic_graph:

    def __init__(self):
        self.edge_types = ['Ret','Sem','Prag']
        self.G = nx.lollipop_graph(100,50)
        self.createNodes()
        self.createEdges()
        self.createHubs()
        self.computeClusters()
        nx.draw(self.G)
        plt.show()
    
    def createNodes(self):
        nx.set_node_attributes(self.G,'iden',None)
        nx.set_node_attributes(self.G,'synsets',[])
        for i in self.G.nodes_iter():
            self.G.node[i]['iden'] = i  
        
   
    def createEdges(self):
        nx.set_edge_attributes(self.G,'iden',None)
        nx.set_edge_attributes(self.G,'weight',1)
        nx.set_edge_attributes(self.G,'type',[self.edge_types.__getitem__(0)])
        for i in self.G.edges_iter():
            self.G.edge[i[0]][i[1]]['iden']= i
            #print(self.G.edge[i[0]][i[1]])
        
    def createHubs(self):
        self.hub_vertexes = []
        self.non_hub_vertexes = []
        self.HVSs = []
        self.clusters = []    
        self.num_percentage_vertexes = 20
        self.num_hub_vertexes = int(self.G.number_of_nodes() * self.num_percentage_vertexes/100.0)
        self.hub_score = 1
        self.no_hub_score = 0.5
        
    def computeClusters(self):
        self.computeHVSs()
        
    def computeHVSs(self):
        # 1. Obtener los 'n' hub vertices y los 'N-n' no hub vertices.
        salience = generate_salience()
        ranking = salience.getSalienceRanking(self.G)
        stop = len(ranking) - self.num_hub_vertexes
        for i in range(len(ranking)-1,stop,-1):
            self.hub_vertexes.append(ranking[i])
            #print("Si",ranking[i].iden,ranking[i].neighbors)
        
        start = len(ranking) - self.num_hub_vertexes - 1
        for i in range(start,0,-1):
            self.non_hub_vertexes.append(ranking[i])
            #print("No",ranking[i].iden,ranking[i].neighbors)
            
        # 2. Inicialmente, creamos un HVS por cada Hub Vertice.
        for i in range(len(self.hub_vertexes)):
            node = self.hub_vertexes[i]
            hvs = []
            hvs.append(node)
            self.HVSs.append(hvs)
            
        # 3. Para cada hub vertice, comprobar si existe un HVS distinto al que pertenece
        #   con el que presente una mayor conectividad que al suyo propio.
        change = True
        while(change):
            change = False
            for i in range(len(self.HVSs)):
                vertexes = self.HVSs[i]
                for j in range(len(vertexes)):
                    node = vertexes[j]
                    intraconnection = self.getConnectionWithHVS2(node,self.HVSs[i])
                    interconnection = self.getMaxConnectionWithHVSs2(node,self.HVSs,intraconnection)
                    if interconnection[0] != -1 and interconnection[1] != 0: #Existe otro HVS con el que se encuentra más conectado.
                        #Cambiar al vértice de HVS.
                        change = True
                        self.HVSs[i].remove(j)
                        j = j - 1
                        self.HVSs[interconnection[0]].append(node)
                if len(self.HVSs[i]) == 0:
                    self.HVSs.remove(i)
                    i = i - 1
                    
        change = True
        while(change):
        # 4. Unir los HVS que presenten una conectividad interna menor que la que tienen entre sí.  
            for i in range(len(self.HVSs)):
                hvs1 = self.HVSs[i]
                for j in range(i,len(hvs1)):
                    hvs2 = self.HVSs[j]
                    intra_sim1 = self.getIntraSimilarity(hvs1)
                    intra_sim2 = self.getIntraSimilarity(hvs2)
                    inter_sim = self.getInterSimilarity(hvs1,hvs2)
                    if (inter_sim > intra_sim1 or inter_sim > intra_sim2):
                        # Unier ambos HVSs.
                        hvs1.append(hvs2)
                        self.HVSs.remove(j)
                        j = j - 1
                        change = True
                
    def getConnectionWithHVS2(self,node,vertexes):
        print("hola")
    
    def getMaxConnectionWithHVSs2(self,node,HVSs,intraconnection):
        print("hola")
    
    def getIntraSimilarity(self,hvs):
        print("hola")
    
    def getInterSimilarity(self,hvs1,hvs2):
        print("hola")
        
class generate_salience:
    
    def __init__(self):
        self.nodes = []
         
    def getSalienceRanking(self,G):
        for i in G.nodes_iter():
            new_salience = salience_node(G.node[i]["iden"],len(G.neighbors(i)))
            self.nodes.append(new_salience)
            #print(self.G.node[i])
        self.nodes = sorted(self.nodes, key = lambda salience_node: salience_node.neighbors)
        #for i in range(len(self.nodes)):
        #    print(self.nodes[i].iden)
        #    print(self.nodes[i].neighbors)
        return self.nodes
            
    
class salience_node: 
    
    def __init__(self,iden,neighbors):
        self.iden = iden
        self.neighbors = neighbors
        
