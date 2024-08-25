from tkinter import *
from PIL import Image, ImageTk

assetWindow = Tk()
assetWindow.geometry('500x250')
assetWindow.title('Assets')

#Textures folder name
textureFolder = 'textures'

#Vars
screenObjs = []
curAssetNum = 0
maxAssetNum = 0
ctrlBtnOffset = (400, 5)
search_var = StringVar()

def apndGraphic(tempList):
    global screenObjs
    for item in tempList:
        screenObjs.append(item)

#All assets
def getAllAssets(objDataFile):
    headList = []
    assetObjList = []
    with open(objDataFile, 'r') as objFile:
        eachAsset = objFile.readlines()
        for item in eachAsset:
            if headList == []:
                headList.append(item.replace('\n', '').split(':'))
            else:
                assetObjList.append((item.replace('\n', '')).split(':'))
    print(headList)
    return headList, assetObjList

def loadAsset(headList, assetObjData, assetNum):
    global assetWindow, textureFolder
    clearAsset()
    thisAsset = {}
    assetObjData = assetObjData[assetNum]
    attributeData = ''
    for objHeadNum in range(len(headList)):
        objHeadName = headList[objHeadNum]
        try:
            attributeData = assetObjData[objHeadNum]
        except:
            attributeData = 'ERR NULL'
        thisAsset[str(objHeadName)] = attributeData

    #Asset ID Data

    idLbl = Label(assetWindow, text=f'ID: {thisAsset["ID"]}')
    objNameLbl = Label(assetWindow, text=f'Name: {thisAsset["assetName"]}')
    objClassLbl = Label(assetWindow, text=f'Class: {thisAsset["itemClass"]}')
    
    #Asset Property Data

    prptyLblList = []
    tempCount = 0
    for i in headList[3:]:
        newlbl = Label(assetWindow, text = f'{i}: {thisAsset[i]}')
        newlbl.place(x=180, y=tempCount*20+5)
        prptyLblList.append(newlbl)
        tempCount += 1

    #Asset Image ------------------
    
    assetImage = Image.open(f'{textureFolder}/{thisAsset["imageFile"]}')
    assetImage = assetImage.resize((150, 150))
    assetImage = ImageTk.PhotoImage(assetImage)
    imgBox = Label(assetWindow, image=assetImage)
    imgBox.image = assetImage

    #GUI Placements
    imgBox.place(x=5,y=5)
    idLbl.place(x=5,y=160)
    objNameLbl.place(x=5,y=185)
    objClassLbl.place(x=5,y=210)

    #Append to assetGraphic
    apndGraphic((idLbl,objNameLbl,objClassLbl,imgBox))
    apndGraphic(prptyLblList)

def clearAsset():
    global screenObjs
    for assetGraphic in screenObjs:
        assetGraphic.destroy()

def nextAsset():
    global curAssetNum, maxAssetNum, assets
    if curAssetNum >= maxAssetNum:
        curAssetNum = 0
    else:
        curAssetNum += 1
    loadAsset(assets[0][0], assets[1], curAssetNum)
    return

def prevAsset():
    global curAssetNum, maxAssetNum, assets
    if curAssetNum > 0:
        curAssetNum -= 1
    else:
        curAssetNum += maxAssetNum
    loadAsset(assets[0][0], assets[1], curAssetNum)
    return

def searchId():
    global curAssetNum, assetIDs, assets, search_var
    ID_TO_SEARCH = search_var.get()
    try:
        curAssetNum = assetIDs[f'{ID_TO_SEARCH}']
        loadAsset(assets[0][0], assets[1], curAssetNum)
    except:
        pass

assets = getAllAssets('ObjectData.txt')
maxAssetNum = len(assets[1])-1

#First Asset
loadAsset(assets[0][0], assets[1], curAssetNum)

#ID and Index
objDList = assets[1]
assetIDs = {}

for idIndex in range(maxAssetNum+1):
    print(idIndex)
    assetIDs[str(objDList[idIndex][0])] = idIndex
    
#Basic GUI
nextAssetBtn = Button(assetWindow, text='>>>', command=nextAsset)
prevAssetBtn = Button(assetWindow, text='<<<', command=prevAsset)
searchIdBtn= Button(assetWindow, text='Find ID', command=searchId)
searchBar = Entry(assetWindow, textvariable=search_var, width=4)

nextAssetBtn.place(x=ctrlBtnOffset[0]+50,y=ctrlBtnOffset[1])
prevAssetBtn.place(x=ctrlBtnOffset[0],y=ctrlBtnOffset[1])
searchIdBtn.place(x=ctrlBtnOffset[0]+30,y=ctrlBtnOffset[1]+30)
searchBar.place(x=ctrlBtnOffset[0]-5,y=ctrlBtnOffset[1]+35)

assetWindow.mainloop()
