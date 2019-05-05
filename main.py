#                ©Daniil Samoylov               #
#                   @volyomaS                   #


from LSM_Tree import MemTable
from LSM_Tree import SSTable
from LSM_Tree import merge

my_SSTable = SSTable()
my_SSTable.set_filename("SSTable.txt")

my_MemTable = None
memSize = 0
max_Size = 5  # you need to change maxSize

print("Type 'append key value' to insert element, 'delete key' to delete element\n"
      "with this key, 'get key' to get value of the key, 'clear' to delete all elements\n"
      "Type 'exit' to close")
while True:
    s = input().split()
    if s[0] == "append":
        key = s[1]
        value = s[2]
        try:
            if not my_MemTable.delete(s[1]):
                if not my_SSTable.delete(s[1]):
                    memSize += 1
        except AttributeError:
            if not my_SSTable.delete(s[1]):
                memSize += 1
        if my_MemTable is None:
            my_MemTable = MemTable(key, value)
        else:
            my_MemTable.append(key, value)
        print("Successfully appended")
        if memSize > max_Size:
            merge(my_MemTable, my_SSTable)
            print("Successfully merged")
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
                if my_SSTable.delete(s[1]):
                    print("Successfully deleted")
                else:
                    print("There is no such key")
            else:
                print("Successfully deleted")
        except AttributeError:
            if my_SSTable.delete(s[1]):
                print("Successfully deleted")
            else:
                print("There is no such key")
    elif s[0] == "get":
        try:
            val = my_MemTable.find(s[1])
            if val != -1 and val is not None:
                print(val)
            else:
                val = my_SSTable.find(s[1])
                if val != -1 and val is not None:
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
