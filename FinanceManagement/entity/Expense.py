class Expense:
    def __init__(self, expense_id=None, user_id=None, amount=0.0, category_id=None, date=None, description=''):
        self.__expense_id = expense_id
        self.__user_id = user_id
        self.__amount = amount
        self.__category_id = category_id
        self.__date = date
        self.__description = description

    # Getters
    def get_expense_id(self): return self.__expense_id
    def get_user_id(self): return self.__user_id
    def get_amount(self): return self.__amount
    def get_category_id(self): return self.__category_id
    def get_date(self): return self.__date
    def get_description(self): return self.__description

    # Additional alias (fixes your error)
    def get_expense_date(self): return self.__date  # Optional alias

    # Setters
    def set_expense_id(self, eid): self.__expense_id = eid
    def set_user_id(self, uid): self.__user_id = uid
    def set_amount(self, amt): self.__amount = amt
    def set_category_id(self, cid): self.__category_id = cid
    def set_date(self, d): self.__date = d
    def set_description(self, desc): self.__description = desc
