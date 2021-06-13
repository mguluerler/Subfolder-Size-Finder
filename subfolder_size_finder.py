import os

def sizeFinder(file_path):
    global subfolders_totalsize, searched_subfolders, nonfoldered_size

    subfolders_totalsize = list()
    everysubfolders_size = 0.0
    which_subfolder = 0
    filepath_everyfolder = ""
    resoulution = 9
    first_loop = False

    for mainfolder, folders, files in os.walk(file_path):
        #If program starts for first loop, it saves searched subfolders.
        if filepath_everyfolder == "":
            searched_subfolders = folders.copy()
            first_loop = True
        #If not first loop:
        if not filepath_everyfolder == "":
            #Investigates which subfolder searching, if new subfolder is started for calculating size then saves size of old subfolder.
            if not os.path.join(file_path, searched_subfolders[which_subfolder]) in mainfolder:
                subfolders_totalsize.append(round(everysubfolders_size/(1024**3), resoulution))
                #print(subfolders_totalsize)
                which_subfolder += 1
                everysubfolders_size = 0

        #Adds every files size to total size of subfolder.
        for everyfiles in files:
            filepath_everyfolder = os.path.join(mainfolder, everyfiles)
            if not os.path.islink(filepath_everyfolder):
                if first_loop:
                    nonfoldered_size += os.path.getsize(filepath_everyfolder)
                else:
                    everysubfolders_size += os.path.getsize(filepath_everyfolder)
        #If there is no files in directory, at 2nd loop of program it thoughts that there is 1st loop because filepath_everyfolder is still empty and it changes searched_subfolders to subfolder of subfolder.
        if len(files) == 0:
            # For stability of program if there is no file in loop filepath changes as first folder of subfolder.
            try:
                filepath_everyfolder = os.path.join(mainfolder, folders[0])
            #If there is no folder, filepath changes as mainfolder.
            except:
                filepath_everyfolder = mainfolder
        first_loop = False
    # Adds size of last subfolder because program was adding that in next loop but there is no next loop for last subfolder.
    subfolders_totalsize.append(round(everysubfolders_size/(1024**3), resoulution))

def sorting_bysize():
    global indexes
    #indexes is created that has equal item with allsearchedfolders.
    indexes = [i for i in range(0, len(allsearchedfolders_size))]
    #for loop is created with len() for registirate every index.
    for index in range(0, len(allsearchedfolders_size)):
        whichrank = 0
        #Every subfolder size is compared with size of other subfolders and if it's bigger than the other adds 1 to whichrank to ranking its size.
        for sizecomp in allsearchedfolders_size:
            if allsearchedfolders_size[index] > sizecomp:
                whichrank += 1
        #The rank of a subfolder is saved in indexes list. Example: indexes[0] = index of biggest folder
        indexes[(len(allsearchedfolders_size) - 1) - whichrank] = index

allsearchedfolders_name = list()
allsearchedfolders_size = list()
nonfoldered_size = 0
totalsize_nonfoldered = 0
##########################################   CHANGE HERE   ##########################################
folders_path = ["YOUR FILE PATH"]
#####################################################################################################
#Searches for every folder and adds every subfolder with extend method to the list for sorting them.
for file_path in folders_path:
    sizeFinder(file_path)
    print("At " + file_path[0] + ": " + str(round(sum(subfolders_totalsize)+nonfoldered_size/(1024**3), 9)) + " GB")
    totalsize_nonfoldered += round(nonfoldered_size/(1024**3), 9)
    allsearchedfolders_size.extend(subfolders_totalsize)
    allsearchedfolders_name.extend(searched_subfolders)

sorting_bysize()
print("Size of non-subfolder files: " + str(totalsize_nonfoldered) + " GB")
for col in range(0, len(allsearchedfolders_size)):
    try:
        print(str(allsearchedfolders_name[indexes[col]]) + " --> " + str(allsearchedfolders_size[indexes[col]]) + " GB")
    except IndexError:
        print("I think you entered a file path that has not any subfolder.\n"
              "If you're taking this except message and you're sure with your file path, I'm sorry for coding non-stable program. :/")