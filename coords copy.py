import cv2
import numpy as np


class coords:
    def __init__(self) -> None:
        pass

    def extract(imgpath):
        # 원본 이미지 불러오기
        origin_img = cv2.imread(imgpath)
        # 작업할 이미지 불러오기
        img = cv2.imread(imgpath)

        # 이미지 그레이 전환
        imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # # 흑과 백으로 임계(threshold) 분할
        # test, thresh = cv2.threshold(imgray, 127, 255, 0)
        # contours, hierarchy = cv2.findContours(
        #     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)     # contour(외곽선)를 찾아냄.(연속된 좌표점)

        # # contour(외곽선)을 그림, 검은색(0, 0, 0), 두께 1로 // 경계 나누기용
        # cv2.drawContours(img, contours, -1, (0, 0, 0), 1)

        # # 이미지 출력
        # cv2.imshow('result', img)
        # # 아무키나 누르면
        # cv2.waitKey(0)
        # # 모든창 닫기
        # cv2.destroyAllWindows()

        imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # 흑과 백으로 임계(threshold) 분할
        test, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)     # contour(외곽선)를 찾아냄.(연속된 좌표점)

        # 원본 이미지에 contour(외곽선)을 그림, 빨간색(0, 0, 255), 두께 1로 -- 확인용
        cv2.drawContours(origin_img, contours, -1, (0, 0, 255), 1)

        # 이미지 출력
        cv2.imshow('result', origin_img)
        # 아무키나 누르면
        cv2.waitKey(0)
        # 모든창 닫기
        cv2.destroyAllWindows()

        temp = list(contours)
        temp.sort(key=len)
        temp.reverse()
        result = list()
        for i in range(len(temp)):
            # 작은 구역은 좌표를 출력하지 않고 PASS
            if len(temp[i]) < 10:
                continue
            result.append(temp[i])
        return result

    def printhtml(contours, n=1):
        # 좌표 생략 계수 default는 1이며 n을 함께 입력시 좌표의 갯수가 n분의 1로 줄어든다
        num = n
        # ---------------- 완성된 contours로 html 파일 제작 -----------------
        f = open('result.html', 'w')
        f.write('''<!DOCTYPE html>
<html>
<head></head>
<body>
<img src="''' + imgpath + ''' "usemap = "#test"/>
<map name="test">
''')
        for i in range(len(contours)):
            # contours 간격을 n분의 1로 조정하여 출력
            arr = np.array(contours[i][0:len(contours[i]):num])
            # N차원의 contours 배열을 1차원으로 축소
            result = arr.ravel()
            f.write('<area shape=\"poly\" alt=\"\" title=\"' +
                    str(i+1)+'\" coords=\"')
            # 배열사이에 들어갈 문자를 지정한 뒤 출력 and 첫번째 좌표를 마지막에 추가
            f.write(str(result).replace("[", "").replace(
                "]", "").replace(" ", ","))  # +result[0:2]
            f.write('" href="" target="_self" />\n')
        f.write('''
</map>
</body>
</html>''')


# 이미지 경로 확장자까지 입력하기
imgpath = "seoul_gu.png"
contours = coords.extract(imgpath)
coords.printhtml(contours, 5)
