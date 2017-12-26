
def create_C1(data_set):
    """
    Create frequent candidate 1-itemset C1 by scaning data set.
    """
    C1 =set()#集合
    for t in data_set:
        for item in t:
            item_set = frozenset([item])#非重复元素
            C1.add(item_set)
    print("C1 is created")
    return C1


def is_apriori(Ck_item, Lksub1):
    """
    Judge whether a frequent candidate k-itemset satisfy Apriori property.
    剪枝
    """
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True


def create_Ck(Lksub1, k):
    """
    Create Ck, a set which contains all all frequent candidate k-itemsets
    by Lk-1's own connection operation.
    Lk-1==Lk-1->Ck
    连接
    """
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                # pruning
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    print("Ck is created by Lk-1")
    return Ck


def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    """
    Generate Lk by executing a delete policy from Ck.
    频繁项目集筛选
    """
    Lk = set()
    item_count = {}#li出现的次数
    for t in data_set:
        for item in Ck:
            if item.issubset(t):#Ck是t的子集
                if item not in item_count:
                    item_count[item] = 1#第一次出现
                else:
                    item_count[item] += 1
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    print("Lk is created by Ck")
    return Lk


def generate_L(data_set, k, min_support,support_data):
    """
    Generate all frequent itemsets.
    所有频繁项目集,最大k-项集
    """
    #support_data = {}#字典-支持度
    C1 = create_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    
    L = []#L1,L2,L3……
    Lksub1 = L1.copy()
    L.append(Lksub1)
    for i in range(2, k+1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support/2**(i-1), support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    print("All the frequent itemsets L is created")
    return L, support_data


def generate_big_rules(L, support_data, min_conf):
    """
    Generate big rules from frequent itemsets.
    强关联规则
    """
    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list
