import math

class Checks:
    def __init__(self, receipt_data, currentPromocode, currentPromocodeDiscount):
        self.receipt_data = receipt_data
        self.currentPromocode = currentPromocode
        self.currentPromocodeDiscount = currentPromocodeDiscount

    def buildCheck(self):
        lines = [
            "==================================",
            "           КАССОВЫЙ ЧЕК           ",
            "=================================="
        ]
        for item in self.receipt_data:
            name = item.get("name")
            price = item.get("price")

            line = f"{name}: {price}"

            lines.append(line)

        lines.append("==================================")
        if self.currentPromocode != "":
            lines.append(f"Промокод {self.currentPromocode}: {math.ceil(1 - self.currentPromocodeDiscount)*10}%")
        return lines

    def toTxt(self):
        lines = self.buildCheck()
        with open("Checks.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(lines))
