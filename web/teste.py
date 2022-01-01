# import bcrypt
# password = b"123"
# # Hash a password for the first time, with a randomly-generated salt
# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# # Check that an unhashed password matches one that has previously been
# # hashed
# if bcrypt.checkpw(password, b'$2y$10$2OpI.cMEvEc7e.B8eER.XO2ZWIo1qrZRVXu5KC3S4hxO5bC.ij35m'):
#      print("It Matches!")
# else:
#      print("It Does not Match :(")