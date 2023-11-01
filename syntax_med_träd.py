from LinkedQFile import LinkedQ
from atomlist import atomer
from molgrafik import *


class Ruta:
    def __init__(self, atom = "()", num = 1):
        self.atom = atom
        self.num = num
        self.next=None
        self.down=None


class Syntaxfel(Exception):
    pass


def readFormel(q):
    if q.peek().isalpha() or q.peek() == '(':
        readMolekyl(q)
        if q.peek() == None:
            return
    
    raise Syntaxfel(f"Felaktig gruppstart vid radslutet {printQueue(q)}")


def readMolekyl(q):
    readGroup(q)
    mol = readGroup(q)

    if q.peek() is None or q.peek() == ')' or q.peek().isnumeric():  # slut på inmatning eller just kommit tillbaka från ett parentesuttryck
        return
    
    else:
        mol.next = readMolekyl(q)


def readGroup(q):
    rutan = Ruta()
    rutan.atom = readAtom(q)

    if q.peek() == None or q.peek().isalpha():
        return
    
    elif q.peek() == '(':
        q.dequeue()
        rutan.down = readMolekyl(q)
        if q.peek() is None:
            raise Syntaxfel(f"Saknad högerparentes vid radslutet {printQueue(q)}")
        
        if q.peek() == ')':
            q.dequeue()
            if q.peek() is not None and '0' <= q.peek() <= '9':
                rutan.num = readNum(q)

            else:
                raise Syntaxfel(f"Saknad siffra vid radslutet {printQueue(q)}")

    elif q.peek().isnumeric():
        rutan.num = readNum(q)

    else:
        return


def readAtom(q):
    if q.peek() == '(':
        return
    
    ATOM = readLETTER(q)

    if q.peek() is not None and 'a' <= q.peek() <= 'z':
        atom = readLetter(q)
        ATom = ATOM + atom
        if kollaAtom(ATom) is True:
            return
        else:
            raise Syntaxfel(f"Okänd atom vid radslutet {printQueue(q)}")
        
    else:
        if kollaAtom(ATOM) is True:
            return

    raise Syntaxfel(f"Okänd atom vid radslutet {printQueue(q)}")


def readLETTER(q):
    if q.peek() is not None and 'A' <= q.peek() <= 'Z':
        LETTER = q.dequeue()
        return LETTER

    raise Syntaxfel(f"Saknad stor bokstav vid radslutet {printQueue(q)}")


def readLetter(q):
    if 'a' <= q.peek() <= 'z':
        letter = q.dequeue()
        return letter
    
    raise Syntaxfel(f"Saknad stor bokstav vid radslutet {printQueue(q)}")   


def readNum(q):
    num = q.dequeue()
    if '2' <= num <= '9':
        while q.peek() is not None and q.peek().isnumeric():
            q.dequeue()
            if q.peek == None:
                break
        return
    
    elif num == '1':
        if q.peek() is not None and q.peek().isnumeric():
            while q.peek() is not None and q.peek().isnumeric():
                q.dequeue()
                if q.peek == None:
                    break
            return

    raise Syntaxfel(f"För litet tal vid radslutet {printQueue(q)}")  


def printQueue(q):
    hold = []
    while not q.isEmpty():
        item = q.dequeue()
        hold.append(item)

    return "".join(hold)


def storeFormel(formel):
    q = LinkedQ()
    for f in formel:
        q.enqueue(f)
    return q


def kollaFormelSyntax(formel):
    q = storeFormel(formel)
    try:
        mol = readFormel(q)
        mg = Molgrafik()
        mg.show(mol)
    except Syntaxfel as fel:
        return str(fel)


def kollaAtom(atom):
    if atom in atomer:
        return True
    else:
        return False


def main():
    while True:
        formel = input("Molekyl: ")
        if formel == '#':
            break
        else:
            resultat = kollaFormelSyntax(formel)
            print(resultat)
    

        

if __name__ == "__main__":
    main()