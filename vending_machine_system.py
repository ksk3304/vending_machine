class Suica:
    count = 1

    def __init__(self, name, balance):
        self.name = name
        self._balance = 500 + balance
        self.account_number = Suica.count
        Suica.count += 1

    def charge(self, charge):
        try:
            if charge < 100:
                raise Exception("100円以上の金額をチャージして下さい")
            self._balance += charge
            return self._balance
        except Exception as e:
            return e

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        self._balance = balance


class VendingMachine:
    def __init__(self):
        self.name = "ペプシ"
        self.price = 150
        self.stock = 5
        self._total_sales = 0
        self.product_list = [{"name": self.name, "price": self.price, "stock": self.stock}]

    @property
    def total_sales(self):
        return self._total_sales

    @total_sales.setter
    def total_sales(self, total_sales):
        self._total_sales = total_sales

    def sales_judge(self, suica):
        available_list = [i["name"] for i in self.product_list if suica.balance >= i["price"]]
        return available_list

    def show_stock(self):
        stock_list = [f"{i["name"]}：{i["stock"]}本" for i in self.product_list]
        return stock_list

    def lineup_expand(self):
        self.name = "いろはす"
        self.price = 120
        self.stock = 5
        self.product_list.append({"name": self.name, "price": self.price, "stock": self.stock})
        self.name = "モンスター"
        self.price = 230
        self.stock = 5
        self.product_list.append({"name": self.name, "price": self.price, "stock": self.stock})
        return "商品を拡充しました。"
    
    def add_stock(self, product, stock):
        for i in self.product_list:
            if i["name"] == product:
                i["stock"] += stock
                return f"{i["name"]}:{stock}本追加して現在{i["stock"]}本"


class Purchase:
    def __init__(self, suica, vendingmachine, product):
        self.product = product
        self.vm = vendingmachine
        self.suica = suica
        target_price = int([i["price"] for i in self.vm.product_list if i["name"] == product][0])
        target_stock = int([i["stock"] for i in self.vm.product_list if i["name"] == product][0])
        self.price = target_price
        self.stock = target_stock

    def product_purchase(self):
        try:
            if self.suica.balance < self.price:
                raise Exception("Suicaのチャージ残高が不足しております")
            if self.stock == 0:
                raise Exception("在庫がありません")
            balance = self.suica.balance
            balance -= self.price
            self.suica.balance = balance
            total_sales = self.vm.total_sales
            total_sales += self.price
            self.vm.total_sales = total_sales
            self.stock -= 1
            for i in self.vm.product_list:
                if i["name"] == self.product:
                    i["stock"] = self.stock
            return f"{self.product}の購入が完了しました。"
        except Exception as e:
            return e
