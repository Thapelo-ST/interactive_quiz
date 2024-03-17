import data.db as db
import program_admin
import program_user

def main():
    db.global_init()
    try:
        while True:
            if find_user_intent() == 'Sign-in to test others':
                program_admin.run()
            else:
                program_user.run()
    except KeyboardInterrupt:
        return


def find_user_intent():
    print("[s]Student")
    print("[a]Admin")
    print()
    choice = input("Are you a [s]student or [a]admin?  ")
    if choice == 'a':
        return 'Sign-in To write'

    return 'Sign-in to test others'
