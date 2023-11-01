from LinkedQFile import LinkedQ
from atomlist import atomer
from molgrafik import *
from atomweight_dict import atom_dict


class Ruta:
    def __init__(self, atom="()", num=1):
        self.atom = atom
        self.num = num
        self.next = None
        self.down = None


class Syntaxfel(Exception):
    pass


def readFormel(q):
    mol = readMolekyl(q)
    print(mol)
    if not q.peek() or q.peek().isalpha() or q.peek() == '(':
        return mol

    raise Syntaxfel(f"Felaktig gruppstart vid radslutet {printQueue(q)}")


def readMolekyl(q):
    first_group = readGroup(q)
    current_group = first_group

    while q.peek() is not None:
        if q.peek().isalpha():
            next_group = readGroup(q)
            current_group.next = next_group
            current_group = next_group
        elif q.peek() == '(':
            # Parse the content inside the parentheses without dequeuing the opening (
            q.dequeue()
            inside_group = readMolekyl(q)

            parenthesis_group = Ruta(atom="()")
            parenthesis_group.down = inside_group
            current_group.next = parenthesis_group
            current_group = parenthesis_group

            # Ensure the closing parenthesis is present and dequeue it
            if q.peek() != ')':
                raise Syntaxfel(f"Saknad högerparentes vid radslutet {printQueue(q)}")
            q.dequeue()

            if q.peek() and q.peek().isnumeric():
                parenthesis_group.num = readNum(q)
        else:
            break

    return first_group

def readGroup(q):
    rutan = Ruta()
    rutan.atom = readAtom(q)
    
    if q.peek() and q.peek().isnumeric():
        rutan.num = readNum(q)
    return rutan



def readAtom(q):
    if q.peek() == '(':
        return

    ATOM = readLETTER(q)

    if q.peek() is not None and 'a' <= q.peek() <= 'z':
        atom = readLetter(q)
        ATom = ATOM + atom
        if kollaAtom(ATom) is True:
            return ATom
        else:
            raise Syntaxfel(f"Okänd atom vid radslutet {printQueue(q)}")

    elif kollaAtom(ATOM) is True:
        return ATOM

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
        return int(num)

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
        return mol
    except Syntaxfel as fel:
        return str(fel)


def kollaAtom(atom):
    if atom in atomer:
        return True
    else:
        return False


def weight(mol):
    tot_weight = 0

    if not mol:
        return 0

    # Check for parenthetical groups and handle accordingly
    if mol.atom == '()':
        tot_weight += weight(mol.down) * mol.num
    else:
        tot_weight += atom_dict.get(mol.atom, 0) * mol.num

    # Recursive call for the next group
    if mol.next:
        tot_weight += weight(mol.next)

    return tot_weight

def main():
    formel = input("Molekyl: ")
    if formel != '#':
        result = kollaFormelSyntax(formel)
        mol_weight = weight(result)
        print(f"The molecular weight of {formel} is: {mol_weight}")




if __name__ == "__main__":
    main()
