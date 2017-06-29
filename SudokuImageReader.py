import numpy as np
import cv2
import pytesseract
import Board
from PIL import Image

class SudokuImageReader:
    def __init__(self, imageFilename):
        self.imageFilename = imageFilename
        self.xBlockSize = 100
        self.yBlockSize = 100
        self.blocksNumber = 9
        self.size = (900,900)
        self.cornersList = []
        self.sudokuBinaryImg = None
        self.sudokuBlock = None
        self.board = Board.Board()
        self.readImgFromFile()
        self.convertImgToBinary()
        self.findSudokuContours()
        self.correctPerspective()
        self.readDigitsFromImg()
        self.showImg()

    def readImgFromFile(self):
        self.sudokuImg = cv2.imread(self.imageFilename)
        self.sudokuImg = cv2.resize(self.sudokuImg, self.size)
        self.sudokuBWImg = cv2.cvtColor(self.sudokuImg, cv2.COLOR_BGR2GRAY)

    def convertImgToBinary(self):
        self.sudokuBinaryImg = cv2.GaussianBlur(self.sudokuBWImg, (9, 9), 0)
        self.sudokuBinaryImg = cv2.adaptiveThreshold(self.sudokuBinaryImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                              cv2.THRESH_BINARY, 7, 2)
        self.sudokuBinaryImg = cv2.bitwise_not(self.sudokuBinaryImg)

    def findSudokuContours(self):
        _,contours, _ = cv2.findContours(self.sudokuBinaryImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        biggest = None
        max_area = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 100:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                if area > max_area and len(approx)==4:
                    biggest = approx
                    max_area = area

        for corner in biggest:
            x,y = corner.ravel()
            self.cornersList.append([x,y])
            cv2.circle(self.sudokuBWImg, (x,y), 3, 255, -1)

    def swapCorners(self):
        tmp = self.cornersList[3]
        self.cornersList.insert(1, tmp)
        self.cornersList.pop(4)
        self.cornersList = np.float32(self.cornersList)

    def correctPerspective(self):
        self.swapCorners()

        pts2 = np.float32([[0,0],[self.size[0],0],[0,self.size[1]],[self.size[0],self.size[1]]])
        M = cv2.getPerspectiveTransform(self.cornersList,pts2)
        self.sudokuBinaryImg = cv2.warpPerspective(self.sudokuBinaryImg,M,self.size)
        self.sudokuImg = cv2.warpPerspective(self.sudokuImg, M, self.size)

    def findCountorsOfDigit(self, image):
        _, contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        countoursList = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            #if are of contours is to big, we ignore it
            #otherwise we appen
            if w * h > 900:
                countoursList.append(cnt)

        _, _, _w, _h = cv2.boundingRect(countoursList[0])
        minAreaSize = _w * _h
        minCnt = countoursList[0]

        x = y = w = h = None
        for cnt in countoursList:
            x, y, w, h = cv2.boundingRect(cnt)
            if w * h < minAreaSize and w > 20 and h > 20:
                minCnt = cnt

        return cv2.boundingRect(minCnt)

    def fillBlockWithWhitePixelsIfHasNotDigit(self):
        image = np.zeros([10, 10, 3], dtype=np.uint8)
        image.fill(255)
        return image

    def cropBlockToDigit(self, image):
        x, y, w, h = self.findCountorsOfDigit(image)
        #print(str(w * h > 8100) + str((10 > h or h > 60)) + str((10 > w or w > 60)))

        if w * h > 8100 or (15 > h or h > 60) or (15 > w or w > 60):
            image = self.fillBlockWithWhitePixelsIfHasNotDigit()
        else:
            #print(str(w) + " " + str(h))
            image = image[y:y+h,x:x+w]
            cv2.rectangle(self.sudokuImg, (self.xSize + x, self.ySize + y), (self.xSize + x + w, self.ySize + y + h),
                          (0, 255, 0), 2)
        #print(image)
        return image

    def cropImgToBlock(self,x,y):
        self.xSize = x * self.xBlockSize
        self.ySize = y * self.yBlockSize

        self.sudokuImgCrop = self.sudokuImg[self.ySize:self.ySize + self.yBlockSize, self.xSize:self.xSize + self.xBlockSize]

        img = cv2.bitwise_not(self.sudokuBinaryImg[self.ySize:self.ySize + self.yBlockSize, self.xSize:self.xSize + self.xBlockSize])
        self.sudokuBlock = self.cropBlockToDigit(img)

    def getDigitFromBlock(self):
        img = Image.fromarray(self.sudokuBlock)
        digit = pytesseract.image_to_string(img, config = "-psm 10")

        for s in list(digit):
            if s.isdigit():
                digit = s
            else:
                digit = ' '

        return digit


    def readDigitsFromImg(self):
        self.sudokuList = []
        for x in range(0, self.blocksNumber):
            listSudokuRows = []
            for y in range(0, self.blocksNumber):
                self.cropImgToBlock(x,y)

                listSudokuRows.append(self.getDigitFromBlock())
            self.sudokuList.append(listSudokuRows)

        self.sudokuList = list(map(list, zip(*self.sudokuList)))
        for row in self.sudokuList:
            print (", ".join(map(str, row)))


    def getBoard(self):
        self.board.set_board(self.sudokuList)
        return self.board

    def showImg(self):
        cv2.imshow("Sudoki - binary", self.sudokuImg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    filename = "sudoku4.jpg"
    sud = SudokuImageReader(filename)
