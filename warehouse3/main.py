import copy


def main(data):
    lines = data.split('\n')
    parts = lines[0].split()
    dSayac = int(parts[0])
    mSayac = int(parts[1])

    depo = []
    dKapasite = []
    dMaliyet = []
    whD = {}

    for i in range(1, dSayac + 1):
        line = lines[i]
        parts = line.split()
        depo.append((int(parts[0]), float(parts[1])))
        dKapasite.append(int(parts[0]))
        dMaliyet.append(float(parts[1]))
        whD[i - 1] = True

    mSize = []
    mMaliyet = []

    lineIndex = dSayac + 1
    for i in range(0, mSayac):
        musteriSize = int(lines[lineIndex + 2 * i])
        musteriMaliyet = list(map(float, lines[lineIndex + 2 * i + 1].split()))
        mSize.append(musteriSize)
        mMaliyet.append(musteriMaliyet)

    whM = {}
    musteriSiralama = []

    def musteriMaliyet():
        nonlocal musteriSiralama
        for i in range(0, mSayac):
            musteriSiralama.append(sorted(range(0, dSayac), key=lambda index: mMaliyet[i][index]))

    def Hesapla():
        deger = 0.0
        for wh, musteriListe in whM.items():
            deger += dMaliyet[wh]
            for maliyet in musteriListe:
                deger += mMaliyet[maliyet][wh]
        return deger

    def Kontrol(musteri):
        nonlocal whM, dKapasite
        ListeMaliyet = musteriSiralama[musteri]
        for wh in ListeMaliyet:
            if whD[wh] == False:
                continue
            if dKapasite[wh] < mSize[musteri]:
                continue
            else:
                if wh in whM:
                    whM[wh].append(musteri)
                else:
                    whM[wh] = [musteri]
                dKapasite[wh] -= mSize[musteri]
                return True
        return False

    def greedy():
        nonlocal minDeger
        listeTalep = sorted(range(0, mSayac), key=lambda index: mSize[index], reverse=True)
        for index in listeTalep:
            Kontrol(index)
        minDeger = Hesapla()

    def Kopya(depo):
        nonlocal whM, dKapasite, minDeger
        localwcMap = copy.deepcopy(whM)
        localwhKapasite = copy.deepcopy(dKapasite)
        durum = True
        if depo not in whM:
            return False
        whD[depo] = False
        listeMusteri = whM[depo][:]
        for musteri in listeMusteri:
            if Kontrol(musteri) == False:
                durum = False
                break
        if durum == False:
            wcMap = localwcMap
            dKapasite = localwhKapasite
            whD[depo] = True
            return False
        else:
            whM[depo] = []
            del whM[depo]
            value = Hesapla()
            if value >= minDeger:
                whM = localwcMap
                dKapasite = localwhKapasite
                whD[depo] = True
                return False
            else:
                minDeger = value
                return True

    def listeFormat():
        returnList = [0] * mSayac
        for warehouse, listeMaliyet in whM.items():
            for musteri in listeMaliyet:
                returnList[musteri] = warehouse
        return returnList

    def tasi():
        nonlocal whD
        depolist = sorted(range(0, dSayac), key=lambda index: depo[index][1] / depo[index][0], reverse=True)
        for wh in depolist:
            if whD[wh] == True:
                Kopya(wh)

    musteriMaliyet()
    minDeger = 0.0
    whM = {}
    greedy()
    tasi()
    dataLast = str(Hesapla()) + " \n"
    # en düşük değeri ve atanan depoları döndürmek.
    dataLast += " ".join(list(map(str, listeFormat()))) 
    return dataLast


dosya = open("wl_500_3", 'r')
data = ''.join(dosya.readlines())
dosya.close()
print(main(data))
