spl = ['b', 'c', 'ć', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'p', 'q', 'r', 's', 'ś', 't', 'v', 'w',
       'x', 'z', 'ź', 'ż']
samo = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
zrosty = ['cz', 'sz', 'dz', 'dż', 'dź', 'rz', 'ch', 'si', 'ci', 'ni', 'zi', 'bi', 'fi', 'ri', 'gi', 'di', 'wi', 'hi',
          'ki', 'mi', 'pi', 'vi', 'li']
zmiekczenia = ['si', 'ci', 'ni', 'zi', 'bi', 'fi', 'ri', 'gi', 'di', 'wi', 'hi', 'ki', 'mi', 'pi', 'vi', 'li']
zmiekczenie3 = ['dzi', 'chi']
wymowasp = ['au', 'eu']
bezdzw = ['k', 'p', 't', 'f', 's', 'c', 'ś', 'ć', 'sz', 'cz', 'ch']


def samogloski(gloski):  # indeksy na których znajduja sie samogłoski
    indeksy = []
    for a in range(len(gloski)):
        if gloski[a].lower() in samo:
            indeksy.append(a)
    return indeksy


def fonet(gloski):  # jezeli samogloska jest wymawiana jako spolgloska, zwroc indeksy takich polaczen
    innawymowa = []
    for a in wymowasp:
        for b in range(len(gloski) - 1):
            string = ''
            string += gloski[b]
            string += gloski[b + 1]
            if a == string.lower():
                innawymowa.append(b)
    return innawymowa


def gloski(slowo): # stworzenie listy składającej się z głosek wymawianych w danym słowie
    gloski = []
    a = 0

    while a < (len(slowo)):
        try:
            if slowo[a:a + 3].lower() in zmiekczenie3 and slowo[a + 3].lower() in samo:
                gloski.append((slowo[a:a + 3]))
                a += 3
            elif slowo[a:a + 3].lower() in zmiekczenie3 and slowo[a + 3].lower() in spl:
                gloski.append(slowo[a:a + 2])
                a += 2

        except:
            gloski.append(slowo[a:a + 2])
            a += 2
        if slowo[a:a + 2].lower() in zrosty:
            if slowo[a:a + 2].lower() in zmiekczenia:
                try:
                    if slowo[a + 2].lower() in samo:
                        gloski.append(slowo[a:a + 2])
                        a += 2
                    else:
                        gloski.append((slowo[a]))
                        a += 1
                except:
                    gloski.append(slowo[a])
                    a += 1
            else:
                gloski.append(slowo[a:a + 2])
                a += 2
        else:
            gloski.append(slowo[a])
            a += 1
    return gloski


def sylabizator(slowo):
    # głoskami = lista, w której rozbijamy słowo na listę głosek (z uwzględnieniem zrostów takich jak "sz", "rz" itp.)
    # fonetycznie = sprawdzenie czy występują zrosty, w których samogłoska jest wymawiana jako spółgłoska (np. "auto")
    # indeksy = lista z indeksami na których znajdują się samogłoski w słowie

    gloskami = gloski(slowo)
    fonetycznie = fonet(gloskami)
    indeksy = samogloski(gloskami)
    sylaby = []
    przesun = []
    druk = ''
    doodjecia = []

    # Sprawdzenie czy słowo nie zaczyna się od przedrostka (np. "przy", "pod", "nad" itp.). Wówczas przedrostek stanowi pierwszą sylabę

    # usunięcie samogłosek, które wymawiane są jako spółgłoski z listy samogłosek
    for f in fonetycznie:
        if f in indeksy:
            indeksy.remove(f)
    # pierwszy krok - wstępne założenie, że każda sylaba rozpoczyna się głoskę przed samogłoską
    # (od teraz lista indeksów samogłosek oznacza indeksy początków sylab)
    for i in range(len(indeksy)):
        indeksy[i] = indeksy[i] - 1
    # jeżeli w słowie występują dwie samogłoski obok siebie, pierwsza z nich jest zakończeniem poprzedniej sylaby, a druga początkiem następnej
    for z in range(len(indeksy) - 1):
        if indeksy[z + 1] - indeksy[z] == 1:
            przesun.append(z + 1)
    for p in przesun:
        indeksy[p] += 1
    # jeżeli pomiędzy dwiema kolejnymi samogłoskami w słowie znajduje się więcej niż 2 spółgłoski, sylaba utworzona wokół pierwszej z tych samogłosek powinna zakończyć się na pierwszej spółgłosce występującej po tej samogłosce
    for x in range(len(indeksy) - 1):
        if indeksy[x + 1] - indeksy[x] > 2:
            doodjecia.append(x + 1)
    for o in range(len(doodjecia) - 1, -1, -1):
        indeksy[doodjecia[o]] = indeksy[doodjecia[o] - 1] + 3
    # w przypadku każdego słowa, pierwsza sylaba zaczyna się w indeksie 0, niezależnie od pozycji pierwszej samogłoski. Wyjątek zapobiega błędom powstającym przy pustej liście indeksów, która powstaje dla słów niezawierających żadnych samogłosek (np. "w", "z")
    try:
        indeksy[0] = 0
    except:
        indeksy.append(0)
    # kończenie sylaby samogłoską+spółgłoską bezdźwięczną i rozpoczynanie kolejnej sylaby spółgłoską nie brzmi naturalnie. Należy ową spółgłoskę bezdźwięczną przesunąć do następnej sylaby
    for i in range(len(indeksy) - 1):
        if gloskami[indeksy[i + 1] - 1].lower() in bezdzw:
            indeksy[i + 1] -= 1

    # tworzymy sylaby poprzed dodanie ciągów głosek zgodnie z indeksami
    for d in range(len(indeksy) - 1):
        sylaby.append(gloskami[indeksy[d]:indeksy[d + 1]])
    sylaby.append(gloskami[indeksy[-1]:])

    for x in range(len(sylaby)):
        sylaby[x] = ''.join(sylaby[x])
    druk += '-'.join(sylaby)
    return druk


def zdania(z):  # zwraca liste zawierajaca poczatkowe i koncowe indeksy wszystkich wykrytych slow

    zdanie = ' ' + z + ' '
    indslow = []
    indreszty = []
    a = 1

    while a < len(zdanie) - 1:
        literaskrajna = (zdanie[a - 1].lower() not in spl and zdanie[a - 1].lower() not in samo) or (
                zdanie[a + 1].lower() not in samo and zdanie[a + 1].lower() not in spl)
        jestlitera = zdanie[a].lower() in samo or zdanie[a].lower() in spl
        literasamotna = (zdanie[a - 1].lower() not in spl and zdanie[a - 1].lower() not in samo) and (
                zdanie[a + 1].lower() not in samo and zdanie[a + 1].lower() not in spl)
        if jestlitera and literasamotna:
            indslow.append(a)
            indslow.append(a)
            a += 1
        elif jestlitera and (literaskrajna):
            indslow.append(a)
            a += 1
        else:
            a += 1
    for b in range(len(indslow)):
        indslow[b] -= 1
    # indreszty to indeksy początków i końców wszystkich ciągów znaków niebędących słowami
    for a in range(1, len(indslow) - 2, 2):
        indreszty.append(indslow[a] + 1)
        indreszty.append(indslow[a + 1])

    try:
        if indslow[0] != 0:
            indreszty = [0, indslow[0]] + indreszty
        else:
            indreszty = [0, 0] + indreszty
        if indslow[-1] != len(z) - 1:
            indreszty.append(indslow[-1] + 1)
            indreszty.append(len(z))
        else:
            indreszty.append(len(z) - 1)
            indreszty.append(len(z) - 1)
    except:
        return "brak słów..."
        print("brak słow :C")
        pass

    return indslow, indreszty


def wywolaj(n, p, zd):
    druk = ''
    listagotowa = []
    for x in range(0, len(n) - 1, 2):
        listagotowa.append(sylabizator(zd[n[x]:n[x + 1] + 1]))
    for a in range(0, len(p), 2):
        druk += zd[p[a]:p[a + 1]]
        try:
            druk += listagotowa[int(a / 2)]
        except:
            break

    return druk

