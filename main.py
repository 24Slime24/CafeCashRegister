from Settings.Settings import *
import flet as ft
import random

def main(page: ft.Page):
    page.title="Калькулятор Чека Блюд"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = WIDTH
    page.window_height = HEIGHT
    page.padding = ft.Padding(0, 0, 0, 0)
    page.bgcolor = "#111214"

    receipt_data = []
    tip_percentage = 0

    receipt_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    total_text = ft.Text("0.00 руб.", size=28, weight=ft.FontWeight.BOLD, color="#FFCC00")
    subtotal_text = ft.Text("Блюда: 0.00 руб.", size=14, color=ft.Colors.GREY_500)
    tips_amount_text = ft.Text("Чаевые: 0.00 руб.", size=14, color=ft.Colors.GREY_500)

    def update_receipt():
        nonlocal tip_percentage
        receipt_column.controls.clear()
        total_price = 0.0

        for item in receipt_data:
            receipt_column.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(item["name"], size=16, weight=ft.FontWeight.W_500, color="#E3E3E3"),
                            ft.Text(f"{item['price']:.2f} руб.", size=16, weight=ft.FontWeight.BOLD, color="#2ECC71"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    bgcolor="#22252A",
                    padding=ft.Padding(12, 12, 12, 12),
                    border_radius=8,
                    animate_opacity=200
                )
            )
            total_price += item["price"]

        final_tips = total_price * (tip_percentage / 100)
        final_total = total_price + final_tips

        subtotal_text.value = f"Блюда: {total_price:.2f} руб."
        tips_amount_text.value = f"Чаевые ({tip_percentage}%): {final_tips:.2f} руб."
        total_text.value = f"{final_total:.2f} руб."
        page.update()

    def add_to_receipt(e):
        dish_name = e.control.data["name"]
        dish_price = e.control.data["price"]
        receipt_data.append({"name": dish_name, "price": dish_price})
        update_receipt()

    def clear_receipt(e):
        nonlocal tip_percentage
        tip_percentage = 0
        tip_radio_group.value = "0"
        receipt_data.clear()
        update_receipt()

    def confirmPaymentDialog(e):
        if not receipt_data:
            return
        confirmDialog.open = True
        page.update()

    def confirmPayment(e):
        confirmDialog.open = False
        clear_receipt(e)
        # Создаем и открываем уведомление способом для старых версий Flet:
        page.snack_bar = ft.SnackBar(ft.Text("Заказ успешно оплачен!"), bgcolor=ft.Colors.GREEN_700)
        page.snack_bar.open = True
        page.update()

    def cancelPayment(e):
        confirmDialog.open = False
        page.update()

    menu_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=12)
    for name, price in menu.items():
        menu_column.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column([
                            ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            ft.Text(f"{price:.2f} руб.", color="#2ECC71", size=14, weight=ft.FontWeight.W_600),
                        ], spacing=4),
                        ft.IconButton(
                            icon=ft.Icons.ADD_ROUNDED,
                            icon_color="#FFFFFF",
                            bgcolor="#107C41",
                            icon_size=20,
                            data={"name": name, "price": price},
                            on_click=add_to_receipt,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.Padding(16, 16, 16, 16),
                bgcolor="#1C1F22",
                border_radius=12,
                border=ft.Border(
                    top=ft.BorderSide(1, "#2C3036"),
                    bottom=ft.BorderSide(1, "#2C3036"),
                    left=ft.BorderSide(1, "#2C3036"),
                    right=ft.BorderSide(1, "#2C3036")
                ),
                shadow=ft.BoxShadow(blur_radius=4, color="#050505", offset=ft.Offset(0, 2))
            )
        )

    confirmDialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Подтверждение оплаты", weight=ft.FontWeight.BOLD),
        content=ft.Text("Вы уверены, что хотите оплатить заказ и очистить чек?", size=16),
        actions=[
            ft.TextButton("Отмена", on_click=cancelPayment, style=ft.ButtonStyle(color=ft.Colors.GREY_400)),
            ft.Button("Подтвердить", on_click=confirmPayment, bgcolor="#107C41", color="#FFFFFF")
        ]
    )

    def change_tips(e):
        nonlocal tip_percentage
        tip_percentage = int(e.control.value)
        update_receipt()

    tip_radio_group = ft.RadioGroup(
        content=ft.Row([
            ft.Text("Чаевые: ", size=14, color=ft.Colors.GREY_400, weight=ft.FontWeight.W_500),
            ft.Radio(value="0", label="0%", active_color="#FFCC00"),
            ft.Radio(value="5", label="5%", active_color="#FFCC00"),
            ft.Radio(value="10", label="10%", active_color="#FFCC00"),
            ft.Radio(value="15", label="15%", active_color="#FFCC00"),
        ], alignment=ft.MainAxisAlignment.START, spacing=10),
        value="0",
        on_change=change_tips
    )

    confirmPaymentBtn = ft.Button(
        content=ft.Row([
            ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, size=20),
            ft.Text("ОПЛАТИТЬ", size=16, weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        bgcolor="#FFCC00",
        color="#111214",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=400,
        height=55,
        on_click=confirmPaymentDialog
    )

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.RESTAURANT_MENU, color="#107C41", size=24),
                            ft.Text("Меню блюд", size=22, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ], spacing=10),
                        ft.Divider(color="#2C3036", height=20),
                        menu_column
                    ]),
                    expand=5,
                    padding=ft.Padding(24, 24, 24, 24),
                ),

                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Row([
                                ft.Icon(ft.Icons.RECEIPT_LONG_ROUNDED, color="#FFCC00", size=24),
                                ft.Text("Ваш Чек", size=22, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            ], spacing=10),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color=ft.Colors.RED_ACCENT_200,
                                on_click=clear_receipt,
                                tooltip="Очистить чек"
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(color="#2C3036", height=20),

                        receipt_column,

                        ft.Divider(color="#2C3036", height=20),

                        tip_radio_group,

                        ft.Container(
                            content=ft.Column([
                                subtotal_text,
                                tips_amount_text,
                                ft.Row([
                                    ft.Text("Итого к оплате:", size=16, weight=ft.FontWeight.W_500,
                                            color=ft.Colors.GREY_400),
                                    total_text
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                            ], spacing=6),
                            padding=ft.Padding(0, 10, 0, 15)
                        ),

                        ft.Row([confirmPaymentBtn], alignment=ft.MainAxisAlignment.CENTER)
                    ]),
                    expand=4,
                    padding=ft.Padding(24, 24, 24, 24),
                    bgcolor="#1C1F22",
                    border=ft.Border(
                        left=ft.BorderSide(1, "#2C3036"),
                        top=ft.BorderSide(0, "transparent"),
                        right=ft.BorderSide(0, "transparent"),
                        bottom=ft.BorderSide(0, "transparent")
                    )
                )
            ],
            expand=True,
            spacing=0
        )
    )

    page.overlay.append(confirmDialog)


if __name__ == "__main__":
    ft.run(main)
