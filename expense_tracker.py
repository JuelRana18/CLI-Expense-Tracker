import json
import os
from datetime import datetime

FILE_NAME = 'expenses.json'


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(expenses):
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(expenses, file, indent=4, ensure_ascii=False)


def add_expense(expenses):
    print('\n--- Add Expense ---')

    title = input('Title: ').strip()

    if not title:
        print('Title cannot be empty.')
        return

    try:
        amount = float(input('Amount: '))

        if amount <= 0:
            print('Amount must be greater than 0.')
            return

    except ValueError:
        print('Please enter a valid amount.')
        return

    category = input('Category: ').strip()

    if not category:
        category = 'Other'

    expense = {
        'id': max([e['id'] for e in expenses], default=0) + 1,
        'title': title,
        'amount': amount,
        'category': category,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    }

    expenses.append(expense)
    save_expenses(expenses)

    print('Expense added successfully!')


def show_expenses(expenses):
    print('\n--- All Expenses ---')

    if not expenses:
        print('No expenses found.')
        return

    print('-' * 75)
    print(f"{'ID':<5} {'Title':<20} {'Amount':>10} {'Category':<15} {'Date':<20}")
    print('-' * 75)

    for expense in expenses:
        print(
            f"{expense['id']:<5} "
            f"{expense['title'][:20]:<20} "
            f"{expense['amount']:>10.2f} "
            f"{expense['category'][:15]:<15} "
            f"{expense['date']:<20}"
        )

    print('-' * 75)


def show_total(expenses):
    total = sum(expense['amount'] for expense in expenses)

    print('\n--- Total Expense ---')
    print(f"Total: RM {total:.2f}")


def category_summary(expenses):
    print('\n--- Category Summary ---')

    if not expenses:
        print('No expenses found.')
        return

    categories = {}

    for expense in expenses:
        category = expense['category']
        categories[category] = categories.get(category, 0) + expense['amount']

    for category, amount in sorted(categories.items()):
        print(f"{category:<20} RM {amount:.2f}")


def delete_expense(expenses):
    print('\n--- Delete Expense ---')

    if not expenses:
        print('No expenses found.')
        return

    show_expenses(expenses)

    try:
        expense_id = int(input('\nEnter expense ID to delete: '))
    except ValueError:
        print('Please enter a valid ID.')
        return

    for expense in expenses:
        if expense['id'] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)

            print('Expense deleted successfully!')
            return

    print('Expense ID not found.')


def main():
    expenses = load_expenses()

    while True:
        print('\n')
        print('=' * 40)
        print('CLI EXPENSE TRACKER')
        print('=' * 40)

        print('1. Add Expense')
        print('2. Show Expenses')
        print('3. Show Total')
        print('4. Category Summary')
        print('5. Delete Expense')
        print('6. Exit')

        choice = input('\nChoose an option: ').strip()

        if choice == '1':
            add_expense(expenses)

        elif choice == '2':
            show_expenses(expenses)

        elif choice == '3':
            show_total(expenses)

        elif choice == '4':
            category_summary(expenses)

        elif choice == '5':
            delete_expense(expenses)

        elif choice == '6':
            print('\nGoodbye!')
            break

        else:
            print('Invalid option. Please choose 1-6.')


if __name__ == '__main__':
    main()