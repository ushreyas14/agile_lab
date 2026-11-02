import json
import os
from datetime import date

DATA_FILE = 'data.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'students': [], 'attendance': {}}


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_student(data):
    name = input("Enter student name: ").strip()
    if name and name not in data['students']:
        data['students'].append(name)
        save_data(data)
        print(f"Added: {name}")
    else:
        print("Name is empty or already exists.")


def remove_student(data):
    if not data['students']:
        print("No students to remove.")
        return
    print("Students:", data['students'])
    name = input("Enter name to remove: ").strip()
    if name in data['students']:
        data['students'].remove(name)
        for day in data['attendance']:
            data['attendance'][day].pop(name, None)
        save_data(data)
        print(f"Removed: {name}")
    else:
        print("Student not found.")


def mark_attendance(data):
    if not data['students']:
        print("No students registered.")
        return
    today = str(date.today())
    print(f"\nMarking attendance for {today}")
    attendance_data = {}
    for student in data['students']:
        status = input(f"  {student} (present/absent) [default: absent]: ").strip().lower()
        attendance_data[student] = status if status in ('present', 'absent') else 'absent'
    if today not in data['attendance']:
        data['attendance'][today] = {}
    data['attendance'][today].update(attendance_data)
    save_data(data)
    print("Attendance saved.")


def view_records(data):
    if not data['attendance']:
        print("No attendance records yet.")
        return
    for day, records in sorted(data['attendance'].items()):
        print(f"\n{day}:")
        for student, status in records.items():
            print(f"  {student}: {status}")


def main():
    data = load_data()
    while True:
        print("\n--- Attendance Tracker ---")
        print("1. Add student")
        print("2. Remove student")
        print("3. Mark attendance")
        print("4. View records")
        print("5. Exit")
        choice = input("Choose (1-5): ").strip()
        if choice == '1':
            add_student(data)
        elif choice == '2':
            remove_student(data)
        elif choice == '3':
            mark_attendance(data)
        elif choice == '4':
            view_records(data)
        elif choice == '5':
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()
