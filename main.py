import cv2 as cv
from win10toast import ToastNotifier
import os
import ctypes
import time

#INITS
dir_path = os.path.dirname(os.path.realpath(__file__))
main_window = "ROOMCOLOR"
toast = ToastNotifier()
cv.namedWindow(main_window, cv.WINDOW_AUTOSIZE)
cam = cv.VideoCapture(0)

#IMAGE LOAD
room_green = cv.imread("room_colors/room_green.png",cv.IMREAD_COLOR)
room_blue = cv.imread("room_colors/room_blue.png",cv.IMREAD_COLOR)
room_red = cv.imread("room_colors/room_red.png",cv.IMREAD_COLOR)

#MAIN OPTIONS
method = cv.TM_CCOEFF_NORMED
threshold = 0.4
retake = 1 
PATH = "~/Documents/self_projects/roomColor/"
fps =10
prev = 0
current = "Nil" # saves the current room color

def TemplateMatching(frame):

    min_g,___,__,_ = cv.minMaxLoc(cv.matchTemplate(frame,room_green,method))
    min_b,___,__,_ = cv.minMaxLoc(cv.matchTemplate(frame,room_blue,method))
    min_r,___,__,_ = cv.minMaxLoc(cv.matchTemplate(frame,room_red,method))
    
    global current

    if min_g > threshold and current != "G":
        print("GREEN")
        ctypes.windll.user32.SystemParametersInfoW(20, 0,dir_path+"/wallpapers/room_green.jpg", 3)
        toast.show_toast("ROOM COLOR: GREEN","changing wallpaper...",duration =3,threaded=True)
        current = "G"
    elif min_b > threshold and current != "B":
        print("BLUE")
        ctypes.windll.user32.SystemParametersInfoW(20, 0,dir_path+"/wallpapers/room_blue.jpeg", 3)
        toast.show_toast("ROOM COLOR: BLUE","changing wallpaper...",duration =3,threaded=True)
        current = "B"
    elif min_r > threshold and current != "R":
        print("RED")
        ctypes.windll.user32.SystemParametersInfoW(20, 0,dir_path+"/wallpapers/room_red.jpg", 3)
        toast.show_toast("ROOM COLOR: RED","changing wallpaper...",duration =3,threaded=True)
        current = "R"

def Defaults():
    ctypes.windll.user32.SystemParametersInfoW(20, 0,dir_path+"/wallpapers/default.jpg", 3)
    toast.show_toast("EXITING ROOMCOLOR SCRIPT","changing wallpaper to default...",duration =3,threaded=True)

def main():
    while(True):
        ret, frame = cam.read()
        cv.imshow(main_window,frame)
        global prev
        global time
        time_elapsed = time.time() - prev
        if time_elapsed > 1./fps:
            TemplateMatching(frame)
            prev = time.time()

        key = cv.waitKey(1)
        if key == 27:#esacpe key 
           break
        elif key == ord('q') and retake == 1 :
            print("RED trigger captured")
            cv.imwrite("room_colors/room_red.png",frame)
        elif key == ord('w') and retake == 1 :
            print("GREEN trigger captured")
            cv.imwrite("room_colors/room_green.png",frame)
        elif key == ord('e') and retake == 1 :
            print("BLUE trigger captured")
            cv.imwrite("room_colors/room_blue.png",frame)
            
    Defaults()
    cam.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
