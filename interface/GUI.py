#https://076923.github.io/posts/Python-tkinter-2/
import tkinter
import tkinter.font
from tkinter import messagebox
from tkinter import *

window=tkinter.Tk()

window.title("YYCPRG GUI") #GUI 제목
window.geometry("1920x1080") #창크기 제목
font=tkinter.font.Font(family="맑은 고딕", size=20, slant="roman", weight="bold") #폰트 설정
font_btn=tkinter.font.Font(family="맑은 고딕",size=100,slant="roman",weight="bold") #버튼 글씨색
font_btn2=tkinter.font.Font(family="맑은 고딕",size=45,slant="roman",weight="bold") #버튼 글씨색
font_btn4=tkinter.font.Font(family="맑은 고딕",size=29,slant="roman",weight="bold") #버튼 글씨색

    #background="바탕 색"
    #foreground="문자열 색"
    #borderwidth="테두리 두께"
    #size=글자 크기
    #테두리 색
    #relief=테두리 형태 [flat=암것도 없음/groove=가느다란 사각 테두리/raised=볼록블럭/ridge=오목블록/solid=진한테두리/sunken=더깊은오목블럭

def btn_fru():
    messagebox.showinfo("과일 위치","지상 1층 A-1구역에 있습니다.")
def btn_veg():
    messagebox.showinfo("채소 위치","지상 1층 A-2구역에 있습니다.")
def btn_ric():
    messagebox.showinfo("쌀/잡곡/견과 위치","지상 1층 A-3구역에 있습니다.")
def btn_mea():
    messagebox.showinfo("정육/계란류 위치","지상 1층 A-4구역에 있습니다.")
def btn_fis():
    messagebox.showinfo("수산물/건어물/해산물 위치","지상 1층 A-5구역에 있습니다.")
def btn_mil():
    messagebox.showinfo("우유/유제품 위치","지상 1층 A-6구역에 있습니다.")
def btn_mee():
    messagebox.showinfo("밀키트/간편식류 위치","지상 1층 A-7구역에 있습니다.")
def btn_kim():
    messagebox.showinfo("김치/반찬/델리 위치","지상 1층 A-8구역에 있습니다.")
def btn_wat():
    messagebox.showinfo("생수/음료/주류","지상 1층 B-1구역에 있습니다.")
def btn_cof():
    messagebox.showinfo("커피/원두/차 위치","지상 1층 B-2구역에 있습니다.")
def btn_nod():
    messagebox.showinfo("면류/통조림 위치","지상 1층 B-3구역에 있습니다.")
def btn_sau():
    messagebox.showinfo("양념/오일 위치","지상 1층 B-4구역에 있습니다.")
def btn_sna():
    messagebox.showinfo("과자/간식 위치","지상 1층 B-5구역에 있습니다.")
def btn_bre():
    messagebox.showinfo("베이커리/잼 위치","지상 1층 B-6구역에 있습니다.")
def btn_hea():
    messagebox.showinfo("건강식품 위치","지상 1층 B-7구역에 있습니다.")
def btn_eco():
    messagebox.showinfo("친환경/유기농 위치","지상 1층 A-1 구역, A-2 구역에 있습니다.")

def btn_tis():
    messagebox.showinfo("제지/위생용품 위치","지상 2층 A-1구역에 있습니다.")
def btn_cle():
    messagebox.showinfo("청소/생활용품 위치","지상 2층 A-2구역에 있습니다.")
def btn_hou():
    messagebox.showinfo("가구/인테리어 위치","지상 2층 C구역에 있습니다.")
def btn_kit():
    messagebox.showinfo("주방용품 위치","지상 2층 A-3구역에 있습니다.")
def btn_lif():
    messagebox.showinfo("생활잡화/공구 위치","지상 2층 A-4구역에 있습니다.")
def btn_pet():
    messagebox.showinfo("반려동물 물품 위치","지상 2층 A-6구역에 있습니다.")
def btn_bea():
    messagebox.showinfo("뷰티용품 위치","지상 1층 출입구에 있습니다.")
def btn_chi():
    messagebox.showinfo("유아용품/완구 위치","지상 2층 A-5구역에 있습니다.")
def btn_god():
    messagebox.showinfo("잡화/명품 위치","지상 3층에 있습니다.")
def btn_pas():
    messagebox.showinfo("패션/언더웨어 위치","지상 2층 B구역에 있습니다.")
def btn_spo():
    messagebox.showinfo("스포츠/여행/자동차용품 위치","지상 2층 B구역에 있습니다.")
def btn_dig():
    messagebox.showinfo("디지털/가전/렌탈 위치","지상 2층 C구역에 있습니다.")

def btn_2(): #물품 안내
    newWindow2 = tkinter.Toplevel(window)
    newWindow2.title("Commodity Information")
    newWindow2.geometry("1920x1080")
    label=tkinter.Label(newWindow2, text="환영합니다. 무엇을 도와드릴까요?", width=1500, height=2, fg="black", relief="solid",background="pink",
        borderwidth="3",foreground="white",font=font)
    btn4=tkinter.Button(newWindow2,text="                            FOOD                            ",overrelief="solid",relief="solid",borderwidth=3
        ,background="chocolate1",foreground="white",font=font_btn2,activebackground="Hotpink1",highlightthickness=3,command=btn_4)
    btn5=tkinter.Button(newWindow2,text="                            LIFE                            ",overrelief="solid",relief="solid",borderwidth=3
        ,background="DarkSeaGreen1",foreground="white",font=font_btn2,activebackground="SeaGreen2",highlightthickness=3,command=btn_5)
    
    label.pack()
    btn5.pack(side="right",fill="y")
    btn4.pack(expand=True,fill="y",anchor="w")

def btn_3(): #쇼핑 종료
    messagebox1=messagebox.askquestion("쇼핑을 종료하시겠습니까?","     쇼핑을     \n종료하시겠습니까\n      ??????    ")
    if messagebox1 =='yes':
        messagebox.showinfo("쇼핑을 종료합니다.","   이용해주셔서 감사합니다.   \n 안녕히 가십시오~ପ(｡ᵔ ⩊ ᵔ｡)ଓ")
    else:
        messagebox.showinfo("쇼핑을 계속합니다.","ପ쇼핑을 계속합니다.ଓ")
    
def btn_4(): #식료품 안내
    newWindow4 = tkinter.Toplevel(window)
    newWindow4.title("FOOD")
    newWindow4.geometry("1920x1080")

    btn_fruit=tkinter.Button    (newWindow4,text="     과일     ",overrelief="solid",relief="solid",borderwidth=3,background="black",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_fru)
    btn_vegitable=tkinter.Button(newWindow4,text="     채소     ",overrelief="solid",relief="solid",borderwidth=3,background="white",foreground="black",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_veg)
    btn_rice=tkinter.Button     (newWindow4,text=" 쌀/잡곡/견과  ",overrelief="solid",relief="solid",borderwidth=3,background="red",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_ric)
    btn_meat=tkinter.Button     (newWindow4,text="  정육/계란류  ",overrelief="solid",relief="solid",borderwidth=3,background="lime",foreground="black",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_mea)
    btn_fish=tkinter.Button     (newWindow4,text=" 수산물/건해산 ",overrelief="solid",relief="solid",borderwidth=3,background="blue",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_fis)
    btn_milk=tkinter.Button     (newWindow4,text=" 우유/유제품류 ",overrelief="solid",relief="solid",borderwidth=3,background="yellow",foreground="black",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_mil)
    btn_meelkit=tkinter.Button  (newWindow4,text=" 밀키트/간편식 ",overrelief="solid",relief="solid",borderwidth=3,background="cyan",foreground="black",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_mee)
    btn_kimchi=tkinter.Button   (newWindow4,text=" 김치/반찬/델리 ",overrelief="solid",relief="solid",borderwidth=3,background="magenta",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_kim)
    btn_water=tkinter.Button    (newWindow4,text=" 생수/음료/주류 ",overrelief="solid",relief="solid",borderwidth=3,background="silver",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_wat)
    btn_coffee=tkinter.Button   (newWindow4,text="  커피/원두/차  ",overrelief="solid",relief="solid",borderwidth=3,background="gray",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_cof)
    btn_noodle=tkinter.Button   (newWindow4,text="  면류/통조림  ",overrelief="solid",relief="solid",borderwidth=3,background="maroon",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_nod)
    btn_sauce=tkinter.Button    (newWindow4,text="   양념/오일   ",overrelief="solid",relief="solid",borderwidth=3,background="olive",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_sau)
    btn_snack=tkinter.Button    (newWindow4,text="   과자/간식   ",overrelief="solid",relief="solid",borderwidth=3,background="green",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_sna)
    btn_bread=tkinter.Button    (newWindow4,text="  베이커리/잼  ",overrelief="solid",relief="solid",borderwidth=3,background="purple",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_bre)
    btn_health=tkinter.Button   (newWindow4,text="    건강식품    ",overrelief="solid",relief="solid",borderwidth=3,background="teal",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_hea)
    btn_back=tkinter.Button     (newWindow4,text=" 뒤로가기 ",overrelief="solid",relief="solid",borderwidth=3,background="navy",foreground="white",width=20,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_2)

    btn_fruit.grid(row=1, column=1)
    btn_vegitable.grid(row=1, column=2)
    btn_rice.grid(row=1, column=3)
    btn_meat.grid(row=1, column=4)
    btn_fish.grid(row=2, column=1)
    btn_milk.grid(row=2, column=2)
    btn_meelkit.grid(row=2, column=3)
    btn_kimchi.grid(row=2, column=4)
    btn_water.grid(row=3, column=1)
    btn_coffee.grid(row=3, column=2)
    btn_noodle.grid(row=3, column=3)
    btn_sauce.grid(row=3, column=4)
    btn_snack.grid(row=4, column=1)
    btn_bread.grid(row=4, column=2)
    btn_health.grid(row=4, column=3)
    btn_back.grid(row=4, column=4)

def btn_5(): #주류 물품 안내
    newWindow5 = tkinter.Toplevel(window)
    newWindow5.title("LIFE")
    newWindow5.geometry("1920x1080")

    btn_tissue=tkinter.Button   (newWindow5,text=" 제지/위생용품 ",overrelief="solid",relief="solid",borderwidth=3,background="black",foreground="white",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_tis)
    btn_clean=tkinter.Button    (newWindow5,text=" 청소/생활용품 ",overrelief="solid",relief="solid",borderwidth=3,background="white",foreground="black",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_cle)
    btn_house=tkinter.Button    (newWindow5,text=" 가구/인테리어 ",overrelief="solid",relief="solid",borderwidth=3,background="red",foreground="white",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_hou)
    btn_kitchen=tkinter.Button  (newWindow5,text=" 주방용품/디지털 ",overrelief="solid",relief="solid",borderwidth=3,background="lime",foreground="black",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_kit)
    btn_life=tkinter.Button     (newWindow5,text=" 생활잡화/공구 ",overrelief="solid",relief="solid",borderwidth=3,background="blue",foreground="white",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_lif)
    btn_peet=tkinter.Button     (newWindow5,text=" 반려동물 ",overrelief="solid",relief="solid",borderwidth=3,background="yellow",foreground="black",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_pet)
    btn_beauty=tkinter.Button   (newWindow5,text=" 뷰티용품 ",overrelief="solid",relief="solid",borderwidth=3,background="cyan",foreground="black",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_bea)
    btn_child=tkinter.Button    (newWindow5,text=" 유아동/완구 ",overrelief="solid",relief="solid",borderwidth=3,background="magenta",foreground="white",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_chi)
    btn_pashion=tkinter.Button  (newWindow5,text=" 패션/언더웨어 ",overrelief="solid",relief="solid",borderwidth=3,background="silver",foreground="white",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_pas)
    btn_goods=tkinter.Button    (newWindow5,text=" 잡화/명품 ",overrelief="solid",relief="solid",borderwidth=3,background="gray",foreground="white",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_god)
    btn_sports=tkinter.Button   (newWindow5,text=" 스포츠/여행/자동차 ",overrelief="solid",relief="solid",borderwidth=3,background="maroon",foreground="white",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_spo)
    btn_back2=tkinter.Button  (newWindow5,text=" 뒤로가기 ",overrelief="solid",relief="solid",borderwidth=3,background="olive",foreground="white",width=26,height=4,font=font_btn4,activebackground="MediumPurple1",highlightthickness=3,command=btn_2)
  
    btn_tissue.grid(row=1, column=1)
    btn_clean.grid(row=1, column=2)
    btn_house.grid(row=1, column=3)
    btn_kitchen.grid(row=2, column=1)
    btn_life.grid(row=2, column=2)
    btn_peet.grid(row=2, column=3)
    btn_beauty.grid(row=3, column=1)
    btn_child.grid(row=3, column=2)
    btn_pashion.grid(row=3, column=3)
    btn_goods.grid(row=4, column=1)
    btn_sports.grid(row=4, column=2)
    btn_back2.grid(row=4, column=3)



label=tkinter.Label(window, text="환영합니다. 무엇을 도와드릴까요?", width=1500, height=2, fg="black", relief="solid",background="pink",
        borderwidth="3",foreground="white",font=font)
btn2=tkinter.Button(window,text="                       물품 안내하기!                  ",overrelief="solid",relief="solid",borderwidth=3,background="DarkSeaGreen1",
        foreground="white",font=font_btn2,activebackground="SeaGreen2",highlightthickness=3,command=btn_2)
btn3=tkinter.Button(window,text="                       쇼핑 그만하기!                  ",overrelief="solid",relief="solid",borderwidth=3,background="LightSteelBlue1",
        foreground="white",font=font_btn2,activebackground="SteelBlue1",highlightthickness=3,command=btn_3)

label.pack()
btn3.pack(side="right",fill="y")
btn2.pack(expand=True,fill="y",anchor="w")

window.mainloop()
