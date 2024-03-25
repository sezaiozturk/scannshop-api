const express = require('express');
const app = express();
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const multer = require('multer');
const cors = require('cors');
const upload = multer({dest: 'uploads/'});
const CompanyModel = require('./models/Company');
const ProductModel = require('./models/Product');
const UserModel = require('./models/User');
const auth = require('./middleware/auth');
const ShoppingCartModel = require('./models/ShoppingCart');
const PastShoppingCartModel = require('./models/PastShoppingCarts');

app.use(cors());
app.use(express.json());

mongoose
    .connect('mongodb://127.0.0.1:27017/ScanNShop')
    .then(() => console.log('Mongodb connected'))
    .catch(err => console.log(err));

app.post('/admin/signup', (req, res) => {
    CompanyModel.create(req.body)
        .then(company => {
            res.json(company);
        })
        .catch(err => {
            res.json(err);
        });
});
app.post('/admin/login', (req, res) => {
    CompanyModel.find({email: req.body.email})
        .then(company => {
            if (req.body.password == company[0].password) {
                res.json(company);
            } else {
                res.json({message: 'şifre yanlış'});
            }
        })
        .catch(err => {
            res.json(err);
        });
});

app.post('/admin/add', (req, res) => {
    ProductModel.create(req.body)
        .then(product => {
            res.json(product);
        })
        .catch(err => {
            res.json(err);
        });
});

app.post('/admin/find', (req, res) => {
    ProductModel.find({companyId: req.body.companyId})
        .then(products => {
            res.json(products);
        })
        .catch(err => {
            res.json(err);
        });
});
app.post('/admin/delete', (req, res) => {
    const {_id} = req.body;
    ProductModel.findByIdAndDelete({_id})
        .then(product => {
            res.json(product);
        })
        .catch(err => {
            res.json(err);
        });
});
app.post('/admin/update', (req, res) => {
    const {_id, companyId, category, image, barkod, name, price, date} =
        req.body;

    ProductModel.findByIdAndUpdate(
        {_id},
        {companyId, category, image, barkod, name, price, date},
        {new: true},
    )
        .then(product => {
            res.json(product);
        })
        .catch(err => {
            res.json(err);
        });
});
app.post('/companies', (req, res) => {
    CompanyModel.find()
        .then(company => {
            res.json(company);
        })
        .catch(err => {
            res.json(err);
        });
});

app.post('/admin/upload', upload.single('file'), (req, res) => {
    const fileName = req.file.filename;
    const filePath = req.file.path;

    res.json({
        message: 'File uploaded successfully',
        fileName: fileName,
        filePath: filePath,
    });
});

app.use('/uploads', express.static('uploads'));

//************************************************************************* */

app.post('/user/signup', async (req, res) => {
    const {name, email, password} = req.body;
    let user = await UserModel.findOne({email: email});

    if (user) return res.send('bu mail zaten var');

    const hashedPassword = await bcrypt.hash(password, 10);

    user = new UserModel({
        name,
        email,
        password: hashedPassword,
    });

    await user.save();
    const token = user.createAuthToken();
    res.header('x-auth-token', token).send(true);
});

app.post('/user/login', async (req, res) => {
    const {email, password} = req.body;
    let user = await UserModel.findOne({email: email});

    if (!user)
        return res.send({user: null, message: 'hatalı şifre yada email'});

    const isSuccess = await bcrypt.compare(password, user.password);

    if (!isSuccess)
        return res.send({user: null, message: 'hatalı şifre yada email'});

    const token = user.createAuthToken();
    res.header('x-auth-token', token).send({user});
});

app.post('/user/updateShoppingCart', auth, async (req, res) => {
    const {_id, shoppingCarts} = req.body;

    let basket = await ShoppingCartModel.findOne({_id});
    if (!basket) {
        ShoppingCartModel.create(req.body)
            .then(basket => {
                res.json(basket);
            })
            .catch(err => {
                res.json(err);
            });
    } else {
        const updated = {
            shoppingCarts: shoppingCarts,
        };
        await ShoppingCartModel.updateOne({_id}, {$set: updated})
            .then(basket => {
                res.json(basket);
            })
            .catch(err => {
                res.json(err);
            });
    }
});

app.post('/user/getShoppingCart', auth, async (req, res) => {
    const {_id} = req.body;
    const existingRecord = await ShoppingCartModel.findOne({_id});

    if (existingRecord) {
        res.send(existingRecord);
    } else {
        res.send([]);
    }
});

app.post('/user/pay', auth, async (req, res) => {
    const {_id, shoppingCarts} = req.body;
    let basket = await PastShoppingCartModel.findOne({_id});

    if (!basket) {
        PastShoppingCartModel.create({
            _id,
            pastShoppingCarts: [{shoppingCarts}],
        })
            .then(basket => {
                res.json(basket);
            })
            .catch(err => {
                res.json(err);
            });
    } else {
        await PastShoppingCartModel.findByIdAndUpdate(
            {_id},
            {$push: {pastShoppingCarts: [{shoppingCarts}]}},
            {new: true},
        )
            .then(basket => {
                res.json(basket);
            })
            .catch(err => {
                res.json(err);
            });
    }
});

app.post('/user/getPastShoppingCart', auth, async (req, res) => {
    const {_id} = req.body;
    const existingRecord = await PastShoppingCartModel.findOne({_id});

    if (existingRecord) {
        res.send(existingRecord);
    } else {
        res.send([]);
    }
});

app.listen(3000, () => {
    console.log('listening on port 3000');
});
