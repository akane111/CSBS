import socket

# 创建客户端套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8888))

while True:
    # 获取用户输入
    action = input('请选择操作（add-添加联系人，update-修改联系人，delete-删除联系人，search-搜索联系人，quit-退出）：')

    if action == 'quit':
        break

    elif action in ['add', 'update', 'delete']:
        name = input('请输入联系人姓名：')
        address = input('请输入联系人住址：')
        phone = input('请输入联系人电话：')

        # 构造请求
        request = f'{action},{name},{address},{phone}'

    elif action == 'search':
        keyword = input('请输入关键字：')

        # 构造请求
        request = f'{action},{keyword}'

    else:
        print('无效的操作')
        continue

    # 发送请求给服务器
    client_socket.send(request.encode())

    # 接收服务器响应
    response = client_socket.recv(1024).decode()

    # 显示响应结果
    print('服务器响应：', response)

# 关闭客户端套接字
client_socket.close()
