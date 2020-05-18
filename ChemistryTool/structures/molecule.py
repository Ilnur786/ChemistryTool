from collections import Counter
from .abc import MoleculeABC
from ..algorithms import Isomorphism
from ..periodictable.element import Element

def sort_alphabet(input):
    return input[0]

class Molecule(Isomorphism, MoleculeABC):
    def add_atom(self, element: Element, number: int, charge: int = 0):
        if number in self._atoms:
            raise KeyError('атом с таким номером уже есть')
        if isinstance(element, Element) and isinstance(number, int) and isinstance(charge, int):
            element.attach(self, number)
            self._charges[number] = charge
            self._atoms[number] = element
            self._bonds[number] = {}
        else:
            raise TypeError('нужно ввести элемент и его заряд')

    def add_bond(self, start_atom: int, end_atom: int, bond_type: int):
        if start_atom == end_atom:
            raise KeyError('атом не может быть связан с сами собой')
        elif start_atom not in self._atoms or end_atom not in self._atoms:
            raise KeyError('таких атомов нет в словаре self._atoms')
        elif end_atom in self._bonds[start_atom]:  #проверка на то что существует ли связь
            raise KeyError('такая связь уже есть')
        else:
            self._bonds[start_atom][end_atom] = bond_type
            self._bonds[end_atom][start_atom] = bond_type

    def get_atom(self, number: int) -> Element:
        return self._atoms[number]

    def get_bond(self, start_atom: int, end_atom: int) -> int:
        return self._bonds[start_atom][end_atom]

    def delete_atom(self, number: int):
        for i in self._bonds[number]:
            del self._bonds[i][number]
        del self._bonds[number]
        del self._atoms[number]

    def delete_bond(self, start_atom: int, end_atom: int):
        del self._atoms[start_atom][end_atom]
        del self._atoms[end_atom][start_atom]

    def update_atom(self, element: Element, number: int):
        if isinstance(element, Element):
            if number in self._atoms:
                self._atoms[number] = element
            else:
                print('атома под таким номером нет в графе')
        else:
            raise TypeError

    def update_bond(self, start_atom: int, end_atom: int, bond_type: int):
        if isinstance(bond_type, int):
            if end_atom in self._bonds[start_atom] and start_atom in self._bonds[end_atom]:
                self._bonds[start_atom][end_atom] = bond_type
                self._bonds[end_atom][start_atom] = bond_type
            else:
                print('атомов с такими связями нет в графе')
        else:
            raise TypeError

    def __enter__(self):
        # todo: make backup of internal data
        self._backup_atoms = self._atoms.copy()     #переменные через селф можно создавать внутри метода, не указав в ините. Отличие таких переменных от обычных в том, что обычные переменные исчезнут сразу же после выполнения метода, а переменные селф сохраняться.
        self._backup_bonds = {}
        for key, value in self._bonds.items():
            self._backup_bonds[key] = value.copy()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # todo: restore internal data in exception case.
        if exc_val is None:
            del self._backup_atoms
            del self._backup_bonds
        else:
            self._atoms = self._backup_atoms
            self._bonds = self._backup_bonds
            del self._backup_atoms
            del self._backup_bonds          #а бэкап-словари лучше чистить или удалять?

    def __str__(self):
        # todo:  brutto formula
        c = Counter(x._mol for x in self._atoms.values())
        pre_formula = []
        for x in c:
            if c[x] > 1:
                pre_formula.append(x + str(c[x]))
            else:
                pre_formula.append(x)
        formula = sorted(pre_formula, key=sort_alphabet)
        self._b_formula = ''.join(formula)
        return self._b_formula

    def __repr__(self):
        return 'Molecule: atoms{}, bonds{}'.format(self._atoms, self._bonds)


__all__ = ['Molecule']

