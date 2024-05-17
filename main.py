# login = 'user'
# password = '1234'
# while True:
#     user_login = input()
#     user_password = input()
#     if user_login == login and user_password == password:
#         print('ok')
#         break
#     else:
#         print('error, try again')

# login = 'user'
# password = '1234'
# user_login = input()
# user_password = input()
# while user_login != login or user_password != password:
#     print('error, try again')
#     user_login = input()
#     user_password = input()
# print('ok')

a = input()
mx = -10**10
while a != 'exit':
    a = int(a)
    if a > mx:
        mx = a
    a = input()
print('max:', mx)



