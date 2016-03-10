'''
Created on 3 de mar. de 2016

@author: fiutten
'''
import networkx as nx
import random as rnd
import matplotlib.pyplot as plt

class semantic_graph:

    def __init__(self): #OK
        self.edge_types = ['Ret','Sem','Prag']
        self.G = nx.grid_graph([3,10])
        self.createNodes()
        self.createEdges()
        operations = graph_operations(self.G)
        operations.computeClusters()
        nx.draw(self.G)
        plt.show()
    
    def createNodes(self): #OK
        nx.set_node_attributes(self.G,'iden',None)
        nx.set_node_attributes(self.G,'concept',None)
        rnd.seed()
        for i in self.G.nodes_iter():
            self.G.node[i]['iden'] = i
            self.G.node[i]['concept'] = rnd.randint(0,10)
   
    def createEdges(self): #OK
        nx.set_edge_attributes(self.G,'iden',None)
        nx.set_edge_attributes(self.G,'weight',1)
        nx.set_edge_attributes(self.G,'type',[self.edge_types.__getitem__(0)])
        for i in self.G.edges_iter():
            self.G.edge[i[0]][i[1]]['iden']= i
        
class graph_operations:
    
    def __init__(self,G):
        self.nodes = []
        self.G = G
        self.createHubs()
        
    def createHubs(self):
        self.hub_vertexes = []
        self.non_hub_vertexes = []
        self.HVSs = []
        self.clusters = []    
        self.num_percentage_vertexes = 20
        self.num_hub_vertexes = int(self.G.number_of_nodes() * self.num_percentage_vertexes/100.0)
        self.hub_score = 1
        self.no_hub_score = 0.5
         
    def getSalienceRanking(self): #OK
        for i in self.G.nodes_iter():
            new_salience = salience_node(self.G.node[i]['iden'],len(self.G.neighbors(i)))
            self.nodes.append(new_salience)
        self.nodes = sorted(self.nodes, key = lambda salience_node: salience_node.neighbors)
        return self.nodes
    
    def computeClusters(self):
        # 1. Obtener los HVS.
        self.computeHVSs()
        # 2. Extraer los que tienen solo un elemento y pasarlos a la lista de non hub vertices.
        self.extractNodesWithOneVertex()
        # 3. Asignar los 'non hub vertices' a los clusters
        self.assignNonHubToClusters()
        for i in range(len(self.clusters)):
            print(self.clusters[i])
        
    def computeHVSs(self):
        # 1. Obtener los 'n' hub vertices y los 'N-n' no hub vertices.
        ranking = self.getSalienceRanking()
        stop = len(ranking) - self.num_hub_vertexes - 2
        for i in range(len(ranking)-1,stop,-1):
            self.hub_vertexes.append(ranking[i].getiden())
            #print("Si",ranking[i].iden,ranking[i].neighbors)
        
        start = len(ranking) - self.num_hub_vertexes - 2
        for i in range(start,0,-1):
            self.non_hub_vertexes.append(ranking[i].getiden())
            #print("No",ranking[i].iden,ranking[i].neighbors)
            
        # 2. Inicialmente, creamos un HVS por cada Hub Vertice.
        for i in range(len(self.hub_vertexes)):
            iden = self.hub_vertexes[i]
            hvs = []
            hvs.append(iden)
            self.HVSs.append(hvs)
            #print(self.HVSs)
        #OK    
        # 3. Para cada hub vertice, comprobar si existe un HVS distinto al que pertenece
        #   con el que presente una mayor conectividad que al suyo propio.
        change = True
        while(change):
            change = False
            i = 0
            while (i < len(self.HVSs)):
                vertexes = self.HVSs[i]
                j = 0
                while (j < len(vertexes)):
                    iden = vertexes[j]
                    intraconnection = self.getConnectionWithHVS2(iden,self.HVSs[i])
                    interconnection = self.getMaxConnectionWithHVSs2(iden,intraconnection)
                    if interconnection[0] != -1 and interconnection[1] != 0: # Existe otro HVS con el que se encuentra más conectado.
                        # Cambiar al vértice de HVS.
                        change = True
                        self.HVSs[i].pop(j)
                        self.HVSs[interconnection[0]].append(iden)
                    else:
                        j = j + 1
                if len(vertexes) == 0:
                    self.HVSs.pop(i)
                else:
                    i = i + 1
                    
        # 4. Unir los HVS que presenten una conectividad interna menor que la que tienen entre sí.  
        change = True
        while(change):
            change = False
            for i in range(len(self.HVSs)):
                hvs1 = self.HVSs[i]
                j = i
                while (j < len(self.HVSs)):
                    hvs2 = self.HVSs[j]
                    intra_sim1 = self.getIntraSimilarity(hvs1)
                    intra_sim2 = self.getIntraSimilarity(hvs2)
                    inter_sim = self.getInterSimilarity(hvs1,hvs2)
                    if (inter_sim > intra_sim1 or inter_sim > intra_sim2):
                        # Unir ambos HVSs.
                        self.HVSs[i].extend(hvs2)
                        self.HVSs.pop(j)
                        change = True
                    else:
                        j = j + 1
        
    # Función que devuelve el nodo del grafo que tiene el identificador indicado.
    def getNodeFromIden(self,iden):
        result = None
        for i in self.G.nodes_iter():
            node = self.G.node[i]
            if iden == node['iden']:
                result = node
                break
        return result                         
    
    # Función que devuelve el HVS con el que un concepto presenta una mayor conectividad, si esta supera su conectividad interna.
    def getMaxConnectionWithHVSs2(self,iden,intraconnection):
        max_connection = 0.0
        max_position = -1
        result = []
        result.append(-1)
        result.append(-1)
        for i in range(len(self.HVSs)):
            connection = self.getConnectionWithHVS2(iden,self.HVSs[i]);
            if (connection> max_connection):
                max_connection = connection
                max_position = i
        if (max_connection > intraconnection):
            result[0] = max_position
            result[1] = max_connection
        else:
            result[0] = -1;
            result[1] = -1;
        return result
    
    # Función que devuelve la conectividad de un concepto con respecto a un HVS.      
    def getConnectionWithHVS2(self,iden,vertexes):
        
        node = self.getNodeFromIden(iden)
        neighbors = self.G.neighbors(node['iden'])
        connection = 0.0
        for i in range(len(neighbors)):
            neighbor_iden = neighbors[i]
            if neighbor_iden in vertexes:
                neighbor = self.getNodeFromIden(neighbor_iden)
                if self.G.has_edge(node['iden'],neighbor['iden']):
                    edge_data = self.G.get_edge_data(node['iden'],neighbor['iden'])
                    connection = edge_data['weight']
                    break
        return connection   
    
    # Función que calcula la similitud (conectividad) entre los conceptos de un HVS.
    def getIntraSimilarity(self,vertexes):
        similarity = 0.0;
        for i in range(len(vertexes)):
            iden = vertexes[i]
            node = self.getNodeFromIden(iden)
            neighbors = self.G.neighbors(node['iden'])
            for j in range(len(neighbors)):
                neighbor_iden = neighbors[j]
                if neighbor_iden in vertexes:
                    neighbor = self.getNodeFromIden(neighbor_iden)
                    if self.G.has_edge(node['iden'],neighbor['iden']):
                        edge_data = self.G.get_edge_data(node['iden'],neighbor['iden'])
                        weight = edge_data['weight']
                        similarity = similarity + weight
        return similarity
    
    # Función que calcula la similitud (conectividad) entre dos HVSx.
    def getInterSimilarity(self,hvs1,hvs2):
        similarity = 0.0;
        for i in range(len(hvs1)):
            iden = hvs1[i]
            node = self.getNodeFromIden(iden)
            neighbors = self.G.neighbors(node['iden'])
            for j in range(len(neighbors)):
                neighbor_iden = neighbors[j]
                if neighbor_iden in hvs2:
                    neighbor = self.getNodeFromIden(neighbor_iden)
                    if self.G.has_edge(node['iden'],neighbor['iden']):
                        edge_data = self.G.get_edge_data(node['iden'],neighbor['iden'])
                        weight = edge_data['weight']
                        similarity = similarity + weight
        return similarity 
    
    # Método que elimina los HVSs con conectividad 1.
    def extractNodesWithOneVertex(self):
        i = 0
        while (i < len(self.HVSs)):
            vertexes = self.HVSs[i]
            if len(vertexes) <= 1:
                self.non_hub_vertexes.append(vertexes[0])
                self.HVSs.remove(vertexes)
            else:
                i = i + 1   
    
    # Método que asigna a los clusters los vértices Non-Hub más similares.
    def assignNonHubToClusters(self):
        self.clusters = []
        for i in range(len(self.HVSs)):
            self.clusters.append(self.HVSs[i])
        change = True
        while (change):
            change = False
            i = 0
            while (i < len(self.non_hub_vertexes)):
                non_hub_vertex = self.non_hub_vertexes[i]
                position = self.getMoreSimilarHVS(non_hub_vertex)
                if position != -1:
                    self.clusters[position].append(non_hub_vertex)
                    change = True
                    self.non_hub_vertexes.remove(non_hub_vertex);
                else:
                    i = i + 1
       
    # Dado un nodo, devuelve el HVS al que más se asemeja, y a cuyo cluster.             
    def getMoreSimilarHVS(self,iden):
        max_position = -1
        max_similarity = 0.0
        for i in range(len(self.HVSs)):
            similarity = 0.0
            vertexes = self.HVSs[i]
            for j in range(len(vertexes)):
                hv = vertexes[j]
                hvnode = self.getNodeFromIden(hv)
                node = self.getNodeFromIden(iden)
                pos = self.find(node,hvnode)
                if (pos != -1):
                    edge_data = self.G.get_edge_data(node['iden'],self.G.node[pos]['iden'])
                    weight = edge_data['weight']
                    similarity = similarity + weight
                if (similarity > max_similarity):
                    max_position = i
                    max_similarity = similarity
        return max_position
    
    def find(self,node1,node2):
        result = -1
        processed = []
        itr = nx.all_neighbors(self.G,node1['iden'])
        for i in itr:
            if i not in processed:
                processed.append(i)
                if self.G.node[i]['concept'] == node2['concept']:
                    result = self.G.node[i]['iden']
                    break
        return result
    
class salience_node: #OK
    
    def __init__(self,iden,neighbors):
        self.iden = iden
        self.neighbors = neighbors
    
    def getiden(self):
        return self.iden
    
    def getneighbors(self):
        return self.neighbors
        
    def __str__(self):
        iden = str(self.iden)
        neighbors = str(self.neighbors )
        return iden + ':' + neighbors
        
