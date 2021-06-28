import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from functools import partial
from PIL import ImageTk, Image 

fileToUse = ""
indexFileName = "quick-cat-index-1.txt" # toby_index-NEWTEST.txt"
xindexFileName = ""

root = Tk()
root.title('Quick Cataloguer Demo using TKinter')
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.resizable(width=True, height=True)

# global vars
buttonRow = height-400
buttonRowLeft = 35
fileList = []
lenFileList = 0
img_no = 0
currentImageNo = 0
variables = []
imageName = ""
inputtxt = Text(root) # , height = 5, width = 75, bg = "azure", fg = "black")
#indexFileName = StringVar()
indextxt = Entry(root) #, height = 5, width = 75, bg = "azure", fg = "black")

makeWebPage = BooleanVar()
makeJsonFile = BooleanVar()


def loadDirectory(root):
    global lenFileList
    global nextImageButton
    global imageChosen
    okFileTypes = ['.jpg', '.jpeg', '.gif', '.png', '.tif','.tiff', '.JPG', '.JPEG', '.GIF', '.PNG', '.TIF','.TIFF']
    root.attributes("-topmost", False)
    open_file = filedialog.askdirectory()
    #print(open_file)
    for root, directories, files in os.walk(open_file, topdown=False):
        for name in files:
            split_tup = os.path.splitext(name)
            if str(split_tup[1]) in okFileTypes:
                    fileList.append(os.path.join(root, name))
        for name in directories:
            if split_tup[1] in okFileTypes:
                    fileList.append(os.path.join(root, name))
        """ TEST HERE """
        if len(fileList) > 0:
            nextImageButton.state(["!disabled"])  #https://stackoverflow.com/questions/21673257/python-ttk-disable-enable-a-button
            previousImage.state(["!disabled"])
        x = "There are "+str(len(fileList)) +" images."
        imageLabel.config(text=x)
        lenFileList = len(fileList) # -1
    setCurrentRecordNumber(-1, False)


def updtcblist():
    #print("65 update c")
    imageNumberList = []
    for j in range(0, lenFileList):
        imageNumberList.append(j)
    imageChosen['values'] = imageNumberList
    imageChosen['state'] = 'readonly'
    imageChosen.bind('<<ComboboxSelected>>',getimage_changed)

def getimage_changed(event):
    setCurrentRecordNumber( int(imageChosen.get())-1, True)

def set_all(value):
    for v in variables:
        v.set(value)
        #print("v = ", v)
    
def saveIndexData(s):
    global indexFileName
    try:
        file1 = open(indexFileName, "a")
        print("Saving data to ", indexFileName)
        file1.write(s)   # entry.get())
        file1.close()
    except OSError as err: 
        print("OS Error {0}". format(err))
        messagebox.showinfo("Information","OS Error {0}". format(err))

def setCurrentRecordNumber(no, isJump):
    global currentImageNo
    if (isJump):
        currentImageNo = int(no)
    else: # not a jump; could be next/prev or reset to 0
        if int(no) > 0:
            currentImageNo += int(no)
        else:
            #print("SETTING current record number to ", no)
            currentImageNo = 0
    
def getCurrentRecordNumber():
    global currentImageNo
    return currentImageNo
    
def nextImage(no):
    global lenFileList
    global imageName
    global inputtxt

    # Getting VALUES from the checkbuttons
    forIndex = ""
    for i in range(0, len(variables)):
        s = imageName+"\t"
        if (variables[i].get() == True):
            forIndex += bnames[i] + "\t"
    if forIndex:
        #print("OKAY TO SAVE TO INDEX")
        xINPUT = inputtxt.get("1.0", "end-1c")
        #print(xINPUT)

        #print("125: s = ", s, forIndex, "\t" + xINPUT)
        strToSave = s + forIndex + "\t" + xINPUT+"\n"
        saveIndexData(strToSave)
        set_all(False)
        inputtxt.delete("1.0", "end-1c")
    # NOTE NOTE NOTE: Added the -1 to test
    if getCurrentRecordNumber() < lenFileList:  #-1 : # len(fileList): -1
        #print("120: currentRecordNumber = ", getCurrentRecordNumber(), " lenFileList = ", lenFileList)
        setCurrentRecordNumber(no, False)
        imageName = fileList[getCurrentRecordNumber()]
        image = Image.open(imageName)
        origHeight = image.size[1]
        origWidth = image.size[0]
        imagespace = height-120

        if origHeight > imagespace:
            x = imagespace/origHeight
            newHeight = round(origHeight * x)
            newWidth = round(origWidth * x)
        if image.size[1] > imagespace:
            image = image.resize( (newWidth, newHeight) , Image.ANTIALIAS )
        image = ImageTk.PhotoImage(image)
        label2.config(image=image)
        label2.image = image
        imageLabel.config(text = str(currentImageNo)+" " + imageName)
    else:
        imageLabel.config(text = "End of the current folder: "+str(lenFileList)+" images.")
        messagebox.showinfo("Information","End of the list of files; resetting to first image.\nThere are {0} total.". format(lenFileList))
        setCurrentRecordNumber(-1, False)

def prevImage():
    #IsADirectoryError
    if (len(fileList) > 2):
        setCurrentRecordNumber(-2, False)
    else:
        imageLabel.config(text="Already at start of folder list.", fb="red")
        messagebox.showinfo("Information","Already at the first record.")

""" ---------------------------------------------------------------------------------"""
def search():
    global lenFileList
    global makeWebPage
    global makeJsonFile
    #print("SEARCH OPTION - make the pageor not? ")
    #print(makeWebPage)
    #print("getting value test ... ", makeWebPage.get())
    listOfTermsToFind = []
    x = []
    for i in range(0, len(variables)):
        if (variables[i].get() == True):
            x.append(bnames[i])

    with open(indexFileName) as file:
        for line in file:
            line = line.strip()
            for i in x:
                if i in line:
                    templine = line.split("\t")
                    # get just the full file name, which is the 0th element in list
                    # but check that it isn't already there. ..
                    if templine[0] not in fileList:
                        fileList.append(templine[0])
    if (len(fileList) == 0):
        messagebox.showinfo("Information","Sorry, no matches.")
    else:
        nextImageButton.state(["!disabled"])
        previousImage.state(["!disabled"])
        lenFileList = len(fileList)
        messagebox.showinfo("Information","There are {0} matches. Press \u25b6 to start.". format(lenFileList))
        setCurrentRecordNumber(0, False)
        updtcblist()
        if makeWebPage.get() == True:
            print("MAKE WEB PAGE")
            messagebox.showinfo("Information","Web Page Output Coming soon ...")
        if makeJsonFile.get() == True:
            messagebox.showinfo("Information",".json output soon ...")
    # clean up the buttons
    set_all(False)
# --- end of search area test.

#
noOfRows = 10
noOfCol = 3
rowHeight = round(height/noOfRows)
cbCount = 1
rowCount = 1
hspacer = 150
vspacer = 20

with open("quick_cat_descriptors.txt") as f:
    bnames = f.read().splitlines()

down = 50
count = 0
downspacer = 30
rownumber = 1
leftstart = 10
spacer = 130
for i in range(0, len(bnames)):
    v = BooleanVar()
    variables.append(v)
    if count == 0:
        right = (count * spacer) + leftstart # 10
    else:
        right = (count * spacer) + leftstart
    Checkbutton(root, text = bnames[i], fg='#0072bb', variable=v).place(x = right, y = down)
    count += 1
    if count > 3:
        count = 0
        down += downspacer


# label 1
label1 = Label(root, text="Quick Cataloguing Tool (beta)",bg='red',fg='white')
label1.place(x=20, y=10)
imageLabel = Label(root, text="current image number "+str(currentImageNo))
#imageLabel.config(font = ("Avenir Next", 9), fg='#6c7a86')
imageLabel.place(x = 320, y = 10)

#
image = Image.open("quick_cat_howto.png") # originally PosterSeagull.png"
origHeight = image.size[1]
origWidth = image.size[0]
imagespace = height-125
#print("Image Size Fix: original h x w: ", origHeight, "x", origWidth)

if origHeight > imagespace:
    x = imagespace/origHeight
    newHeight = round(origHeight * x)-10
    newWidth = round(origWidth * x)
if image.size[1] > imagespace:
    image = image.resize( (newWidth, newHeight) , Image.ANTIALIAS )
image = ImageTk.PhotoImage(image)

# label 2
label2 = Label(root, image = image
)
label2.place(relx=0.9, y=25, relwidth=0.45, anchor='ne')
label2.image = image

# see https://www.geeksforgeeks.org/python-add-style-to-tkinter-button/
style = ttk.Style()
style.theme_use('default')  # clam, alt, default, classic, 
# WINDOWS:vista, xpnative, winnative
style.configure('TButton', background='white', foreground='black', borderwidth=1, focusthickness=3, focuscolor='none')
style.map('TButton', background=[('active','red')])

# test of separate colors
#style.configure("W.TButton", font=("Courier", 10), foreground="green")
style.configure("W.TButton",  foreground="green")

# BUTTONS
# ROW 1
searchImages = ttk.Button(root, text="Search", style="W.TButton",command = lambda:search()).place(x=buttonRowLeft, y=buttonRow)
loadImages = ttk.Button(root, text="Load Folder", command = lambda:loadDirectory(root)).place(x=(buttonRowLeft+100), y=buttonRow)

# row 1 - output options
make_webpage_cb = Checkbutton(root, text = "Create webpage of search results", variable=makeWebPage).place(x = (buttonRowLeft + 200), y = buttonRow)
#print("283: test of button state - makeWebPage = ", makeWebPage.get())
make_json_cb = Checkbutton(root, text = "Output search results in .json", variable=makeJsonFile).place(x = (buttonRowLeft + 200), y = (buttonRow+25))

# ROW 2
buttonRow = buttonRow + 50
# must be two separate commands - create and then place for the state() to work.
previousImage = ttk.Button(root, text="\u25c0 Previous", command=lambda: nextImage(-1))
previousImage.place(x=buttonRowLeft, y=buttonRow)
previousImage.state(["disabled"])
nextImageButton = ttk.Button(root, text="Next \u25b6", command=lambda: nextImage(1))
nextImageButton.place(x=(buttonRowLeft+100), y=buttonRow)
nextImageButton.state(["disabled"])

# add #s for each image for jump to...
jumpToLabel = Label(root, text="Jump to ").place(x=(buttonRowLeft+205), y=(buttonRow+3))
jumpTo = IntVar()
imageChosen = ttk.Combobox(root, width=5, textvariable = jumpTo, postcommand=updtcblist)
imageChosen.place(x=(buttonRowLeft+265), y=(buttonRow+7))

# ROW 3
buttonRow = buttonRow + 50
clearAll = ttk.Button(root, text="Clear", command=partial(set_all, False)).place(x=buttonRowLeft, y=buttonRow)
quit = ttk.Button(root, text="Quit", command=root.destroy).place(x=(buttonRowLeft+100), y=buttonRow)

# TEXT NOTES ... 
buttonRow = buttonRow + 50
inputTxtLabel = Label(root, text = "Optional notes.").place(x = buttonRowLeft, y = buttonRow)
inputtxt.config(height = 5, width = 75, bg = "azure", fg = "black")
#inputtxtLabel = Label(root, text="Notes", fg="black").place(x = buttonRowLeft, y = 425)
buttonRow = buttonRow + 25
inputtxt.place(x = buttonRowLeft, y = buttonRow)

root.mainloop()