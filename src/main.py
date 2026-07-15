import flet as ft
from home import Homepage_view
import softwareSettings
import utils

ROUTES ={
    "/":Homepage_view ,
    "/settings" : softwareSettings.Settings_page
}




def main(page:ft.Page):
    
    #确定窗口&界面主题
    page.title = "mjpeg 识图工具"
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_100


    def main_change_route (target_page):
        page.views.clear()
        
        view_func = ROUTES.get(page.route)  #找到并简化页面查找

        if page.route == None :
            print ("跳转对象不在Route里")
        else :
            page.views.append(view_func(page)) # type: ignore
        pass
        page.update()

    page.on_route_change = main_change_route
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)