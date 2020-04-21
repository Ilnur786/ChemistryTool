from collections import Counter
from .abc import MoleculeABC
from ..algorithms import Isomorphism
from ..periodictable.element import Element


def sortByAlphabet(inputStr):
    return inputStr[0]

class Molecule(Isomorphism, MoleculeABC):
    def add_atom(self, element: str, number: int):
        if number in self._atoms:
            raise KeyError('атом с таким номером уже есть')
        if isinstance(element, str):
            self._atoms[number] = element
            self._bonds[number] = {}
        else:
            raise TypeError('нужно ввести строку')

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
        if isinstance(number, int):
            return self._atoms[number]
        else:
            raise TypeError

    def get_bond(self, start_atom: int, end_atom: int) -> int:
        if isinstance(start_atom, int) and isinstance(end_atom, int):
            return self._bonds[start_atom][end_atom]
        else:
            raise TypeError

    def delete_atom(self, number: int):
        if isinstance(number, int):
            del self._atoms[number]
        else:
            raise TypeError

    def delete_bond(self, start_atom: int, end_atom: int):
        if isinstance(start_atom, int) and isinstance(end_atom, int):
            del self._atoms[start_atom][end_atom]
        else:
            raise TypeError

    def update_atom(self, element: Element, number: int):
        if isinstance(element, Element) and isinstance(number, int):
            self._atoms[number] = element
        else:
            raise TypeError

    def update_bond(self, start_atom: int, end_atom: int, bond_type: int):
        if isinstance(start_atom, int) and isinstance(end_atom, int) and isinstance(bond_type, int):
            self._bonds[start_atom][end_atom] = bond_type
        else:
            raise TypeError

    def __enter__(self):
        # todo: make backup of internal data
        self._backup_atoms = self._atoms.copy()     #а здесь переменные писать через селф или без? и если писать с селф то надо их в ините прописывать? переменные через селф можно сохдавать внутри метода, не указав в ините. Отличие таких переменных от обычных в том, что обычные переменные исчезнут сразу же после выполнения метода, а переменные сылф сохраняться.
        self._backup_bonds = self._bonds.copy()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # todo: restore internal data in exception case.
        if exc_val is None:
            del self._backup_atoms
            del self._backup_bonds
            return self._atoms, self._bonds
        else:
            self._atoms = self._backup_atoms
            self._bonds = self._backup_bonds


    def __str__(self):
        # todo:  brutto formula
        c = Counter
        atoms = [x for x in self._atoms.values()]
        for element in atoms:
            c[element] += 1
        pre_formula = []
        for x in c:
            if c[x] > 1:
                pre_formula.append(x + str(c[x]))
            else:
                pre_formula.append(x)
        formula = sorted(pre_formula, key=sortByAlphabet)
        b_formula = ''.join(formula)
        return b_formula

    def __repr__(self):
        return 'Molecule: atoms{}, bonds{}'.format(self._atoms, self._bonds)


__all__ = ['Molecule']

# Управлениие ПО. Сделать питон файл setup файлом.