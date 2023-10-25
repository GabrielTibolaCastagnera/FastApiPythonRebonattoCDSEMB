def indexOf(list, id):
    print(list)
    print(id)
    for estufa in list:
        if(estufa.id == id):
            return list.index(estufa)
    return None