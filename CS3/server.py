import socket
import sqlite3

# 创建数据库连接
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# 创建联系人表
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                  (name TEXT PRIMARY KEY, address TEXT, phone TEXT)''')

# 创建服务器套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8888))
server_socket.listen(1)

print('服务器已启动，等待客户端连接...')

while True:
    # 等待客户端连接
    client_socket, client_address = server_socket.accept()
    print('客户端已连接：', client_address)

    while True:
        # 接收客户端请求
        request = client_socket.recv(1024).decode()

        if not request:
            break

        # 解析请求
        request_parts = request.split(',')
        action = request_parts[0]

        if action == 'add':
            # 添加联系人
            name = request_parts[1]
            address = request_parts[2]
            phone = request_parts[3]

            try:
                # 插入联系人信息到数据库
                cursor.execute("INSERT INTO contacts VALUES (?, ?, ?)", (name, address, phone))
                conn.commit()
                response = '联系人已添加'
            except sqlite3.IntegrityError:
                response = '联系人已存在'

        elif action == 'update':
            # 更新联系人
            name = request_parts[1]
            address = request_parts[2]
            phone = request_parts[3]

            try:
                # 更新联系人信息到数据库
                cursor.execute("UPDATE contacts SET address=?, phone=? WHERE name=?", (address, phone, name))
                conn.commit()
                response = '联系人已更新'
            except sqlite3.Error:
                response = '联系人更新失败'

        elif action == 'delete':
            # 删除联系人
            name = request_parts[1]

            try:
                # 从数据库删除联系人信息
                cursor.execute("DELETE FROM contacts WHERE name=?", (name,))
                conn.commit()
                response = '联系人已删除'
            except sqlite3.Error:
                response = '联系人删除失败'

        elif action == 'search':
            # 搜索联系人
            keyword = request_parts[1]

            # 在数据库中查询匹配的联系人信息
            cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR address LIKE ? OR phone LIKE ?",
                           ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
            contacts = cursor.fetchall()

            if contacts:
                response = '\n'.join([f'姓名：{contact[0]}，住址：{contact[1]}，电话：{contact[2]}' for contact in contacts])
            else:
                response = '未找到匹配的联系人'

        else:
            response = '无效的请求'

        # 发送响应给客户端
        client_socket.send(response.encode())

    # 关闭客户端连接
    client_socket.close()

# 关闭数据库连接
conn.close()
