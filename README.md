# CIBC-Budgeting-App
This app parses your bank transactions into a formatted table. It then calculates your lifetime/yearly expenses and income to allow for easy budgetting. More is coming!

## How to use if your bank is not supported

1) Ensure you have Python 3.7+ and all the dependancies in requirements.txt installed.

    `pip install -r requirements.txt`
2) Download your bank transactions in .csv format. Most banks provide this on their site, you just have to find it.
3) Navigate to `app/BankClassify.py` and create a method that parses your banks data. It must return a pandas dataframe with columns of `date`, `desc`, and `amount`.
4) Then modify the add_data method to include the method you created.
5) Run any of the scripts in app/models. 


## How to use if your bank is supported
