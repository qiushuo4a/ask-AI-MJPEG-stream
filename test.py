import flet as ft
import time



def main(page: ft.Page):
    pass

    def add_button(e):
        t.data +=1
        t.text = str(t.data)
        t.update()

    counter = ft.Text("0", size=20)
    t=ft.ElevatedButton(text="点我", data=0,on_click=add_button)
    


    page.add(
        ft.Column(
            controls=[
                ft.Text("babaBOIE__666", size=20, font_family="Noto Sans", color="#85bce7"),
                ft.Text("beautoful", text_align=ft.TextAlign.RIGHT),
            ]
        ),
        ft.Row(
            controls=[
                counter,
                t
            ]
        )
    )


ft.app(main)
