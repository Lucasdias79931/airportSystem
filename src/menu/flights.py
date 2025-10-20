class Flight:
    #inteiros
    id = None
    price = None

    #Strings 
    source = None
    destination = None 

    #datas/tempo
    entryTime = None
    exitTime = None

    def __init__(self, id, price, source, destination, entryTime, exitTime):
        self.id = id
        self.price = price
        self.source = source
        self.destination = destination
        self.entryTime = entryTime
        self.exitTime = exitTime
        return 

#local onde irá ser colocado todos os voos
#chave vai ser o id do voo e o conteúdo vai ser a struct do voo em si
flights = {
        0: Flight(0, 10, "sp", "rj", 4, 12),
        1: Flight(1, 15, "ilhéus", "salvador", 12, 13),
} 
    
lastId = 1
