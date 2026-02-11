import json
import datetime
from datetime import timedelta

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
DATA_FILE = "library_data.json"
FINE_PER_DAY = 1.00  # Phase 4: Change Request (Late Fee)
LOAN_PERIOD_DAYS = 7

# ==========================================
# DATA HANDLING (PERSISTENCE)
# ==========================================
def load_data():
    """Loads library data from a JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default empty structure if file doesn't exist
        return {"books": [], "loans": []}

def save_data(data):
    """Saves library data to a JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ==========================================
# CORE FUNCTIONS (PHASE 2 & 5)
# ==========================================
def add_book(data):
    """Phase 2: Functional Requirement - Add Book"""
    print("\n--- ADD NEW BOOK ---")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    
    # Simple validation
    if any(b['isbn'] == isbn for b in data['books']):
        print("Error: Book with this ISBN already exists!")
        return

    new_book = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "is_borrowed": False
    }
    
    data['books'].append(new_book)
    save_data(data)
    print(f"Success: '{title}' added to library.")

def search_book(data):
    """Phase 2: Functional Requirement - Search Book"""
    print("\n--- SEARCH BOOKS ---")
    query = input("Enter Title or Author to search: ").lower()
    
    results = [b for b in data['books'] if query in b['title'].lower() or query in b['author'].lower()]
    
    if not results:
        # Phase 6: Bug Fix (Handling empty results)
        print("No results found.")
    else:
        print(f"\nFound {len(results)} matches:")
        print(f"{'ISBN':<15} {'Title':<30} {'Author':<20} {'Status'}")
        print("-" * 75)
        for book in results:
            status = "Borrowed" if book['is_borrowed'] else "Available"
            print(f"{book['isbn']:<15} {book['title']:<30} {book['author']:<20} {status}")

def borrow_book(data):
    """Phase 2: Use Case - Borrow Book"""
    print("\n--- BORROW BOOK ---")
    isbn = input("Enter Book ISBN to borrow: ")
    member_id = input("Enter Member ID: ")

    # Find the book
    book = next((b for b in data['books'] if b['isbn'] == isbn), None)

    if not book:
        print("Error: Book not found.")
        return
    
    if book['is_borrowed']:
        print("Error: Book is already borrowed.")
        return

    # Process Loan
    due_date = datetime.date.today() + timedelta(days=LOAN_PERIOD_DAYS)
    loan_record = {
        "isbn": isbn,
        "member_id": member_id,
        "due_date": str(due_date)
    }

    book['is_borrowed'] = True
    data['loans'].append(loan_record)
    save_data(data)
    print(f"Success: Book borrowed! Due Date: {due_date}")

def return_book(data):
    """Phase 4: Change Request - Late Fee Calculation"""
    print("\n--- RETURN BOOK ---")
    isbn = input("Enter Book ISBN to return: ")
    
    # Find the loan record
    loan = next((l for l in data['loans'] if l['isbn'] == isbn), None)
    
    if not loan:
        print("Error: No active loan found for this book.")
        return

    # Calculate Fine
    due_date = datetime.datetime.strptime(loan['due_date'], "%Y-%m-%d").date()
    return_date = datetime.date.today()
    
    overdue_days = (return_date - due_date).days
    
    print(f"\nReturn Details:")
    print(f"Due Date: {due_date}")
    print(f"Return Date: {return_date}")
    
    if overdue_days > 0:
        fine = overdue_days * FINE_PER_DAY
        print(f"⚠️  BOOK IS OVERDUE BY {overdue_days} DAYS.")
        print(f"💰 LATE FEE APPLICABLE: ${fine:.2f}")
    else:
        print("✅ Book returned on time. No fine.")

    # Confirm Return
    confirm = input("Confirm return? (y/n): ")
    if confirm.lower() == 'y':
        # Update Data
        book = next(b for b in data['books'] if b['isbn'] == isbn)
        book['is_borrowed'] = False
        data['loans'].remove(loan)
        save_data(data)
        print("Success: Book returned.")
    else:
        print("Return cancelled.")

# ==========================================
# MAIN MENU (UI)
# ==========================================
def main():
    data = load_data()
    
    while True:
        print("\n=== LIBRARY MANAGEMENT SYSTEM (v3.0) ===")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Borrow Book")
        print("4. Return Book (with Fine Calculation)")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            add_book(data)
        elif choice == '2':
            search_book(data)
        elif choice == '3':
            borrow_book(data)
        elif choice == '4':
            return_book(data)
        elif choice == '5':
            print("Exiting system...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()