#                ©Daniil Samoylov               #
#                   @volyomaS                   #


from LSM_Tree import MemTable
from LSM_Tree import SSTable
from LSM_Tree import merge

my_SSTable = SSTable()
my_SSTable.set_filename("SSTable.txt")

my_MemTable = None
memSize = 0
max_Size = 5 # you need to change maxSize

while True:
    s = input().split()
    if s[0] == "append":
        key = s[1]
        value = s[2]
        memSize += 1
        if my_MemTable is None:
            my_MemTable = MemTable(key, value)
        else:
            my_MemTable.append(key, value)
        if memSize > max_Size:
            merge(my_MemTable, my_SSTable)
            my_MemTable = None
            memSize = 0
    elif s[0] == "exit":
        if my_MemTable is not None:
            merge(my_MemTable, my_SSTable)
        del my_MemTable
        break
    elif s[0] == "delete":
        try:
            if not my_MemTable.delete(s[1]):
                my_SSTable.delete(s[1])
        except AttributeError:
            my_SSTable.delete(s[1])
    elif s[0] == "get":
        try:
            val = my_MemTable.find(s[1])
            if val != -1:
                print(val)
            else:
                val = my_SSTable.find(s[1])
                if val != -1:
                    print(val)
                else:
                    print("There is no such key")
        except AttributeError:
            val = my_SSTable.find(s[1])
            if val != -1:
                print(val)
            else:
                print("There is no such key")
    elif s[0] == "clear":
        my_MemTable = None
        my_SSTable.clear()
