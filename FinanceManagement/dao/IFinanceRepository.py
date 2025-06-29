from abc import ABC, abstractmethod

class IFinanceRepository(ABC):

    @abstractmethod
    def createUser(self, user): pass

    @abstractmethod
    def createExpense(self, expense): pass

    @abstractmethod
    def deleteUser(self, user_id): pass

    @abstractmethod
    def deleteExpense(self, expense_id): pass

    @abstractmethod
    def getAllCategories(self) -> list: pass

    @abstractmethod
    def getAllExpenses(self, user_id): pass

    @abstractmethod
    def updateExpense(self, user_id, expense): pass
