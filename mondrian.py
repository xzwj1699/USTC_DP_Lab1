import math
import sys
def mondrian(datalist :list, k):
    data_size = len(datalist)
    if data_size < 2 * k:
        return anonymitization(datalist)
    else:
        mid = math.floor(data_size / 2)
        datalist_0 = [x[0] for x in datalist]
        datalist_1 = [x[1] for x in datalist]
        if max(datalist_0) - min(datalist_0) > max(datalist_1) - min(datalist_1):
            datalist.sort(key = lambda x : x[0])
        else:
            datalist.sort(key = lambda x : x[1])
        ano_list_1, age_loss_1, edu_loss_1 = mondrian(datalist[0:mid], k)
        ano_list_2, age_loss_2, edu_loss_2 = mondrian(datalist[mid:], k)
        return ano_list_1 + ano_list_2, age_loss_1 + age_loss_2, edu_loss_1 + edu_loss_2
    

def anonymitization(datalist):
    datalist_0 = [x[0] for x in datalist]
    datalist_1 = [x[1] for x in datalist]
    data_size = len(datalist_1)
    max_0 = max(datalist_0)
    min_0 = min(datalist_0)
    max_1 = max(datalist_1)
    min_1 = min(datalist_1)
    str_0 = str(min_0) + '~' + str(max_0)
    str_1 = str(min_1) + '~' + str(max_1)
    age_loss = (max_0 - min_0) * data_size
    edu_loss = (max_1 - min_1) * data_size
    return_list = []
    for data in datalist:
        return_list.append([str_0, str_1, data[2]])
    return return_list, age_loss, edu_loss
def main():
    data_file = open("data_privacy_lab1/adult.data",'r').readlines()
    data_list = []
    k = 10
    if not (len(sys.argv) == 1 or len(sys.argv) == 2):
        print("error arg number!")
        print(len(sys.argv))
    elif len(sys.argv) == 2:
        k = int(sys.argv[1])
    max_age = 0
    min_age = 100
    max_edu = 0
    min_edu = 100
    data_num = 0
    for lines in data_file:
        if not '?' in lines:
            age,education_num,occupation = int(lines.split(',')[0].strip()), int(lines.split(',')[4].strip()),lines.split(',')[6].strip()
            max_age = max(max_age, age)
            min_age = min(min_age, age)
            max_edu = max(max_edu, education_num)
            min_edu = min(min_edu, education_num)
            data_num += 1
            data_list.append([age, education_num, occupation])
    ano_data, age_loss, edu_loss = mondrian(data_list, k)
    age_loss = age_loss / ((max_age - min_age) * data_num)
    edu_loss = edu_loss / ((max_edu - min_edu) * data_num)
    print("max age is %d, min age is %d, max edu is %d, min edu is %d" % (max_age,min_age,max_edu,min_edu))
    print("the age loss is : %f" % age_loss)
    print("the edu loss is : %f" % edu_loss)
    print("the total loss is : %f" % (age_loss + edu_loss))
    # print(age_loss + edu_loss)
    write_file = open("mondrian_k-anonymity_adult.data", 'w')
    for lines in ano_data:
        write_file.write(','.join(lines))
        write_file.write('\n')

if __name__ == '__main__':
    main()