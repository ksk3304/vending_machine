from juice import Juice
from suica import Suica

class VendingMachine:
    def __init__(self):
        pepsi = Juice("ペプシ", 150)
        self.product_list = [{"juice": pepsi, "stock": 5}]
        self._total_sales = 0

    @property
    def total_sales(self):
        return self._total_sales

    @total_sales.setter
    def total_sales(self, total_sales):
        self._total_sales = total_sales

    def sales_judge(self, suica):
        available_list = [i["juice"].name for i in self.product_list if suica.balance >= i["juice"].price] # check because i fixed.
        return f"現在買える商品は{available_list}です。"

    def show_stock(self):
        stock_list = [f"{i["juice"].name}:{i["stock"]}本" for i in self.product_list]
        return f"現在の在庫状況は{stock_list}です。"

    def lineup_expand(self):
        existing_names = {i["juice"].name for i in self.product_list}
        new_products = [("いろはす", 120), ("モンスター", 230)]
        for name, price in new_products:
            if name not in existing_names:
                self.product_list.append({"juice": Juice(name, price), "stock": 5})
        return f"商品を拡充して、現在{[i["juice"].name for i in self.product_list]}を販売中。"
        
    def add_stock(self, product, stock):
        for i in self.product_list:
            if i["juice"].name == product:
                i["stock"] += stock
                return f"{i["juice"].name}の在庫に{stock}本追加して、現在の在庫は{i["stock"]}本。"

    def purchase(self, suica, product):
        self.suica = suica
        selected_product = next((i for i in self.product_list if i["juice"].name == product), None)
        try:
            if self.suica.balance < selected_product["juice"].price:
                raise Exception(f"Suicaのチャージ残高が不足しております。")
            if selected_product["stock"] == 0:
                raise Exception(f"{product}の在庫がありません。")
            self.suica.decrease_balance(selected_product["juice"].price)
            selected_product["stock"] -= 1
            for i in self.product_list:
                if i["juice"].name == product:
                    i["stock"] = selected_product["stock"]
                    return f"{i['juice'].name}の購入が完了しました。"
        except Exception as e:
            return e