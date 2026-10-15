import flet as ft


def main(page: ft.Page):
    page.title = "Калькулятор Чека Блюд"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 600

    # Меню блюд
    menu_items = {
        "Пицца Маргарита": 15.00,
        "Паста Карбонара": 12.50,
        "Салат Цезарь": 9.00,
        "Суп Том Ям": 14.00,
        "Кофе Капучино": 3.50,
        "Чизкейк": 6.00
    }

    receipt_data = []

    receipt_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("Итого: 0.00 руб.", size=20, weight=ft.FontWeight.BOLD)

    def update_receipt():
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

        total_text.value = f"Итого: {total_price:.2f} руб."
        page.update()

    def add_to_receipt(e):
        dish_name = e.control.data["name"]
        dish_price = e.control.data["price"]
        receipt_data.append({"name": dish_name, "price": dish_price})
        update_receipt()

    def clear_receipt(e):
        receipt_data.clear()
        update_receipt()

    # Создаем меню без использования сложных модулей border/margin
    menu_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    for name, price in menu_items.items():
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
                # Вместо сложных классов используем простые числа и логические значения:
                animate_opacity=True,
                border_radius=8  # Просто число, без .all()
            )
        )

    # Собираем главный экран (также убраны все сложные border)
    page.add(
        ft.Row(
            [
                # Левая колонка - Меню
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

                # Правая колонка - Чек
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Ваш Чек", size=22, weight=ft.FontWeight.BOLD),
                            ft.TextButton("Очистить", on_click=clear_receipt, icon=ft.Icons.DELETE)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(),
                        receipt_column,
                        ft.Divider(),
                        total_text
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


if __name__ == "__main__":
    ft.run(main)
