'''
apriori實作
給定transactions和min support (頻率)，實作演算法找出frequent patterns

執行: python3 你的學號_hw2.py [min support] [輸入檔名] [輸出檔名]

'''
import sys
from itertools import combinations
from decimal import Decimal


class Apriori(object):
    def __init__(self):
        self.min_support = float(sys.argv[1])
        self.input_file = sys.argv[2]
        self.output_file = sys.argv[3]
        # self.min_support = 0.2
        # self.input_file = 'sample.txt'
        # self.output_file = 'sample_output2.txt'
        self.output_list = []
        self.apriori()

    def create_c(self, input_data, pre_l_list, level):
        new_itemSet = []
        for item in pre_l_list:
            for i in item[0]:
                if i not in new_itemSet:
                    new_itemSet.append(i)

        new_itemSet = list(combinations(sorted(new_itemSet), level))  # 計算不重複組合
        new_itemSet = [list(i) for i in new_itemSet]
        new_support = [0] * len(new_itemSet)

        for i in input_data:
            for j in new_itemSet:
                if all(idx in i for idx in j):
                    new_support[new_itemSet.index(j)] += 1

        return new_itemSet, new_support

    def create_l(self, c_itemset, c_support, total):
        l_combine = []
        for item, sup in zip(c_itemset, c_support):
            sup = Decimal.from_float(sup/total)
            if sup >= self.min_support:  # 保留c中大於min sup
                x = [item, round(sup, 4)]  # 輸出四捨五入
                l_combine.append(x)

        self.output_queue(l_combine)

        return l_combine

    def output_queue(self, result_list):
        for i in result_list:
            self.output_list.append(i)

    def apriori(self):
        with open(self.input_file, 'r') as f:
            _input_data = f.read().splitlines()
            _input_data = [x.split(',') for x in _input_data]
            input_data = []
            for i in _input_data:
                i = [int(j) for j in i]
                input_data.append(i)

        total = len(input_data)

        # C1 L1
        c1_itemSet = []
        c1_support = []
        for i in input_data:
            for j in i:
                if [j] not in c1_itemSet:
                    c1_itemSet.append([j])
                    c1_support.append(1)
                else:
                    c1_support[c1_itemSet.index([j])] += 1

        # filter out <min_support
        c_combine = []
        for item, sup in zip(c1_itemSet, c1_support):
            sup = Decimal.from_float(sup/total)
            if sup >= self.min_support:
                x = [item, round(sup, 4)]  # 輸出四捨五入
                c_combine.append(x)

        level = 2
        c_combine.sort(key=lambda x: x[0])
        self.output_queue(c_combine)
        # CN
        while bool(c_combine):
            c_itemSet, c_support = self.create_c(input_data, c_combine, level)  # 得到新的 C set
            c_combine = self.create_l(c_itemSet, c_support, total)  # 得到新的 L set
            level += 1

        with open(self.output_file, 'w') as f:
            for i in self.output_list:
                lst_new = [str(a) for a in i[0]]
                set_new = ",".join(lst_new)
                f.write(set_new + ':' + str(i[1]) + '\n')


if __name__ == '__main__':
    Apriori()
    # python hw2.py 0.2 sample.txt sample_output2.txt
