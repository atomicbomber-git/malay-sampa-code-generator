#file : suku.py
#auth : Peb Ruswono Aryan
#desc : pemenggalan suku kata bahasa indonesia
#edited by arif
import os, sys
 
vokal = ['a', 'i', 'u', 'e', '@', 'o']
awalan = ["be", "me", "pe"]
 
def replacer(kata, pola):
    result = kata
    for p,r in pola.items():
        result = result.replace(p, r)
    return result
     
def unreplacer(kata, pola):
    result = kata
    for p,r in pola.items():
        result = result.replace(r, p)
    return result
     
def praproses(kata):
    result = []
    tmp = ""
    i=0
    inkonsonan = False
    numkonsonan = 0
    for karakter in kata:
        iskonsonan = (karakter not in vokal)
        if iskonsonan:
            if not inkonsonan:
                inkonsonan = True
            numkonsonan += 1
            tmp += karakter
        else:
            if inkonsonan:
                inkonsonan = False
                 
                if len(tmp)==1:
                    result += [tmp+karakter]
                else:
                    result += [tmp[0], tmp[1:]+karakter]
                tmp = ""
            else:
                result += [karakter]
    if len(tmp)>0:
        result += [tmp]
    return result
     
def kaidah1(listsuku):
    global vokal
    result = []
    last = ""
    i = 0
    for suku in listsuku:
        if len(suku)==1 and i>0:
            if suku in vokal:
                result += [suku]
            elif listsuku[i-1][-1] in vokal:
                if i<len(listsuku)-1 and len(listsuku[i+1])==1 and listsuku[i+1][0] in vokal:
                    result += [suku]
                else:
                    result[-1] = result[-1] + suku
        else:
            result += [suku]
        i += 1
        last = suku
    return result
     
def kaidah2(listsuku):
    global vokal, awalan
    dift = ["$", "%", "^", "&", "*", "("]
    if len(listsuku)>1:
        if listsuku[0] in awalan and listsuku[1][0] not in vokal and listsuku[1][0] not in dift and len(listsuku[1])>2:
            listsuku[0] += listsuku[1][0]
            listsuku[1] = listsuku[1][1:]
        if len(listsuku[0])==1:
            listsuku = [listsuku[0]+listsuku[1]] + listsuku[2:]
    return listsuku
     
def kaidah3(listsuku):
    global vokal
    result = []
    last = ""
    i = 0
    for suku in listsuku:
        if len(suku)==1 and i>0:
            if listsuku[i-1][-1] in vokal:
                result[-1] = result[-1] + suku
            else:
                result += [suku]
        else:
            result += [suku]
        i += 1
        last = suku
    return result
     
def pecah(kata):
    kdift = {"kh":"$", "ng":"%", "ny":"^", "sy":"&", "tr":"*", "gr":"("}
     
    suku = praproses(replacer(kata, kdift))
    #print suku
    suku = kaidah1(suku)
    #print "1 ", suku
    #suku = kaidah2(suku)
    #print "2 ", suku
    suku = kaidah3(suku)
    #print "3 ", suku
    return [unreplacer(s, kdift) for s in suku]
    #return [unreplacer(s, kdift) for s in kaidah3(kaidah2(kaidah1(praproses(replacer(kata, kdift)))))]


####--------------------------------------------------------------------------------------------- ^ koding suku2.py

def cariSukuKata(kata):
	return pecah(kata)

def konversiKV(fonem):
	return "V" if fonem in vokal else "K"

def cekTipeSukuKata(suku_kata):								#pemisalan: suku_kata = "sa"
	
	sk_konversi = []

	for fonem in suku_kata: 								# ["s", "a"] 		# diftong?
		sk_konversi.append(konversiKV(fonem))					# ["K", "V"]

	sk_konversi = str.join("", sk_konversi)						# "KV"


	daftar_tipe_kv = {
		"V" : ["V1"],		
		"VK" : ["V2", "K1"],		
		"KV" : ["K2", "V3"],		
		"KVK" : ["K3", "V4", "K4"],	
		"KKV" : ["K5", "K6", "V5"],
        "KKVK" : ["K7", "K8", "V6", "K9"],
        "VKK" : ["V7", "K10","K11"],
        "KVKK" : ["K12", "V8","K13", "K14"],
        "KKVKK" : ["K15", "K16", "V9", "K17", "K18"],
        "KKKV" : ["K19", "K20","K21", "V10"],
        "KKKVK" : ["K22", "K23","K24", "V11", "K25"],
        # "KVV" : ["K26", "V12", "V13"],		
	}

	nilai_kv = daftar_tipe_kv[sk_konversi];

	nilai_fonem_kv = {};
	i = 0

	for fonem in suku_kata: 								# ["s", "a"] 		# diftong?
		nilai_fonem_kv[fonem] = nilai_kv[i]			# urutan daftar_tipe_kv harus sesuai
		i = i + 1

	return nilai_fonem_kv;



def hitungDurasi(kalimat):
	teks = "Salam sepok,       lok kite.! &(&(*&(&(&( 12"

	 # diproses dulu
		# 1. huruf besar => huruf kecil
		# 2. hilangkan tanda baca dan huruf atau (angka ?)
		# 3. spasi yg berlebihan

	teks_hasil_bersih2 = "salam sepok lok kite duak belas"
	teks_hasil_bersih2 = kalimat


	#tokenisasi
	daftar_kata = teks_hasil_bersih2.split(" ");				#daftar_kata = ["salam", "sepok", "lok", "kite", 'duak', "belas"]

	for kata in daftar_kata:
		daftar_suku_kata = cariSukuKata(kata) 					#["sa", "lam"] 
		for suku_kata in daftar_suku_kata:
			daftar_tipe_sk = cekTipeSukuKata(suku_kata) 				# ["s" => K2", "a"=> V3"]
			print(suku_kata, daftar_tipe_sk)
			print()





if __name__=='__main__':
    if len(sys.argv)>1:
        kalimat = sys.argv[1]
        print(hitungDurasi(kalimat))
        # print(pecah(kalimat))