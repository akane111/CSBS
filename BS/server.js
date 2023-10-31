const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const PORT = 5500;

// 使用body-parser中间件解析请求体
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 模拟存储联系人的数据库
let contacts = [
    { id: 1, name: '张三', address: '北京', phone: '123456789' },
    { id: 2, name: '李四', address: '上海', phone: '987654321' },
];

// 获取所有联系人
app.get('/contacts', (req, res) => {
    res.json(contacts);
});

// 根据关键字搜索联系人
app.get('/contacts/search', (req, res) => {
    const keyword = req.query.keyword;
    const results = contacts.filter(contact =>
        contact.name.includes(keyword) ||
        contact.address.includes(keyword) ||
        contact.phone.includes(keyword)
    );
    res.json(results);
});

// 添加联系人
app.post('/contacts', (req, res) => {
    const newContact = {
        id: contacts.length + 1,
        name: req.body.name,
        address: req.body.address,
        phone: req.body.phone
    };
    contacts.push(newContact);
    res.send('联系人添加成功');
});

// 更新联系人
app.put('/contacts/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const updatedContact = {
        id: id,
        name: req.body.name,
        address: req.body.address,
        phone: req.body.phone
    };
    contacts = contacts.map(contact =>
        contact.id === id ? updatedContact : contact
    );
    res.send('联系人更新成功');
});

// 删除联系人
app.delete('/contacts/:id', (req, res) => {
    const id = parseInt(req.params.id);
    contacts = contacts.filter(contact => contact.id !== id);
    res.send('联系人删除成功');
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`服务器运行在 http://localhost:${PORT}`);
});
