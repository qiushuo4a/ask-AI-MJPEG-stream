"""
提供软件设置功能和页面
"""
import flet as ft 
import webbrowser
import utils

fontsize1 = 18 



def open_website(url):
    """打开一个网站"""
    webbrowser.open(url)





def Settings_page(page:ft.Page):
    # page.title = "软件设置"

    #设置项生成器
    # def Setting_lable(text,)

    def return_main_page(e):
        page.go("/")
        pass

    title = ft.Container(
        content=ft.Row(
            controls=[
                ft.Button(icon=ft.Icons.ARROW_BACK,text="返回主页",on_click=return_main_page,),
                ft.Text(value="设置页面", text_align=ft.TextAlign.CENTER, size=20,expand=True),
                ft.Text(value="Ver 0.13",selectable=True)
            ],
            # alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.BLUE_50,
        padding=10,
        border_radius=8,

    )

    def get_APIKEY_web (e):
        input_APIKEY.label = "请填入 API_KEY"
        input_APIKEY.update()
        pass

    input_APIKEY =ft.TextField(value="",label="API_KEY",expand=True)
    btn_get_APIKEY = ft.Button(icon=ft.Icons.INSERT_LINK,text="前往获取",on_click=get_APIKEY_web)

    #输入api key的地方
    lable_api_key = ft.Row(
        controls=([
            ft.Text(value="API_KEY",size=fontsize1),
            input_APIKEY,
            btn_get_APIKEY
            ])
                              )

    #设置连接的默认地址
    def set_default_addr(e):
        pass

    lable_default_addr = ft.Row(
        controls=([
            ft.Text(value="默认地址",size=fontsize1),
            ft.TextField(value="",label="默认地址",expand=True),
            ft.Button(icon=ft.Icons.SETTINGS_BACKUP_RESTORE,text="使用默认",on_click=set_default_addr)
            ])
                              )
    

    def set_default_prompt(e):
        pass

    lable_prompt = ft.Row(
    controls=([
        ft.Text(value="传入提示词",size=fontsize1),
        ft.TextField(value=None,label="请填入提示词",expand=True),
        ft.Button(icon=ft.Icons.SETTINGS_BACKUP_RESTORE,text="使用默认",on_click=set_default_prompt)
        ])
                            )


    settings_column = ft.Column(
        controls=[
            lable_api_key,
            lable_default_addr,
            lable_prompt
                  ],
    )



    display_view = ft.View(
        route="/settings" ,
        controls=[
            title,
            settings_column,
        ]
    )
    return display_view


    pass

def main(page: ft.Page):

    def route_change(route):
        page.views.clear()
        if route == "/settings":
            page.views.append(Settings_page(page))
        # 可以添加更多路由分支
        page.update()

    def mix_change_route(route):
        utils.change_route(page,route.route)

    
    page.on_route_change = mix_change_route


    page.go("/settings")

if __name__ == "__main__" :
    ft.app(main)

