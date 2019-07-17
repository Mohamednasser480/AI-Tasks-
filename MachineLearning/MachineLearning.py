import math


class item:
    def __init__(self, age, prescription, astigmatic, tearRate, needLense):
        self.age = age
        self.prescription = prescription
        self.astigmatic = astigmatic
        self.tearRate = tearRate
        self.needLense = needLense


def getDataset():
    data = []
    labels = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]
    data.append(item(0, 0, 0, 0, labels[0]))
    data.append(item(0, 0, 0, 1, labels[1]))
    data.append(item(0, 0, 1, 0, labels[2]))
    data.append(item(0, 0, 1, 1, labels[3]))
    data.append(item(0, 1, 0, 0, labels[4]))
    data.append(item(0, 1, 0, 1, labels[5]))
    data.append(item(0, 1, 1, 0, labels[6]))
    data.append(item(0, 1, 1, 1, labels[7]))
    data.append(item(1, 0, 0, 0, labels[8]))
    data.append(item(1, 0, 0, 1, labels[9]))
    data.append(item(1, 0, 1, 0, labels[10]))
    data.append(item(1, 0, 1, 1, labels[11]))
    data.append(item(1, 1, 0, 0, labels[12]))
    data.append(item(1, 1, 0, 1, labels[13]))
    data.append(item(1, 1, 1, 0, labels[14]))
    data.append(item(1, 1, 1, 1, labels[15]))
    data.append(item(1, 0, 0, 0, labels[16]))
    data.append(item(1, 0, 0, 1, labels[17]))
    data.append(item(1, 0, 1, 0, labels[18]))
    data.append(item(1, 0, 1, 1, labels[19]))
    data.append(item(1, 1, 0, 0, labels[20]))
    return data


class Feature:
    def __init__(self, name):
        self.name = name
        self.visited = -1
        self.infoGain = -1


class node:
    def __init__(self, value):
        self.name = value
        self.right = -1
        self.left = -1
        self.value_0 = -1
        self.value_1 = -1
class ID3:

    def __init__(self, features):
        self.features = features

    def cal_total_entropy(self, dataset):
        zero = 0
        one = 0
        for i in range(len(dataset)):
            if dataset[i].needLense == 0:
                zero += 1
            else:
                one += 1
        return self.entropy(zero, one)

    def clean_column(self, dataset):
        clean = 1
        for i in range(len(dataset) - 1):
            if dataset[i].needLense != dataset[i+1].needLense:
                clean = 0
                break
        return clean

    def solve(self, newda, features1, parent_node, my):
        total_entropy = self.cal_total_entropy(newda)
        gainofdata = [0, 0, 0, 0]
        feature = features1[0]
        if feature.visited == -1:
            new_age = list()
            for i in newda:
                new_age.append(i.age)
            gainofdata[0] = self.gain(total_entropy, new_age, newda)
        feature = features1[1]
        if feature.visited == -1:
            new_prescription = list()
            for i in newda:
                new_prescription.append(i.prescription)
            gainofdata[1] = self.gain(total_entropy, new_prescription, newda)
        feature = features1[2]
        if feature.visited == -1:
            new_astigmatic = list()
            for i in newda:
                new_astigmatic.append(i.astigmatic)
            gainofdata[2] = self.gain(total_entropy, new_astigmatic, newda)
        feature = features1[3]
        if feature.visited == -1:
            new_tear_rate = list()
            for i in newda:
                new_tear_rate.append(i.tearRate)
            gainofdata[3] = self.gain(total_entropy, new_tear_rate, newda)
        ch = 1
        for i in gainofdata:
            if i != 0:
                ch = 0
        if ch:
            return
        table_one = list()
        table_zero = list()
        gain_max = -1
        if gainofdata[2] >= gainofdata[0] and gainofdata[2] >= gainofdata[1] and gainofdata[2] >= gainofdata[3]:
            features1[2].visited = 1
            gain_max = 2  # 2 == astigmatic
            for i in newda:
                if i.astigmatic == 0:
                    table_zero.append(i)
                else:
                    table_one.append(i)
        elif gainofdata[1] >= gainofdata[0] and gainofdata[1] >= gainofdata[2] and gainofdata[1] >= gainofdata[3]:
            features1[1].visited = 1
            gain_max = 1  # 1 == prescription
            for i in newda:
                if i.prescription == 0:
                    table_zero.append(i)
                else:
                    table_one.append(i)
        elif gainofdata[0] >= gainofdata[1] and gainofdata[0] >= gainofdata[2] and gainofdata[0] >= gainofdata[3]:
            features1[0].visited = 1
            gain_max = 0  # 0 == age
            for i in newda:
                if i.age == 0:
                    table_zero.append(i)
                else:
                    table_one.append(i)
        elif gainofdata[3] >= gainofdata[0] and gainofdata[3] >= gainofdata[1] and gainofdata[3] >= gainofdata[2]:
            features1[3].visited = 1
            gain_max = 3  # 3 == tearRate
            for i in newda:
                if i.tearRate == 0:
                    table_zero.append(i)
                else:
                    table_one.append(i)
        if len(table_one) > 0:
            if parent_node == -1:
                Graph.append(node(gain_max))
                if self.clean_column(table_one) == 1:
                    Graph[0].value_1 = table_one[0].needLense
                else:
                    self.solve(table_one, features1, 0, 1)
            else:
                Graph.append(node(gain_max))
                Graph[parent_node].right = my
                if self.clean_column(table_one) == 1:
                    Graph[my].value_1 = table_one[0].needLense
                else:
                    self.solve(table_one, features1, len(Graph)-1, my+1)

        if len(table_zero) > 0:
            if parent_node == -1:
                Graph.append(node(gain_max))
                if self.clean_column(table_zero) == 1:
                    Graph[0].value_0 = table_zero[0].needLense
                else:
                    self.solve(table_zero, features1, 0, 1)
            else:
                Graph.append(node(gain_max))
                Graph[parent_node].left = my
                if self.clean_column(table_zero) == 1:
                    Graph[my].value_0 = table_zero[0].needLense
                else:
                    self.solve(table_zero, features1, len(Graph)-1, my + 1)

    def classify(self, input):
        self.solve(dataset, features, -1, 0)
        now = 0
        while 1 == 1:
            inp = input[Graph[now].name]

            if inp == 1:
                if Graph[now].value_1 != -1:
                    return Graph[now].value_1
                else:
                    if Graph[now].right != -1:
                        now = Graph[now].right
                    else:
                        break
            else:
                if Graph[now].value_0 != -1:
                    return Graph[now].value_0
                else:
                    if Graph[now].left != -1:
                        now = Graph[now].left
                    else:
                        break

    def get_graph(self, current_node):
        if current_node.left != -1:
            self.get_graph(current_node.left)
        if current_node.right != -1:
            self.get_graph(current_node.right)

    def entropy(self, zero, one):
        total = zero + one
        if zero == 0:
            return - (one / total) * math.log2(one / total)
        elif one == 0:
            return -(zero / total) * math.log2(zero / total)
        return -(zero / total) * math.log2(zero / total) - (one / total) * math.log2(one / total)

    def gain(self, total_entropy, to_cal, dataset):
        zero_one = 0
        one_zero = 0
        zero_zero = 0
        one_one = 0
        for i in range(len(dataset)):
            if to_cal[i] == 0:
                if dataset[i].needLense == 0:
                    zero_zero += 1
                else:
                    zero_one += 1

            else:
                if dataset[i].needLense == 0:
                    one_zero += 1
                else:
                    one_one += 1
        return total_entropy - (one_one + one_zero) / len(dataset) * self.entropy(one_one, one_zero) - (
                    zero_one + zero_zero) / len(dataset) * self.entropy(zero_one, zero_zero)


dataset = getDataset()
features = [Feature('age'), Feature('prescription'), Feature('astigmatic'), Feature('tearRate')]


Graph = list()

id3 = ID3(features)
cls = id3.classify([0, 0, 1, 1])  # should print 1
print('testcase 1: ', cls)
cls = id3.classify([1, 1, 0, 0])  # should print 0
print('testcase 2: ', cls)
cls = id3.classify([1, 1, 1, 0])  # should print 0
print('testcase 3: ', cls)
cls = id3.classify([1, 1, 0, 1])  # should print 1
print('testcase 4: ', cls)