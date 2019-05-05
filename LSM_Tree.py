#                ©Daniil Samoylov               #
#                   @volyomaS                   #


class MemTable:
    size: int = 0

    def __init__(self, key, value):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.value = value
        self.size += 1

    def append(self, key, value):
        if key >= self.key:
            if self.right is not None:
                self.right.append(key, value)
            else:
                self.right = MemTable(key, value)
                self.right.parent = self
        else:
            if self.left is not None:
                self.left.append(key, value)
            else:
                self.left = MemTable(key, value)
                self.left.parent = self

    def min(self):
        curnode = self
        while curnode.left is not None:
            curnode = curnode.left
        return curnode

    def max(self):
        curnode = self
        while curnode.right is not None:
            curnode = curnode.right
        return curnode

    def next(self):
        curnode = self
        if curnode.right is not None:
            return curnode.right.min()
        p = curnode.parent
        while p is not None and curnode == p.right:
            curnode = p
            p = p.parent
        return p

    def prev(self):
        curnode = self
        if curnode.left is not None:
            return curnode.left.max()
        p = curnode.parent
        while p is not None and curnode == p.left:
            curnode = p
            p = p.parent
        return p

    def find(self, key):
        curnode = self
        if curnode.key == key:
            return curnode.value
        elif curnode.key < key:
            if curnode.right is not None:
                return curnode.right.find(key)
            else:
                return -1
        elif curnode.key > key:
            if curnode.left is not None:
                return curnode.left.find(key)
            else:
                return -1

    def delete(self, key):
        try:
            curnode = self
            if key > curnode.key and curnode.right is not None:
                curnode.right.delete(key)
            elif key < curnode.key and curnode.left is not None:
                curnode.left.delete(key)
            elif key == curnode.key:
                if curnode.right is not None and curnode.left is not None:
                    next = curnode.next()
                    curnode.key = next.key
                    curnode.value = next.value
                    next.delete(key)
                elif curnode.right is not None and curnode.left is None:
                    curnode.key = curnode.right.key
                    curnode.value = curnode.right.value
                    curnode.right = None
                    return True
                elif curnode.right is None and curnode.left is not None:
                    curnode.key = curnode.left.key
                    curnode.value = curnode.left.value
                    curnode.left = None
                    return True
                elif curnode.right is None and curnode.left is None:
                    if curnode.parent is not None:
                        p = curnode.parent
                        if p.left == curnode:
                            p.left = None
                        else:
                            p.right = None
                    return True
                return False
        except TypeError:
            pass


class SSTable:
    filename: str

    def __init__(self):
        self.filename = "SSTable.txt"
        self.data = []

    def set_filename(self, new_filename):
        self.filename = new_filename

    def delete(self, key):
        data = open(self.filename, "r").readlines()
        check = -1
        for i in range(len(data)):
            if data[i].split()[0] == key:
                check = i
                break
        if check != -1:
            fout = open(self.filename, "w")
            for i in range(len(data)):
                if i != check:
                    fout.write(data[i])
            fout.close()
            return True
        else:
            return False

    def find(self, key):
        data = open(self.filename, "r").readlines()
        check = -1
        for i in range(len(data)):
            if data[i].split()[0] == key:
                check = i
                break
        if check == -1:
            return -1
        else:
            return data[check].split()[1]

    def clear(self):
        open(self.filename, "w").write("")


def merge(my_MemTable, my_SSTable):
    new_data = []
    curm = my_MemTable.min()
    data = open(my_SSTable.filename, "r").readlines()
    curs = 0
    while curm is not None and curs < len(data):
        if curm.key < data[curs].split()[0]:
            new_data.append(str(curm.key) + " " + str(curm.value))
            curm = curm.next()
        else:
            new_data.append(data[curs])
            curs += 1
    if curm is None:
        while curs < len(data):
            new_data.append(data[curs])
            curs += 1
    else:
        while curm is not None:
            new_data.append(str(curm.key) + " " + str(curm.value))
            curm = curm.next()
    fout = open(my_SSTable.filename, "w")
    for line in new_data:
        fout.write(line.strip() + "\n")
    fout.close()
