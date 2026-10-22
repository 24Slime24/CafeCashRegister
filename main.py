from Settings.Settings import *
import flet as ft
from Classes.Checks import Checks


def main(page: ft.Page):
    page.title = "Калькулятор Чека Блюд"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = WIDTH
    page.window_height = HEIGHT

    receipt_data = []
    currentPromocodeDiscount = 1
    currentPromocode = str()

    # Т1: Переменная для хранения процента чаевых
    tip_percentage = 0

    receipt_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("Итого: 0.00 руб.", size=20, weight=ft.FontWeight.BOLD)

    def update_receipt():
        nonlocal tip_percentage
        receipt_column.controls.clear()
        total_price = 0.0
        for item in receipt_data:
            receipt_column.controls.append(
                ft.Row(
                    [
                        ft.Text(item["name"], size=16),
                        ft.Text(f"{item['price']:.2f} руб.", size=16, weight=ft.FontWeight.W_500),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
            total_price += item["price"]
            total_price *= currentPromocodeDiscount

        final_total = total_price * (1 + tip_percentage / 100)
        total_text.value = f"Итого: {final_total:.2f} руб."
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
        confirmDialog.open = True
        page.update()

    def confirmPayment(e):
        confirmDialog.open = False

        check = Checks(receipt_data, currentPromocode, currentPromocodeDiscount, tip_percentage)
        check.toTxt()

        clear_receipt(e)

    def cancelPayment(e):
        confirmDialog.open = False

    def checkPromocode(e):
        nonlocal currentPromocode, currentPromocodeDiscount
        currentPromocode = e.control.value
        if currentPromocode == "TEEN10":
            currentPromocodeDiscount = 1 + pricingScenarios["TEEN10"]
            promocodeField.prefix_icon = ft.Icons.CHECK
            update_receipt()
        else:
            currentPromocodeDiscount = 1
            promocodeField.prefix_icon = ft.Icons.CLOSE
            update_receipt()

    menu_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    for name, price in menu.items():
        menu_column.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column([
                            ft.Text(name, size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{price:.2f} руб.", color=ft.Colors.GREY_700),
                        ]),
                        ft.IconButton(
                            icon=ft.Icons.ADD_SHOPPING_CART,
                            icon_color=ft.Colors.GREEN,
                            data={"name": name, "price": price},
                            on_click=add_to_receipt
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10,
                animate_opacity=True,
                border_radius=8
            )
        )

    confirmDialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Подтверждение оплаты"),
        content=ft.Text("Вы уверены, что хотите оплатить заказ?"),
        actions=[
            ft.TextButton("Отмена", on_click=cancelPayment),
            ft.TextButton("Подтвердить", on_click=confirmPayment)
        ]
    )

    def change_tips(e):
        nonlocal tip_percentage
        tip_percentage = int(e.control.value)
        update_receipt()

    tip_radio_group = ft.RadioGroup(
        content=ft.Row([
            ft.Text("Чаевые:", size=16, weight=ft.FontWeight.BOLD),
            ft.Radio(value="0", label="0%"),
            ft.Radio(value="5", label="5%"),
            ft.Radio(value="10", label="10%"),
            ft.Radio(value="15", label="15%"),
        ], alignment=ft.MainAxisAlignment.START),
        value="0",
        on_change=change_tips
    )

    confirmPaymentBtn = ft.Button(
        content="Оплатить",
        bgcolor=ft.Colors.YELLOW,
        width=200,
        height=50,
        on_click=confirmPaymentDialog
    )

    promocodeField = ft.TextField(
        label="Введите промокод",
        prefix_icon=ft.Icons.CLOSE,
        width=400,
        on_change=checkPromocode
    )

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Меню блюд", size=22, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        menu_column
                    ]),
                    expand=1,
                    padding=20,
                    border_radius=10
                ),

                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Ваш Чек", size=22, weight=ft.FontWeight.BOLD),
                            ft.TextButton("Очистить", on_click=clear_receipt, icon=ft.Icons.DELETE)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(),
                        receipt_column,
                        ft.Divider(),


                        tip_radio_group,

                        total_text,
                        ft.Row([promocodeField, confirmPaymentBtn], alignment=ft.MainAxisAlignment.END)
                    ]),
                    expand=1,
                    padding=20,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=10
                )
            ],
            expand=True
        )
    )

    page.overlay.append(confirmDialog)


if __name__ == "__main__":
    ft.run(main)
