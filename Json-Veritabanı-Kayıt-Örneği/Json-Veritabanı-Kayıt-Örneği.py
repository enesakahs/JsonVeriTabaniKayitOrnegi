import json,re,time,random

class Site:
    def __init__(self):
        self.loop=True
        self.datas=self.getdata() #veritabanından kayıt okuma işlemi gerceklestirdigimizde veritabanındaki bilgileri okuyup veriler kısmına iletecek self.veriler=self.verial()

    def program(self): #PROGRAM
        selection=self.menu() #kullanıcının menu kısmında sectıgı degerı alıp secım degıskenıne tanımlıyor.
        
        if selection=="1":
            self.entry() #GİRİŞ
            time.sleep(2)
        if selection=="2":
            self.signup() #KAYIT OL
            time.sleep(2)
        if selection=="3":
            self.exit() #CIKIS
            time.sleep(2)


    def menu(self): #MENU
        def control(selection): #kontrol edecegı yapı secımden gelen yapı
            if re.search("[^1-3]",selection):
                raise Exception ("Lütfen 1-3 arasında gecerli bir secim yapınız")
            elif len(selection)!=1:
                raise Exception ("Lütfen 1-3 arasında gecerli bir secim yapınız")
        while True: #eger 1-3 dısında girirse tekrar secım alabilmesi icin bir dongu kuruyoruz
            try:
                selection=input("merhabalar KAYIT ORNEGI Sitesine hosgeldınız\n\nLutfen yapmak ıstedıgınız ıslemı secınız\n\n1-GİRİS\n2-KAYIT OL\n3-CIKIS\n\n")
                control(selection)
            except Exception as error:
                print(error)
                time.sleep(3)
            else:
                break
        return selection


    def entry(self): #GİRİŞ
        #sistemde kayıtlı olan kullanıcının giris kısmı
        print("Giris Menusune Yönlendiriliyorsunuz...")
        time.sleep(2)
        username=input("Kullanıcı Adınızı Giriniz: ")
        password=input("Kullanıcı Şifrenizi Giriniz: ")
        #username ve pasword degerlerını gırıs kontrol fonk. icine tanımlamamız lazım ki veritabanından gelen bilgilerle karsılastırabilsin.
        result=self.entrycontrol(username,password) #sonuc degıskenıne username,password atadık. sonux degıskenınıde giris kontrolde kullanıcaz
        #[3]. [2] true döndüğü icin sonuc degıskenıne true atayacak
        
        if result==True: 
            self.entrysucces() #[4]
        else:
            self.entryfailed()


    def entrycontrol(self,username,password): #GİRİS KONTROL [2] true dönecek kısım
        #parametre olarak username,password u ekledık.
        #giris kontrol kısmı bıze br sonuc dondurecek. kısının username,password verıtabanında varsa True degerı döndürecek. burdan alınan true veya false degerı sonuc degerıne atanacak

        #listeyi for dongusu ile tarayıp sözlük ıcınden istenilen degerı alacagız
        self.datas=self.getdata() #yani verial fonk. verileri aldı. veriler kısmına attı
        try:
            for user in self.datas["Kullanıcılar"]: #veriler kısmından Kullanıcılar ı taradı
                if user["Kullanıcıadı"]==username and user["Sifre"]==password:
                    return True # username ve password kısının girdigi bilgilerle eslestiyse true dönecek.[1]
        except KeyError:
            return False
        return False
        
    def entrysucces(self): #GİRİS BASARILI
        print("Kontrol Ediliyor..")
        time.sleep(2)
        print("Giris Basarılı. KAYIT ORNEGI Sitesine hosgeldınız")
        self.result=False
        self.loop=False

    def entryfailed(self): #GİRİS BASARISIZ
        print("Giris Bilgileri Hatalı..")
        time.sleep(2)
        self.backtomenu()


    def signup(self): #KAYIT OL YENI KAYIT

        def ControlUserName(UN): #kullanıcı adını kontrol eıyoruz
            if len(UN)<8:
                raise Exception("Kullanıcı adınız en az 8 karakterden olusmalıdır..")
        while True: #kullanıcı 8 karakterden daha az bır deger girerse tekrar sorması ıcın:
            try:
                UN=input("Kullanıcı Adınız: ")
                ControlUserName(UN)
            except Exception as errorname:
                print(errorname)
                time.sleep(2)
            else:
                break

        def ControlPassword(password): #sifreyi adını kontrol eıyoruz
            if len(password)<8:
                raise Exception("Şifreniz en az 8 karakterden olusmalıdır..")
            elif not re.search("[0-9]",password):
                raise Exception("Şifreniz 0-9 arasında en az bir deger barındırmalıdır..")
            elif not re.search("[A-Z]",password):
                raise Exception("Şifreniz en az bir BÜYÜK HARF barındırmalıdır..")
            elif not re.search("[a-z]",password):
                raise Exception("Şifreniz en az bir küçük harf barındırmalıdır..")
        while True: #şifre 8 karakterden daha az bır deger girerse tekrar sorması ıcın:
            try:
                Password=input("Kullanıcı Şifreniz: ")
                ControlPassword(Password)
            except Exception as errorpassword:
                print(errorpassword)
                time.sleep(2)
            else:
                break

        def controlmail(mail): #MAIL kontrol edıyoruz
            if not re.search("@" and ".com",mail): #eger bulundurmuyorsa demek
                raise Exception ("gecerlı bır mail adresi giriniz..")
        while True:
            try:
                mail=input("Mail Adresiniz: ")
                controlmail(mail) 
            except Exception as Errormail:
                print(Errormail)
                time.sleep(2)
            else:
                break
        
        sonuc=self.istherearecord(UN,mail) #kayıt var mı fok. gelecek bilgi sonuc degıskenıne atandı. ve eger kayıt varsa yanı true ise:
        if sonuc==True:
            print("Kullanıcı Adınız ve Mail Sistemde Kayıtlı..")
        else: #kayıt yoksa
            activationcode=self.sendactivation() #AKTİVASYON GONDER kısmı bır kod olusturup activationcode a aktaracak
            #sonra aktivasyon koduyla kısıden ıstedıgım aktıvasyon kodunu eslestırmek ıcın activationcontrol ü yazdık. oradan cıkan true yada false degeri, durum dıye degere atandı
            durum=self.activationcontrol(activationcode)
        while True:
            if durum==True:
                self.savedata(UN,Password,mail)
                break
            else: #ELSE DURUMU ICIN WHİLE DONGUSU OLUSUTURULDU   
                input("aktıvasyon kodu gecersiz. Lütfen tekrar giriniziz...\n...")


    def istherearecord(self,UN,mail): #KAYIT VAR MI?
        self.datas=self.getdata()
        #try blogu ekleme sebebımız kullanıcı adı ve sıfresını tararken bulamazsa python kendı dılınde KeyError hatası verıyo. onu almamak ıcın
        try:
            for kullanıcı in self.datas["Kullanıcılar"]:
                if kullanıcı["Kullanıcıadı"]==UN and kullanıcı["Mail"]==mail:
                    return True
        except KeyError:
            return False
        return False


    def sendactivation(self): #AKTİVASYON GONDER
        with open("C:/Users/enes_/OneDrive/Masaüstü/Python Egitimleri/Json-Veritabanı-Kayıt-Örneği/Aktivasyon.txt","w",encoding="utf-8") as File:
            activation = str(random.randint(10000,99999))
            File.write("Aktivasyon Kodunuz: " + activation)
        return activation


    def activationcontrol(self,activation): #AKTİVASYON KONTROL
        inputactivationcode=input("Maile gelen kodunuzu giriniz: ")
        if activation==inputactivationcode:
            return True
        else:
            return False


    def getdata(self): #VERİ AL (görevi veritabanından verileri alıp icinde barındırmak)
        try:
            with open("C:/Users/OneDrive/Masaüstü/Python Egitimleri/Json-Veritabanı-Kayıt-Örneği/Kullanıcılar.json","r",encoding="utf-8") as File:
                data=json.load(File) #bulursa okuyacak verılerı ıcıne atacak
        except FileNotFoundError: #dosyayı bulamazsa verecegı hata. Dosya yoksa yenı dosya olusturacak
            with open("C:/Users/OneDrive/Masaüstü/Python Egitimleri/Json-Veritabanı-Kayıt-Örneği/Kullanıcılar.json","w",encoding="utf-8") as File:
                File.write("{}")
            with open("C:/UsersOneDrive/Masaüstü/Python Egitimleri/Json-Veritabanı-Kayıt-Örneği/Kullanıcılar.json","r",encoding="utf-8") as File:
                data=json.load(File)
        return data


    def savedata(self,UN,Password,mail): #VERİ KAYDET(ilk kayıtta json db'e kaydedecek)
        self.datas=self.getdata()

        try:
            self.datas["Kullanıcılar"].append({"Kullanıcıadı":UN,"Sifre":Password,"Mail":mail})
        except KeyError:
            self.datas["Kullanıcılar"]=list()
            self.datas["Kullanıcılar"].append({"Kullanıcıadı":UN,"Sifre":Password,"Mail":mail})

        with open("C:/Users/OneDrive/Masaüstü/Python Egitimleri/Json-Veritabanı-Kayıt-Örneği/Kullanıcılar.json","w",encoding="utf-8") as File:
            json.dump(self.datas,File,ensure_ascii=False,indent=4)
            print("Kayıt BASARILI..")
        self.backtomenu()


    def exit(self): #CIKIS
        print("Siteden cıkıs yapılıyor")
        time.sleep(3)
        self.loop=False
        exit()


    def backtomenu(self): #MENUYE DON
        while True:
            x=input(print("Ana menuye donmek ıcın 5, Cıkmak ıcın lutfen 4'e basınız.\n"))
            if x=="5":
                print("ana menuye dönüyorsunuz..")
                time.sleep(3)
                self.program()
                break
            elif x=="4":
                self.exit()
                break
            else:
                print("gecerli bir deger giriniz.")


#site sınıfından yapıyı alıp sistem degiskenine atıyor. Sistem degiskenidenki dongude benı her zaman program isimli fonksiyona yönlerdirmesi icin;
Sistem=Site() 
while Sistem.loop:
    Sistem.program()
