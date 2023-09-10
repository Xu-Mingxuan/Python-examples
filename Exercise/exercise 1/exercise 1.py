with open("C:\\Users\\11366\\Desktop\\file_to_read.txt", "r") as f1,open("C:\\Users\\11366\\Desktop\\output.txt","w") as f2:
    data = f1.readline()
    list = data.split()
    print(list)
    num=0
    for items in list:
        new_line = items
        if "terrible" in items:
           num=num+1
           if num%2 ==0:
              new_line = new_line.replace("terrible","pathetic")
           elif num%2 ==1:
              new_line = new_line.replace("terrible","marvellous")
        f2.write(new_line+" ")

    print("terrible出现的次数为:", num)
with open("C:\\Users\\11366\\Desktop\\output.txt","r") as f3:
        data2 = f3.readline()
        list2 = data2.split()
        print(list2)
    
 