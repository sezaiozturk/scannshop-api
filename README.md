# scannshop-api

Bu proje, scanNShop web ve mobil uygulaması için gerekli olan backend API'sini sağlayan bir Node.js uygulamasıdır.

## Giriş

scannshop-api, scanNShop uygulaması için gerekli olan backend hizmetlerini sağlar. Bu API, ürün bilgilerini sağlamak, kullanıcı yönetimi ve istek listesi işlevselliğini gerçekleştirmek için kullanılabilir.

## Özellikler

- **CRUD İşlemleri**: 
  - **Ürünler**: Ürünleri oluşturma, okuma, güncelleme ve silme işlemleri.
  - **Kullanıcılar**: Kullanıcı hesaplarını oluşturma, güncelleme, silme ve oturum açma işlemleri.
  - **İstek Listesi**: Kullanıcıların ürünleri istek listelerine ekleme, güncelleme ve silme işlemleri.

- **Gelen İsteklerin Yönetimi**: 
  - Sunucu üzerinde gelen HTTP isteklerini yönetir ve uygun yanıtları döner.
  - API isteklerini verimli bir şekilde işlemek için çeşitli HTTP metodlarını destekler.

- **Child Process Kullanımı**:
  - Yoğun ve zaman alıcı işlemleri ana iş parçacığını engellemeden yönetmek için Node.js `child_process` modülünü kullanır.
  -`.py` dosyalarını çalıştırarak Python tabanlı işlemleri yürütür, böylece Python kodunu Node.js uygulamasından bağımsız olarak çalıştırabilir.

- **Veri Güvenliği ve Doğrulama**:
  - JSON Web Tokens (JWT) ile güvenli kimlik doğrulama ve yetkilendirme sağlar.
  - Veri doğrulama ve sanitasyon işlemleri ile güvenli API erişimi sunar.

## Kullanılan Teknolojiler

- **Node.js**: Sunucu tarafı JavaScript çalıştırma ortamı.
- **Express.js**: Web uygulamaları ve API'ler için minimal ve esnek Node.js framework'ü.
- **MongoDB**: NoSQL veritabanı.
- **Mongoose**: MongoDB ile çalışmak için kullanılan Node.js kütüphanesi.
- **JWT (JSON Web Tokens)**: Kimlik doğrulama için kullanılan standart.
  
