#-*-coding:utf-8-*-
import random
import math
'''
read data from file
'''
def read_data(file_path):
    x_title = []
    y_title = []
    data = []
    with open(file_path, 'r') as f:
        #the first row is title
        line = f.readline().strip()
        #title data
        x_title = line.split(',')
        del x_title[0]
        #get data
        line = f.readline()
        while line:
            #split the data with delimiter ','
            content = line.strip().split(',')
            #title
            y_title.append(content[0])
            #remove the title row
            del content[0]
            data.append(content)
            line = f.readline()
    return x_title, y_title, data

'''
calculate the mean value of a column
'''
def calmeanvalue(data, col):
    count = 0
    total = 0.0
    for row in range(len(data)):
        try:
            #is numeric data?
            fValue = float(data[row][col])
            count += 1
            total += fValue
        except ValueError:
            pass
    return total / count

'''
replace NA by mean value
'''

def replacenabymean(data):
    meandict = {}
    n_data = []
    for row in range(len(data)):
        row_data = []
        for col in range(len(data[row])):
            value = data[row][col]
            try:
                #is numeric data?
                fValue = float(value)
                row_data.append(fValue)
            except ValueError:
                #repleace the nonnumeric data with the mena value
                if col in meandict.keys():
                    mean_value = meandict.get(col)
                else:
                    #store the value that is not inside the dictionary into the dictionary
                    mean_value = calmeanvalue(data, col)
                    meandict[col] = mean_value
                #add mean value
                row_data.append(mean_value)
        n_data.append(row_data)
    return n_data

'''
randomly generate 'percentNA' percent of the original data，return the list and the index
'''
def generatena(data1, percent):
    data = []
    row_count = len(data1)
    col_count = len(data1[0])
    #total count
    tcount = row_count * col_count
    #generated count
    gcount = int(percent*tcount)
    rset = set()
    #generate random numbers
    while len(rset) < gcount:
        r = random.randrange(0, tcount)
        rset.add(r)
    #
    count = 0
    for row in range(row_count):
        row_data = []
        for col in range(col_count):
            if count in rset:
                row_data.append('NA')
            else:
                row_data.append(data1[row][col])
            count += 1
        data.append(row_data)
    return data, rset

'''
calculate the mean difference(error)
'''
def calerror(n_data1, n_data2, rset):
    error = 0.0
    count = 0
    #real number
    rcount = 0
    #number of row
    row_count = len(n_data1)
    #number of column
    col_count = len(n_data1[0])
    for row in range(row_count):
        for col in range(col_count):
            #sum the error value
            try:
                error += math.fabs(n_data1[row][col] - n_data2[row][col]) / math.fabs(n_data1[row][col])
                rcount += 1
            except Exception:
                #when denominator equals to 0
                pass
    error = error / rcount
    return error

if __name__ == '__main__':
    print('1.Now loading data.')
    x_title, y_title, data1 = read_data('data/ctrl_trans.csv')
    print('Loading completed，total {} rows, {} column'.format(len(y_title), len(x_title)))

    #replace NA by mean value
    print('2.Use average value to replace NA')
    n_data1 = replacenabymean(data1)

    #randomly generate NA
    percent = 0.05
    print('3.generate {:.2f}% of NA'.format(percent * 100))
    data2,reset = generatena(data1, percent)
    print('Totally generate {} NA'.format(len(reset)))

    print('4.Use average value to replace the random NA')
    n_data2 = replacenabymean(data2)
    print('5.calculate error')
    error = calerror(n_data1, n_data2, reset)
    print('Error is {:.2f}%'.format(error * 100))
    print('Accuracy is {:.2f}%'.format(100 - error * 100))

