class Suica:
    count = 1

    def __init__(self, name):
        self.name = name
        self._balance = 500
        self.account_number = Suica.count
        Suica.count += 1

    def charge(self, charge):
        try:
            if charge < 100:
                raise Exception("100円以上の金額をチャージして下さい")
            self._balance += charge
            return f"チャージが完了しました。現在のチャージ残高:{self._balance}円"
        except Exception as e:
            return e

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        self._balance = balance