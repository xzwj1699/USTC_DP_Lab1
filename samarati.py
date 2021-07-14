from os import X_OK, write
from typing import DefaultDict
import math
import sys

def samarati(data_file, k, maxSup, GT, vectors_list, LossTable):
    datas = []
    out_count = 0
    count = 0
    low, high = 0, 8
    for lines in data_file:
        out_count = out_count + 1
        if not '?' in lines:
            lines = lines.strip()
            age,gender,race,marital_state = lines.split(',')[0],lines.split(',')[9],lines.split(',')[8],lines.split(',')[5]
            datas.append([age,gender.strip(),race.strip(),marital_state.strip()])
    sol = None
    unsatisfy_list = []
    #pre define a large loss, and aim to minimize loss
    loss = 300.0
    while low < high: # to search a minimum vector that satisfy k-anonymity
        mid = math.floor((low + high) / 2)
        print("high : %d, low : %d, mid : %d" % (high, low, mid))
        vectors = vectors_list[mid]
        reach_k = False

        for vector in vectors:
            satisfy_or_not, temp_list = satisfy(datas, k, vector, GT, maxSup)
            # print('-----')
            # print(satisfy_or_not)
            if satisfy_or_not:
                lm = cal_loss_metric(datas, vector, GT, LossTable, temp_list)
                # print(lm)
                if lm < loss:
                    sol = vector
                    unsatisfy_list = temp_list
                    loss = lm
                    # print(loss)
                    # print(sol)
                reach_k = True
            # print('-----')
        if reach_k:
            high = mid
        else:
            low = mid + 1
    return sol, unsatisfy_list, loss
        

def cal_loss_metric(datas, sol, GT, LossTable, unsatisfy_list):
    age_lm, gender_lm, race_lm, marital_loss = 0, 0, 0, 0
    age_tree = GT['age']
    gender_tree = GT['gender']
    race_tree = GT['race']
    marital_state_tree = GT['marital_status']
    # print(len(datas))
    for line in datas:
        age,gender,race,marital_state = line[0],line[1],line[2],line[3]
        for i in range(0, sol[0]):
            age = age_tree[age]
        for i in range(0, sol[1]):
            gender = gender_tree[gender]
        for i in range(0, sol[2]):
            race = race_tree[race]
        for i in range(0, sol[3]):
            marital_state = marital_state_tree[marital_state]
        str1 = age + gender + race + marital_state
        if str1 in unsatisfy_list:
            age_lm += 1
            gender_lm += 1
            race_lm += 1
            marital_loss += 1
        else:
            age_lm += LossTable['age'][age]
            gender_lm += LossTable['gender'][gender]
            race_lm += LossTable['race'][race]
            marital_loss += LossTable['marital'][marital_state]
    return (age_lm + gender_lm + race_lm + marital_loss) / len(datas)

def satisfy(datas, k, vec, GT, maxSup):
    data_count = {}
    age_tree = GT['age']
    gender_tree = GT['gender']
    race_tree = GT['race']
    marital_state_tree = GT['marital_status']
    data_num = len(datas)
    for line in datas:
        age,gender,race,marital_state = line[0],line[1],line[2],line[3]
        #generalization according to vec
        for i in range(0, vec[0]):
            age = age_tree[age]
        for i in range(0, vec[1]):
            gender = gender_tree[gender]
        for i in range(0, vec[2]):
            race = race_tree[race]
        for i in range(0, vec[3]):
            marital_state = marital_state_tree[marital_state]
        str1 = age + gender + race + marital_state
        if str1 in data_count:
            data_count[str1] += 1
        else:
            data_count[str1] = 1
    unsatisfy_count = 0
    unsatisfy_list = []
    for key in data_count.keys():
        # print(str(data_count[key]) + " : " + str(k))
        if data_count[key] < k:
            unsatisfy_list.append(key)
            # print(key)
            unsatisfy_count = unsatisfy_count + data_count[key]
    
    # print(unsatisfy_count)
    # print("-----------------")
    if unsatisfy_count <= maxSup:
        return True, unsatisfy_list
    else:
        return False, None

#return if node x is a child of y
def is_child(GT : dict, x, y):
    while(x in GT.keys()):
        if GT[x] == y:
            return True
        x = GT[x]
    return False

#calculate the number of node rooted x
def cal_node_num(GT : dict, x):
    num = 0
    for key in GT.keys():
        if is_child(GT, key, x) and not key in GT.values():
            num += 1
    return num

def cal_generalization_loss(GT : dict):
    loss = {}
    tree_node = 0
    for key in GT.keys():
        if not key in GT.values():
            tree_node += 1
            loss[key] = 0
    for value in GT.values():
        loss[value] = (cal_node_num(GT, value) - 1) / (tree_node - 1)
    # print(loss)
    return loss

def main():
    data_file = open("data_privacy_lab1/adult.data",'r').readlines()
    generalization_tree = {}
    loss_table = {}
    #to calculate the loss of age, need get age tree node list 
    age_list = []
    for lines in data_file:
        if not '?' in lines:
            age = lines.split(',')[0]
            if not age in age_list:
                age_list.append(age)
    print(sorted(age_list))
    #build generalization trees
    
    #build gender generalization tree
    gender_tree = {}
    gender_height = 1
    for lines in open("data_privacy_lab1/adult_gender.txt",'r').readlines():
        lines = lines.strip()
        son_node,father_node = lines.split(',')[0], lines.split(',')[1]
        gender_tree[son_node] = father_node
    generalization_tree['gender'] = gender_tree
    
    # print(gender_tree)

    #build gender loss table
    gender_loss = cal_generalization_loss(gender_tree)
    loss_table['gender'] = gender_loss

    #build race generalization tree
    race_tree = {}
    race_height = 1
    for lines in open("data_privacy_lab1/adult_race.txt",'r'):
        lines = lines.strip()
        son_node,father_node = lines.split(',')[0], lines.split(',')[1]
        race_tree[son_node] = father_node
    generalization_tree['race'] = race_tree

    race_loss = cal_generalization_loss(race_tree)
    loss_table['race'] = race_loss

    #build marital_status generalization tree
    marital_tree = {}
    marital_height = 2
    for lines in open("data_privacy_lab1/adult_marital_status.txt",'r').readlines():
        if lines.split():
            lines = lines.strip()
            son_node,father_node = lines.split(',')[0], lines.split(',')[1]
            marital_tree[son_node] = father_node
    generalization_tree['marital_status'] = marital_tree

    marital_loss = cal_generalization_loss(marital_tree)
    loss_table['marital'] = marital_loss

    #build age generalization tree
    age_tree = {}
    age_height = 4
    for i in range(0,5):
        str_1 = str(i * 20) + '~' + str((i + 1) * 20 - 1)
        age_tree[str_1] = '*'
        for j in range(0,2):
            str_2 = str(i * 20 + j * 10) + '~' + str(i * 20 + (j + 1) * 10 - 1)
            age_tree[str_2] = str_1
            for k in range(0,2):
                str_3 = str(i * 20 + j * 10 + k * 5) + '~' + str(i * 20 + j * 10 + (k + 1) * 5 - 1)
                age_tree[str_3] = str_2
                for l in range(0,5):
                    str_4 = str(i * 20 + j * 10 + k * 5 + l)
                    #delete not exist age
                    if str_4 in age_list:
                        age_tree[str_4] = str_3
    while True:
        pop_list = []
        for key in age_tree.keys():
            if not key in age_list and not key in age_tree.values():
                pop_list.append(key)
        if len(pop_list) == 0:
            break
        for key in pop_list:
            age_tree.pop(key)
    generalization_tree['age'] = age_tree

    age_loss = cal_generalization_loss(age_tree)
    loss_table['age'] = age_loss
    # for key in age_tree.keys():
    #     print(str(key) + ' : ' + age_tree[key])
    k_anonimity = 3
    maxSup = 20
    if not (len(sys.argv) == 1 or len(sys.argv) == 3):
        print("error arg number!")
        print(len(sys.argv))
    elif len(sys.argv) == 3:
        k_anonimity = int(sys.argv[1])
        maxSup = int(sys.argv[2])
    
    vectors = DefaultDict(list)
    for i in range(0,5):
        for j in range(0,2):
            for k in range(0,2):
                for l in range(0,3):
                    vectors[i + j + k + l].append([i,j,k,l])
    
    sol, unsatisfy_list, total_loss = samarati(data_file, k_anonimity, maxSup, generalization_tree, vectors, loss_table)
    print(sol)
    print(unsatisfy_list)
    print("the loss metric is %f" % total_loss)
    # print(total_loss)
    write_file = open("samarati_k-anonymity_adult.data", 'w')
    for lines in data_file:
        if not '?' in lines:
            read_content = []
            for i in range(0,15):
                read_content.append(lines.split(',')[i].strip())
            age,gender,race,marital_state, occupation = read_content[0],read_content[9],read_content[8],read_content[5],read_content[6]
            # generalization data in origin file
            for i in range(0, sol[0]):
                age = age_tree[age]
            for i in range(0, sol[1]):
                gender = gender_tree[gender]
            for i in range(0, sol[2]):
                race = race_tree[race]
            for i in range(0, sol[3]):
                marital_state = marital_tree[marital_state]
            if not age+gender+race+marital_state in unsatisfy_list:
                write_content = []
                write_content.append(age)
                write_content.append(gender)
                write_content.append(race)
                write_content.append(marital_state)
                write_content.append(occupation)
                write_file.write(','.join(write_content))
                write_file.write('\n')


if __name__ == '__main__':
    main()