import math

class Checks:
    def __init__(self, receipt_data, currentPromocode, currentPromocodeDiscount, tip_percentage):
        self.receipt_data = receipt_data
        self.currentPromocode = currentPromocode
        self.currentPromocodeDiscount = currentPromocodeDiscount
        self.tip_percentage = tip_percentage

    def buildCheck(self):
        lines = [
            "==================================",
            "           КАССОВЫЙ ЧЕК           ",
            "=================================="
        ]
        totalPrice = 0
        for item in self.receipt_data:
            name = item.get("name")
            price = item.get("price")

            line = f"{name}: {price}"

            lines.append(line)
            totalPrice += price

        lines.append("==================================")

        if self.currentPromocode != "":
            lines.append(f"Промокод {self.currentPromocode}: {math.ceil(1 - self.currentPromocodeDiscount)*10}%")
        lines.append(f"Чаевые {self.tip_percentage}%")

        lines.append("==================================")

        lines.append(f"Итого: {totalPrice}")
        return lines

    def toTxt(self):
        lines = self.buildCheck()
        with open("Checks.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(lines))
