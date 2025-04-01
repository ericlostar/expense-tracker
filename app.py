import pandas as pd
import datetime

# 基础分类关键词
categories = {
    'Medical': ['doctor', 'hospital', 'medicine', 'pharmacy'],
    'Education': ['school', 'tuition', 'bookstore', 'university'],
    'Business': ['office', 'stationery', 'client', 'business'],
    'Charity': ['donation', 'charity'],
    'Transportation': ['gas', 'uber', 'taxi', 'bus'],
    'Personal': ['restaurant', 'movie', 'shopping', 'amazon']
}

# 自动分类函数
def categorize_expense(description):
    description = description.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                return category
    return 'Other'

# 创建空DataFrame来存放消费记录
columns = ['Date', 'Merchant', 'Description', 'Amount', 'Category', 'Entered By']
expenses_df = pd.DataFrame(columns=columns)

# 手动添加消费记录
def add_expense(date, merchant, description, amount, entered_by):
    category = categorize_expense(description)
    global expenses_df
    expenses_df = pd.concat([expenses_df, pd.DataFrame([{
        'Date': date,
        'Merchant': merchant,
        'Description': description,
        'Amount': amount,
        'Category': category,
        'Entered By': entered_by
    }])], ignore_index=True)

# 从CSV导入消费记录
def import_expenses_from_csv(csv_file, entered_by):
    global expenses_df
    imported_df = pd.read_csv(csv_file)
    imported_df['Category'] = imported_df['Description'].apply(categorize_expense)
    imported_df['Entered By'] = entered_by
    expenses_df = pd.concat([expenses_df, imported_df[columns]], ignore_index=True)

# 导出分类后的消费记录

def export_expenses_to_csv(filename=None):
    global expenses_df
    if filename is None:
        filename = f'expenses_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
    expenses_df.to_csv(filename, index=False)
    print(f'Expenses exported to {filename}')

# 示例用法
add_expense('2025-04-01', 'Walgreens', 'Medicine prescription', 20.50, 'Alice')
add_expense('2025-04-02', 'Uber', 'Ride to office', 15.00, 'Bob')

# 从CSV导入示例（CSV文件需包含Date,Merchant,Description,Amount四列）
# import_expenses_from_csv('expenses_input.csv', 'Charlie')

# 导出数据
export_expenses_to_csv()
