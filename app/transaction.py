class Transaction:
    def __init__(self, date, name, input_amount, output_amount):
        self.date = date
        self.name = name
        self.input_amount = input_amount
        self.output_amount = output_amount

    def fromJSON(self, json):
        return Transaction(
            json["date"], json["name"], json["input_amount"], json["output_amount"]
        )